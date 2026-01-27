
function init_layouts() {
    vlayout = {
        "left.style.display": "none",
        "center.style.width": "100%",
        "center.style.height": "calc(var(--cell-size) * 11.0 + 24px)",
//        "board_center.style.height": "calc(var(--cell-size) * 11.0)",
        "right.style.width": "100%",
        "right.style.height": "calc(var(--cell-size) * 2.0)",
    }
    for (let key in vlayout) {
        let hfunc = new Function("hlayout['"+ key + "'] = " + key);
        hfunc();
    }
}

function load_layout(layout) {
//    center.style.setProperty(
//        '--cell-size',
//        'calc((max(100%, 100%) - 24px) / 13)'
//    );
//    const value = getComputedStyle(center).getPropertyValue('--cell-size').trim();
//    console.log(value);
    for (let key in layout) {
        let vfunc = new Function(key + " = '" + layout[key] + "'");
        vfunc();
    }
}