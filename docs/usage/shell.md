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
