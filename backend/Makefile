.PHONY:
	migrate

sync:
	uv sync


migrate:
	uv run src/manage.py makemigrations users locations equipments reservations maintenance
	uv run src/manage.py migrate

entrypoint:
	uv run src/entrypoints

startapp: sync migrate

runserver:
	uv run src/manage.py runserver