#!/usr/bin/env bash

# Установка uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Установка зависимостей
make install

# Применение миграций — ДО запуска любых тестов!
python3 manage.py migrate

# Сборка статики
make collectstatic
