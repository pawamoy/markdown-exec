# Caching

Markdown Exec supports filesystem-based caching of code execution results to speed up documentation builds and development workflows.

## Overview

When generating images, charts, or running expensive computations in your documentation, re-executing the same code on every build can significantly slow down the rendering process. The caching feature allows you to:

- **Speed up builds**: Reuse previously computed results instead of re-executing code
- **Persist across builds**: All cache is stored on the filesystem for cross-build persistence
- **Global cache refresh**: Force refresh of all cached results with a single environment variable

## Cache Storage

All cached results are stored in `.markdown-exec-cache/` in your project root directory:

```sh
your-project/
├── docs/
├── mkdocs.yml
└── .markdown-exec-cache/
    └── abc123def456.cache      # Hash-based cache files
```

Add this directory to your `.gitignore`:

```gitignore
.markdown-exec-cache/
```

## Usage

### Hash-Based Caching

Enable caching by adding `cache="yes"` to your code block. A hash is computed from the code content and execution options:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="yes" cache="yes"
import time
print(f"Executed at: {time.time()}")
```
````

The cache is automatically invalidated when the code or execution options change.

### Cache Invalidation

The cache is automatically invalidated when the code content or execution options change (a new hash is computed). **Stale cache files** — from code blocks that have been removed or changed — are cleaned up automatically:

- **MkDocs builds**: at the end of each build (`on_post_build`), any `.cache` file not used during that build is deleted.
- **Standalone usage**: stale files are cleaned up when the Python process exits.

To force re-execution of **all** cached blocks (e.g. when an external dependency changes), use the `MARKDOWN_EXEC_CACHE_REFRESH` environment variable instead of touching the code:

```bash
# Force refresh all caches during build
MARKDOWN_EXEC_CACHE_REFRESH=1 mkdocs build

# Or with other truthy values
MARKDOWN_EXEC_CACHE_REFRESH=yes mkdocs build
MARKDOWN_EXEC_CACHE_REFRESH=true mkdocs build
MARKDOWN_EXEC_CACHE_REFRESH=on mkdocs build
```

This is useful for:

- CI/CD pipelines where you want fresh builds
- Ensuring all documentation is up-to-date
- Debugging cache-related issues

## Clearing Cache

Remove the entire cache directory:

```bash
rm -rf .markdown-exec-cache/
```

## How It Works

1. **Hash Computation**: For `cache="yes"`, a SHA-256 hash is computed from:

   - The code content
   - Execution options (language, HTML mode, working directory, etc.)

1. **Cache Lookup**: Before execution, the filesystem cache is checked for a matching entry

1. **Execution & Storage**: If no cached result is found:

   - Code is executed
   - Output is stored in the filesystem cache

1. **Cache Retrieval**: Cached output is used instead of re-executing the code

## Best Practices

### When to Use Caching

✅ **Good use cases:**

- Generating plots, diagrams, or images
- Running expensive computations
- Calling external APIs or services
- Processing large datasets

❌ **Avoid caching for:**

- Simple print statements
- Code demonstrating output variations
- Time-sensitive or non-deterministic code

### Choosing Cache Type

Use `cache="yes"` for all caching needs. The cache is automatically invalidated when the code or execution options change — no manual cache management needed.

### Cache Invalidation Strategy

Cache is automatically invalidated when code or options change — no manual intervention needed. To force re-execution of all cached blocks, use:

```bash
MARKDOWN_EXEC_CACHE_REFRESH=1 mkdocs build
```

Or [clear the cache directory](#clearing-cache) before the build.

## Examples

### Caching a Matplotlib Plot

````markdown
```python exec="yes" html="yes" cache="yes"
import matplotlib.pyplot as plt
import io
import base64

# Expensive plot generation
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
ax.set_title("Population Growth")

# Save to base64
buffer = io.BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)
img_str = base64.b64encode(buffer.read()).decode()
print(f'<img src="data:image/png;base64,{img_str}"/>')
plt.close()
```
````

## Troubleshooting

### Cache Not Working

1. Ensure the cache directory is writable
1. Check that you're using `cache="yes"` or a custom ID
1. Verify the cache directory exists: `ls -la .markdown-exec-cache/`

### Stale Cache Results

1. Use `refresh="yes"` to force re-execution
1. Delete the specific cache file
1. Clear the entire cache directory

### Large Cache Directory

Cache files accumulate over time. Periodically clean up:

```bash
# See cache directory size
du -sh .markdown-exec-cache/

# Remove all cache files
rm -rf .markdown-exec-cache/
```
