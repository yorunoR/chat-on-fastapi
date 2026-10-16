import os

DB_USER = os.environ.get("DB_USER", "developer")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "password")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "api_dev")

ENV = os.environ.get("ENV", "local")
ADMIN_SESSION_SECRET = os.environ.get("ADMIN_SESSION_SECRET", "sqladmin_secret")

# プロンプトを DB に保存するか。ローカル開発用(同期の DB アクセスになるため、本番では有効にしない)
SAVE_PROMPT_TEMPLATE = os.environ.get("SAVE_PROMPT_TEMPLATE", "false").lower() == "true"

# WebSocket の接続を開いておける最大時間(秒)。過ぎたらサーバーから閉じる
WS_TIMEOUT_SECONDS = float(os.environ.get("WS_TIMEOUT_SECONDS", "300"))

# 終了時に後処理(バックグラウンドタスク)の完了を待つ最大時間(秒)。過ぎたらキャンセルする
BACKGROUND_TASK_SHUTDOWN_TIMEOUT_SECONDS = float(os.environ.get("BACKGROUND_TASK_SHUTDOWN_TIMEOUT_SECONDS", "30"))
