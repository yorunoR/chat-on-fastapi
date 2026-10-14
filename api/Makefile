run:
	uv run uvicorn interfaces.main:api --host 0.0.0.0 --port 5000 --reload

fmt:
	uv run ruff format

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

show:
	uv run alembic --config db/alembic.ini history
	uv run alembic --config db/alembic.ini current

migrations:
	uv run alembic --config db/alembic.ini revision --autogenerate -m ${msg}

migrate:
	uv run alembic --config db/alembic.ini upgrade head

rollback:
	uv run alembic --config db/alembic.ini downgrade ${rev}

rollback-all:
	uv run alembic --config db/alembic.ini downgrade base

rollback-one:
	uv run alembic --config db/alembic.ini downgrade -1

shell:
	uv run shell.py

adminuser:
	uv run scripts/create_admin_user.py
