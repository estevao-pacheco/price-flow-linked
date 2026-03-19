import os
import json


def transform_prices(data):
    """
    Recebe o retorno bruto da API CSTECH
    e retorna somente os campos necessários:
    - date
    - minStay
    - valor BRL
    """
    result = []

    for day in data:
        date = day.get("date")

        prices = []
        for p in day.get("prices", []):
            if p.get("minStay") != 1:
                continue

            value = p.get("_mcval", {}).get("BRL")

            # ignora registros sem valor
            if value is None:
                continue

            prices.append({
                "minStay": 1,
                "value": value
            })

        # só adiciona se tiver preço válido
        if prices:
            result.append({
                "date": date,
                "prices": prices
            })

    return result


def transform_and_save(data, listing_id, path="data"):
    """
    Transforma e salva em JSON (debug/auditoria)
    """

    os.makedirs(path, exist_ok=True)

    transformed = transform_prices(data)

    file_name = f"{path}/prices_{listing_id}.json"

    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(transformed, f, indent=4, ensure_ascii=False)

    return transformed


def build_xtay_payload(data):
    """
    Converte o formato interno para o formato esperado pelo XTAY
    """

    payload = []

    for day in data:
        prices = [
            {
                "minStay": p["minStay"],
                "_f_val": p["value"]
            }
            for p in day["prices"]
        ]

        payload.append({
            "from": day["date"],
            "to": day["date"],
            "closedToArrival": False,
            "closedToDeparture": False,
            "prices": prices
        })

    return payload