import json
import os
from datetime import datetime
from typing import Any

import requests
from dotenv import load_dotenv

from src.readers import excel_reader


def main_views(date_time: str) -> str:
    """Функция объединяющая весь функционал модуля views"""

    def hello_message() -> str:
        """Функция выводящая приветствие в соответствии с текущим временем"""

        time = str(datetime.now().time())
        result = ""
        if "06:00:00" > time > "00:00:00":
            result = "Доброй ночи!"
        elif "12:00:00" > time > "06:00:00":
            result = "Доброе утро!"
        elif "18:00:00" > time > "12:00:00":
            result = "Добрый день!"
        elif "00:00:00" > time > "18:00:00":
            result = "Добрый вечер!"
        return result

    def get_operations(start: str, end: str) -> list[dict]:
        """Функция выводящий список операций входящих в диапазон данных"""

        date_operations = []
        data = excel_reader()
        for operation in data:
            if start <= operation["Дата операции"] <= end:
                date_operations.append(operation)
        return date_operations

    def card_information(main_operations: list[dict]) -> list[dict]:
        """Функция выводящая данные о каждой карте в соответствии с диапазоном данных"""

        def get_card_numbers(list_operations: list[dict]) -> list[str]:
            """Функция выводящая список номеров карт из списка операций"""

            numbers = []
            for operation in list_operations:
                if operation["Номер карты"] not in numbers:
                    numbers.append(operation["Номер карты"])
            return numbers

        def get_result(
            input_numbers: list[str], input_operations: list[dict]
        ) -> list[dict]:
            """Функция выводящая конечный результат - список словарей с данными по каждой карте"""

            result = []
            for number in input_numbers:
                one_card = {}
                summ = 0
                for operation in input_operations:
                    if (
                        operation["Сумма операции"] < 0
                        and operation["Статус"] != "FAILED"
                    ):
                        summ += int(operation["Сумма операции"])
                one_card["Номер карты"] = number
                one_card["Сумма трат"] = str(summ)
                one_card["Кешбэк"] = str(-summ // 100)
                result.append(one_card)
            return result

        card_numbers = get_card_numbers(main_operations)
        output = get_result(card_numbers, main_operations)
        return output

    def top_five(main_operations: list[dict]) -> list[dict]:
        """Функция выводящая топ 5 категорий по тратам"""

        def get_categories(list_operations: list[dict]) -> list[str]:
            """Подфункция выводящая список категорий из общего списка"""
            result = []
            for operation in list_operations:
                if operation["Категория"] not in result:
                    result.append(operation["Категория"])
            return result

        def get_value(
            list_operations: list[dict], list_categories: list[str]
        ) -> list[dict]:
            """Подфункция выводящая суммы трат к списку категорий"""

            result = []
            for category in list_categories:
                one_card = {}
                summ = 0
                for operation in list_operations:
                    if (
                        operation["Категория"] == category
                        and operation["Статус"] != "FAILED"
                    ):
                        summ += int(operation["Сумма операции"])
                one_card["Категория"] = category
                one_card["Сумма"] = str(summ)
                result.append(one_card)
            return result

        categories = get_categories(main_operations)
        categories_list = get_value(main_operations, categories)
        sorted_result = sorted(categories_list, key=lambda x: x["Сумма"], reverse=True)
        result_list = sorted_result[:6]
        return result_list

    def top_transactions(main_operations: list[dict]) -> list[dict]:
        """Функция выводящая топ 5 транзакций по тратам"""

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
        return output_list

    def user_options(path: str) -> dict:
        """Функция выводящая список настроек из файла формата JSON"""

        with open(path, encoding="utf8") as file:
            data = json.load(file)
        return data

    def value_course() -> list[dict]:
        """Функция выводящая курс валют"""

        def user_value(options: dict) -> dict:
            """Подфункция выводящая курсы валют по настройкам пользователя"""

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
            output = course.json()
            all_rates = output["rates"]
            return all_rates

        user_option = user_options("../user_settings.json")
        rates = user_value(user_option)
        result = []
        for rate, price in rates.items():
            one_value = {"currency": rate, "rate": price}
            result.append(one_value)
        return result

    def action_value() -> Any:
        """Функция выводящая стоимость акций по опциям пользователя"""

        option = user_options("../user_settings.json")
        symbols = option["user_stocks"]
        load_dotenv()
        api_key = os.getenv("FINANCE_KEY")
        url = f"https://api.marketstack.com/v1/eod?access_key={api_key}"
        querystring = {
            "symbols": symbols,
            "exchange": "S&P500",
            "date_from": "2024-10-07",
        }
        responses = requests.get(url, params=querystring)
        response = responses.json()
        data = response.get("data")
        result = []
        for symbol in data:
            stock = symbol["symbol"]
            price = symbol["adj_close"]
            one_symbol = {"symbol": stock, "price": price}
            result.append(one_symbol)
        return result

    date = date_time[3:9]
    start_date = f"01.{date}"
    operations = get_operations(start_date, date_time)
    print(hello_message())
    answer = {
        "greeting": hello_message(),
        "cards": card_information(operations),
        "top transactions": top_transactions(operations),
        "top categories": top_five(operations),
        # "currency rates" : value_course(),
        # "stock prices" : action_value(),
    }
    json_data = json.dumps(answer, ensure_ascii=False)
    return json_data


a = main_views("2019:05:30 15:15:15")
print(a)
