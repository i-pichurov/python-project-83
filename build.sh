#!/usr/bin/env bash

# Устанавливаем Poetry, если он ещё не установлен
if ! command -v poetry &> /dev/null; then
    echo "Poetry не установлен. Устанавливаем..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"  # Добавляем Poetry в PATH
fi

# Устанавливаем зависимости через Poetry
echo "Устанавливаем зависимости..."
poetry install

# Запускаем команду make install и создаем базу данных
echo "Запускаем make install..."
make install && psql -a -d $DATABASE_URL -f database.sql