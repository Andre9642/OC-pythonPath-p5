import json
import requests
from typing import Optional, List, Tuple
from . import database as db


url_products = "https://world.openfoodfacts.org/country/france/{page}.json"
url_category_products = "https://fr.openfoodfacts.org/categorie/{id_category}.json"



def get_products_from_category(id_category: str, page=1):
    url = url_category_products.format(id_category=id_category, page=page)
    req = requests.get(url)
    json_ = req.json()
    if not "products" in json_:
        return {}
    return json_
