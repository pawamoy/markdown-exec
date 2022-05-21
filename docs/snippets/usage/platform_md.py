import platform
from textwrap import dedent

print(
    # we must dedent, otherwise Markdown
    # will render it as a code block!
    dedent(
        f"""
        - machine: `{platform.machine()}`
        - version: `{platform.version()}`
        - platform: `{platform.platform()}`
        - system: `{platform.system()}`
        """
    )
)
