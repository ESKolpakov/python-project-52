#!/usr/bin/env bash

# Установка uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Установка зависимостей и подготовка проекта
make install && make collectstatic && make migrate