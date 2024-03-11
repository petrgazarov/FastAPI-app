install:
		poetry install

server:
		uvicorn fastapi_app.main:app --reload

worker:
		celery -A fastapi_app.celery worker --loglevel=info --concurrency=5

lint:
		mypy fastapi_app

migration_generate:
		alembic revision -m "$(name)"

migration_autogenerate:
		alembic revision --autogenerate -m "$(name)"

migrate:
		alembic upgrade head

rollback:
		alembic downgrade -1

rollback_base:
		alembic downgrade base

reset:
		make rollback migrate seed
