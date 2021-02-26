makemigrations:
	alembic revision --autogenerate -m $(name)

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

install_all_requirements:
	pip install -r requirements.txt -r requirements_test.txt
