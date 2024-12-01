import json
import random

def generate_record():
    """
    Генерирует запись в формате JSON с соблюдением логики и условий.

    Паттерны генерации данных:
    1. Сегментация по бизнесу (`segment`):
       - Значения случайны: "Малый бизнес", "Средний бизнес", "Крупный бизнес".
       - Используются для определения характера клиента.
    2. Роль клиента (`role`):
       - Возможные роли: "ЕИО" или "Сотрудник".
       - Влияет на рекомендованные методы, особенно для "Крупного бизнеса".
    3. Текущий метод (`currentMethod`):
       - Выбирается случайно из ["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"].
       - Если мобильное приложение отсутствует, корректируется (исключается "КЭП в приложении").
    4. Наличие мобильного приложения (`mobileApp`):
       - Если `mobileApp` = False:
         - Подписи на мобильных устройствах (`signatures.common.mobile`, `signatures.special.mobile`) равны 0.
         - Метод "КЭП в приложении" удаляется из `availableMethods`.
    5. Подписи (`signatures`):
       - Если `mobileApp` = True:
         - Подписи на мобильных устройствах выбираются случайно.
       - Подписи для веба всегда имеют случайное значение.
    6. Доступные методы (`availableMethods`):
       - Генерируются случайным образом (1-4 метода).
       - Если нет мобильного приложения, "КЭП в приложении" удаляется.
       - Гарантируется, что `availableMethods` не будет пустым.
    7. Обращения (`claims`):
       - `claims` > 0 только если `currentMethod` = "SMS".
    8. Рекомендованный метод (`recommendedMethod`):
       - Если только один доступный метод: выбирается он.
       - Если есть `claims`, "SMS" исключается из рекомендованных.
       - Если есть `mobileApp`, приоритет у "PayControl" и "КЭП в приложении".
       - Если клиент из "Крупного бизнеса" с ролью "ЕИО", предпочитается "КЭП на токене".
       - Если ничего из вышеуказанного не применимо, выбирается первый доступный метод.

    Возвращаемая структура:
    {
        "clientId": str,
        "organizationId": str,
        "segment": str,
        "role": str,
        "organizations": int,
        "currentMethod": str,
        "mobileApp": bool,
        "signatures": {
            "common": {"mobile": int, "web": int},
            "special": {"mobile": int, "web": int}
        },
        "availableMethods": list,
        "claims": int,
        "recommendedMethod": str
    }
    """
    client_id = f"client_{random.randint(1000, 99999)}"
    organization_id = f"organization_{random.randint(1000, 99999)}"
    segment = random.choice(["Малый бизнес", "Средний бизнес", "Крупный бизнес"])
    role = random.choice(["ЕИО", "Сотрудник"])
    organizations = random.randint(1, 300)
    current_method = random.choice(["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"])
    mobile_app = random.choice([True, False])

    signatures = {
        "common": {
            "mobile": random.randint(1, 50) if mobile_app else 0,
            "web": random.randint(1, 50),
        },
        "special": {
            "mobile": random.randint(1, 50) if mobile_app else 0,
            "web": random.randint(1, 50),
        }
    }

    available_methods = random.sample(
        ["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"], 
        k=random.randint(1, 4)
    )

    if not mobile_app and "КЭП в приложении" in available_methods:
        available_methods.remove("КЭП в приложении")
    
    if not available_methods:
        available_methods = ["SMS", "PayControl", "КЭП на токене", "КЭП в приложении"]

    claims = random.randint(0, 10) if current_method == "SMS" else 0

    if len(available_methods) == 1:
        recommended_method = available_methods[0]
    elif claims > 0:
        filtered_methods = [m for m in available_methods if m != "SMS"]
        if not filtered_methods:
            filtered_methods = available_methods
        recommended_method = filtered_methods[0]
    elif mobile_app:
        filtered_methods = [m for m in available_methods if m in ["PayControl", "КЭП в приложении"]]
        if not filtered_methods:
            filtered_methods = available_methods
        recommended_method = filtered_methods[0]
    elif segment == "Крупный бизнес" and role == "ЕИО":
        if "КЭП на токене" in available_methods:
            recommended_method = "КЭП на токене"
        else:
            recommended_method = available_methods[0]
    else:
        recommended_method = available_methods[0]

    if not mobile_app and current_method == "КЭП в приложении":
        current_method = "КЭП на токене" if "КЭП на токене" in available_methods else "PayControl"

    return {
        "clientId": client_id,
        "organizationId": organization_id,
        "segment": segment,
        "role": role,
        "organizations": organizations,
        "currentMethod": current_method,
        "mobileApp": mobile_app,
        "signatures": signatures,
        "availableMethods": available_methods,
        "claims": claims,
        "recommendedMethod": recommended_method
    }

if __name__ == "__main__":
    data = [generate_record() for _ in range(50000)]

    output_file = "synthetic_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        