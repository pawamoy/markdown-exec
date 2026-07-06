# Special module without future annotations for executing Python code.

from typing import Any


def exec_python(code: str, filename: str, exec_globals: dict[str, Any] | None = None) -> None:
    compiled = compile(code, filename=filename, mode="exec")
    exec(compiled, exec_globals)  # noqa: S102
