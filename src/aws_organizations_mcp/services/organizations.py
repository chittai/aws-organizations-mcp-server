"""
AWS Organizations Service Wrapper
AWS Organizations API のラッパー実装

Phase 1: 基盤実装
Phase 2: SCP機能実装
"""

import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, List, Optional

from ..config import config


class OrganizationsService:
    """AWS Organizations Service ラッパークラス
    
    AWS Organizations APIの操作を抽象化し、
    エラーハンドリングと設定管理を統一
    """
    
    def __init__(self):
        """サービスを初期化"""
        self.session = boto3.Session(profile_name=config.aws_profile)
        self.client = self.session.client('organizations', region_name=config.aws_region)
        self._org_info: Optional[Dict[str, Any]] = None
    
    @property
    def organization_info(self) -> Optional[Dict[str, Any]]:
        """Organization情報を取得（キャッシュ付き）
        
        Returns:
            Optional[Dict[str, Any]]: Organization情報、またはNone
        """
        if self._org_info is None:
            try:
                response = self.client.describe_organization()
                self._org_info = response['Organization']
            except ClientError as e:
                if e.response['Error']['Code'] != 'AWSOrganizationsNotInUseException':
                    raise
                return None
        return self._org_info
    
    def is_master_account(self, account_id: str) -> bool:
        """指定されたアカウントがマスターアカウントかチェック
        
        Args:
            account_id: 確認するアカウントID
            
        Returns:
            bool: マスターアカウントの場合True
        """
        org_info = self.organization_info
        if not org_info:
            return False
        return org_info['MasterAccountId'] == account_id
    
    def list_policies(self, filter_type: str = 'SERVICE_CONTROL_POLICY') -> List[Dict[str, Any]]:
        """ポリシー一覧を取得
        
        Args:
            filter_type: ポリシータイプフィルター
            
        Returns:
            List[Dict[str, Any]]: ポリシー一覧
            
        Raises:
            ValueError: Organizations未設定やアクセス権限不足の場合
        """
        try:
            # マスターアカウントのみアクセス可能かチェック
            if config.master_account_only:
                sts_client = self.session.client('sts', region_name=config.aws_region)
                caller_identity = sts_client.get_caller_identity()
                
                if not self.is_master_account(caller_identity['Account']):
                    raise ValueError(
                        "このアカウントはOrganizationsのマスターアカウントではありません。"
                        "MASTER_ACCOUNT_ONLY=falseで設定を変更してください。"
                    )
            
            # ポリシー一覧を取得
            paginator = self.client.get_paginator('list_policies')
            policies = []
            
            for page in paginator.paginate(Filter=filter_type):
                policies.extend(page['Policies'])
            
            return policies
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'AWSOrganizationsNotInUseException':
                raise ValueError("このアカウントではAWS Organizationsが有効化されていません")
            elif error_code == 'AccessDenied':
                raise ValueError("AWS Organizationsポリシーへのアクセス権限がありません")
            else:
                raise ValueError(f"AWS Organizations API エラー: {error_code}")
    
    def get_policy(self, policy_id: str) -> Dict[str, Any]:
        """指定されたポリシーの詳細を取得
        
        Args:
            policy_id: ポリシーID
            
        Returns:
            Dict[str, Any]: ポリシー詳細情報
            
        Raises:
            ValueError: ポリシーが見つからない場合など
        """
        try:
            response = self.client.describe_policy(PolicyId=policy_id)
            return response['Policy']
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'PolicyNotFoundException':
                raise ValueError(f"ポリシーID '{policy_id}' が見つかりません")
            elif error_code == 'AccessDenied':
                raise ValueError("ポリシーへのアクセス権限がありません")
            else:
                raise ValueError(f"AWS Organizations API エラー: {error_code}")


# グローバルサービスインスタンス
org_service = OrganizationsService()
