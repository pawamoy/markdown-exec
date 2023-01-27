# Shell

Shell code blocks are executed using the same interpreter specified
as language of the code block, in sub-processes. The output is captured
and rendered as Markdown or HTML (see [Usage](../#html-vs-markdown)).

## Bash

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```bash exec="1" source="material-block"
echo $BASH_VERSION
```
````

## Console

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```console exec="1" source="console"
$ mkdocs --help
```
````

## sh

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```sh exec="1" source="material-block"
echo Markdown is **cool**
```
````

## Expecting a non-zero exit code

You will sometimes want to run a command
that returns a non-zero exit code,
for example to show how errors look to your users.

You can tell Markdown Exec to expect
a particular exit code with the `returncode` option:

````md
```bash exec="true" returncode="1"
echo Not in the mood today
exit 1
```
````

In that case, the executed code won't be considered
to have failed, its output will be rendered normally,
and no warning will be logged in the MkDocs output,
allowing your strict builds to pass.

If the exit code is different than the one specified
with `returncode`, it will be considered a failure,
its output will be renderer anyway (stdout and stderr combined),
and a warning will be logged in the MkDocs output.
