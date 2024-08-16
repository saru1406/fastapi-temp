setup:
	docker compose up -d --build
	@make up
	docker compose exec app alembic upgrade head

shell:
	docker compose exec app bash

build:
	docker compose up -d --build

up:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose exec app alembic upgrade head

fresh:
	docker compose exec app alembic downgrade base
	docker compose exec app alembic upgrade head

history:
	docker compose exec app alembic history

format:
	docker-compose exec app black .
	docker-compose exec app isort .
