let config = null;

window.addEventListener("load", function () {
    config = new Config();

    window.addEventListener('resize', function (e) {
        config.resize_window(e);
    });

    config.resize_window(null);

    state.update_state();
    animate();
});
