# Task Manager

[![hexlet-check](https://github.com/ESKolpakov/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/ESKolpakov/python-project-52/actions/workflows/hexlet-check.yml)  
[![Maintainability](https://qlty.sh/badges/3bebc0e0-3138-474b-960c-cff05cdb37ce/maintainability.svg)](https://qlty.sh/gh/ESKolpakov/projects/python-project-52)
[![Quality Gate](https://sonarcloud.io/api/project_badges/quality_gate?project=ESKolpakov_python-project-52)](https://sonarcloud.io/summary/new_code?id=ESKolpakov_python-project-52)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ESKolpakov_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=ESKolpakov_python-project-52)
[![Maintainability](https://sonarcloud.io/api/project_badges/measure?project=ESKolpakov_python-project-52&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=ESKolpakov_python-project-52)
[![Reliability](https://sonarcloud.io/api/project_badges/measure?project=ESKolpakov_python-project-52&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=ESKolpakov_python-project-52)


Проект "Менеджер задач" — веб-приложение для управления задачами с авторизацией, статусами, метками и фильтрацией.

## Демо

🌐 [Онлайн-версия проекта на Render](https://python-project-52-7b5l.onrender.com)

## Установка и запуск

```bash
git clone https://github.com/ESKolpakov/python-project-52.git
cd python-project-52
make setup
make render-start
```

## Команды Makefile

- `make install` — установка зависимостей через `uv`
- `make migrate` — применение миграций базы данных
- `make collectstatic` — сборка статических файлов
- `make setup` — полная настройка проекта (`install + migrate + collectstatic`)
- `make render-start` — запуск приложения через Gunicorn
- `make tests` — запуск unit-тестов Django

## Стек технологий

- Python 3.12
- Django 5.2
- PostgreSQL / SQLite
- Gunicorn (продакшн-сервер)
- Render (платформа для деплоя)
- Rollbar (система логирования ошибок)
- Qlty.sh (сервис для оценки качества кода)