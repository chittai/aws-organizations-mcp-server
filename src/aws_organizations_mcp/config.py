"""
AWS Organizations MCP Server Configuration
AWS公式MCPサーバの設定管理パターンに準拠
"""

import os
from typing import Optional


class MCPConfig:
    """MCP サーバ設定管理クラス
    
    AWS公式MCPサーバと同様の環境変数ベース設定管理を実装
    """
    
    def __init__(self):
        # AWS設定
        self.aws_profile: str = os.getenv("AWS_PROFILE", "default")
        self.aws_region: str = os.getenv("AWS_REGION", "us-east-1")
        
        # MCP設定
        self.log_level: str = os.getenv("FASTMCP_LOG_LEVEL", "INFO")
        
        # セキュリティ設定 (読み取り専用がデフォルト)
        self.readonly_mode: bool = not bool(os.getenv("ALLOW_WRITE", False))
        
        # AWS Organizations固有設定
        self.master_account_only: bool = bool(os.getenv("MASTER_ACCOUNT_ONLY", True))
    
    @property
    def is_debug(self) -> bool:
        """デバッグモードかどうか"""
        return self.log_level.upper() == "DEBUG"
    
    def __repr__(self) -> str:
        return (
            f"MCPConfig("
            f"aws_profile='{self.aws_profile}', "
            f"aws_region='{self.aws_region}', "
            f"log_level='{self.log_level}', "
            f"readonly_mode={self.readonly_mode}"
            f")"
        )


# グローバル設定インスタンス
config = MCPConfig()
