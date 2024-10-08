import json

from src.readers import excel_reader


def search_in_operations(request: str) -> str:
    """Функция поиска операций по переданному значению"""

    operations = excel_reader()
    result = []
    for value in operations:
        if (
            value["Категория"] != ""
            and type(value["Категория"]) is str
            and value["Описание"] != ""
            and type(value["Описание"]) is str
        ):
            if request in value["Категория"] or request in value["Описание"]:
                result.append(value)
    json_data = json.dumps(result, ensure_ascii=False)
    return json_data
