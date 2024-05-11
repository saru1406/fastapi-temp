setup:
	docker compose up -d --build
shell:
	docker compose exec app bash
up:
	docker compose up -d
down:
	docker compose down

migrate:
	docker compose exec app alembic upgrade head

fresh:
	docker compose exec app alembic downgrade base
	docker compose exec app alembic upgrade head
