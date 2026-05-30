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

replacers = [
    {
        "from": "x/xmap/author/playground-games/ru-book.xml",
        "to": "x/xmap/author/playground-games/ru-book.html",
    }
]

for i in range(len(tasks)):
    xml_doc = etree.parse(tasks[i]["xml"])
    xsl_doc = etree.parse(tasks[i]["xsl"])
    transform = etree.XSLT(xsl_doc)
    tasks[i]["output"] = str(transform(xml_doc))
    for r in replacers:
        tasks[i]["output"] = tasks[i]["output"].replace(r["from"], r["to"])
    with open(tasks[i]["html"], "w", encoding="utf-8") as f:
        f.write(tasks[i]["output"])
    print(f"✅ HTML успешно создан: {tasks[i]['html']}")
