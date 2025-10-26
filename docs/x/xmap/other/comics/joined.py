import os

output = ""

for name_html in os.listdir("rus"):
    with open("rus/" + name_html, mode="r", encoding="utf-8") as f:
        html = f.read()
    output += html + "\n<br />\n<br />\n<br />\n"
    print(name_html)

with open("output.html", mode="w", encoding="utf-8") as f:
    f.write(output)
