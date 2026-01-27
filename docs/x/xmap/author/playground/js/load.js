window.addEventListener("load", function () {
    init();



    window.addEventListener('resize', function (e) {
        resize_window(e);
    });
    init_layouts();
    resize_window(null);
});
