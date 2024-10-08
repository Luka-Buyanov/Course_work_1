import pandas as pd


def excel_reader() -> list[dict]:
    """Функция выводящая данные из excel файла"""

    result = []
    error_result = []
    try:
        excel_data = pd.read_excel("../data/operations.xlsx")
    except FileNotFoundError:
        error_result = [{"error": "Ошибка, файл не найден"}]
    else:
        result = excel_data.to_dict(orient="records")
    if not result:
        return result
    else:
        return error_result
