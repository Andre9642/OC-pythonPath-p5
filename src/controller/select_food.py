import models.products as model
from typing import List
from collections import namedtuple


Product = namedtuple(
    "product",
    (
        "id",
        "name",
        "brands",
        "nutrition_grade",
        "fat",
        "saturated_fat",
        "sugars",
        "salt",
        "stores",
        "url",
        "categories_tags",
    ),
)

def get_products_from_category(id_category):
    res = model.get_products_from_category(id_category)
    products = process_json(res)
    return products

def process_json(json_: dict) -> List:
    out = []
    for product in json_["products"]:
        if (
            "categories_tags" not in product.keys()
            or "product_name" not in product.keys()
            or not all([product["id"], product["product_name"], product["url"]])
        ):
            continue
        out.append(
            Product(
                product["id"],
                product["product_name"],
                product.get("brands", ""),
                product.get("nutrition_grade"),
                float(product["nutriments"].get("fat", -1)),
                float(product["nutriments"].get("saturated-fat", -1)),
                float(product["nutriments"].get("sugars", -1)),
                float(product["nutriments"].get("salt", -1)),
                product.get("stores"),
                product["url"],
                product["categories_tags"],
            )
        )
    return out