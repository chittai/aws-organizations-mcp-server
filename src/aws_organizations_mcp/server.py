#!/usr/bin/env python3
"""
AWS Organizations MCP Server Main Implementation
AWS公式MCPサーバの実装パターンに準拠
"""

import sys
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from .config import config
from .tools.health_tools import register_health_tools
from .tools.scp_tools import register_scp_tools


def create_server() -> FastMCP:
    """MCPサーバを作成
    
    Returns:
        FastMCP: 設定されたMCPサーバインスタンス
    """
    # サーバー名とバージョン情報
    server_name = "AWS Organizations MCP Server"
    
    if config.is_debug:
        server_name += f" (Profile: {config.aws_profile}, Region: {config.aws_region})"
    
    # MCPサーバを作成
    mcp = FastMCP(server_name)
    
    # ヘルスチェックツールを登録
    register_health_tools(mcp)
    
    # SCP関連ツールを登録 (Phase 2で実装予定)
    # register_scp_tools(mcp)
    
    return mcp


def main():
    """メインエントリーポイント"""
    try:
        # 設定情報をログ出力 (DEBUG時のみ)
        if config.is_debug:
            print(f"Configuration: {config}", file=sys.stderr)
        
        # サーバ作成と実行
        mcp = create_server()
        mcp.run()
        
    except KeyboardInterrupt:
        print("\nサーバを停止しています...", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
