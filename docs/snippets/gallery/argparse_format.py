from duty import get_parser

parser = get_parser()
print(f"```\n{parser.format_help()}\n```")
