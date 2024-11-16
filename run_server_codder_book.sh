#!/bin/bash

# Проверка, что передан аргумент
if [ -z "$1" ]; then
  echo "Ошибка: укажите путь к рабочей области."
  exit 1
fi

WORKSPACE_PATH="$1"

# Проверка существования директории рабочей области
if [ ! -d "$WORKSPACE_PATH" ]; then
  echo "Ошибка: рабочая область '$WORKSPACE_PATH' не существует."
  exit 1
fi

# Проверка существования виртуального окружения
if [ ! -d "$WORKSPACE_PATH/.venv" ]; then
  echo "Ошибка: виртуальное окружение не найдено в '$WORKSPACE_PATH/.venv'."
  exit 1
fi

cd $WORKSPACE_PATH
exec $WORKSPACE_PATH/.venv/bin/python3 $WORKSPACE_PATH/manage.py runserver 127.0.0.1:8000