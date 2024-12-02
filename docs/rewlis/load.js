window.addEventListener("load", function () {
    init();
    player.addEventListener('play', function (e) {
        play_player(e);
    });
    player.addEventListener('pause', function (e) {
        pause_player(e);
    });
    player.addEventListener('stop', function (e) {
        stop_player(e);
    });
    player.addEventListener('seeked', function (e) {
        seeked_player(e);
    });
    player.addEventListener('seeking', function (e) {
        seeking_player(e);
    });
    first_book.addEventListener('click', function (e) {
        click_first_book(e);
    });
    second_book.addEventListener('click', function (e) {
        click_second_book(e);
    });
    link_catalog.addEventListener('click', function (e) {
        click_catalog(e);
    });
    link_reader.addEventListener('click', function (e) {
        click_reader(e);
    });
    window.addEventListener('resize', function (e) {
        resize_window(e);
    });
    init_layouts();
    resize_window(null);
    getList();
    link_catalog.click();
});
