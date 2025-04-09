# Task Manager

[![Maintainability](https://qlty.sh/badges/3bebc0e0-3138-474b-960c-cff05cdb37ce/maintainability.svg)](https://qlty.sh/gh/ESKolpakov/projects/python-project-52)

Проект "Менеджер задач" — веб-приложение для управления задачами с авторизацией, статусами, метками и фильтрацией.

## Демо

🌐 [Онлайн-деплой на Render](https://python-project-52-7b5l.onrender.com)

## Установка и запуск

```bash
git clone https://github.com/ESKolpakov/python-project-52.git
cd python-project-52
make install
cp .env.example .env
make migrate
make render-start
```

## Команды Makefile

- `make install` — установка зависимостей
- `make migrate` — применение миграций
- `make render-start` — запуск через gunicorn
- `make collectstatic` — сборка статики
- `make lint` — проверка кода `flake8`
- `make format` — автоформат `black`
- `make check` — линтинг и формат-чек (`flake8`, `black`, `isort`)
- `make build` — команда для билда

## Стек

- Python 3.12
- Django 5.2
- PostgreSQL / SQLite
- Render (деплой)
- Rollbar (лог ошибок)
- Qlty (проверка качества кода)
