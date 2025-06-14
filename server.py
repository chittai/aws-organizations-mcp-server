#!/usr/bin/env python3
"""
AWS Organizations MCP Server
最小実装版 - helloツールのみ
"""

from mcp.server.fastmcp import FastMCP

# MCPサーバを作成
mcp = FastMCP("AWS Organizations MCP Server")

@mcp.tool()
def hello(name: str = "World") -> str:
    """MCPサーバの動作確認用のシンプルなツール
    
    Args:
        name: 挨拶する相手の名前 (デフォルト: "World")
        
    Returns:
        str: 挨拶メッセージ
    """
    return f"Hello, {name}! AWS Organizations MCPサーバが正常に動作しています。"

if __name__ == "__main__":
    # サーバを実行
    mcp.run()
