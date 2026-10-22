# api

FastAPI による LLM 回答サービスの API サーバー。

## ドキュメント

番号順に読む。

1. [構成](docs/01_構成.md)
2. [アプリの追加](docs/02_アプリの追加.md)

## ディレクトリ構成

| ディレクトリ | 役割 |
|---|---|
| `interfaces/` | FastAPI の入口。認証・接続・送受信だけの薄い層 |
| `apps/` | 回答アプリ。1 アプリ = 1 ディレクトリ |
| `libs/` | アプリ共通の処理。DB 接続・ORM モデル・リポジトリ・プロンプト・外部 API クライアント |
| `admin/` | 管理画面(sqladmin) |
| `config/` | 環境変数の読み込み |
| `db/` | alembic マイグレーション |
| `scripts/` | 手動で実行する補助スクリプト |

詳しくは [構成](docs/01_構成.md) を参照。

## コマンドを実行する場所

`api` コンテナの中(`/api`)で実行する。ホストからは `docker compose exec api make xxx` で実行できる。

- サーバーは `make up` で `api` コンテナが起動すると自動で立ち上がる(コードの変更も自動で反映される)
- 動作確認のスクリプト(`make chat-session`・`make ws-normal-chat`)は `localhost:5000` に接続するため、`api` コンテナで実行する
- `make routes`・`make adminuser` はプロジェクトのモジュールを import するため、`PYTHONPATH=.` が設定されている `api` コンテナで実行する
- `make fmt`・`make lint`・マイグレーションは、`ai` コンテナの `/ai/api` で実行してもよい

## 最初の会話まで

ルートの [README](../README.md) のセットアップ(`.env.api.local` の `OPENAI_API_KEY` を含む)とマイグレーションを終えた状態から始める。

1. 管理画面のユーザーを作る

   ```sh
   docker compose exec api make adminuser
   ```

2. http://localhost:5000/admin に 1 のメールアドレスとパスワードでログインし、`User` を作る(`email` と `uid` を入力する。`uid` は API の認証に使う)

3. 2 の `User` として chat_session を作る。HTTP API の認証は `Authorization: Bearer <User の uid>`

   ```sh
   docker compose exec api make chat-session user_uid=<User の uid> session_uid=<新しい chat_session の uid>
   ```

4. 3 の chat_session で会話する

   ```sh
   docker compose exec api make ws-normal-chat session_uid=<chat_session の uid> text=こんにちは
   ```

   回答の一部(`message`)が続けて届き、`stop: true` で回答が終わり、`done: true` で接続を閉じる(形式は [構成](docs/01_構成.md) の「送信の形式」)

## よく使うコマンド

| コマンド | 内容 |
|---|---|
| `make run` | サーバー起動(port 5000)。`api` コンテナでは起動済みなので使わない |
| `make fmt` | フォーマット |
| `make lint` / `make lint-fix` | lint / lint の自動修正 |
| `make migrations msg=xxx` | マイグレーションの自動生成 |
| `make migrate` | マイグレーションの適用 |
| `make rollback-one` | 1 つ前に戻す |
| `make rollback rev=xxx` | 指定したリビジョンまで戻す |
| `make rollback-all` | すべて戻す |
| `make show` | マイグレーションの履歴と現在のリビジョン |
| `make shell` | `shell.py` を実行する(`shell.py` は作成予定。まだ使えない) |
| `make routes` | 登録されているパスの一覧(WebSocket も含む) |
| `make adminuser` | 管理画面のユーザー作成 |
| `make chat-session user_uid=xxx session_uid=xxx initial_message=xxx` | chat_session 作成 API の動作確認(`initial_message` は省略可) |
| `make ws-normal-chat session_uid=xxx text=xxx` | normal_chat の WebSocket 動作確認 |
