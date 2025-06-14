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

- [uv](https://docs.astral.sh/uv/) (推奨)
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

### 1. uvのインストール

```bash
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. プロジェクトのクローン・初期化

```bash
# GitHubからクローン
git clone https://github.com/chittai/aws-organizations-mcp-server.git
cd aws-organizations-mcp-server

# または新規作成の場合
uv init aws-organizations-mcp-server
cd aws-organizations-mcp-server
```

### 3. 依存関係のインストール

```bash
# MCPとboto3をインストール
uv add "mcp[cli]" boto3

# インストール確認
uv tree
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

### 開発・テスト

#### MCP Inspector を使用（推奨）

```bash
# ブラウザベースのテストツール
uv run mcp dev server.py
```

#### 直接実行

```bash
# サーバを直接起動
uv run python server.py
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
      "command": "uv",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/aws-organizations-mcp-server"
    }
  }
}
```

**注意**: `/path/to/aws-organizations-mcp-server` を実際のプロジェクトパスに置き換えてください。

### 簡単インストール（将来対応予定）

```bash
# Claude Desktopに直接インストール
uv run mcp install server.py --name "AWS Organizations"
```

### 動作確認

Claude Desktop を再起動後、以下をテスト：

```
利用可能なツールを教えてください
```

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
├── server.py               # メインサーバファイル
├── pyproject.toml          # プロジェクト設定
├── uv.lock                 # 依存関係ロック
├── README.md              # このファイル
└── .venv/                 # 仮想環境（uv管理）
```

### 開発の進め方

このプロジェクトはMVP（Minimum Viable Product）アプローチで開発しています：

1. **ステップ1**: 最低限のMCPサーバ実装
2. **ステップ2**: MCPクライアント接続確認
3. **ステップ3**: 段階的な機能追加

各機能はGitHub Issuesで管理されています。

### 開発コマンド

```bash
# 依存関係の追加
uv add package_name

# 開発依存関係の追加
uv add --dev package_name

# 依存関係の同期
uv sync

# プロジェクトの実行
uv run python server.py

# MCP Inspector でテスト
uv run mcp dev server.py

# Claude Desktop にインストール（将来）
uv run mcp install server.py
```

## トラブルシューティング

### 一般的な問題

1. **MCPサーバが起動しない**
   - `uv sync` で依存関係を同期
   - `uv tree` で依存関係を確認

2. **Claude Desktop で認識されない**
   - 設定ファイルの`cwd`パスが正しいか確認
   - Claude Desktop を再起動
   - ログでエラーを確認

3. **AWS API エラー**
   - AWS認証情報が正しく設定されているか確認
   - 必要なIAM権限があるか確認
   - リージョン設定を確認

### デバッグ

```bash
# 詳細ログでMCP Inspector を実行
uv run mcp dev server.py --verbose

# uvの環境情報確認
uv info

# Python環境確認
uv run python --version
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 貢献

Issue報告、機能要望、プルリクエストを歓迎します。

## 参考リンク

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [uv - Python package manager](https://docs.astral.sh/uv/)
- [AWS Organizations API](https://docs.aws.amazon.com/organizations/latest/APIReference/)
- [Claude Desktop](https://claude.ai/desktop)
