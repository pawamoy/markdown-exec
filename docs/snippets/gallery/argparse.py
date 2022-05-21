import argparse

from duty.cli import get_parser

parser = get_parser()
lines = []
lines.append(f"## duty")
if parser.description:
    lines.append(parser.description)
lines.append("\nOptions:\n")
for action in parser._actions:
    opts = [f"`{opt}`" for opt in action.option_strings]
    if not opts:
        continue
    line = "- " + ",".join(opts)
    if action.metavar:
        line += f" `{action.metavar}`"
    line += f": {action.help}"
    if action.default and action.default != argparse.SUPPRESS:
        line += f"(default: {action.default})"
    lines.append(line)
print("\n".join(lines))
