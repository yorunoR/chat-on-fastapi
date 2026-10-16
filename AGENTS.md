# AGENTS.md

AI エージェント向けの作業ルール。設計の説明は各ドキュメントを参照し、ここには重複して書かない。

## リポジトリ構成

- `api/`: FastAPI による LLM 回答サービスの API サーバー。概要は `api/README.md`
- `containers/`: 各コンテナの Dockerfile
- `db/init/`: PostgreSQL コンテナの初期化スクリプト
- `compose.yaml`: 開発環境(ai / api / db)

## api/ での作業

- 作業前に `api/docs/` のドキュメントを番号順に読み、構成に従う
  - @api/docs/01_構成.md
- 新しい回答アプリは `apps/<app_name>/` に、`<app_name>_controller.py`・`flows/`・`nodes/`・`prompt_templates.yaml` の構成で作る
- コードを変更したら `api/` で `make fmt` と `make lint` を実行し、エラーがない状態にする
- マイグレーションは `make migrations msg=xxx` で自動生成する。手で書かない
- 依存パッケージは `uv add` で追加する(`pyproject.toml` を直接編集しない)
- プロジェクト内のモジュールは、関数・クラスを直接 import する
  - 良い例: `from libs.repositories.chat_session_repository import create_chat_session`
  - 悪い例: `from libs.repositories import chat_session as chat_session_repository`(モジュールの import、`as` による別名)
  - 名前が衝突したら、`as` を使わずに呼び出し側の関数名を変える
  - 例外: `interfaces/urls.py` のルーター登録は、各モジュールの `router` が同名になるためモジュール単位で import する

## ドキュメント

- 構成や設計を変えたら、`api/docs/` の該当ドキュメントも更新する
- `api/docs/` のファイル名は `NN_日本語名.md`(読む順番の番号付き)。追加したら `api/README.md` の一覧にも足す

## コミット

- 形式は `changelog.config.js` に従う: `{emoji}{type}: {subject}`
  - 例: `🎸 feat: ...`、`🐛 fix: ...`、`💡 refactor: ...`、`✏️ docs: ...`
- subject は日本語で書く
