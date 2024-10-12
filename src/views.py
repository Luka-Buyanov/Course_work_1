import json
import logging

from src.utils import (action_value, card_information, get_operations, hello_message, top_five, top_transactions,
                       value_course)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/views.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def main_views(date_time: str) -> str:
    """Функция объединяющая весь функционал модуля views"""

    logger.info("Запущена основная функция модуля views")
    date = date_time[3:10]
    start_date = f"01.{date}"
    operations = get_operations(start_date, date_time)
    logger.info("Получен список операций в промежутке дат")
    answer = {
        "greeting": hello_message(),
        "cards": card_information(operations),
        "top transactions": top_transactions(operations),
        "top categories": top_five(operations),
        "currency rates": value_course(),
        "stock prices": action_value(),
    }
    json_data = json.dumps(answer, ensure_ascii=False)
    logger.info("Получен JSON ответ в соответствии с ТЗ")
    logger.info("Завершена основная функция модуля views")
    return json_data
