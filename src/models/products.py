import json
import requests
from urllib.parse import quote
from typing import Optional, List, Tuple
from . import database as db


url_products = "https://world.openfoodfacts.org/country/france/{page}.json"
url_category_products = "https://fr.openfoodfacts.org/categorie/{id_category}.json"
url_substitutes = "https://fr.openfoodfacts.org/cgi/search.pl?action=process&search_terms={terms}&tagtype_0=categories&tag_contains_0=contains&tag_0={category}&sort_by=unique_scans_n&json=1"


def get_products_from_category(id_category: str, page: int=1):
    url = url_category_products.format(id_category=id_category, page=page)
    req = requests.get(url)
    json_ = req.json()
    if not "products" in json_:
        return {}
    return json_


def get_product_substitutes(terms: str, id_category: str):
    url = url_substitutes.format(terms=quote(
        terms), category=quote(id_category))
    req = requests.get(url)
    return req.json()

def save_products_db(products: List):
    for product in products:
        save_product_db(product, False)
    db.handler.commit()

def save_product_db(product: List, commit=True):
    query = (
        "INSERT INTO `products`"
        "(id_api, name, brands, nutriscore_grade, fat, saturated_fat, sugars, salt, stores, url, ingredients_text, quantity, code)\n"
        "VALUES (%(id_api)s, %(name)s, %(brands)s, %(nutriscore_grade)s, %(fat)s, %(saturated_fat)s, %(sugars)s, %(salt)s, %(stores)s, %(url)s, %(ingredients_text)s, %(quantity)s, %(code)s)\n"
        "ON DUPLICATE KEY UPDATE\n"
        "name=%(name)s, brands=%(brands)s, nutriscore_grade=%(nutriscore_grade)s, fat=%(fat)s, saturated_fat=%(saturated_fat)s, sugars=%(sugars)s, salt=%(salt)s, stores=%(stores)s, url=%(url)s, ingredients_text=%(ingredients_text)s, quantity=%(quantity)s, code=%(code)s"
    )
    args = {
        "id_api": product.id,
        "name": product.name,
        "brands": product.brands,
        "nutriscore_grade": product.nutriscore_grade,
        "fat": product.fat,
        "saturated_fat": product.saturated_fat,
        "sugars": product.sugars,
        "salt": product.salt,
        "stores": product.stores,
        "url": product.url,
        "ingredients_text": product.ingredients_text,
        "quantity": product.quantity,
        "code": product.code
    }
    ok, msg = db.handler.execute_query(query, args, False)
    if commit:
        db.handler.commit()
    return ok, msg

