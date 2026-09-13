# main.py
from server import mcp
import runtime  # ツールを登録させるためにインポートが必要

if __name__ == "__main__":
    # 開発モードでSSEサーバとして起動
    mcp.run(transport="sse", host="0.0.0.0", port=8000)