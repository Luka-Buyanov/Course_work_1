import logging
from datetime import datetime
from typing import Any, Optional

import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("../logs/reports.log", "w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def log(filename: Any = "result.log") -> Any:
    """Функция декоратор вызывающая функции для записи результатов работы функции"""

    def decorator(func: Any) -> Any:
        """Подфункция декоратора, использующая функцию под декоратором"""

        def checking(*args: Any, **kwargs: Any) -> None:
            """Подфункция декоратора, выводит результаты работы функции в файл"""

            logger.info("Используется логирующий декоратор")
            result = func(*args, **kwargs)
            file = open(f"../logs/{filename}", "w")
            file.write(str(result))
            file.close()

        return checking

    return decorator


@log()
def spending_by_category(main_transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> list[dict]:
    """Функция выводящая траты по категориям, принимает на вход DataFrame с транзакциями, категорию,
    и опциональную дату для сортировки. Принимает дату в формате 'DD.MM.YYYY'."""

    logger.info("Запущена функция выводящая траты по категориям и опциональной дате")
    result = []
    output = []
    transactions = main_transactions.to_dict(orient="records")
    if date is not None:
        logger.info("Дата введена")
        day = date[:2]
        month = int(date[3:5])
        if month <= 3:
            logger.info("Введён месяц раньше Марта")
            year = int(date[6:10]) - 1
            month = month + 9
        else:
            logger.info("Введён месяц после Марта")
            year = int(date[6:10])
            month = month - 3
        if month < 10:
            start_date = f"{day}.0{month}.{year}"
        else:
            start_date = f"{day}.{month}.{year}"
        start_dates = datetime.strptime(start_date, "%d.%m.%Y")
        dates = datetime.strptime(date, "%d.%m.%Y")
        for transaction in transactions:
            transaction_date = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
            if start_dates < transaction_date < dates:
                result.append(transaction)
    else:
        logger.info("Дата не введена")
        result = transactions
    for transaction in result:
        if category.upper() == transaction["Категория"].upper():
            output.append(transaction)
    logger.info("Завершена функция выводящая данные из Exel")
    return output
