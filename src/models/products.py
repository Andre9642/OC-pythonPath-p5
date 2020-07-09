import json
import requests
from urllib.parse import quote
from typing import Optional, List, Tuple
from . import database as db


url_products = "https://world.openfoodfacts.org/country/france/{page}.json"
url_category_products = "https://fr.openfoodfacts.org/categorie/{id_category}.json"
url_substitutes = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms={terms}&tagtype_0=categories&tag_contains_0=contains&tag_0={category}&sort_by=unique_scans_n&json=1"


def get_products_from_category(id_category: str, page=1):
    url = url_category_products.format(id_category=id_category, page=page)
    req = requests.get(url)
    json_ = req.json()
    if not "products" in json_:
        return {}
    return json_

def get_product_substitutes(terms, id_category):
    url = url_substitutes.format(terms=quote(terms), category=quote(id_category))
    req = requests.get(url)
    return req.json()
