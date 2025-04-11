install:
	pip install -r requirements.txt

collectstatic:
	python manage.py collectstatic --noinput

migrate:
	python manage.py migrate

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh

lint:
	flake8 .

format:
	black .

lint-isort:
	isort .

check-black:
	black --check .

check-isort:
	isort --check .

check:
	flake8 . && black --check . && isort --check-only .

setup:
	@$(MAKE) install && \
	$(MAKE) migrate && \
	$(MAKE) collectstatic

tests:
	python manage.py test
