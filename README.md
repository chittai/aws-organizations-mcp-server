# AWS Organizations MCP Server

AWS Service Control Policy (SCP) audit server for MCP (Model Context Protocol).

## 概要

このプロジェクトは、AWS Organizations の Service Control Policy (SCP) を監査・分析するためのMCPサーバです。Claude等のMCPクライアントと連携して、SCP設定の確認、比較、トラブルシューティングを支援します。

## 主な機能

- SCP一覧の取得
- SCP詳細情報の取得
- SCP適用対象の確認
- 設定比較・差分検出
- エラーログ分析

## 前提条件

- Python 3.8以上
- AWS CLI設定済み（適切なIAM権限）
- AWS Organizations の管理アカウントまたは委任管理者権限

### 必要なAWS権限

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

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/chittai/aws-organizations-mcp-server.git
cd aws-organizations-mcp-server
```

### 2. Python仮想環境の作成

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境をアクティベート
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. AWS認証情報の設定

AWS CLIまたは環境変数で認証情報を設定してください：

```bash
# AWS CLI設定
aws configure

# または環境変数
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

## 使用方法

### MCPサーバの起動

```bash
python server.py
```

### Claude Desktop との連携

Claude Desktop の設定ファイルに以下を追加：

**設定ファイルの場所：**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**設定内容：**
```json
{
  "mcpServers": {
    "aws-organizations": {
      "command": "python",
      "args": ["/path/to/aws-organizations-mcp-server/server.py"],
      "env": {
        "PYTHONPATH": "/path/to/aws-organizations-mcp-server/venv/lib/python3.x/site-packages"
      }
    }
  }
}
```

**注意**: `/path/to/aws-organizations-mcp-server/` を実際のプロジェクトパスに置き換えてください。

### 動作確認

Claude Desktop を再起動後、以下をテスト：

```
helloツールを使って挨拶してください
```

## 利用可能なツール

### 基本ツール

- `hello` - 動作確認用ツール

### SCP関連ツール（予定）

- `list_scp_policies` - SCP一覧取得
- `get_scp_detail` - SCP詳細取得
- `get_scp_targets` - SCP適用対象取得
- `compare_scp_simple` - 基本的な設定比較
- `analyze_error_basic` - 基本的なエラーログ分析

## 開発

### プロジェクト構造

```
aws-organizations-mcp-server/
├── server.py              # メインサーバファイル
├── requirements.txt       # Python依存関係
├── README.md             # このファイル
└── venv/                 # Python仮想環境
```

### 開発の進め方

このプロジェクトはMVP（Minimum Viable Product）アプローチで開発しています：

1. **ステップ1**: 最低限のMCPサーバ実装
2. **ステップ2**: MCPクライアント接続確認
3. **ステップ3**: 段階的な機能追加

各機能はGitHub Issuesで管理されています。

## トラブルシューティング

### 一般的な問題

1. **MCPサーバが起動しない**
   - Python仮想環境がアクティベートされているか確認
   - 依存関係が正しくインストールされているか確認

2. **Claude Desktop で認識されない**
   - 設定ファイルのパスが正しいか確認
   - Claude Desktop を再起動
   - ログでエラーを確認

3. **AWS API エラー**
   - AWS認証情報が正しく設定されているか確認
   - 必要なIAM権限があるか確認
   - リージョン設定を確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

Issue報告、機能要望、プルリクエストを歓迎します。

## 参考リンク

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [AWS Organizations API](https://docs.aws.amazon.com/organizations/latest/APIReference/)
- [Claude Desktop](https://claude.ai/desktop)
