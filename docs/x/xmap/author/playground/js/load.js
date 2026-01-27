
window.addEventListener("load", function () {
    init();
    init_layouts();
    window.addEventListener('resize', function (e) {
        resize_window(e);
    });
    resize_window(null);
    update_state();
});
