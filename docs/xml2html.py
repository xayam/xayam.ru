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
    {
        "xml": "x/xmap/author/playground-games/ru-book.fb2.xml",
        "xsl": "x/xmap/author/playground-games/ru-book.xsl",
        "html": "x/xmap/author/playground-games/ru-book.fb2.html"
    },
    {
        "xml": "x/xmap/author/playground-games/ru-book.pdf.xml",
        "xsl": "x/xmap/author/playground-games/ru-book.xsl",
        "html": "x/xmap/author/playground-games/ru-book.pdf.html"
    },
]

simple_replacers = [
    {
        "from": "x/xmap/author/playground-games/ru-book.xml",
        "to": "x/xmap/author/playground-games/ru-book.html",
    }
]

file_replacers = [
    {
        "template": "//{{{DEFAULT_CSS}}}",
        "file": "x/xmap/author/playground-games/xbook.xgame/resources/default.css",
    },
    {
        "template": "//{{{STYLE_CSS}}}",
        "file": "x/xmap/author/playground-games/xbook.xgame/resources/style.css",
    },
    {
        "template": "//{{{PAGED}}}",
        "file": "x/xmap/author/playground-games/xbook.xgame/resources/paged.polyfill.js",
    },
]

for i in range(len(tasks)):
    xml_doc = etree.parse(tasks[i]["xml"])
    xsl_doc = etree.parse(tasks[i]["xsl"])
    transform = etree.XSLT(xsl_doc)
    tasks[i]["output"] = str(transform(xml_doc))
    for r in simple_replacers:
        tasks[i]["output"] = tasks[i]["output"].replace(r["from"], r["to"])
    for r in file_replacers:
        with open(r["file"], "r", encoding="utf-8") as f:
            r_file = f.read()
        tasks[i]["output"] = tasks[i]["output"].replace(r["template"], r_file)
    with open(tasks[i]["html"], "w", encoding="utf-8") as f:
        f.write(tasks[i]["output"])
    print(f"✅ HTML успешно создан: {tasks[i]['html']}")
