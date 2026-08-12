import re
import base64
import json
import os

from lxml import etree

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(current_dir + "/build.json", 'r', encoding='utf-8') as f:
    config = json.load(f)
tasks = config["tasks"]
string_replaces = config["tasks_string"]
mime_types = config["mime_types"]

for task in tasks:
    task["base"] = current_dir + "/" + task["base"]
    xml_doc = etree.parse(task["base"] + task["xml"])
    xsl_doc = etree.parse(task["base"] + task["xsl"])
    templates = []
    if task["templates"]:
        xml_template = etree.parse(task["base"] + task["templates"])
        root_template = xml_template.getroot()
        templates = [item.text for item in root_template.xpath("//item")]
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

    for r in string_replaces:
        task["output"] = task["output"].replace(r["from"], r["to"])
    for r in templates:
        with open(task["base"] + r, "r", encoding="utf-8") as f:
            r_file = f.read()
        task["output"] = task["output"].replace("{{{" + r + "}}}", r_file)
    with open(task["base"] + task["file"], "w", encoding="utf-8") as f:
        f.write(task["output"])
    print("✅ Файл успешно создан: " + task['base'].replace(current_dir + "/../docs/", "") + task['file'])
