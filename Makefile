install:
		pip install --no-cache-dir -r requirements/common.txt

install_dev:
		pip install --no-cache-dir -r requirements/common.txt
		pip install --no-cache-dir -r requirements/dev.txt

server:
		uvicorn app.main:app --reload

worker:
		celery -A app.celery worker --loglevel=info --concurrency=5

lint:
		mypy app

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

seed:
		PYTHONPATH=$(PWD) python app/db/seeds/all.py

reset:
		make rollback migrate seed