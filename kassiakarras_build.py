import os
import codecs
import json

products = []


def create_index():
    f = codecs.open("templates/index.html", 'r', 'utf-8').read()
    f = f.replace("{REPLACE}", "<p> hi </p>")

    print(f)

    with open("index.html", "w") as new_file:
        new_file.write(f)


def create_product_page():
    with open("templates/product.html", "r") as html_file:
        print(html_file.read())


def process_product_json():
    with open("products/products.json", "r", encoding="utf-8") as json_file:

        data = json.load(json_file)

        for i in range(0, len(data)):
            products.append(Product(
                data[i]['name'],
                data[i]['price'],
                data[i]['image'],
            ))


class Product:

    def __init__(self, name, price, image):
        self.name = name
        self.price = price
        self.image = image


process_product_json()
