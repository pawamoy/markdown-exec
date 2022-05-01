# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
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
