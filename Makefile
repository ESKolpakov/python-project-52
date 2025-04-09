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

check:
	flake8 . && black --check . && isort --check-only .