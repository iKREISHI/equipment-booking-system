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
	uv run src/manage.py create_groups
	uv run src/manage.py entrypoint
	uv run src/manage.py create_locations
	uv run src/manage.py create_inventory_status
	uv run src/manage.py create_maintenance_status

startapp: sync migrate entrypoint collect-static

runserver:
	uv run src/manage.py runserver

tests:
	uv run src/manage.py test apps api.v0 --parallel