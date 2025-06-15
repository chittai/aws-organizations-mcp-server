"""
AWS Organizations MCP Server SCP Tools
Service Control Policy (SCP) 関連ツール実装

Phase 2で実装予定：
- list_scp_policies
- get_scp_detail
- validate_scp_syntax
"""

from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, List

from ..config import config


def register_scp_tools(mcp: FastMCP) -> None:
    """SCP関連ツールをMCPサーバに登録
    
    Args:
        mcp: FastMCPサーバインスタンス
    """
    
    # Phase 2で実装予定
    # TODO: list_scp_policies ツール実装
    # TODO: get_scp_detail ツール実装
    # TODO: validate_scp_syntax ツール実装
    
    pass
