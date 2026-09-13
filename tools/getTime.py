# tools.py
from datetime import datetime
from server import mcp  # 作成したインスタンスをインポート

@mcp.tool()
def get_current_time() -> str:
    """現在の正確な日付と時刻を取得します。"""
    now = datetime.now()
    return f"現在の時刻は {now.strftime('%Y-%m-%d %H:%M:%S')} です。"
