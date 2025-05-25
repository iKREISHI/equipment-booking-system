.PHONY:
	migrate

sync:
	uv sync

collect-static:
	uv run src/manage.py collectstatic

migrate:
	uv run src/manage.py makemigrations users locations equipments reservations maintenance
	uv run src/manage.py migrate

entrypoint:
	uv run src/manage.py entrypoint

startapp: sync migrate entrypoint collect-static

runserver:
	uv run src/manage.py runserver

tests:
	uv run src/manage.py test apps api.v0 --parallel