# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
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
