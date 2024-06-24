# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [1.9.3](https://github.com/pawamoy/markdown-exec/releases/tag/1.9.3) - 2024-06-24

<small>[Compare with 1.9.2](https://github.com/pawamoy/markdown-exec/compare/1.9.2...1.9.3)</small>

### Bug Fixes

- Fix patching lines in tracebacks on Python 3.13 ([917af4c](https://github.com/pawamoy/markdown-exec/commit/917af4c90138a861fb488b91b754231a04bf9f96) by Timothée Mazzucotelli). [Issue-58](https://github.com/pawamoy/markdown-exec/issues/58)

## [1.9.2](https://github.com/pawamoy/markdown-exec/releases/tag/1.9.2) - 2024-06-20

<small>[Compare with 1.9.1](https://github.com/pawamoy/markdown-exec/compare/1.9.1...1.9.2)</small>

### Bug Fixes

- Render source even if output is empty ([d3f1e6b](https://github.com/pawamoy/markdown-exec/commit/d3f1e6bcf245c656b0014e859e66137ad1e89549) by Timothée Mazzucotelli). [Issue-57](https://github.com/pawamoy/markdown-exec/issues/57)

## [1.9.1](https://github.com/pawamoy/markdown-exec/releases/tag/1.9.1) - 2024-06-14

<small>[Compare with 1.9.0](https://github.com/pawamoy/markdown-exec/compare/1.9.0...1.9.1)</small>

### Build

- Re-include tests folder in source distributions ([ae549db](https://github.com/pawamoy/markdown-exec/commit/ae549dbfb7382cf4fa8c35bdcfa4619231f37f4b) by Timothée Mazzucotelli). [Issue-55](https://github.com/pawamoy/markdown-exec/issues/55)

## [1.9.0](https://github.com/pawamoy/markdown-exec/releases/tag/1.9.0) - 2024-06-13

<small>[Compare with 1.8.3](https://github.com/pawamoy/markdown-exec/compare/1.8.3...1.9.0)</small>

### Features

- Abort with error when the plugin is configured to require the ANSI extra but it is not installed ([25bcbbe](https://github.com/pawamoy/markdown-exec/commit/25bcbbe6cbc0e0df764456a508f03de2abfcd938) by Timothée Mazzucotelli).
- Allow excluding assets when rendering Pyodide fence ([5412353](https://github.com/pawamoy/markdown-exec/commit/541235354210522f67af8ff2dc03dfa5216bca20) by Timothée Mazzucotelli).
- Detect when SuperFences is not enabled and error out early ([5d771d2](https://github.com/pawamoy/markdown-exec/commit/5d771d285cecfcb631438f04b94f5b20275d03df) by Timothée Mazzucotelli). [Issue-39](https://github.com/pawamoy/markdown-exec/issues/39)
- Allow changing the console width for the execution of code blocks ([76d603c](https://github.com/pawamoy/markdown-exec/commit/76d603ce57232f2ee98f5abec265d2f67174fbdd) by Timothée Mazzucotelli). [Issue-34](https://github.com/pawamoy/markdown-exec/issues/34)
- Allow automatic execution of code blocks thanks to the `MARKDOWN_EXEC_AUTO` environment variable ([0db27b2](https://github.com/pawamoy/markdown-exec/commit/0db27b23dd7697afb19755b4ec32db43c4add75a) by Timothée Mazzucotelli). [Issue-24](https://github.com/pawamoy/markdown-exec/issues/24)
- Allow changing working directory for code blocks execution ([ee3fae9](https://github.com/pawamoy/markdown-exec/commit/ee3fae957193e2beb6ac9a0bad3b261d1b67584e) by Timothée Mazzucotelli). [Issue-20](https://github.com/pawamoy/markdown-exec/issues/20)

### Bug Fixes

- Reuse existing loggers tp prevent wrong dispatch ([8967270](https://github.com/pawamoy/markdown-exec/commit/8967270d821e5e021a2298ff8e458bc6ce0f1762) by Timothée Mazzucotelli).
- Don't render anything when code block output is empty ([4337d13](https://github.com/pawamoy/markdown-exec/commit/4337d1337b5aedd190627287f7e0a48000396902) by Timothée Mazzucotelli). [Issue-17](https://github.com/pawamoy/markdown-exec/issues/17)
- Increase minimum height of Pyodide output code blocks ([93598b2](https://github.com/pawamoy/markdown-exec/commit/93598b285babfca59b2b297adf804719f012f812) by Timothée Mazzucotelli). [Issue-40](https://github.com/pawamoy/markdown-exec/issues/40)
- Fix removal of temporary div for headings forwarding ([c012c1d](https://github.com/pawamoy/markdown-exec/commit/c012c1d9f194f492dcb055638c790580aa91c51e) by Timothée Mazzucotelli). [Issue-50](https://github.com/pawamoy/markdown-exec/issues/50)

### Code Refactoring

- Wrap placeholders in `<div>` to avoid them being wrapped in `<p>` ([500ed1b](https://github.com/pawamoy/markdown-exec/commit/500ed1b3a6bb94edd3d5d7152cd818bc3db27bbd) by Timothée Mazzucotelli).

## [1.8.3](https://github.com/pawamoy/markdown-exec/releases/tag/1.8.3) - 2024-05-22

<small>[Compare with 1.8.2](https://github.com/pawamoy/markdown-exec/compare/1.8.2...1.8.3)</small>

### Bug Fixes

- Don't leak future annotations in user code ([ba0c35e](https://github.com/pawamoy/markdown-exec/commit/ba0c35e89e3056325b3dcbc7e61b6f108ec55885) by Timothée Mazzucotelli). [Issue-47](https://github.com/pawamoy/markdown-exec/issues/47)

## [1.8.2](https://github.com/pawamoy/markdown-exec/releases/tag/1.8.2) - 2024-05-20

<small>[Compare with 1.8.1](https://github.com/pawamoy/markdown-exec/compare/1.8.1...1.8.2)</small>

### Bug Fixes

- Give `__name__` to executed Python "modules", and populate `sys.modules` too ([db25ee7](https://github.com/pawamoy/markdown-exec/commit/db25ee703da9b70cb4a13b2b4b61634d697119c4) by Timothée Mazzucotelli). [Issue-47](https://github.com/pawamoy/markdown-exec/issues/47)

## [1.8.1](https://github.com/pawamoy/markdown-exec/releases/tag/1.8.1) - 2024-04-15

<small>[Compare with 1.8.0](https://github.com/pawamoy/markdown-exec/compare/1.8.0...1.8.1)</small>

### Bug Fixes

- Add missing CSS classes to the ANSI stylesheet ([51493f2](https://github.com/pawamoy/markdown-exec/commit/51493f255dd91f28ce6c8d7e7176ec5687e28b4a) by Timothée Mazzucotelli). [Issue-43](https://github.com/pawamoy/markdown-exec/issues/43)

## [1.8.0](https://github.com/pawamoy/markdown-exec/releases/tag/1.8.0) - 2024-01-05

<small>[Compare with 1.7.0](https://github.com/pawamoy/markdown-exec/compare/1.7.0...1.8.0)</small>

### Features

- Add `pyodide` fence ([3a2fab0](https://github.com/pawamoy/markdown-exec/commit/3a2fab0b23196a4122bcee6d9b81d3f421f11bbb) by Timothée Mazzucotelli).
- Add `ansi` option to mark ANSI extra as required or not ([27743c2](https://github.com/pawamoy/markdown-exec/commit/27743c20f56dd00ce730e1d028d362a4f95e48c7) by Timothée Mazzucotelli). [Issue #28](https://github.com/pawamoy/markdown-exec/issues/28), [Issue #29](https://github.com/pawamoy/markdown-exec/issues/29)

### Code Refactoring

- Modernize MkDocs plugin ([4864608](https://github.com/pawamoy/markdown-exec/commit/48646081746c6c5ece0c6566a4b9733ace518791) by Timothée Mazzucotelli).

## [1.7.0](https://github.com/pawamoy/markdown-exec/releases/tag/1.7.0) - 2023-10-17

<small>[Compare with 1.6.0](https://github.com/pawamoy/markdown-exec/compare/1.6.0...1.7.0)</small>

### Features

- Set `MKDOCS_CONFIG_DIR` environment variable to build file path relative to it ([a2cbea5](https://github.com/pawamoy/markdown-exec/commit/a2cbea52d39ef43960c910830eae14dc846624d0) by Timothée Mazzucotelli).

## [1.6.0](https://github.com/pawamoy/markdown-exec/releases/tag/1.6.0) - 2023-04-18

<small>[Compare with 1.5.3](https://github.com/pawamoy/markdown-exec/compare/1.5.3...1.6.0)</small>

### Features

- Add `idprefix` option allowing to change/remove HTML id/href prefixes ([4d91463](https://github.com/pawamoy/markdown-exec/commit/4d914630e5642feb87103644800d3c9f7b59c6ad) by Timothée Mazzucotelli).

## [1.5.3](https://github.com/pawamoy/markdown-exec/releases/tag/1.5.3) - 2023-04-18

<small>[Compare with 1.5.2](https://github.com/pawamoy/markdown-exec/compare/1.5.2...1.5.3)</small>

### Code Refactoring

- Reuse Markdown configuration as declared in mkdocs.yml ([afe091c](https://github.com/pawamoy/markdown-exec/commit/afe091caa33ed54fd65e25e4f90b8b60786ba3f9) by Timothée Mazzucotelli).

## [1.5.2](https://github.com/pawamoy/markdown-exec/releases/tag/1.5.2) - 2023-04-18

<small>[Compare with 1.5.1](https://github.com/pawamoy/markdown-exec/compare/1.5.1...1.5.2)</small>

### Code Refactoring

- Reset counter in post build event ([3bf80de](https://github.com/pawamoy/markdown-exec/commit/3bf80deabe9a7438b459c73e962c9693bce71135) by Timothée Mazzucotelli).

## [1.5.1](https://github.com/pawamoy/markdown-exec/releases/tag/1.5.1) - 2023-04-17

<small>[Compare with 1.5.0](https://github.com/pawamoy/markdown-exec/compare/1.5.0...1.5.1)</small>

### Bug Fixes

- Remove pycon output lines when rendering source as console ([fb5a23d](https://github.com/pawamoy/markdown-exec/commit/fb5a23d8d1d50aa2a1ede97150c269a07fa200ec) by Timothée Mazzucotelli).
- Fix nested rendering ([a110d44](https://github.com/pawamoy/markdown-exec/commit/a110d446209b390ec8a4ad8868818352f72a9808) by Timothée Mazzucotelli).

## [1.5.0](https://github.com/pawamoy/markdown-exec/releases/tag/1.5.0) - 2023-04-17

<small>[Compare with 1.4.1](https://github.com/pawamoy/markdown-exec/compare/1.4.1...1.5.0)</small>

### Features

- Update ToC with generated headings ([5ea2263](https://github.com/pawamoy/markdown-exec/commit/5ea2263d53729b6d3e79da69c29b171bb6c3e22d) by Timothée Mazzucotelli).

## [1.4.1](https://github.com/pawamoy/markdown-exec/releases/tag/1.4.1) - 2023-04-16

<small>[Compare with 1.4.0](https://github.com/pawamoy/markdown-exec/compare/1.4.0...1.4.1)</small>

### Bug Fixes

- Improve handling of errors within sessions ([87ac5f3](https://github.com/pawamoy/markdown-exec/commit/87ac5f352ce44370f52a7fb56d846c04b76447f9) by Timothée Mazzucotelli).
- Swallow non-extra parameters in run functions ([f5d4fef](https://github.com/pawamoy/markdown-exec/commit/f5d4fef1f78d94c3f8850f873076e3cd68c0a981) by Timothée Mazzucotelli).

### Code Refactoring

- Simplify tree formatter signature ([09d5427](https://github.com/pawamoy/markdown-exec/commit/09d542772ccb0d1250366b39fa3a9c9362e1ed42) by Timothée Mazzucotelli).

## [1.4.0](https://github.com/pawamoy/markdown-exec/releases/tag/1.4.0) - 2023-03-15

<small>[Compare with 1.3.0](https://github.com/pawamoy/markdown-exec/compare/1.3.0...1.4.0)</small>

### Features

- Sessions: persist and reuse state for Python and Pycon code blocks ([a8fef5e](https://github.com/pawamoy/markdown-exec/commit/a8fef5e90b1d7165e16ff5afe4b84e8441503098) by Timothée Mazzucotelli). [Issue #16](https://github.com/pawamoy/markdown-exec/issues/16)

## [1.3.0](https://github.com/pawamoy/markdown-exec/releases/tag/1.3.0) - 2023-02-18

<small>[Compare with 1.2.0](https://github.com/pawamoy/markdown-exec/compare/1.2.0...1.3.0)</small>

### Features

- Support wrapping result with console source ([268c82e](https://github.com/pawamoy/markdown-exec/commit/268c82e6f005dcaa1ddc75608d2f28927f069761) by Timothée Mazzucotelli). [Issue #13](https://github.com/pawamoy/markdown-exec/issues/13)

### Code Refactoring

- Remove margin hack from Material source ([beec237](https://github.com/pawamoy/markdown-exec/commit/beec2374b27075e66ddb4a7cdc2f2c81b7455b95) by Timothée Mazzucotelli).
- Better support pycon syntax ([22b51c6](https://github.com/pawamoy/markdown-exec/commit/22b51c64155060922e46ea10e6c0d1c1c1b00a2f) by Timothée Mazzucotelli).

## [1.2.0](https://github.com/pawamoy/markdown-exec/releases/tag/1.2.0) - 2023-02-01

<small>[Compare with 1.1.0](https://github.com/pawamoy/markdown-exec/compare/1.1.0...1.2.0)</small>

### Features
- Support ANSI code blocks ([39719c5](https://github.com/pawamoy/markdown-exec/commit/39719c5d7ac1bbde6d60002082a0ad3b48730545) by Timothée Mazzucotelli). [Issue #11](https://github.com/pawamoy/markdown-exec/issues/11)


## [1.1.0](https://github.com/pawamoy/markdown-exec/releases/tag/1.1.0) - 2023-01-27

<small>[Compare with 1.0.0](https://github.com/pawamoy/markdown-exec/compare/1.0.0...1.1.0)</small>

### Features
- Log details to help debugging errors ([4c0228d](https://github.com/pawamoy/markdown-exec/commit/4c0228da41f5970e719b20a40c0fab47a9d12244) by Timothée Mazzucotelli). [Issue #12](https://github.com/pawamoy/markdown-exec/issues/12)
- Allow expecting specific exit codes ([620ec66](https://github.com/pawamoy/markdown-exec/commit/620ec66182dd0f84600258408720779822615085) by Timothée Mazzucotelli). [Issue #10](https://github.com/pawamoy/markdown-exec/issues/10)

### Code Refactoring
- Formatters now only accept keyword arguments ([0940ca9](https://github.com/pawamoy/markdown-exec/commit/0940ca98e81548474351e234715df2fc290fdc1e) by Timothée Mazzucotelli).


## [1.0.0](https://github.com/pawamoy/markdown-exec/releases/tag/1.0.0) - 2022-11-24

<small>[Compare with 0.7.4](https://github.com/pawamoy/markdown-exec/compare/0.7.4...1.0.0)</small>

### Features
- Allow defining IDs on code blocks (for warnings) ([0091167](https://github.com/pawamoy/markdown-exec/commit/009116719e81dd91190b391c82709fb179a62364) by Timothée Mazzucotelli).

### Code Refactoring
- Use base format everywhere (more flexible) ([cefba70](https://github.com/pawamoy/markdown-exec/commit/cefba704ae45df1b115b969e3d4d5105ebd052dd) by Timothée Mazzucotelli).


## [0.7.4](https://github.com/pawamoy/markdown-exec/releases/tag/0.7.4) - 2022-11-13

<small>[Compare with 0.7.3](https://github.com/pawamoy/markdown-exec/compare/0.7.3...0.7.4)</small>

### Bug Fixes
- Render source for non-HTML output (regression) ([3028dcd](https://github.com/pawamoy/markdown-exec/commit/3028dcd4f20f94b578995c326fd68d53a6dc3638) by Timothée Mazzucotelli).


## [0.7.3](https://github.com/pawamoy/markdown-exec/releases/tag/0.7.3) - 2022-11-13

<small>[Compare with 0.7.2](https://github.com/pawamoy/markdown-exec/compare/0.7.2...0.7.3)</small>

### Bug Fixes
- Don't wrap HTML in `p` tag ([420d79d](https://github.com/pawamoy/markdown-exec/commit/420d79d67c2a6bdc925b3bc3d89790258f922317) by Timothée Mazzucotelli).


## [0.7.2](https://github.com/pawamoy/markdown-exec/releases/tag/0.7.2) - 2022-09-01

<small>[Compare with 0.7.1](https://github.com/pawamoy/markdown-exec/compare/0.7.1...0.7.2)</small>

### Bug Fixes
- Make `tree` formatter forward extra options ([54996a9](https://github.com/pawamoy/markdown-exec/commit/54996a9bc2c803bb8c9de0861af69723ddb000fa) by Timothée Mazzucotelli).
- Fix race condition issue ([37d7f86](https://github.com/pawamoy/markdown-exec/commit/37d7f86eeaa73029ae89c1c5d07146d2387b10d3) by Timothée Mazzucotelli).


## [0.7.1](https://github.com/pawamoy/markdown-exec/releases/tag/0.7.1) - 2022-08-28

<small>[Compare with 0.7.0](https://github.com/pawamoy/markdown-exec/compare/0.7.0...0.7.1)</small>

### Bug Fixes
- Allow printing non-string objects ([ceaa482](https://github.com/pawamoy/markdown-exec/commit/ceaa482d16adfbd1609595a2ed6a241bad71f9de) by Timothée Mazzucotelli). [Issue #7](https://github.com/pawamoy/markdown-exec/issues/7)


## [0.7.0](https://github.com/pawamoy/markdown-exec/releases/tag/0.7.0) - 2022-05-28

<small>[Compare with 0.6.0](https://github.com/pawamoy/markdown-exec/compare/0.6.0...0.7.0)</small>

### Features
- Add ability to hide source lines ([3cb1934](https://github.com/pawamoy/markdown-exec/commit/3cb19345fa2b65478ac439b5f486d04bf5ff5337) by Timothée Mazzucotelli).


## [0.6.0](https://github.com/pawamoy/markdown-exec/releases/tag/0.6.0) - 2022-05-21

<small>[Compare with 0.5.0](https://github.com/pawamoy/markdown-exec/compare/0.5.0...0.6.0)</small>

### Features
- Add tree formatter ([8096990](https://github.com/pawamoy/markdown-exec/commit/8096990dcbf6795572e5e5afee12195d5a56c6f6) by Timothée Mazzucotelli).
- Handle code blocks execution errors and log warnings ([34e16db](https://github.com/pawamoy/markdown-exec/commit/34e16db679721db7d1df375912d512b5aed80b1a) by Timothée Mazzucotelli).

### Bug Fixes
- Fix Python execution to support nested scopes ([74b9a95](https://github.com/pawamoy/markdown-exec/commit/74b9a95ade3862752fb78d6c64be8b9b1d4d3886) by Timothée Mazzucotelli).


## [0.5.0](https://github.com/pawamoy/markdown-exec/releases/tag/0.5.0) - 2022-05-09

<small>[Compare with 0.4.0](https://github.com/pawamoy/markdown-exec/compare/0.4.0...0.5.0)</small>

### Features
- Allow wrapping result in code block ([37201e4](https://github.com/pawamoy/markdown-exec/commit/37201e4409badec903f311bcc0a6ab7acddff37c) by Timothée Mazzucotelli).
- Add support for shell code blocks ([f2b4b67](https://github.com/pawamoy/markdown-exec/commit/f2b4b671f4399637d0dac235a0af7739033f9526) by Timothée Mazzucotelli).

### Code Refactoring
- Fetch plugin languages from dict ([de8309e](https://github.com/pawamoy/markdown-exec/commit/de8309e6895a079031461bfea317215bcff9bc21) by Timothée Mazzucotelli).
- Add reusable base formatter ([c265bee](https://github.com/pawamoy/markdown-exec/commit/c265bee9abf0ad545b7fdc6ccf2e320071295a18) by Timothée Mazzucotelli).


## [0.4.0](https://github.com/pawamoy/markdown-exec/releases/tag/0.4.0) - 2022-05-09

<small>[Compare with 0.3.1](https://github.com/pawamoy/markdown-exec/compare/0.3.1...0.4.0)</small>

### Features
- Add literate Markdown support ([8d3ed7e](https://github.com/pawamoy/markdown-exec/commit/8d3ed7ef5c9a88849be0a5da44e7b478eb44c180) by Timothée Mazzucotelli).
- Add `material-block` style to show source ([ff10ee1](https://github.com/pawamoy/markdown-exec/commit/ff10ee1f0b55b2e77b97f272b49b24024f9de2ac) by Timothée Mazzucotelli).
- Support up to 8 levels of exec code block nesting ([bfde808](https://github.com/pawamoy/markdown-exec/commit/bfde8087ca6f4eb91aba8eb01b37755dfacb4cdb) by Timothée Mazzucotelli).


## [0.3.1](https://github.com/pawamoy/markdown-exec/releases/tag/0.3.1) - 2022-05-07

<small>[Compare with 0.3.0](https://github.com/pawamoy/markdown-exec/compare/0.3.0...0.3.1)</small>

### Bug Fixes
- Actually prevent HTML re-rendering ([4374852](https://github.com/pawamoy/markdown-exec/commit/4374852706207beac3b8dbd8dc9d75be51b1df0d) by Timothée Mazzucotelli).


## [0.3.0](https://github.com/pawamoy/markdown-exec/releases/tag/0.3.0) - 2022-05-01

<small>[Compare with 0.2.0](https://github.com/pawamoy/markdown-exec/compare/0.2.0...0.3.0)</small>

### Features
- Support `pycon` code blocks ([2c86394](https://github.com/pawamoy/markdown-exec/commit/2c86394417858654af21316c3555aff0e9fd2d26) by Timothée Mazzucotelli).
- Add `console` source integration option ([62dfd74](https://github.com/pawamoy/markdown-exec/commit/62dfd74185f7f33cdf6f4726b3aa898a1ac5d22f) by Timothée Mazzucotelli).
- Provide a MkDocs plugin for easier setup ([5fce814](https://github.com/pawamoy/markdown-exec/commit/5fce81462063b7c61d9833939e44958a466d4b24) by Timothée Mazzucotelli).
- Support changing tabs titles ([d150596](https://github.com/pawamoy/markdown-exec/commit/d150596beda1e5a5304bc06e27668294a75ff220) by Timothée Mazzucotelli).
- Allow using `print` in code blocks ([7c124fd](https://github.com/pawamoy/markdown-exec/commit/7c124fd416d6923bea2834479d972b14c3e22112) by Timothée Mazzucotelli).
- Allow passing extra opts like title to source code blocks ([bb3252a](https://github.com/pawamoy/markdown-exec/commit/bb3252a3e959cea198966ba59a70f6f5aa57a963) by Timothée Mazzucotelli).

### Code Refactoring
- Split Python formatter to allow reuse ([fc56702](https://github.com/pawamoy/markdown-exec/commit/fc56702b9c393323adc30abba42c823f601ef738) by Timothée Mazzucotelli).
- Setup a more robust Markdown converter ([395f4c4](https://github.com/pawamoy/markdown-exec/commit/395f4c4c21ab7f4afcc88250c1fd882269a06d02) by Timothée Mazzucotelli).


## [0.2.0](https://github.com/pawamoy/markdown-exec/releases/tag/0.2.0) - 2022-04-18

<small>[Compare with 0.1.0](https://github.com/pawamoy/markdown-exec/compare/0.1.0...0.2.0)</small>

### Features
- Add ability to render using tabs ([91a95ae](https://github.com/pawamoy/markdown-exec/commit/91a95ae4c6ad82e85dac24a110d09ca71eff688a) by Timothée Mazzucotelli).


## [0.1.0](https://github.com/pawamoy/markdown-exec/releases/tag/0.1.0) - 2022-02-19

<small>[Compare with first commit](https://github.com/pawamoy/markdown-exec/compare/41c8d81992d2443cd5c3418df0f461b0af1a6ec8...0.1.0)</small>

### Features
- Implement execution of code blocks ([41c8d81](https://github.com/pawamoy/markdown-exec/commit/41c8d81992d2443cd5c3418df0f461b0af1a6ec8) by Timothée Mazzucotelli).
