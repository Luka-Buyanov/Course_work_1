from typing import Any



def log(filename: Any = "result.log") -> Any:
    """Функция декоратор вызывающая функции для записи результатов работы функции"""

    def decorator(func: Any) -> Any:
        """Подфункция декоратора, использующая функцию под декоратором"""

        def checking(*args: Any, **kwargs: Any) -> None:
            """Подфункция декоратора, выводит результаты работы функции в файл"""

            result = func(*args, **kwargs)
            file = open(f"../logs/{filename}", "w")
            file.write(str(result))
            file.close()

        return checking

    return decorator

@log()
def spending_by_category(transactions: list[dict], category: str, date: str = None) -> list[dict]:
    result = []
    output = []
    if date is not None:
        day = int(date[:2])
        month = int(date[3:5])
        if month <= 3:
            year = int(date[6:10]) - 1
            month = month + 9
        else:
            year = int(date[6:10])
            month = month - 3
        start_date = f"{day}.0{month}.{year}"
        for transaction in transactions:
            if start_date < transaction["Дата операции"] < date:
                result.append(transaction)
    else:
        result = transactions
    for transaction in result:
        if category == transaction["Категория"]:
            output.append(transaction)
    return output
