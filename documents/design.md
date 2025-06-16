# AWS Organizations MCP Server 設計ドキュメント

## 1. プロジェクト概要

### 1.1 プロジェクト名
AWS Organizations MCP Server

### 1.2 目的
AWS Service Control Policy (SCP) の設定ミスを検出し、トラブルシューティングを支援するMCPサーバを開発する。

### 1.3 背景
- AWSのSCPが依頼内容と異なって設定されている可能性がある
- 既存のAWS公式MCPサーバではSCP監査機能が提供されていない
- エラーログから必要なAWSサービス設定変更を特定したい

## 2. ビジネス要件

### 2.1 主要なユースケース
1. **SCP設定ミスの検出**
   - 依頼内容（期待値）とのSCP設定比較
   - 設定差分の検出と報告
   - 設定ミス箇所の特定

2. **トラブルシューティング支援**
   - エラーログ分析による設定確認対象の特定
   - 修正推奨事項の提示

3. **SCP監査機能**
   - SCP一覧の取得
   - SCP詳細情報の取得
   - SCP適用対象の確認

### 2.2 解決したい問題
- AWSのSCPが依頼内容と誤って設定されている可能性
- エラーログから関連するAWS設定の特定が困難
- 手動でのSCP監査の非効率性

## 3. 技術要件

### 3.1 開発環境
- **言語**: Python 3.8以上
- **フレームワーク**: MCP Python SDK (FastMCP)
- **パッケージ管理**: uv (公式推奨)
- **AWS SDK**: boto3

### 3.2 実行環境
- **環境**: ローカル開発環境
- **OS**: 制限なし（Python実行可能環境）
- **認証**: AWS CLI設定またはIAM権限

### 3.3 外部依存
- AWS Organizations API
- AWS IAM API（SCP関連）

## 4. システム設計

### 4.1 アーキテクチャ
```
Claude Desktop ← MCP Protocol → MCP Server ← boto3 → AWS Organizations API
```

### 4.2 主要コンポーネント
1. **MCPサーバ基盤** (FastMCP)
2. **AWS Organizations クライアント** (boto3)
3. **SCP監査エンジン**
4. **エラーログ分析エンジン**
5. **設定比較エンジン**

### 4.3 データフロー
1. ユーザーがClaude DesktopでMCPツールを呼び出し
2. MCPサーバがAWS Organizations APIを呼び出し
3. SCP情報を取得・分析
4. 結果をClaude Desktopに返却

## 5. 機能設計

### 5.1 提供ツール

#### 5.1.1 基本ツール
- `hello` - 動作確認用ツール

#### 5.1.2 SCP関連ツール（実装予定）
- `list_scp_policies` - SCP一覧取得
- `get_scp_detail` - SCP詳細取得  
- `get_scp_targets` - SCP適用対象取得
- `compare_scp_config` - SCP設定比較
- `analyze_error_log` - エラーログ分析

### 5.2 機能仕様

#### 5.2.1 SCP情報取得機能
- AWS Organizations配下のSCP一覧取得
- 特定のSCPの詳細情報取得
- SCPの適用状況（OU、アカウント）取得

#### 5.2.2 SCP監査機能
- 依頼内容（期待値）とのSCP設定比較
- 設定差分の検出と報告
- 設定ミス箇所の特定

#### 5.2.3 トラブルシューティング支援機能
- エラーログ分析による設定確認対象の特定
- 修正推奨事項の提示

## 6. セキュリティ設計

### 6.1 認証・認可
- **認証**: AWS認証情報（IAMロール/ユーザー）
- **アクセス制御**: 単一ユーザー（開発者本人）のみ
- **通信**: HTTPS（AWS API）

