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

startapp: sync run-dev migrate entrypoint collect-static

runserver:
	uv run src/manage.py runserver

tests:
	uv run src/manage.py test apps api.v0 --parallel

run-dev:
	docker compose -f ../docker-compose-local-dev.yml up postgres -d
	docker compose -f ../docker-compose-local-dev.yml up minio -d
	docker compose -f ../docker-compose-local-dev.yml up nginx -d

stop:
	docker compose -f ../docker-compose-local-dev.yml down

logs:
	docker compose -f .../docker-compose-local-dev.yml logs