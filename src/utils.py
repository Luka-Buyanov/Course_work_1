import json
import logging
import os
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv

from src.readers import excel_reader

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/utils.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def hello_message() -> str:
    """Функция выводящая приветствие в соответствии с текущим временем"""

    logger.info("Запущена функция выдающая приветствие")
    time = str(datetime.now().time())
    result = ""
    if "06:00:00" > time > "00:00:00":
        logger.info("Сейчас ночь")
        result = "Доброй ночи!"
    elif "12:00:00" > time > "06:00:00":
        logger.info("Сейчас утро")
        result = "Доброе утро!"
    elif "18:00:00" > time > "12:00:00":
        logger.info("Сейчас день")
        result = "Добрый день!"
    elif "24:00:00" > time > "18:00:00":
        logger.info("Сейчас вечер")
        result = "Добрый вечер!"
    logger.info("Завершена функция выдающая приветствие")
    return result


def get_operations(start: str, end: str) -> list[dict]:
    """Функция выводящий список операций входящих в диапазон данных"""

    logger.info("Запущена функция выводящая список операций в диапазоне дат")
    date_operations = []
    data = excel_reader()
    for operation in data:
        if start <= operation["Дата операции"] <= end:
            date_operations.append(operation)
    logger.info("Завершена функция выводящая список операций в диапазоне дат")
    return date_operations


def card_information(main_operations: list[dict]) -> list[dict]:
    """Функция выводящая данные о каждой карте в соответствии с диапазоном данных"""

    def get_card_numbers(list_operations: list[dict]) -> list[str]:
        """Подфункция выводящая список номеров карт из списка операций"""

        logger.info("Запущена подфункция выводящая список номеров карт из общего списка")
        numbers = []
        for operation in list_operations:
            if operation["Номер карты"] not in numbers:
                numbers.append(operation["Номер карты"])
        logger.info("Завершена подфункция выводящая список номеров карт из общего списка")
        return numbers

    def get_result(input_numbers: list[str], input_operations: list[dict]) -> list[dict]:
        """Подфункция выводящая конечный результат - список словарей с данными по каждой карте"""

        logger.info("Запущена подфункция выводящая список словарей с данными по карте")
        result = []
        for number in input_numbers:
            one_card = {}
            summ = 0
            for operation in input_operations:
                if operation["Сумма операции"] < 0 and operation["Статус"] != "FAILED":
                    summ += int(operation["Сумма операции"])
            one_card["Номер карты"] = number
            one_card["Сумма трат"] = str(summ)
            one_card["Кешбэк"] = str(-summ // 100)
            result.append(one_card)
        logger.info("Завершена подфункция выводящая список словарей с данными по карте")
        return result

    logger.info("Запущена функция выводящая список операций по номеру карты")
    card_numbers = get_card_numbers(main_operations)
    output = get_result(card_numbers, main_operations)
    logger.info("Завершена функция выводящая список операций по номеру карты")
    return output


def top_five(main_operations: list[dict]) -> list[dict]:
    """Функция выводящая топ 5 категорий по тратам"""

    def get_categories(list_operations: list[dict]) -> list[str]:
        """Подфункция выводящая список категорий из общего списка"""

        logger.info("Запущена подфункция выводящая список категорий из общего списка")
        result = []
        for operation in list_operations:
            if operation["Категория"] not in result:
                result.append(operation["Категория"])
        logger.info("Завершена подфункция выводящая список категорий из общего списка")
        return result

    def get_value(list_operations: list[dict], list_categories: list[str]) -> list[dict]:
        """Подфункция выводящая суммы трат к списку категорий"""

        logger.info("Запущена подфункция выводящая сумму трат к каждой категории")
        result = []
        for category in list_categories:
            one_card = {}
            summ = 0
            for operation in list_operations:
                if operation["Категория"] == category and operation["Статус"] != "FAILED":
                    summ += int(operation["Сумма операции"])
            one_card["Категория"] = category
            one_card["Сумма"] = str(summ)
            result.append(one_card)
        logger.info("Завершена подфункция выводящая сумму трат к каждой категории")
        return result

    logger.info("Запущена функция выводящая топ 5 категорий по тратам")
    categories = get_categories(main_operations)
    categories_list = get_value(main_operations, categories)
    sorted_result = sorted(categories_list, key=lambda x: x["Сумма"], reverse=True)
    result_list = sorted_result[:6]
    logger.info("Завершена функция выводящая топ 5 категорий по тратам")
    return result_list


def top_transactions(main_operations: list[dict]) -> list[dict]:
    """Функция выводящая топ 5 транзакций по тратам"""

    logger.info("Запущена функция выводящая топ 5 транзакций по тратам")
    sorted_result = sorted(
        main_operations,
        key=lambda x: x["Сумма операции с округлением"],
        reverse=True,
    )
    result_list = sorted_result[:6]
    output_list = []
    for operation in result_list:
        one_operation = {
            "Дата": operation["Дата платежа"],
            "Сумма": operation["Сумма платежа"],
            "Категория": operation["Категория"],
            "Описание": operation["Описание"],
        }
        output_list.append(one_operation)
    logger.info("Завершена функция выводящая топ 5 транзакций по тратам")
    return output_list


def user_options(path: str) -> Any:
    """Функция выводящая список настроек из файла формата JSON"""

    logger.info("Запущена функция выводящая список настроек из файла JSON")
    with open(path, encoding="utf8") as file:
        data = json.load(file)
    logger.info("Завершена функция выводящая список настроек из файла JSON")
    return data


def value_course() -> list[dict]:
    """Функция выводящая курс валют"""

    def user_value(options: dict) -> Any:
        """Подфункция выводящая курсы валют по настройкам пользователя"""

        logger.info("Запущена подфункция выводящая курс валют с сайта")
        load_dotenv()
        symbols = options["user_currencies"]
        symbol = ""
        for currency in symbols:
            symbol = symbol + f"{currency},"
        api_key = os.getenv("API_KEY")
        course = requests.get(
            f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbol}&base=RUB",
            headers={"apikey": api_key},
            data={},
        )
        logger.info("Получен ответ от сайта")
        output = course.json()
        all_rates = output["rates"]
        logger.info("Завершена функция выводящая курс валют с сайта")
        return all_rates

    logger.info("Запущена функция выводящая курс валют")
    user_option = user_options("../user_settings.json")
    rates = user_value(user_option)
    result = []
    for rate, price in rates.items():
        one_value = {"currency": rate, "rate": price}
        result.append(one_value)
    logger.info("Завешена функция выводящая курс валют")
    return result


def action_value() -> Any:
    """Функция выводящая стоимость акций по опциям пользователя"""

    logger.info("Запущена функция выводящая стоимость акций")
    option = user_options("../user_settings.json")
    symbols = ""
    i = 0
    for symbol in option["user_stocks"]:
        if i == 0:
            symbols = symbols + f"{symbol}"
            i += 1
        else:
            symbols = symbols + f",{symbol}"
    load_dotenv()
    api_key = os.getenv("FINANCE_KEY")
    responses = requests.get(f"https://api.marketstack.com/v1/eod/latest?access_key={api_key}&symbols={symbols}")
    logger.info("Получен ответ от сайта")
    response = responses.json()
    data = response.get("data")
    result = []
    for symbol in data:
        stock = symbol["symbol"]
        price = symbol["adj_close"]
        one_symbol = {"symbol": stock, "price": price}
        result.append(one_symbol)
    logger.info("Завершена функция выводящая стоимость акций")
    return result
