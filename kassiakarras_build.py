import os
import codecs
import json
import shutil
import time

start_time = time.time()


DIRECTORY_NAME = os.path.basename(os.path.dirname(os.path.realpath(__file__)))  # Name of current directory
CURRENT_DIR = dir_path = os.path.dirname(os.path.realpath(__file__))  # Full path to current directory

PRODUCT_DIR = CURRENT_DIR + "/products"  # Gets path to blog folder

products = []


def create_index(product_list):
    f = codecs.open("templates/index.html", 'r', 'utf-8').read()

    add_to_html = ""

    for i in range(0, len(product_list)):
        add_to_html += "<div class=\"index_product\">"
        add_to_html += "<a class=\"post_link\" href=\"" + "/" + product_list[i].image + "\">" + \
                       product_list[i].name + "</a>"
        add_to_html += "<img src=\"" + product_list[i].image + "\">"
        add_to_html += "<p>" + product_list[i].type + ". " + str(product_list[i].price) + "</p>"

        if i == (len(product_list) - 1):
            add_to_html += "</div>\n                "

        else:
            add_to_html += "</div><br />\n                "

    f = f.replace("{REPLACE}", add_to_html)

    with open("index.html", "w") as new_file:
        new_file.write(f)


def process_product_json():
    with open("products.json", "r", encoding="utf-8") as json_file:

        data = json.load(json_file)

        for i in range(0, len(data)):
            products.append(Product(
                data[i]['name'],
                data[i]['type'],
                data[i]['price'],
                data[i]['image'],
            ))
    return products


def create_product_pages(product_list):

    for i in range(0, len(product_list)):

        path = PRODUCT_DIR + "/" + product_list[i].name + ".html"

        if os.path.exists(path):
            os.remove(path)

        with open("templates/product.html", "r") as template_file:
            template_text = template_file.read()


        add_to_html = ""

        add_to_html += "<div>"
        add_to_html += "<p>Product name: " + product_list[i].name + "</p>"
        add_to_html += "<img src=\"" + product_list[i].image + "\">"
        add_to_html += "<p>Price: " + str(product_list[i].price) + "</p>"

        template_text = template_text.replace("{PRODUCT}", add_to_html)

        with open(path, "w") as new_file:
            new_file.write(template_text)


def reset_product_dir():
    if os.path.exists("products/"):
        shutil.rmtree("products")
        os.makedirs("products")


class Product:

    def __init__(self, name, type, price, image):
        self.name = name
        self.type = type
        self.price = price
        self.image = image


reset_product_dir()

process_product_json()

create_index(products)

create_product_pages(products)

print("--- %s seconds ---" % (time.time() - start_time))
