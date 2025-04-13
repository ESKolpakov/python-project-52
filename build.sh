#!/usr/bin/env bash

# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# установка зависимостей, статики и миграций
make install && make collectstatic && make migrate
