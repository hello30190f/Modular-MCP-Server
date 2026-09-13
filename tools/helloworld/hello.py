from datetime import datetime
from server import mcp

@mcp.tool()
def hello_world(name: str) -> str:
    """挨拶を返します。"""
    return f"こんにちは、{name}さん！"