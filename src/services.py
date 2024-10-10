import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/services.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def search_in_operations(request: str, main_operations: list[dict]) -> str:
    """Функция поиска операций по переданному значению"""

    logger.info("Запущена функция поиска операций по значению")
    result = []
    for value in main_operations:
        if (
            value["Категория"] != ""
            and type(value["Категория"]) is str
            and value["Описание"] != ""
            and type(value["Описание"]) is str
        ):
            if request in value["Категория"] or request in value["Описание"]:
                result.append(value)
    json_data = json.dumps(result, ensure_ascii=False)
    logger.info("Завершена функция поиска операций по значению")
    return json_data
