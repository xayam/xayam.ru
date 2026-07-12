import re
import base64
import json

from lxml import etree

with open("xml2html.json", 'r', encoding='utf-8') as f:
    config = json.load(f)
tasks = config["tasks"]
string_replacers = config["string_replacers"]
file_replacers = config["file_replacers"]
mime_types = config["mime_types"]

for task in tasks:
    xml_doc = etree.parse(task["base"] + task["xml"])
    xsl_doc = etree.parse(task["base"] + task["xsl"])
    transform = etree.XSLT(xsl_doc)
    task["output"] = str(transform(xml_doc))
    images = re.findall(r"src=\"(.+?)\.(png|jpg|webp)\"", task["output"])
    images = [
        {
            "orig": j[0] + "." + j[1],
            "path": task["base"] + j[0] + "." + j[1],
            "ext": j[1]
        } for j in images
    ]
    for image in images:
        with open(image["path"], mode='rb') as f:
            ext = image['ext'].lower()
            mime_type = mime_types.get(ext, ext)
            binary_data = f.read()
            base64_bytes = base64.b64encode(binary_data)
            base64_string = base64_bytes.decode('utf-8')
            src = f"data:image/{mime_type};base64,{base64_string}"
        task["output"] = task["output"].replace(
            f"src=\"{image['orig']}\"", f"src=\"{src}\"")

    for r in string_replacers:
        task["output"] = task["output"].replace(r["from"], r["to"])
    for r in file_replacers:
        with open(r["file"], "r", encoding="utf-8") as f:
            r_file = f.read()
        task["output"] = task["output"].replace(r["template"], r_file)
    with open(task["base"] + task["html"], "w", encoding="utf-8") as f:
        f.write(task["output"])
    print(f"✅ HTML успешно создан: {task['base'] + task['html']}")
