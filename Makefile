makemigrations:
	alembic revision --autogenerate -m $(name)

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1
