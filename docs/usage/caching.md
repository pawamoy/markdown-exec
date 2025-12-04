# Caching

Markdown Exec supports filesystem-based caching of code execution results to speed up documentation builds and development workflows.

## Overview

When generating images, charts, or running expensive computations in your documentation, re-executing the same code on every build can significantly slow down the rendering process. The caching feature allows you to:

- **Speed up builds**: Reuse previously computed results instead of re-executing code
- **Persist across builds**: All cache is stored on the filesystem for cross-build persistence
- **Global cache refresh**: Force refresh of all cached results with a single environment variable

## Cache Storage

All cached results are stored in `.markdown-exec-cache/` in your project root directory:

```
your-project/
├── docs/
├── mkdocs.yml
└── .markdown-exec-cache/
    ├── my-plot.cache          # Custom ID cache
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

### Custom Cache IDs

For more control, use a custom cache ID (string value). This is useful for expensive operations where you want explicit control over cache invalidation:

````md exec="1" source="tabbed-left" tabs="Markdown|Rendered"
```python exec="yes" cache="my-plot"
import matplotlib.pyplot as plt
# Expensive plot generation...
print("Generated plot")
```
````

The cache file will be stored as `.markdown-exec-cache/my-plot.cache`.

### Cache Invalidation

To force re-execution and update the cache for a specific code block, use `refresh="yes"`:

```markdown
```python exec="yes" cache="my-plot" refresh="yes"
# This will always re-execute and update the cache
print("Fresh execution!")
```
```

!!! note "refresh vs removing cache"
    **`refresh="yes"`** forces re-execution but **keeps the cache enabled** - it updates the cached result for future builds.
    
    **Removing `cache` option** completely disables caching - the code executes every time with no caching at all.
    
    Use `refresh="yes"` when you want to update stale cache but keep caching benefits for subsequent builds.

### Global Cache Refresh

To refresh **all** cached results at once, set the `MARKDOWN_EXEC_CACHE_REFRESH` environment variable:

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

### Delete Specific Cache Entry

Remove the cache file for a specific custom ID:

```bash
rm .markdown-exec-cache/my-custom-id.cache
```

### Clear All Cache

Remove the entire cache directory:

```bash
rm -rf .markdown-exec-cache/
```

## How It Works

1. **Hash Computation**: For `cache="yes"`, a SHA-256 hash is computed from:
   - The code content
   - Execution options (language, HTML mode, working directory, etc.)
   
2. **Cache Lookup**: Before execution, the filesystem cache is checked for a matching entry
   
3. **Execution & Storage**: If no cached result is found:
   - Code is executed
   - Output is stored in the filesystem cache
   
4. **Cache Retrieval**: Cached output is used instead of re-executing the code

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

- **`cache="yes"`** (hash-based):
  - Automatically invalidated when code changes
  - Great for development and production
  - No manual cache management needed

- **`cache="custom-id"`** (custom ID):
  - Use for expensive operations where you want explicit control
  - Easier to identify and manage specific cache files
  - Requires manual invalidation or `refresh="yes"` when code changes

### Cache Invalidation Strategy

**For hash-based caching (`cache="yes"`):**
- Cache is automatically invalidated when code or options change
- No manual intervention needed

**For custom ID caching (`cache="custom-id"`):**

1. **Change the ID** when you want to force re-execution:
   ```markdown
   cache="my-plot-v2"  # Changed from my-plot
   ```

2. **Use refresh temporarily**:
   ```markdown
   cache="my-plot" refresh="yes"  # Remove refresh="yes" after update
   ```

3. **Use global refresh** for all caches:
   ```bash
   MARKDOWN_EXEC_CACHE_REFRESH=1 mkdocs build
   ```

4. **Clear cache directory** before important builds:
   ```bash
   rm -rf .markdown-exec-cache/
   ```

## Examples

### Caching a Matplotlib Plot

````markdown
```python exec="yes" html="yes" cache="population-chart"
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

### Caching API Calls

````markdown
```python exec="yes" cache="github-stars" refresh="no"
import requests
response = requests.get("https://api.github.com/repos/pawamoy/markdown-exec")
stars = response.json()["stargazers_count"]
print(f"⭐ **{stars}** stars on GitHub!")
```
````

## Troubleshooting

### Cache Not Working

1. Ensure the cache directory is writable
2. Check that you're using `cache="yes"` or a custom ID
3. Verify the cache directory exists: `ls -la .markdown-exec-cache/`

### Stale Cache Results

1. Use `refresh="yes"` to force re-execution
2. Delete the specific cache file
3. Clear the entire cache directory

### Large Cache Directory

Cache files accumulate over time. Periodically clean up:

```bash
# See cache directory size
du -sh .markdown-exec-cache/

# Remove all cache files
rm -rf .markdown-exec-cache/
```
