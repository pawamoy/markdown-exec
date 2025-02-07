# TypeScript

## Regular TypeScript

TypeScript code is executed via a Jupyter kernel. Markdown Exec will attempt to
use any kernel that lists TypeScript as a supported language, however
Markdown Exec is tested using the Jupyter kernel provided by the Deno project.
See Deno's [installation instructions](https://docs.deno.com/runtime/getting_started/installation/)
and [Jupyter kernel docs](https://docs.deno.com/runtime/reference/cli/jupyter/#quickstart)
for more information.

### Output capturing

Outputs are captured just as they are in jupyter notebooks.

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```typescript exec="1"
console.log("**Hello world!**");
```
````

### Type checking

TypeScript code blocks will be type checked using Deno's type checker.

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```typescript exec="yes" returncode="1"
const x: string = 1;
```
````

## TypeScript REPL console code

Code blocks syntax-highlighted with the `tscon` identifier are also supported.
These code blocks will be pre-processed to keep only the lines
starting with `> `, and the chevron (prompt) will be removed from these lines,
so we can execute them. Continuation lines starting with `... ` are also supported
(and the ellipses will be removed as well).

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```tscon exec="1" source="console"
--8<-- "usage/source.tscon"
```
````

It also means that multiple blocks of instructions will be concatenated,
as well as their output:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```tscon exec="1" source="console"
--8<-- "usage/multiple.tscon"
```
````
