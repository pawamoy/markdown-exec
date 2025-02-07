"""Formatter for executing TypeScript code."""

from __future__ import annotations

import functools
import os
import pathlib
import re
import shutil
import subprocess
import tempfile

from markdown_exec.formatters.base import ExecutionError
from markdown_exec.formatters.jupyter import _jupyter_formatter, _run_jupyter
from markdown_exec.rendering import code_block

_sessions: dict[str, list[str]] = {}


def _clean_typecheck_error(filename: str, stderr: str, session: str | None) -> str:
    cleaned_filename = (
        f"<session {session}>" if session else "<anonymous session>"
    ) + ".ts"
    file_url = pathlib.Path(filename).as_uri()
    stderr = stderr.replace(f"at {file_url}", f"at {cleaned_filename}")

    # given an error line like: "at <anonymous session>.ts:1:5", subtract the number of lines of old code from the line number
    # so the line number aligns with the one in the code block
    old_lines = 0 if not session else len(_sessions[session])

    cleaned_lines = []
    for line in stderr.split("\n"):
        if match := re.match(
            r"^(\s*at .*:)(?P<line_number>\d+):(?P<column_number>\d+)$",
            line,
        ):
            line_number = int(match.group("line_number")) - old_lines
            column_number = int(match.group("column_number"))
            cleaned_lines.append(f"{match.group(1)}{line_number}:{column_number}")
        else:
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def _check_types(
    code_history: list[str],
    session: str | None,
    returncode: int | None = None,
    **extra: str,
) -> str | None:
    code = "\n".join(code_history)
    env = {**os.environ, "NO_COLOR": "1"}
    deno_path = shutil.which("deno")

    if not deno_path:
        raise ExecutionError(
            "Deno not found. Please install it from "
            "https://deno.land/manual/getting_started/installation. Be sure to "
            "also install the deno jupyter kernel by running `deno jupyter "
            "install`.",
        )

    with tempfile.NamedTemporaryFile(
        suffix=".ts",
        delete=True,
        encoding="utf-8",
        mode="w",
    ) as file:
        file.write(code)
        file.flush()
        with subprocess.Popen(  # noqa: S603
            [deno_path, "check", "--quiet", file.name],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            text=True,
            cwd=os.getcwd(),
        ) as check_proc:
            check_proc.wait()
            stderr = check_proc.stderr.read() if check_proc.stderr else ""
            if check_proc.returncode != 0:
                if returncode:
                    return code_block(
                        "typescript",
                        _clean_typecheck_error(file.name, stderr, session),
                        **extra,
                    )
                raise ExecutionError(
                    code_block(
                        "typescript",
                        _clean_typecheck_error(file.name, stderr, session),
                        **extra,
                    ),
                )
            return None


def _get_code_history(session: str | None, code: str) -> list[str]:
    if session is None or session == "":
        return code.split("\n")

    _sessions[session] = _sessions.get(session, []) + code.split("\n")

    return _sessions[session]


def _run_typescript(
    code: str,
    returncode: int | None = None,
    session: str | None = None,
    id: str | None = None,  # noqa: A002
    **extra: str,
) -> str:
    code_history = _get_code_history(session, code)
    type_check_errors = _check_types(code_history, session, returncode, **extra)
    if type_check_errors:
        return type_check_errors
    start_kernel_kwargs = {
      "env": {**os.environ, "NO_COLOR": "1"},
      "extra_arguments": ["--quiet"],
    }
    return _run_jupyter(
        "typescript", start_kernel_kwargs, code, returncode, session, id, **extra,
    )


_format_typescript = functools.partial(_jupyter_formatter, "typescript", _run_typescript)
