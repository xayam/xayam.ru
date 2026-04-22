from lxml import etree

tasks = [
    {
        "xml": "index.xml",
        "xsl": "x/index.xsl",
        "html": "index.html"
    },
    {
        "xml": "x/xmap/author/playground-games/ru-book.xml",
        "xsl": "x/xmap/author/playground-games/ru-book.xsl",
        "html": "x/xmap/author/playground-games/ru-book.html"
    },
]

for i in range(len(tasks)):
    xml_doc = etree.parse(tasks[i]["xml"])
    xsl_doc = etree.parse(tasks[i]["xsl"])
    transform = etree.XSLT(xsl_doc)
    tasks[i]["output"] = str(transform(xml_doc))
    if i == 1:
        file_output = tasks[0]["html"]
        str_replace = tasks[0]["output"]
        from_replace = tasks[1]["xml"]
        to_replace = tasks[1]["html"]
        str_replace = str_replace.replace(from_replace, to_replace)
        with open(file_output, "w", encoding="utf-8") as f:
            f.write(str_replace)
    else:
        with open(tasks[i]["html"], "w", encoding="utf-8") as f:
            f.write(tasks[i]["output"])
    print(f"✅ HTML успешно создан: {tasks[i]['html']}")
