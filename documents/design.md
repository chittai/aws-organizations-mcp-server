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

#### フェーズ1: 基盤実装（完了）
- ✅ uvプロジェクト初期化
- ✅ 依存関係インストール
- ✅ 最小MCPサーバ実装
- 🔄 サーバ起動確認
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

### 8.1 プロジェクト構造
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

#### 8.2.2 実装中項目
- サーバ起動確認
- Claude Desktop連携

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

**ドキュメントバージョン**: 1.0  
**最終更新**: 2025年6月14日  
**作成者**: Development Team
