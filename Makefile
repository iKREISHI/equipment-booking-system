run-db:
	docker compose -f ./docker-compose.yml up postgres -d

stop-db:
	docker compose -f ./docker-compose.yml down postgres

logs:
	docker compose -f ./docker-compose.yml logs

build:
	docker compose -f ./docker-compose.yml up -d --build
	# migrate
	docker-compose -f ./docker-compose.yml exec backend uv run manage.py makemigrations
	docker-compose -f ./docker-compose.yml exec backend uv run manage.py migrate
	# Collect static
	docker-compose -f ./docker-compose.yml exec backend uv run manage.py collectstatic --no-input
	# Entrypoints
	docker-compose -f ./docker-compose.yml exec backend uv run manage.py create_groups
	docker-compose -f ./docker-compose.yml exec backend uv run manage.py entrypoint
	docker-compose -f ./docker-compose.yml exec backend uv run manage.py create_locations
	docker-compose -f ./docker-compose.yml exec backend uv run manage.py create_inventory_status
	docker-compose -f ./docker-compose.yml exec backend uv run manage.py create_maintenance_status
