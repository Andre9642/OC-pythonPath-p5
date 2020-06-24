from collections import namedtuple
import json
import requests
import sys
from typing import Optional, List, Tuple
from . import database as db
from . import categories
from common import *

Product = namedtuple(
    "Product",
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
urlProducts = "https://world.openfoodfacts.org/country/france/{page}.json"


class Products:
    def display(
        self, tableNameProducts: str, min: int, max: int, categoryID: str
    ) -> List:
        out = []
        query = f"SELECT * FROM {tableNameProducts} where category = %(category)s"
        args = {"min": min, "max": max, "category": categoryID}
        ok, res = db.handler.executeQuery(query, args)
        if ok:
            for i, row in enumerate(res[1], min + 1):
                out.append(Product(*row[1:10], categoryID))
            return out
        else:
            raise RuntimeError(res[-1])

    def retrieveFromAPI(
        self, page: int, limit: int = 0, lang: str = "fr", minProducts: int = 10
    ) -> List:
        res = []
        curPage = 0
        while curPage <= page:
            curPage += 1
            print(f"Processing page {curPage}...")
            url = urlProducts.format(page=page)
            req = requests.get(url)
            json_ = req.json()
            if not "products" in json_:
                break
            res += self.processJSON(req.json())
        return res

    def processJSON(self, json_: dict) -> List:
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

    def writeInDB(
        self, products: dict, tableName: str = "products"
    ) -> List[Tuple[int, int]]:
        updatedEntriesNumber = addedEntriesNumber = 0
        for product in products:
            query = (
                f"INSERT INTO `{tableName}`"
                "(id_api, name, brands, nutrition_grade, fat, saturated_fat, sugars, salt, stores, url)"
                "VALUES (%(id)s, %(name)s, %(brands)s, %(nutrition_grade)s, %(fat)s, %(saturated_fat)s, %(sugars)s, %(salt)s, %(stores)s, %(url)s)"
            )
            args = {
                "id": product.id,
                "name": product.name,
                "brands": product.brands,
                "nutrition_grade": product.nutrition_grade,
                "fat": product.fat,
                "saturated_fat": product.saturated_fat,
                "sugars": product.sugars,
                "salt": product.salt,
                "stores": product.stores,
                "url": product.url,
            }
            ok, res = db.handler.executeQuery(query, args, False)
            if not ok:
                if res[0] == db.errorcode.ER_DUP_ENTRY:
                    query = (
                        "UPDATE `products`"
                        "SET name = %(name)s, brands = %(brands)s, nutrition_grade = %(nutrition_grade)s, fat = %(fat)s, saturated_fat = %(saturated_fat)s, sugars = %(sugars)s, salt = %(salt)s, url = %(url)s"
                        "WHERE id_api = %(id)s"
                    )
                    ok, res = db.handler.executeQuery(query, args, False)
                    if not ok:
                        raise RuntimeError(res)
                    updatedEntriesNumber += 1
                else:
                    raise RuntimeError(res)
            else:
                addedEntriesNumber += 1
                ids_categories = []
                for tag in product.categories_tags:
                    ok, id_ = categories.handler.getCategoryID(tag)
                    ids_categories.append(id_)
            if res:
                if res[0]:
                    i += 1
                else:
                    raise RuntimeError(res[-1])
        db.handler.commit()
        return addedEntriesNumber, updatedEntriesNumber

    def terminate(self):
        """Free ressources"""
        pass


#: The singleton Products handler instance.
handler: Optional[Products] = None


def initialize():
    global handler
    handler = Products()


def terminate():
    global handler
    if handler:
        handler.terminate()
        handler = None


if __name__ == "__main__":
    products = Products()
    res = products.retrieveFromAPI()
    writeInFile(res, "out_products.txt")
    print("Done")
