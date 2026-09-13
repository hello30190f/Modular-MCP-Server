# tools.py
from datetime import datetime
from server import mcp  # 作成したインスタンスをインポート

# 他にツールを増やしたい場合は、ここに追加していく
@mcp.tool()
def hello_world(name: str) -> str:
    """挨拶を返します。"""
    return f"こんにちは、{name}さん！"