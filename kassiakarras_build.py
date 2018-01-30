import os
import codecs


def create_index():
    f = codecs.open("templates/index.html", 'r', 'utf-8').read()
    f = f.replace("{REPLACE}", "<p> hi </p>")
    print(f)

    with open("index.html", "w") as new_file:
        new_file.write(f)


create_index()