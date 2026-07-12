import re
import base64

from lxml import etree

mime_types = {
    'png': 'png',
    'jpg': 'jpeg',
    'webp': 'webp'
}

tasks = [
    {
        "base": "../docs/",
        "xml": "../docs/index.xml",
        "xsl": "../docs/x/index.xsl",
        "html": "../docs/index.html"
    },
    {
        "base": "../docs/x/xmap/author/playground-games/",
        "xml": "../docs/x/xmap/author/playground-games/ru-book.xml",
        "xsl": "../docs/x/xmap/author/playground-games/ru-book.xsl",
        "html": "../docs/x/xmap/author/playground-games/ru-book.html"
    },
    {
        "base": "../docs/x/xmap/author/playground-games/",
        "xml": "../docs/x/xmap/author/playground-games/ru-book.fb2.xml",
        "xsl": "../docs/x/xmap/author/playground-games/ru-book.xsl",
        "html": "../docs/x/xmap/author/playground-games/ru-book.fb2.html"
    },
    {
        "base": "../docs/x/xmap/author/playground-games/",
        "xml": "../docs/x/xmap/author/playground-games/ru-book.pdf.xml",
        "xsl": "../docs/x/xmap/author/playground-games/ru-book.xsl",
        "html": "../docs/x/xmap/author/playground-games/ru-book.pdf.html"
    },
]

string_replacers = [

    {
        "from": '<?xml version="1.0"?>',
        "to": "<!DOCTYPE html>",
    },
    {
        "from": "x/xmap/author/playground-games/ru-book.xml",
        "to": "x/xmap/author/playground-games/ru-book.html",
    }
]

file_replacers = [
    {
        "template": "//{{{DEFAULT_CSS}}}",
        "file": "../docs/x/xmap/author/playground-games/xbook.xgame/resources/default.css",
    },
    {
        "template": "//{{{STYLE_CSS}}}",
        "file": "../docs/x/xmap/author/playground-games/xbook.xgame/resources/style.css",
    },
    {
        "template": "//{{{PAGED}}}",
        "file": "../docs/x/xmap/author/playground-games/xbook.xgame/resources/paged.polyfill.js",
    },
]

for i in range(len(tasks)):
    xml_doc = etree.parse(tasks[i]["xml"])
    xsl_doc = etree.parse(tasks[i]["xsl"])
    transform = etree.XSLT(xsl_doc)
    tasks[i]["output"] = str(transform(xml_doc))
    images = re.findall(r"src=\"(.+?)\.(png|jpg|webp)\"", tasks[i]["output"])
    images = [
        {
            "orig": j[0] + "." + j[1],
            "path": tasks[i]["base"] + j[0] + "." + j[1],
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
        tasks[i]["output"] = tasks[i]["output"].replace(
            f"src=\"{image['orig']}\"", f"src=\"{src}\"")
        # print(f"src=\"{image['orig']}\"")
        # print(tasks[i]["output"])
        # sys.exit()

    for r in string_replacers:
        tasks[i]["output"] = tasks[i]["output"].replace(r["from"], r["to"])
    for r in file_replacers:
        with open(r["file"], "r", encoding="utf-8") as f:
            r_file = f.read()
        tasks[i]["output"] = tasks[i]["output"].replace(r["template"], r_file)
    with open(tasks[i]["html"], "w", encoding="utf-8") as f:
        f.write(tasks[i]["output"])
    print(f"✅ HTML успешно создан: {tasks[i]['html']}")
