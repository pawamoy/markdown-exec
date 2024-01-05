# Shell

Shell code blocks are executed using the same interpreter specified
as language of the code block, in sub-processes. The output is captured
and rendered as Markdown or HTML (see [Usage](../index.md#html-vs-markdown)).

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

## Support for ANSI colors

If you installed Markdown Exec with the `ansi` extra (`pip install markdown-exec[ansi]`),
the ANSI colors in the output of shell commands will be translated to HTML/CSS,
allowing to render them naturally in your documentation pages.


To enable ANSI colors in the output of a code block, use the
[`result="ansi"` option](http://localhost:8000/markdown-exec/usage/#wrap-result-in-a-code-block).

````md exec="true" source="tabbed-left" title="ANSI terminal output"
```bash exec="true" result="ansi"
--8<-- "gallery/ansi.sh"
```
````

/// admonition
    type: warning

Unless you enable Markdown Exec through our MkDocs plugin,
you will need to provide your own CSS rules. How to do that
depends on the tool(s) you use to convert Markdown to HTML,
so we cannot provide generic guidance here.


//// details | CSS rules used by our MkDocs plugin
    type: example

```css
/*
  Inspired by https://spec.draculatheme.com/ specification, they should work
  decently with both dark and light themes.
  */
:root {
    --ansi-red: #ff5555;
    --ansi-green: #50fa7b;
    --ansi-blue: #265285;
    --ansi-yellow: #ffb86c;
    --ansi-magenta: #bd93f9;
    --ansi-cyan: #8be9fd;
    --ansi-black: #282a36;
    --ansi-white: #f8f8f2;
}

.-Color-Green,
.-Color-Faint-Green,
.-Color-Bold-Green {
    color: var(--ansi-green);
}

.-Color-Red,
.-Color-Faint-Red,
.-Color-Bold-Red {
    color: var(--ansi-red);
}

.-Color-Yellow,
.-Color-Faint-Yellow,
.-Color-Bold-Yellow {
    color: var(--ansi-yellow);
}

.-Color-Blue,
.-Color-Faint-Blue,
.-Color-Bold-Blue {
    color: var(--ansi-blue);
}

.-Color-Magenta,
.-Color-Faint-Magenta,
.-Color-Bold-Magenta {
    color: var(--ansi-magenta);
}

.-Color-Cyan,
.-Color-Faint-Cyan,
.-Color-Bold-Cyan {
    color: var(--ansi-cyan);
}

.-Color-White,
.-Color-Faint-White,
.-Color-Bold-White {
    color: var(--ansi-white);
}

.-Color-Black,
.-Color-Faint-Black,
.-Color-Bold-Black {
    color: var(--ansi-black);
}

.-Color-Faint {
    opacity: 0.5;
}

.-Color-Bold {
    font-weight: bold;
}

.-Color-BGBlack,
.-Color-Black-BGBlack,
.-Color-Blue-BGBlack,
.-Color-Bold-BGBlack,
.-Color-Bold-Black-BGBlack,
.-Color-Bold-Green-BGBlack,
.-Color-Bold-Cyan-BGBlack,
.-Color-Bold-Blue-BGBlack,
.-Color-Bold-Magenta-BGBlack,
.-Color-Bold-Red-BGBlack,
.-Color-Bold-White-BGBlack,
.-Color-Bold-Yellow-BGBlack,
.-Color-Cyan-BGBlack,
.-Color-Green-BGBlack,
.-Color-Magenta-BGBlack,
.-Color-Red-BGBlack,
.-Color-White-BGBlack,
.-Color-Yellow-BGBlack {
    background-color: var(--ansi-black);
}

.-Color-BGRed,
.-Color-Black-BGRed,
.-Color-Blue-BGRed,
.-Color-Bold-BGRed,
.-Color-Bold-Black-BGRed,
.-Color-Bold-Green-BGRed,
.-Color-Bold-Cyan-BGRed,
.-Color-Bold-Blue-BGRed,
.-Color-Bold-Magenta-BGRed,
.-Color-Bold-Red-BGRed,
.-Color-Bold-White-BGRed,
.-Color-Bold-Yellow-BGRed,
.-Color-Cyan-BGRed,
.-Color-Green-BGRed,
.-Color-Magenta-BGRed,
.-Color-Red-BGRed,
.-Color-White-BGRed,
.-Color-Yellow-BGRed {
    background-color: var(--ansi-red);
}

.-Color-BGGreen,
.-Color-Black-BGGreen,
.-Color-Blue-BGGreen,
.-Color-Bold-BGGreen,
.-Color-Bold-Black-BGGreen,
.-Color-Bold-Green-BGGreen,
.-Color-Bold-Cyan-BGGreen,
.-Color-Bold-Blue-BGGreen,
.-Color-Bold-Magenta-BGGreen,
.-Color-Bold-Red-BGGreen,
.-Color-Bold-White-BGGreen,
.-Color-Bold-Yellow-BGGreen,
.-Color-Cyan-BGGreen,
.-Color-Green-BGGreen,
.-Color-Magenta-BGGreen,
.-Color-Red-BGGreen,
.-Color-White-BGGreen,
.-Color-Yellow-BGGreen {
    background-color: var(--ansi-green);
}

.-Color-BGYellow,
.-Color-Black-BGYellow,
.-Color-Blue-BGYellow,
.-Color-Bold-BGYellow,
.-Color-Bold-Black-BGYellow,
.-Color-Bold-Green-BGYellow,
.-Color-Bold-Cyan-BGYellow,
.-Color-Bold-Blue-BGYellow,
.-Color-Bold-Magenta-BGYellow,
.-Color-Bold-Red-BGYellow,
.-Color-Bold-White-BGYellow,
.-Color-Bold-Yellow-BGYellow,
.-Color-Cyan-BGYellow,
.-Color-Green-BGYellow,
.-Color-Magenta-BGYellow,
.-Color-Red-BGYellow,
.-Color-White-BGYellow,
.-Color-Yellow-BGYellow {
    background-color: var(--ansi-yellow);
}

.-Color-BGBlue,
.-Color-Black-BGBlue,
.-Color-Blue-BGBlue,
.-Color-Bold-BGBlue,
.-Color-Bold-Black-BGBlue,
.-Color-Bold-Green-BGBlue,
.-Color-Bold-Cyan-BGBlue,
.-Color-Bold-Blue-BGBlue,
.-Color-Bold-Magenta-BGBlue,
.-Color-Bold-Red-BGBlue,
.-Color-Bold-White-BGBlue,
.-Color-Bold-Yellow-BGBlue,
.-Color-Cyan-BGBlue,
.-Color-Green-BGBlue,
.-Color-Magenta-BGBlue,
.-Color-Red-BGBlue,
.-Color-White-BGBlue,
.-Color-Yellow-BGBlue {
    background-color: var(--ansi-blue);
}

.-Color-BGMagenta,
.-Color-Black-BGMagenta,
.-Color-Blue-BGMagenta,
.-Color-Bold-BGMagenta,
.-Color-Bold-Black-BGMagenta,
.-Color-Bold-Green-BGMagenta,
.-Color-Bold-Cyan-BGMagenta,
.-Color-Bold-Blue-BGMagenta,
.-Color-Bold-Magenta-BGMagenta,
.-Color-Bold-Red-BGMagenta,
.-Color-Bold-White-BGMagenta,
.-Color-Bold-Yellow-BGMagenta,
.-Color-Cyan-BGMagenta,
.-Color-Green-BGMagenta,
.-Color-Magenta-BGMagenta,
.-Color-Red-BGMagenta,
.-Color-White-BGMagenta,
.-Color-Yellow-BGMagenta {
    background-color: var(--ansi-magenta);
}

.-Color-BGCyan,
.-Color-Black-BGCyan,
.-Color-Blue-BGCyan,
.-Color-Bold-BGCyan,
.-Color-Bold-Black-BGCyan,
.-Color-Bold-Green-BGCyan,
.-Color-Bold-Cyan-BGCyan,
.-Color-Bold-Blue-BGCyan,
.-Color-Bold-Magenta-BGCyan,
.-Color-Bold-Red-BGCyan,
.-Color-Bold-White-BGCyan,
.-Color-Bold-Yellow-BGCyan,
.-Color-Cyan-BGCyan,
.-Color-Green-BGCyan,
.-Color-Magenta-BGCyan,
.-Color-Red-BGCyan,
.-Color-White-BGCyan,
.-Color-Yellow-BGCyan {
    background-color: var(--ansi-cyan);
}

.-Color-BGWhite,
.-Color-Black-BGWhite,
.-Color-Blue-BGWhite,
.-Color-Bold-BGWhite,
.-Color-Bold-Black-BGWhite,
.-Color-Bold-Green-BGWhite,
.-Color-Bold-Cyan-BGWhite,
.-Color-Bold-Blue-BGWhite,
.-Color-Bold-Magenta-BGWhite,
.-Color-Bold-Red-BGWhite,
.-Color-Bold-White-BGWhite,
.-Color-Bold-Yellow-BGWhite,
.-Color-Cyan-BGWhite,
.-Color-Green-BGWhite,
.-Color-Magenta-BGWhite,
.-Color-Red-BGWhite,
.-Color-White-BGWhite,
.-Color-Yellow-BGWhite {
    background-color: var(--ansi-white);
}

.-Color-Black,
.-Color-Bold-Black,
.-Color-Black-BGBlack,
.-Color-Bold-Black-BGBlack,
.-Color-Black-BGGreen,
.-Color-Red-BGRed,
.-Color-Bold-Red-BGRed,
.-Color-Bold-Blue-BGBlue,
.-Color-Blue-BGBlue {
    text-shadow: 0 0 1px var(--ansi-white);
}

.-Color-Bold-Cyan-BGCyan,
.-Color-Bold-Magenta-BGMagenta,
.-Color-Bold-White,
.-Color-Bold-Yellow-BGYellow,
.-Color-Bold-Green-BGGreen,
.-Color-Cyan-BGCyan,
.-Color-Cyan-BGGreen,
.-Color-Green-BGCyan,
.-Color-Green-BGGreen,
.-Color-Magenta-BGMagenta,
.-Color-White,
.-Color-White-BGWhite,
.-Color-Yellow-BGYellow {
    text-shadow: 0 0 1px var(--ansi-black);
}
```

////

///


> IMPORTANT: We also recommend setting `ansi: required` in `mkdocs.yml`
> when using our MkDocs plugin and enabling ANSI support,
> to help tools like MkDocs and its `get-deps` command
> know that the `ansi` extra dependency is required.
> 
> ```yaml
> plugins:
> - markdown-exec:
>     ansi: required
> ```
