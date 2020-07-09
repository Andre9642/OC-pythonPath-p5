import models.products as model
from typing import List
from collections import namedtuple


Product = namedtuple(
    "product",
    (
        "id",
        "name",
        "brands",
        "nutriscore_grade",
        "fat",
        "saturated_fat",
        "sugars",
        "salt",
        "stores",
        "url",
        "ingredients_text",
        "quantity",
        "code",
        "categories_tags",
    ),
)


def get_product_substitutes(terms, id_category, id_product):
    res = model.get_product_substitutes(terms, id_category)
    products = process_json(res)
    return {
        "count": int(res["count"]),
        "page_size": int(res["page_size"]),
        "page": res["page"],
        "products": products
    }


def get_products_from_category(id_category, page=1):
    if page < 1:
        page = 1
    res = model.get_products_from_category(id_category)
    products = process_json(res)
    return {
        "count": int(res["count"]),
        "page_size": int(res["page_size"]),
        "page": res["page"],
        "products": products
    }


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
                product.get("nutriscore_grade"),
                float(product["nutriments"].get("fat", -1)),
                float(product["nutriments"].get("saturated-fat", -1)),
                float(product["nutriments"].get("sugars", -1)),
                float(product["nutriments"].get("salt", -1)),
                product.get("stores"),
                product["url"],
                product.get("ingredients_text"),
                product.get("quantity"),
                product.get("code"),
                product["categories_tags"],
            )
        )
    return out
