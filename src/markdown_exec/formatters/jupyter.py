"""Formatter for executing code using Jupyter kernels."""

from __future__ import annotations

import functools
import os
import platform
import queue
from typing import TYPE_CHECKING, Any, Callable

from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

from markdown_exec.formatters.base import ExecutionError, base_format
from markdown_exec.rendering import code_block

if TYPE_CHECKING:
    from jupyter_client.blocking.client import BlockingKernelClient

# Store kernel managers by session and kernel name
_kernel_managers: dict[str, dict[tuple[str | None, str], KernelManager]] = {}
_kernel_clients: dict[str, dict[tuple[str | None, str], BlockingKernelClient]] = {}


def _get_available_kernels() -> dict[str, dict[str, Any]]:
    """Get information about all available Jupyter kernels.

    Returns:
        A dictionary mapping kernel names to their information including:
        - display_name: Human readable name
        - language: The programming language
        - language_version: Version of the language (if available)
        - language_info: Additional language information
    """
    ksm = KernelSpecManager()
    # Find all available kernel specs
    kernel_specs = ksm.get_all_specs()

    # Get detailed information for each kernel
    return {
        name: {
            "display_name": spec["spec"]["display_name"],
            "languages": [
                spec["spec"]["language"],
                *(spec["spec"].get("aliases", [])),
            ],
            "language_version": spec["spec"].get("language_version", None),
            "language_info": spec["spec"].get("language_info", {}),
        }
        for name, spec in kernel_specs.items()
    }

_language_to_kernel: dict[str, str] = {}

def _get_kernel_for_language(language: str) -> str:
    """Get the best matching kernel for a given language name.

    Args:
        language: Name of the programming language (case insensitive)

    Returns:
        The kernel name to use, or None if no matching kernel is found
    """
    if language in _language_to_kernel:
        return _language_to_kernel[language]
    language = language.lower()
    kernels = _get_available_kernels()
    for kernel in kernels:
        if language in [name.lower() for name in kernels[kernel]["languages"]]:
            _language_to_kernel[language] = kernel
            return kernel

    no_kernel_msg = f"No jupyter kernel found that supports language '{language}'."

    if language == "typescript":
        no_kernel_msg += "Please install the deno jupyter kernel by running `deno jupyter install`."
        if os.environ.get("JUPYTER_PLATFORM_DIRS", "") and (platform.system() == "Darwin" or platform.system() == "Windows"):
            no_kernel_msg += ("You may need additional install steps when running"
                "with JUPYTER_PLATFORM_DIRS=1. See "
                 "https://github.com/denoland/deno/issues/27984 for more info.")
    else:
        no_kernel_msg += "Available kernels:\n" + "\n".join(
            f"- {info['language']}: {name} ({info['display_name']})"
            for name, info in kernels.items()
        )
    raise ExecutionError(no_kernel_msg)


def _get_kernel_manager_and_client(
    language: str,
    session: str | None = None,
) -> tuple[KernelManager, BlockingKernelClient]:
    """Get or create a kernel manager and client for the given kernel name and session."""
    kernel_name = _get_kernel_for_language(language)
    key = (session, kernel_name)

    if language not in _kernel_managers:
        _kernel_managers[language] = {}
    if language not in _kernel_clients:
        _kernel_clients[language] = {}
    if key not in _kernel_managers[language]:
        km = KernelManager(kernel_name=kernel_name)
        km.start_kernel()
        _kernel_managers[language][key] = km
    km = _kernel_managers[language][key]
    if key not in _kernel_clients[language]:
        kc = km.client()
        kc.start_channels()
        _kernel_clients[language][key] = kc
    kc = _kernel_clients[language][key]
    return km, kc

def _shutdown_kernels() -> None:
    for clients in _kernel_clients.values():
        for kc in clients.values():
            kc.stop_channels()
    _kernel_clients.clear()
    for managers in _kernel_managers.values():
        for km in managers.values():
            km.shutdown_kernel()
    _kernel_managers.clear()

# Because this is a language agnostic runner, it has an extra initial language
# argument. This makes it easy to use functools.partial to create a language
# specific runner when needed.
def _run_jupyter(
    language: str,
    code: str,
    returncode: int | None = None,
    session: str | None = None,
    id: str | None = None,  # noqa: A002, ARG001
    **extra: str,
) -> str:
    """Execute code using a Jupyter kernel."""
    is_named_session = session is not None and session != ""

    # Get kernel manager and client
    km, kc = _get_kernel_manager_and_client(language, session)

    kc.wait_for_ready()
    # Send code for execution
    msg_id = kc.execute(code, store_history=is_named_session)

    # Collect output
    outputs = []
    error_outputs = []
    execution_completed = False

    while not execution_completed:
        try:
            # Check for shell messages (execution replies)
            shell_msg = kc.get_shell_msg(timeout=0.1)
            if shell_msg["parent_header"].get("msg_id") == msg_id:
                execution_completed = True

                if shell_msg["content"]["status"] == "error":
                    if (
                        shell_msg["content"]["traceback"] is not None
                        and len(shell_msg["content"]["traceback"]) > 0
                    ):
                        if shell_msg["content"]["traceback"][0] == "Stack trace:":
                            error_outputs.extend(
                                shell_msg["content"]["traceback"][1:],
                            )
                        else:
                            error_outputs.extend(shell_msg["content"]["traceback"])
                    break
                # note: abort is deprecated, but some older kernels may still send it
                # it doesn't send error info, however - so we'll need to populate a fake abort error instead
                if shell_msg["content"]["status"] == "abort":
                    error_outputs.append("AbortError: Execution aborted")
                    break
        except queue.Empty:
            pass

        try:
            # nested while here so we consume all iopub messages for this execution before moving on.
            # this lets us consume all pending messages after execution has completed before exiting the loop
            while True:
                # Check for iopub messages (output)
                iopub_msg = kc.get_iopub_msg(timeout=0.1)
                if iopub_msg["parent_header"].get("msg_id") != msg_id:
                    continue

                msg_type = iopub_msg["header"]["msg_type"]
                content = iopub_msg["content"]

                if msg_type == "stream":
                    outputs.append(content["text"])
                elif msg_type in ("execute_result", "display_data"):
                    # TODO: these can contain other MIME types (including HTML) - do we want to support them?
                    outputs.append(str(content["data"].get("text/plain", "")))
                elif msg_type == "error":
                    # ignore these because we already got it from the shell message
                    pass

        except queue.Empty:
            # No messages received in timeout period, check if kernel is still alive
            if not km.is_alive():
                raise ExecutionError(
                    "Error: Kernel died during execution",
                ) from None
            continue

    # Check for errors
    if error_outputs:
        if returncode:
            return "\n".join(error_outputs)
        raise ExecutionError(
            code_block(language, "\n".join(error_outputs), **extra),
        )

    return "\n".join(outputs)



def _jupyter_formatter(language: str, runner: Callable[[str], str] | None = None, **kwargs: Any) -> str:
    """Format and execute code using Jupyter kernels."""
    return base_format(
        language=language,
        run=runner or functools.partial(_run_jupyter, language),
        **kwargs,
    )

