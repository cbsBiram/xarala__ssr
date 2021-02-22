.PHONY: docs clean

COMMAND = docker-compose run --rm djangoapp /bin/bash -c

all: build test

build:
	docker-compose build

run:
	docker-compose up

migrate:
	$(COMMAND) 'cd xarala; for db in default database2; do ./manage.py migrate --database=$${db}; done'

collectstatic:
	docker-compose run --rm djangoapp xarala/manage.py collectstatic --no-input

check: checksafety checkstyle

test:
	cd src && pytest

checksafety:
	$(COMMAND) "pip install tox && tox -e checksafety"

checkstyle:
	$(COMMAND) "pip install tox && tox -e checkstyle"

coverage:
	$(COMMAND) "pip install tox && tox -e coverage"

clean:
	rm -rf build
	rm -rf xarala.egg-info
	rm -rf dist
	rm -rf htmlcov
	rm -rf .tox
	rm -rf .cache
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete
	rm -rf $(find . -type d -name __pycache__)
	rm .coverage
	rm .coverage.*

dockerclean:
	docker system prune -f
	docker system prune -f --volumes

runserver:
	python src/manage.py runserver

migration:
	python src/manage.py makemigrations

migratedb:
	python src/manage.py migrate

superuser:
	python src/manage.py createsuperuser

codestyle:
	pipenv run flake8
	pipenv run black --check .