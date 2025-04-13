install:
	uv pip install --no-cache-dir .

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
	isort --check-only .

check:
	flake8 . && black --check . && isort --check-only .

setup:
	python -m pip install --upgrade pip && \
	uv pip install --no-cache-dir . && \
	python manage.py migrate && \
	python manage.py collectstatic --noinput

tests:
	python manage.py test