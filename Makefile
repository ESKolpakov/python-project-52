build:
	./build.sh

install:
	uv pip install -r requirements.txt

migrate:
	python3 manage.py migrate

collectstatic:
	python3 manage.py collectstatic --noinput

render-start:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000