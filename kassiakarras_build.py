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

    last = (len(product_list) - 1)

    add_to_html = ""

    stage = 0

    for i in range(0, len(product_list)):

        if stage % 3 == 0:
            add_to_html += "<div class=\"set_of_three\">"

        add_to_html += "<div class=\"index_product\">"
        add_to_html += "<a class=\"post_link\" href=\"" + product_list[i].link + "\">" + \
                       product_list[i].name + "</a>"
        add_to_html += "<img src=\"" + product_list[i].image + "\">"
        add_to_html += "<p>" + product_list[i].type + ". " + str(product_list[i].price) + "</p>"

        add_to_html += "</div>"

        stage += 1

        if (stage == 3) | (i == last):
            add_to_html += "</div>"
            stage = 0

        #if i == last:
         #   add_to_html += "</div>"

    f = f.replace("{PRODUCTS}", add_to_html)

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
                "NULL"
            ))
    return products


def create_product_pages(product_list):
    for i in range(0, len(product_list)):

        name = product_list[i].name.strip()
        name = name.lower()

        path = PRODUCT_DIR + "/" + name + ".html"

        rel_path = path.split(".io/", 1)[1]

        product_list[i].set_link(rel_path)

        if os.path.exists(path):
            os.remove(path)

        with open("templates/product.html", "r") as template_file:
            template_text = template_file.read()

        add_to_html = ""
        add_to_html += "<div>"
        add_to_html += "<p>Product name: " + product_list[i].name + "</p>"
        add_to_html += "<img class=\"product_image\" src=\"" + product_list[i].image + "\">"
        add_to_html += "<p>Price: " + str(product_list[i].price) + "</p>"

        template_text = template_text.replace("{PRODUCTS}", add_to_html)

        with open(path, "w") as new_file:
            new_file.write(template_text)


def reset_product_dir():
    if os.path.exists("products/"):
        shutil.rmtree("products")
        os.makedirs("products")


class Product:

    def __init__(self, name, type, price, image, link):
        self.name = name
        self.type = type
        self.price = price
        self.image = image
        self.link = link

    def set_link(self, link):
        self.link = link


reset_product_dir()

process_product_json()

create_product_pages(products)

create_index(products)

print("--- %s seconds ---" % (time.time() - start_time))
