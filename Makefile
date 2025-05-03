build:
	./build.sh

install:
	uv pip install -r requirements.txt

collectstatic:
	python3 manage.py collectstatic --noinput

migrate:
	python3 manage.py migrate

render-start:
	gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000

setup:
	make install && make migrate && make collectstatic

tests:
	python3 manage.py test

coverage:
	coverage run manage.py test && coverage xml