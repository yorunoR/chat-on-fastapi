# api

FastAPI による LLM 回答サービスの API サーバー。

## ドキュメント

番号順に読む。

1. [構成](docs/01_構成.md)

## ディレクトリ構成

| ディレクトリ | 役割 |
|---|---|
| `interfaces/` | FastAPI の入口。認証・接続・送受信だけの薄い層 |
| `apps/` | 回答アプリ。1 アプリ = 1 ディレクトリ |
| `libs/` | アプリ共通の処理。DB 接続・ORM モデル・リポジトリ・外部 API クライアント |
| `admin/` | 管理画面(sqladmin) |
| `config/` | 環境変数の読み込み |
| `db/` | alembic マイグレーション |
| `scripts/` | 手動で実行する補助スクリプト |

詳しくは [構成](docs/01_構成.md) を参照。

## よく使うコマンド

`api/` ディレクトリで実行する。

| コマンド | 内容 |
|---|---|
| `make run` | サーバー起動(port 5000) |
| `make fmt` | フォーマット |
| `make lint` / `make lint-fix` | lint / lint の自動修正 |
| `make migrations msg=xxx` | マイグレーションの自動生成 |
| `make migrate` | マイグレーションの適用 |
| `make rollback-one` | 1 つ前に戻す |
| `make show` | マイグレーションの履歴と現在のリビジョン |
| `make adminuser` | 管理画面のユーザー作成 |
| `make ws-normal-chat uid=xxx text=xxx` | normal_chat の WebSocket 動作確認 |
| `make chat-session token=xxx uid=xxx initial_message=xxx` | chat_session 作成 API の動作確認 |
