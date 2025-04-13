#!/usr/bin/env bash

# Установка зависимостей и подготовка проекта
make install
make collectstatic
make migrate
