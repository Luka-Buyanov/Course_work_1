import logging

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/readers.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def excel_reader() -> list[dict]:
    """Функция выводящая данные из excel файла"""

    logger.info("Запущена функция выводящая данные из Exel")
    result = []
    error_result = []
    try:
        excel_data = pd.read_excel("../data/operations.xlsx")
    except FileNotFoundError:
        logger.error("Ошибка, файл не найден!")
        error_result = [{"error": "Ошибка, файл не найден"}]
    else:
        result = excel_data.to_dict(orient="records")
    if result:
        logger.info("Завершена функция выводящая данные из Exel")
        return result
    else:
        logger.error("Завершена с ошибкой функция выводящая данные из Exel")
        return error_result
