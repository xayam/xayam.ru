
function init_layouts() {
    vlayout = {
        "first_book.style.position": "absolute",
        "second_book.style.position": "absolute",
        "first_book.style.width": "100%",
        "second_book.style.width": "100%",
        "first_book.style.height": "calc(50% - 30px)",
        "second_book.style.height": "calc(50% - 30px)",
        "second_book.style.top": "calc(50% - 30px)",
        "second_book.style.left": "0",
        "second_book.style.borderLeftWidth": "0",
        "second_book.style.borderTop": "1px solid gray",
        "link_catalog.style.position": "absolute",
        "link_reader.style.position": "absolute",
        "link_reader.style.left": "50%",
        "link_catalog.style.width": "50%",
        "link_reader.style.width": "50%",
        "link_catalog.style.height": "100%",
        "link_reader.style.height": "100%",
        "links.style.width": "100%",
        "links.style.height": "100px",
        "tabs.style.left": "0",
        "tabs.style.top": "100px",
        "tabs.style.width": "100%",
        "tabs.style.height": "calc(100% - 100px)",
    }
    for (let key in vlayout) {
        let hfunc = new Function("hlayout['"+ key + "'] = " + key);
        hfunc();
    }
}

function load_layout(layout) {
    for (let key in layout) {
        let vfunc = new Function(key + " = '" + layout[key] + "'");
        vfunc();
    }
}