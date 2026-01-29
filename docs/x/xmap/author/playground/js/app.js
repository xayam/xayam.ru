
window.addEventListener("load", function () {
    config = new Config();

    window.addEventListener('resize', function (e) {
        config.reSizeWindow(e);
    });

    config.reSizeWindow(null);

    state.update();
    animate();
});
