import requests
from config import CSTECH_URL, get_cstech_headers


def get_prices(listing_id: str, from_date: str, to_date: str):
    url = f"{CSTECH_URL}/{listing_id}"

    params = {
        "from": from_date,
        "to": to_date
    }

    response = requests.get(
        url,
        headers=get_cstech_headers(),
        params=params
    )

    if response.status_code != 200:
        raise Exception(f"Erro GET CSTECH [{listing_id}]: {response.text}")

    return response.json()