# Makefile generated with pymakefile
help:
	@grep -E '^[A-Za-z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "[36m%-30s[0m %s\n", $$1, $$2}'

lint:  ## lint fix
	black .
	isort . --profile black
	flake8 .

lint-check: ## lint check
	black . --check
	isort . --check-only --profile black
	flake8 .


## Dev Commands

runserver:
	docker-compose run --rm -p 8080:8080 app python manage.py runserver 0.0.0.0:8080

migrate:
	docker-compose run --rm app python manage.py migrate

migrations:
	docker-compose run --rm app python manage.py makemigrations

menu:
	docker-compose run --rm app python manage.py createpublicmenus

