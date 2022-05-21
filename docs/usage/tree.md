# Tree

Markdown Exec provides a `tree` formatter that can be used
to render file-system trees easily:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```tree
root1
    file1
    dir1
        file
    dir2
        file1
        file2
    file2
    file3
root2
    file1
```
````

By default, the language used for syntax highlight is `bash`.
It means you can add comments with `#`:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```tree
root1            # comment 1
    file1
    dir1
        file
    dir2
        file1    # comment 2
        file2    # comment 3
    file2
    file3
root2
    file1
```
````

You can change the syntax highlight language with the `result` option:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```tree result="javascript"
root1            // comment 1
    file1
    dir1
        file
    dir2
        file1    // comment 2
        file2    // comment 3
    file2
    file3
root2
    file1
```
````

You can force an entry to be displayed as a directory instead of a regular file
by appending a trailing slash to the name:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```tree
root1
    dir1/
    dir2/
    dir3/
```
````

It is recommended to always append trailing slashes to directory anyway.

WARNING: **Limitation**  
Spaces in file names are not supported when searching for a trailing slash.
