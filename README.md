## Описание
Данный сайт создан с использованием фреймворка [*plotly*](https://dash.plotly.com/), вспомогательной библиотеки
[*Dash Bootstrap Components*](https://dash-bootstrap-components.opensource.faculty.ai/) и базы данных
[*SQLite3*](https://www.sqlite.org/) с наполнением [*Chinook*](https://github.com/lerocha/chinook-database).

## Установка
### Зависимости

1. установить [*python3.11*](https://www.python.org/downloads/release/python-3119/)
    1. [*создать виртуальное окружение*](https://docs.python.org/3/library/venv.html#creating-virtual-environments)
       ```shell
       python -m venv c:\path\to\myenv
       ```
       ```shell
       python -m venv venv  # пример
       ```
    2. [*активировать виртуальное окружение*](https://docs.python.org/3/library/venv.html#how-venvs-work)
       ```shell
       venv\Scripts\activate.bat  # для Windows
       ```
       ```shell
       venv\bin\activate  # для Unix
       ```
2. установить [*библиотеки*](requirements.txt)
   ```shell
   pip install -r requirements.txt
   ```
3. [*создать бд*](#генерация-бд)

## База данных
[*Скрипт*](chinook_sqlite.sql) для генерации.

### Генерация БД
Достаточно выполнить:

```shell
python db.py
```

## Запуск
Команда ниже запустит сайт по адресу [*http://127.0.0.1:8050/*](http://127.0.0.1:8050/), что будет написано при запуске.

```shell
python app.py
```
