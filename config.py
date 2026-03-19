from os import environ
from dotenv import load_dotenv

load_dotenv()

#Gmail
GMAIL_KEY = environ.get('GMAIL_KEY')

# 🔐 Credenciais
CSTECH_STAYS_API_KEY = environ.get("CSTECH_STAYS_API_KEY")
XTAY_STAYS_API_KEY = environ.get("XTAY_STAYS_API_KEY")

if not CSTECH_STAYS_API_KEY:
    raise Exception("❌ CSTECH_STAYS_API_KEY não encontrada no .env")

if not XTAY_STAYS_API_KEY:
    raise Exception("❌ XTAY_STAYS_API_KEY não encontrada no .env")


# 🌐 URLs
CSTECH_URL = "https://cstech.stays.net/external/v1/calendar/listing"
XTAY_URL = "https://xtay.stays.net/external/v1/calendar/listing"


#Headers
def get_cstech_headers():
    return {
        "accept": "application/json",
        "Authorization": f"Basic {CSTECH_STAYS_API_KEY}"
    }


def get_xtay_headers():
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {XTAY_STAYS_API_KEY}"
    }


#Mapping (DE-PARA)
LISTING_MAPPING = [
    {
        "name": "Sleep Suite Single",
        "cstech": "66d8c0e3a919e968e4dfbf58",
        "xtay": "6866ac3492aa7d2cf68078b5"
    },
    {
        "name": "Sleep Suite Double",
        "cstech": "66d8c0baf4e5ae6debcbd141",
        "xtay": "6866a97292aa7d2cf6807878"
    },
    {
        "name": "Suite Pne",
        "cstech": "66d8c08cec3557cf86346d10",
        "xtay": "6866a81392aa7d2cf6807846"
    },
    {
        "name": "Suite Plus",
        "cstech": "66d8c057a919e968e4dfbaa3",
        "xtay": "6866a53a92aa7d2cf6807811"
    },
    {
        "name": "Suite",
        "cstech": "6851677b140b3243b4bea325",
        "xtay": "6866b03392aa7d2cf68078e6"
    },
    {
        "name": "Studio",
        "cstech": "66d8b896327401ca8835ab74",
        "xtay": "6866a28792aa7d2cf68077be"
    }
]