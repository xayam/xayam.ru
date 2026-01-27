
function resize_window(_) {
    if (window.innerWidth > window.innerHeight) {
        load_layout(hlayout);
    } else {
        load_layout(vlayout);
    }
}
