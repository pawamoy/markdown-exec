from fnmatch import fnmatch
from pathlib import Path

exclude = {"dist", "*cache*", ".devbox", ".hypothesis", ".pdm*", ".coverage*", "profile.*"}
no_recurse = {".venv*", "site", "htmlcov", ".git"}


def exptree(path: str, session: str) -> None:
    # List files and directories separately.
    files = []
    dirs = []
    for node in Path(path).iterdir():
        if any(fnmatch(node.name, pattern) for pattern in exclude):
            continue
        if node.is_dir():
            dirs.append(node)
        else:
            files.append(node)

    # Print directories first, then files (both sorted).
    recurse = []
    print("```tree")
    for directory in sorted(dirs):
        if any(fnmatch(directory.name, pattern) for pattern in no_recurse):
            print(f"{directory.name}/")
        else:
            recurse.append(directory.name)
            # Add code annotation at the end.
            print(f"{directory.name}/ # ({len(recurse)})!")
    for file in sorted(files):
        print(file.name)
    print("```\n")

    # Print contents of each annotated directory.
    for index, directory in enumerate(recurse, 1):
        new_path = f"{path}/{directory}"
        print(f"{index}. \n")
        # The recursive part!
        print(f'    ```python exec="1" session="{session}"')
        print(f'    exptree("{new_path}", "{session}")')
        print("    ```\n")
