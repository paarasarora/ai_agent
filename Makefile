build:
	docker-compose -f docker-compose.yml up --build -d --remove-orphans

up:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose -f docker-compose.yml down

show-logs:
	docker-compose -f docker-compose.yml logs

show-logs-api:
	docker compose -f docker-compose.yml logs web

makemigrations:
	docker-compose -f docker-compose.yml run --rm web python manage.py makemigrations

migrate:
	docker-compose -f docker-compose.yml run --rm web python manage.py migrate

superuser:
	docker-compose -f docker-compose.yml run --rm web python3 manage.py createsuperuser




