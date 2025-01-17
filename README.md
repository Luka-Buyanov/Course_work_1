# Курсовая 1
Это приложение для работы с данными которые находятся в Excel-файле, и их вывода.

Создаётся в рамках домашнего задания курсовой работы 3 курса "Python - разработчик" от Skypro.

## Содержание
- [Используемые версии](#используемые-версии)
- [Использование](#использование)
- [Тестирование](#тестирование)
- [Сделано](#сделано)


## Используемые версии
- python = "^3.12"
- black = "^24.8.0"
- isort = "^5.13.2"
- flake8 = "^7.1.1"
- mypy = "^1.11.2"
- pytest = "^8.3.3"
- requests = "^2.32.3"
- pandas = "^2.2.3"
- openpyxl = "^3.1.5"
- python-dotenv = "^1.0.1"
- freezegun = "^1.5.1"
- pytest-cov = "^5.0.0"

## Использование
Скачать и открыть в pycharm.
В папку проекта поместить файл с настройками.
В папку data поместить excel файл с транзакциями.

## Тестирование
В проекте имеются инструменты для проверки:
- black
- isort
- flake 8
- mypy

Для их использования введите команду:

``
(название инструмента) .
``

В проекте проверены все функциональности проекта и некоторые ошибочные случаи.
Для их запуска перейдите в файл с тестом через PyCharm и запустите соответствующий файл.


## Сделано
Добавлено несколько функций:

- Функция главной страницы, принимающая на вход дату и выводящая JSON ответ содержащий данные от начала месяца и до введённой даты:
- - Приветствие
- - Данные по картам: последние 4 цифры, сумма расходов, кэшбэк.
- - Топ 5 категорий трат
- - Топ 5 транзакций
- - Курс валют
- - Стоимость акций
- Функция простого поиска в описании или категории списка
- Функция выводящая траты по категориям в файл

Все функции залогированы, логи с результатами выводятся в папку logs.

В папке htmlcov находится отчёт о покрытии кода тестами.