import requests
from config import XTAY_URL, get_xtay_headers


def send_prices(listing_id: str, payload):
    url = f"{XTAY_URL}/{listing_id}/batch"

    response = requests.patch(
        url,
        headers=get_xtay_headers(),
        json=payload
    )

    if response.status_code not in (200, 204):
        raise Exception(f"Erro POST XTAY [{listing_id}]: {response.text}")

    print(f"Listing {listing_id} atualizado com sucesso")