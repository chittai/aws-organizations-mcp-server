"""
AWS Organizations MCP Server Health Check Tools
AWS公式MCPサーバの実装パターンに準拠
"""

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

from ..config import config


def register_health_tools(mcp: FastMCP) -> None:
    """ヘルスチェックツールをMCPサーバに登録
    
    Args:
        mcp: FastMCPサーバインスタンス
    """
    
    @mcp.tool()
    def hello(name: str = "World") -> str:
        """MCPサーバの動作確認用のシンプルなツール
        
        Args:
            name: 挨拶する相手の名前 (デフォルト: "World")
            
        Returns:
            str: 挨拶メッセージ
        """
        return f"Hello, {name}! AWS Organizations MCPサーバが正常に動作しています。"
    
    @mcp.tool()
    def aws_health_check() -> Dict[str, Any]:
        """AWS接続のヘルスチェック
        
        Returns:
            Dict[str, Any]: AWS接続状態の詳細情報
        """
        try:
            # AWS認証情報の確認
            session = boto3.Session(profile_name=config.aws_profile)
            
            # STS経由で現在のアカウント情報を取得
            sts_client = session.client('sts', region_name=config.aws_region)
            caller_identity = sts_client.get_caller_identity()
            
            # Organizations クライアントの動作確認
            org_client = session.client('organizations', region_name=config.aws_region)
            
            # 現在のアカウントがOrganizationsのマスターアカウントかチェック
            try:
                org_info = org_client.describe_organization()
                is_master_account = (
                    org_info['Organization']['MasterAccountId'] == 
                    caller_identity['Account']
                )
                org_status = "accessible"
                org_id = org_info['Organization']['Id']
                org_arn = org_info['Organization']['Arn']
            except ClientError as e:
                if e.response['Error']['Code'] == 'AWSOrganizationsNotInUseException':
                    is_master_account = False
                    org_status = "not_in_use"
                    org_id = None
                    org_arn = None
                else:
                    raise
            
            return {
                "status": "healthy",
                "aws_profile": config.aws_profile,
                "aws_region": config.aws_region,
                "account_id": caller_identity['Account'],
                "user_arn": caller_identity['Arn'],
                "organizations": {
                    "status": org_status,
                    "is_master_account": is_master_account,
                    "organization_id": org_id,
                    "organization_arn": org_arn
                },
                "config": {
                    "readonly_mode": config.readonly_mode,
                    "master_account_only": config.master_account_only
                }
            }
            
        except NoCredentialsError:
            return {
                "status": "error",
                "error": "AWS認証情報が見つかりません",
                "aws_profile": config.aws_profile,
                "suggestion": "AWS_PROFILEを確認するか、AWS認証情報を設定してください"
            }
        except ClientError as e:
            return {
                "status": "error",
                "error": f"AWS API エラー: {e.response['Error']['Code']}",
                "message": e.response['Error']['Message'],
                "aws_profile": config.aws_profile,
                "aws_region": config.aws_region
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"予期しないエラー: {str(e)}",
                "aws_profile": config.aws_profile,
                "aws_region": config.aws_region
            }
