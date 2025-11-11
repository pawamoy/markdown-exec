# Markdown Exec

[![ci](https://github.com/pawamoy/markdown-exec/workflows/ci/badge.svg)](https://github.com/pawamoy/markdown-exec/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://pawamoy.github.io/markdown-exec/)
[![pypi version](https://img.shields.io/pypi/v/markdown-exec.svg)](https://pypi.org/project/markdown-exec/)
[![gitter](https://img.shields.io/badge/matrix-chat-4DB798.svg?style=flat)](https://app.gitter.im/#/room/#markdown-exec:gitter.im)
[![radicle](https://img.shields.io/badge/rad-clone-6666FF.svg?style=flat)](https://app.radicle.at/nodes/seed.radicle.at/rad:z77aiLJkzYXtuNpZuvizfGkDuZbQ)

Utilities to execute code blocks in Markdown files.

For example, you write a Python code block that computes some HTML,
and this HTML is injected in place of the code block.

## Installation

```bash
pip install "markdown-exec[ansi]"
```

The `ansi` extra provides the necessary bits (`pygments-ansi-color` and a CSS file)
to render ANSI colors in HTML code blocks. The CSS file is automatically added
to MkDocs' `extra_css` when Markdown Exec is activated via `plugins` (see below).

## Configuration

This extension relies on the
[SuperFences](https://facelessuser.github.io/pymdown-extensions/extensions/superfences/)
extension of
[PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/).

To allow execution of code blocks,
configure a custom fence from Python:

```python
from markdown import Markdown
from markdown_exec import formatter, validator

Markdown(
    extensions=["pymdownx.superfences"],
    extension_configs={
        "pymdownx.superfences": {
            "custom_fences": [
                {
                    "name": "python",
                    "class": "python",
                    "validator": validator,
                    "format": formatter,
                }
                # ...one fence for each language we support:
                # bash, console, md, markdown, py, python, pycon, pyodide, sh, tree, etc.
            ]
        }
    }
)
```

...or in MkDocs configuration file, as a Markdown extension:

```yaml
# mkdocs.yml
markdown_extensions:
- pymdownx.superfences:
    custom_fences:
    - name: python
      class: python
      validator: !!python/name:markdown_exec.validator
      format: !!python/name:markdown_exec.formatter
    # ...one fence for each language we support:
    # bash, console, md, markdown, py, python, pycon, sh, tree
```

...or in MkDocs configuration file, as a plugin:

```yaml
# mkdocs.yml
plugins:
- search
- markdown-exec

# SuperFences must still be enabled!
markdown_extensions:
- pymdownx.superfences
```

TIP: We recommend enabling Markdown Exec with the MkDocs plugin
if you are using MkDocs: it will take care of adding relevant
assets (CSS/JS) to the final site when needed.

WARNING: **Limitation of configuration through Markdown/PyMDown.**
Configuration through `pymdownx.superfences` directly is not well supported for fences that require assets inclusion, like `pyodide`.
For these you will have to include the assets manually. In the future we will provide ways to include them automatically.

## Usage

You are now able to execute code blocks instead of displaying them:

````md
```python exec="on"
print("Hello Markdown!")
```
````

The `exec` option will be true for every possible value except `0`, `no`, `off` and `false` (case insensitive).

Below you can see an example of running a bash script that is expected to
return a non-zero exit code:

````md
```bash exec="1" source="tabbed-left" returncode="2"
grep extra_css README.md && exit 2
```
````

See [usage](https://pawamoy.github.io/markdown-exec/usage/) for more details,
and the [gallery](https://pawamoy.github.io/markdown-exec/gallery/) for more examples!

## Sponsors

<!-- sponsors-start -->

<div id="premium-sponsors" style="text-align: center;">

<div id="silver-sponsors"><b>Silver sponsors</b><p>
<a href="https://squidfunk.github.io/mkdocs-material/"><img alt="Material for MkDocs" src="https://raw.githubusercontent.com/squidfunk/mkdocs-material/master/.github/assets/logo.svg" style="height: 320px; "></a><br>
<a href="https://fastapi.tiangolo.com/"><img alt="FastAPI" src="https://raw.githubusercontent.com/tiangolo/fastapi/master/docs/en/docs/img/logo-margin/logo-teal.png" style="height: 200px; "></a><br>
<a href="https://docs.pydantic.dev/latest/"><img alt="Pydantic" src="https://pydantic.dev/assets/for-external/pydantic_logfire_logo_endorsed_lithium_rgb.svg" style="height: 180px; "></a><br>
</p></div>

<div id="bronze-sponsors"><b>Bronze sponsors</b><p>
<a href="https://www.nixtla.io/"><picture><source media="(prefers-color-scheme: light)" srcset="https://www.nixtla.io/img/logo/full-black.svg"><source media="(prefers-color-scheme: dark)" srcset="https://www.nixtla.io/img/logo/full-white.svg"><img alt="Nixtla" src="https://www.nixtla.io/img/logo/full-black.svg" style="height: 60px; "></picture></a><br>
</p></div>
</div>

---

<div id="sponsors"><p>
<a href="https://github.com/ofek"><img alt="ofek" src="https://avatars.githubusercontent.com/u/9677399?u=386c330f212ce467ce7119d9615c75d0e9b9f1ce&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/samuelcolvin"><img alt="samuelcolvin" src="https://avatars.githubusercontent.com/u/4039449?u=42eb3b833047c8c4b4f647a031eaef148c16d93f&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/tlambert03"><img alt="tlambert03" src="https://avatars.githubusercontent.com/u/1609449?u=922abf0524b47739b37095e553c99488814b05db&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/ssbarnea"><img alt="ssbarnea" src="https://avatars.githubusercontent.com/u/102495?u=c7bd9ddf127785286fc939dd18cb02db0a453bce&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/femtomc"><img alt="femtomc" src="https://avatars.githubusercontent.com/u/34410036?u=f13a71daf2a9f0d2da189beaa94250daa629e2d8&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/cmarqu"><img alt="cmarqu" src="https://avatars.githubusercontent.com/u/360986?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/kolenaIO"><img alt="kolenaIO" src="https://avatars.githubusercontent.com/u/77010818?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/ramnes"><img alt="ramnes" src="https://avatars.githubusercontent.com/u/835072?u=3fca03c3ba0051e2eb652b1def2188a94d1e1dc2&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/machow"><img alt="machow" src="https://avatars.githubusercontent.com/u/2574498?u=c41e3d2f758a05102d8075e38d67b9c17d4189d7&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/BenHammersley"><img alt="BenHammersley" src="https://avatars.githubusercontent.com/u/99436?u=4499a7b507541045222ee28ae122dbe3c8d08ab5&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/trevorWieland"><img alt="trevorWieland" src="https://avatars.githubusercontent.com/u/28811461?u=74cc0e3756c1d4e3d66b5c396e1d131ea8a10472&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/laenan8466"><img alt="laenan8466" src="https://avatars.githubusercontent.com/u/21331242?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/MarcoGorelli"><img alt="MarcoGorelli" src="https://avatars.githubusercontent.com/u/33491632?u=7de3a749cac76a60baca9777baf71d043a4f884d&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/analog-cbarber"><img alt="analog-cbarber" src="https://avatars.githubusercontent.com/u/7408243?u=642fc2bdcc9904089c62fe5aec4e03ace32da67d&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/OdinManiac"><img alt="OdinManiac" src="https://avatars.githubusercontent.com/u/22727172?u=36ab20970f7f52ae8e7eb67b7fcf491fee01ac22&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/rstudio-sponsorship"><img alt="rstudio-sponsorship" src="https://avatars.githubusercontent.com/u/58949051?u=0c471515dd18111be30dfb7669ed5e778970959b&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/schlich"><img alt="schlich" src="https://avatars.githubusercontent.com/u/21191435?u=6f1240adb68f21614d809ae52d66509f46b1e877&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/SuperCowPowers"><img alt="SuperCowPowers" src="https://avatars.githubusercontent.com/u/6900187?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/butterlyn"><img alt="butterlyn" src="https://avatars.githubusercontent.com/u/53323535?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/livingbio"><img alt="livingbio" src="https://avatars.githubusercontent.com/u/10329983?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/NemetschekAllplan"><img alt="NemetschekAllplan" src="https://avatars.githubusercontent.com/u/912034?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/EricJayHartman"><img alt="EricJayHartman" src="https://avatars.githubusercontent.com/u/9259499?u=7e58cc7ec0cd3e85b27aec33656aa0f6612706dd&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/15r10nk"><img alt="15r10nk" src="https://avatars.githubusercontent.com/u/44680962?u=f04826446ff165742efa81e314bd03bf1724d50e&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/cdwilson"><img alt="cdwilson" src="https://avatars.githubusercontent.com/u/14631?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/activeloopai"><img alt="activeloopai" src="https://avatars.githubusercontent.com/u/34816118?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/roboflow"><img alt="roboflow" src="https://avatars.githubusercontent.com/u/53104118?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/wrath-codes"><img alt="wrath-codes" src="https://avatars.githubusercontent.com/u/90050913?u=b26582409dfff8ce2b60016fd119be09309708da&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/leodevian"><img alt="leodevian" src="https://avatars.githubusercontent.com/u/167141781?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/cmclaughlin"><img alt="cmclaughlin" src="https://avatars.githubusercontent.com/u/1061109?u=ddf6eec0edd2d11c980f8c3aa96e3d044d4e0468&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/blaisep"><img alt="blaisep" src="https://avatars.githubusercontent.com/u/254456?u=97d584b7c0a6faf583aa59975df4f993f671d121&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/RapidataAI"><img alt="RapidataAI" src="https://avatars.githubusercontent.com/u/104209891?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/rodolphebarbanneau"><img alt="rodolphebarbanneau" src="https://avatars.githubusercontent.com/u/46493454?u=6c405452a40c231cdf0b68e97544e07ee956a733&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/theSymbolSyndicate"><img alt="theSymbolSyndicate" src="https://avatars.githubusercontent.com/u/111542255?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/blakeNaccarato"><img alt="blakeNaccarato" src="https://avatars.githubusercontent.com/u/20692450?u=bb919218be30cfa994514f4cf39bb2f7cf952df4&v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/ChargeStorm"><img alt="ChargeStorm" src="https://avatars.githubusercontent.com/u/26000165?v=4" style="height: 32px; border-radius: 100%;"></a>
<a href="https://github.com/Alphadelta14"><img alt="Alphadelta14" src="https://avatars.githubusercontent.com/u/480845?v=4" style="height: 32px; border-radius: 100%;"></a>
</p></div>


*And 8 more private sponsor(s).*

<!-- sponsors-end -->
