up:
	@docker compose up --build -d
dev:
	@docker compose watch
down:
	@docker compose down
run:
	docker compose run --user appuser --build runner python src/project/$(target).py
exec-db:
	docker exec -u postgres -it github-pi-db-1 /bin/bash
backup-db:
	./docker_postgres_backup.sh
restore-db:
	./docker_postgres_restore.sh
migrate-db:
	docker compose run --build runner alembic -c src/project/alembic.ini upgrade head
reset-db:
	docker compose down
	docker volume rm github-pi-db
