run-db:
	docker compose -f ./docker-compose.yml up postgres -d

stop-db:
	docker compose -f ./docker-compose.yml down postgres

logs:
	docker compose -f ./docker-compose.yml logs