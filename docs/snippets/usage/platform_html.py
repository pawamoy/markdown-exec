import platform

print(
    f"""
    <ul>
    <li>machine: <code>{platform.machine()}</code></li>
    <li>version: <code>{platform.version()}</code></li>
    <li>platform: <code>{platform.platform()}</code></li>
    <li>system: <code>{platform.system()}</code></li>
    </ul>
    """
)
