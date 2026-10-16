# chat-on-fastapi

LLM を使った回答サービス。

## 構成

| パス | 内容 |
|---|---|
| `api/` | FastAPI の API サーバー。詳しくは [api/README.md](api/README.md) |
| `web/` | Vue(Vite)のフロントエンド。API と WebSocket で通信して会話する |
| `containers/` | 各コンテナの Dockerfile |
| `db/init/` | PostgreSQL コンテナの初期化スクリプト(ユーザーと DB の作成) |
| `compose.yaml` | 開発環境の定義 |
| `AGENTS.md` | AI エージェント向けの作業ルール(`CLAUDE.md` から参照) |

コンテナ:

- `ai`: Claude Code / Codex を動かす作業用コンテナ
- `api`: API サーバー(port 5000)
- `web`: フロントエンド(port 3000)
- `db`: PostgreSQL(port 5432)

## セットアップ

```sh
cp .env.ai.local.sample .env.ai.local
cp .env.api.local.sample .env.api.local
# 各ファイルの値を埋める
#   .env.ai.local:  ANTHROPIC_API_KEY(Claude Code 用)
#   .env.api.local: OPENAI_API_KEY(回答の生成に使う)。ほかの環境変数はファイル内のコメントを参照

make build
make up
```

初回はマイグレーションを適用する。

```sh
docker compose exec api make migrate
```

ここから最初の会話までの手順は [api/README.md](api/README.md) の「最初の会話まで」を参照。

## ブラウザで会話する

`api/README.md` の手順 2 で作った `User` の `uid` を、http://localhost:3000 に入力すると、chat_session を作って会話できる(chat_session の uid はブラウザの localStorage に保存する)。API の接続先は `web/` の環境変数 `VITE_API_URL`(既定 `http://localhost:5000`)で変える。

## よく使うコマンド

| コマンド | 内容 |
|---|---|
| `make up` / `make stop` / `make down` | コンテナの起動 / 停止 / 削除 |
| `make b` | ai コンテナに入る |
| `make cl` | ai コンテナで Claude Code を起動 |
| `make cx` | ai コンテナで Codex を起動 |
