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

COLUMNS = 3


class Product:

    def __init__(self, name, type, price, image, link, id):
        self.name = name
        self.type = type
        self.price = price
        self.image = image
        self.link = link
        self.id = id

    def set_link(self, link):
        self.link = link


def create_product_thumbnails(product_list, subset):
    last = (len(product_list) - 1)

    add_to_html = ""

    stage = 0

    if subset == 0:
        pass
    else:
        product_list = product_list[0:subset]  # Only show first 6 things on home page

    for i in range(0, len(product_list)):

        if stage % COLUMNS == 0:
            add_to_html += "<div class=\"set_of_three\">"

        add_to_html += "<div class=\"index_product\">"
        add_to_html += "<a href=\"" + product_list[i].link + "\"><img src=\"" + product_list[i].image + "\"></a>"
        add_to_html += "<a class=\"post_link\" href=\"" + product_list[i].link + "\">" + \
                       product_list[i].name + "</a>"
        add_to_html += "<p class=\"price_text\">" + "$" + str(product_list[i].price) + "</p>"

        add_to_html += "</div>"

        stage += 1

        if (stage == COLUMNS) | (i == last):
            add_to_html += "</div>"
            stage = 0

    return add_to_html


def create_index(product_list):
    f = codecs.open("templates/index.html", 'r', 'utf-8').read()

    add_to_html = create_product_thumbnails(product_list, 6)

    f = f.replace("{PRODUCTS}", add_to_html)

    with open("index.html", "w") as new_file:
        new_file.write(f)


def create_additional_page(name):
    with open("templates/" + name + ".html", "r") as current_template:
        template_string = current_template.read()

        if os.path.exists(name):
            shutil.rmtree(name)

        os.mkdir(name)

        if name == "shop":
            add_to_html = create_product_thumbnails(products, 0)
        else:
            add_to_html = "<p> test </p>"

        replacements = {
            "TEST": add_to_html
        }

        finished_html = html_replace(template_string, replacements)

        with open(name + "/index.html", "w") as new_html:
            new_html.write(finished_html)


def process_product_json():
    with open("products.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

        for i in range(0, len(data)):

            if data[i]['hosted_button_id'] != "":
                button_id = data[i]['hosted_button_id']
            else:
                button_id = "NULL"

            products.append(Product(
                data[i]['name'],
                data[i]['type'],
                data[i]['price'],
                data[i]['image'],
                "NULL",
                button_id
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

        if product_list[i].id != "NULL":  # Only replaces if there's an ID
            template_text = template_text.replace("{BUTTON_ID}", product_list[i].id)

        if product_list[i].type in has_size:
            template_text = template_text.replace("{TABLE}",
                                                  "<table><tr><td><input type=\"hidden\" name=\"on0\" value=\"Size\">"
                                                  "Size</td></tr><tr><td><select name=\"os0\"><option value=\"Small\">"
                                                  "Small</option><option value=\"Medium\">Medium</option"
                                                  "><option value=\"Large\">Large</option></select> </td></tr></table>")
        else:
            template_text = template_text.replace("{TABLE}", "")

        template_text = template_text.replace("{PRODUCTS}", add_to_html)

        with open(path, "w") as new_file:
            new_file.write(template_text)


def reset_product_dir():
    if os.path.exists("products/"):
        shutil.rmtree("products")
        os.makedirs("products")


def html_replace(original, replace_dict):

    for key, value in replace_dict.items():
        original = original.replace(
            "{" + key + "}",
            str(value)
        )

    return original


has_size = ["shirt"]

extras = ["shop", "lookbook", "portfolio"]

reset_product_dir()

process_product_json()

create_product_pages(products)

create_index(products)

for name in extras:
    create_additional_page(name)

print("--- %s seconds ---" % (time.time() - start_time))
