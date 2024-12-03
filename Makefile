run:
	docker compose up
install:
	make migrations
	make migrate
	make superuser
migrations:
	docker compose exec app bash -c "python manage.py makemigrations"
migrate:
	docker compose exec app bash -c "python manage.py migrate"
superuser:
	docker compose exec app bash -c "python manage.py createsuperuser"
shell:
	docker compose exec app bash -c "python manage.py shell"
lint:
	docker compose run --rm app ruff check --fix