### 6.2 必要なAWS権限
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "organizations:ListPolicies",
                "organizations:DescribePolicy",
                "organizations:ListTargetsForPolicy",
                "organizations:ListAccounts",
                "organizations:ListOrganizationalUnits"
            ],
            "Resource": "*"
        }
    ]
}
```

## 7. 開発アプローチ

### 7.1 MVP（Minimum Viable Product）アプローチ
1. **ステップ1**: 最低限のMCPサーバ実装
2. **ステップ2**: MCPクライアント接続確認
3. **ステップ3**: 段階的な機能追加

### 7.2 開発フェーズ

#### フェーズ1: 基盤実装（進行中）
- ✅ uvプロジェクト初期化
- ✅ 依存関係インストール
- ✅ 最小MCPサーバ実装
- ✅ サーバ起動確認（Issue#4完了）
- 🔄 Claude Desktop設定
- 🔄 基本動作確認

#### フェーズ2: AWS接続とSCP基本取得
- AWS認証設定
- Organizations API接続
- SCP一覧取得機能
- SCP詳細取得機能
- SCP適用対象取得機能

#### フェーズ3: 監査機能実装
- 設定比較機能
- 差分検出ロジック
- レポート生成機能

#### フェーズ4: エラーログ分析機能
- ログパーサー実装
- AWS サービス識別機能
- 推奨事項生成機能

## 8. 実装詳細

### 8.1 プロジェクト構造（旧版）
```
aws-organizations-mcp-server/
├── server.py               # メインサーバファイル
├── pyproject.toml          # プロジェクト設定
├── uv.lock                 # 依存関係ロック
├── README.md              # セットアップガイド
├── documents/             # ドキュメント
│   └── design.md          # このファイル
└── .venv/                 # 仮想環境（uv管理）
```

### 8.2 現在の実装状況

#### 8.2.1 完了項目
- FastMCPベースのサーバ実装
- helloツールの実装
- 基本的なエラーハンドリング
- サーバ起動確認（Issue#4完了）
- MCP Inspector での動作確認

#### 8.2.2 実装中項目
- Claude Desktop連携
- Claude Desktop経由での基本動作確認

## 9. 運用設計

### 9.1 制約事項
- **技術的制約**
  - AWS Organizations の管理アカウントまたは委任管理者権限が必要
  - SCP関連のIAM権限が必要
  - インターネット接続が必要（AWS API アクセス）

- **運用制約**
  - ローカル環境での実行のみ
  - 単一ユーザーでの利用

### 9.2 非機能要件
- **パフォーマンス**: 特別な要件なし
- **可用性**: ローカル実行のため高可用性は不要
- **セキュリティ**: AWS API権限に依存

## 10. リスク管理

### 10.1 技術的リスク
- AWS API制限による実行制約
- 大量のSCPがある場合のパフォーマンス影響

### 10.2 運用リスク
- AWS認証情報の管理
- 権限設定の誤り

## 11. 今後の拡張計画

### 11.1 短期的な拡張
- SCP監査機能の実装
- エラーログ分析機能の実装
- レポート機能の充実

### 11.2 長期的な拡張
- 他のAWSサービス（IAM、GuardDuty等）への対応
- 自動修正機能
- Web UIの提供

## 12. 参考情報

### 12.1 技術リファレンス
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [AWS Organizations API](https://docs.aws.amazon.com/organizations/latest/APIReference/)
- [uv - Python package manager](https://docs.astral.sh/uv/)

### 12.2 プロジェクト情報
- **リポジトリ**: https://github.com/chittai/aws-organizations-mcp-server
- **Issue管理**: GitHub Issues
- **開発開始**: 2025年6月14日

---

## 📋 プロジェクト継続用コンテキスト

### 🎯 **プロジェクト概要**

- **名前**: AWS Organizations MCP Server
- **目的**: AWS Service Control Policy (SCP) の監査・分析を行うMCPサーバ
- **リポジトリ**: https://github.com/chittai/aws-organizations-mcp-server
- **アプローチ**: AWS公式MCPサーバの実装方針に完全準拠

### 📊 **現在の進捗状況**

#### ✅ **完了済み**

1. **Issue #1**: uvプロジェクト初期化 - 完了
1. **Issue #2**: uv依存関係インストール - 完了
1. **Issue #3**: 最小MCPサーバ実装 - 完了
- `server.py`にhelloツール実装済み
- FastMCP使用、基本動作確認済み

#### 🔄 **進行中**

- **Issue #7**: プロジェクト構造のAWS公式準拠化
  - AWS公式MCPサーバと同じディレクトリ構造への変更
  - 現在のserver.pyから新構造への移行が必要

### 🏗️ **技術スタック（AWS公式準拠）**

- **言語**: Python 3.8+
- **フレームワーク**: FastMCP (AWS公式推奨)
- **パッケージ管理**: uv
- **AWS SDK**: boto3
- **設定**: 環境変数ベース (AWS_PROFILE, AWS_REGION, FASTMCP_LOG_LEVEL)

### 📁 **目標のプロジェクト構造（AWS公式準拠）**

```
aws-organizations-mcp-server/
├── server.py                          # エントリーポイント
├── pyproject.toml                     # パッケージ設定
├── src/
│   └── aws_organizations_mcp/
│       ├── __init__.py
│       ├── server.py                  # FastMCPサーバ実装
│       ├── config.py                  # 設定管理
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── health_tools.py        # ヘルスチェック
│       │   └── scp_tools.py           # SCP関連ツール
│       └── services/
│           ├── __init__.py
│           └── organizations.py       # Organizations API wrapper
```

### 🎯 **実装すべき機能（優先順）**

#### **Phase 1: 基盤構築（進行中）**

- **Issue #7**: プロジェクト構造AWS公式準拠化
- **Issue #8**: AWS公式準拠設定管理実装
- **Issue #9**: Organizations Service基盤
- **Issue #10**: AWS接続ヘルスチェックツール

#### **Phase 2: SCP機能**

- **Issue #11**: `list_scp_policies` ツール
- **Issue #12**: `get_scp_detail` ツール

#### **Phase 3: 統合・配布**

- **Issue #13**: 統合テスト
- **Issue #14**: ドキュメント・配布準備

### 🔧 **実装パターン（AWS公式準拠）**

#### **環境変数設定**

```json
{
  "mcpServers": {
    "aws-organizations": {
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/aws-organizations-mcp-server",
      "env": {
        "AWS_PROFILE": "your-profile",
        "AWS_REGION": "us-east-1",
        "FASTMCP_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

#### **設定管理クラス**

```python
class MCPConfig:
    def __init__(self):
        self.aws_profile = os.getenv("AWS_PROFILE", "default")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.log_level = os.getenv("FASTMCP_LOG_LEVEL", "INFO")
        self.readonly_mode = not bool(os.getenv("ALLOW_WRITE", False))
```

#### **ツール実装パターン**

```python
@mcp.tool()
def list_scp_policies() -> List[Dict[str, Any]]:
    """List all Service Control Policies in AWS Organizations"""
    try:
        return org_service.list_policies()
    except Exception as e:
        raise ValueError(f"Failed to retrieve SCP policies: {str(e)}")
```

### 🚨 **現在の問題**

- **Claude Desktop表示問題**: MCPサーバがClaude Desktopで認識されない
- **対処法**: まず `uv run mcp dev server.py` でMCP Inspectorでの動作確認から開始

### 📚 **重要な参考情報**

- **AWS公式MCPサーバ**: https://github.com/awslabs/mcp
- **設計ドキュメント**: https://github.com/chittai/aws-organizations-mcp-server/blob/main/documents/design.md
- **MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk

### 🔄 **次の具体的アクション**

1. **Claude Desktop問題の解決**: MCP Inspector での動作確認
1. **Issue #7完了**: AWS公式準拠のプロジェクト構造への移行
1. **環境変数設定**: AWS_PROFILE, AWS_REGION対応
1. **ヘルスチェックツール**: AWS接続確認機能

### 💡 **重要な実装方針**

- **AWS公式完全準拠**: すべてのパターンをAWS公式MCPサーバに合わせる
- **セキュリティファースト**: 読み取り専用デフォルト
- **段階的実装**: 各フェーズで動作確認を行う
- **MVPアプローチ**: 動作するものから順次実装

---

**ドキュメントバージョン**: 1.1  
**最終更新**: 2025年6月16日  
**作成者**: Development Team
