

function click_catalog(_) {
    reader.style.display = "none";
    catalog.style.display = "block";
}

function click_reader(_) {
    catalog.style.display = "none";
    reader.style.display = "block";
}

function pause_player(_) {
    clearInterval(first_timer);
    clearInterval(span_timer);
}

function stop_player(_) {
    clearInterval(first_timer);
    clearInterval(span_timer);
}

function seeked_player(_) {
    leftSpan();
}

function seeking_player(_) {

}

function click_first_book(_){
    current_lang = "eng";
    clearInterval(first_timer);
    player.src = "data/eng/" + current_book + "/all.mp3";
    player.currentTime = eng_position;
    player.play();
}

function click_second_book (_) {
    current_lang = "rus";
    clearInterval(first_timer);
    player.src = "data/rus/" + current_book + "/all.mp3";
    player.currentTime = rus_position;
    player.play();
}

function resize_window(_) {
    if (window.innerWidth > window.innerHeight) {
        load_layout(hlayout);
    } else {
        load_layout(vlayout);
    }
}

function play_player(_) {
    first_timer = setInterval(function() {
        let time = parseInt((player.currentTime * 100).toString());
        let lang = "r";
        if (current_lang === "eng")
            lang = "e";
        for (let i = 0; i < 10000; i++) {
            let ela = document.getElementById(
                lang + "a" + (time + i).toString());
            if (ela) {
                ela.scrollIntoView({
                    behavior: 'auto',
                    block: 'center',
                    inline: 'center'
                });

                let content1 = parseInt(ela.innerText)
                if (current_lang === "eng") {
                    eng_selection = ela
                    eng_position = player.currentTime;
                    for (let j = 0; j < rus_sync.length; j++)
                        if (rus_sync[j][4] >= content1) {
                            rus_position = rus_sync[j][0];
                            time = parseInt((rus_position * 100).toString());
                            for (let k = 0; k < 100000000; k++) {
                                let ela = document.getElementById(
                                    "ra" + (time + k).toString());
                                // console.log(ela);
                                if (ela) {
                                    rus_selection = ela
                                    ela.scrollIntoView({
                                        behavior: 'auto',
                                        block: 'center',
                                        inline: 'center'
                                    });
                                    break;
                                }
                            }
                            break;
                        }
                } else {
                    rus_selection = ela
                    rus_position = player.currentTime;
                    for (let i = 0; i < eng_sync.length; i++)
                        if (eng_sync[i][4] >= content1) {
                            eng_position = eng_sync[i][0];
                            time = parseInt((eng_position * 100).toString());
                            for (let k = 0; k < 100000000; k++) {
                                let ela = document.getElementById(
                                    "ea" + (time + k).toString());
                                if (ela) {
                                    eng_selection = ela
                                    ela.scrollIntoView({
                                        behavior: 'auto',
                                        block: 'center',
                                        inline: 'center'
                                    });
                                    break;
                                }
                            }
                            break;
                        }
                }
                setSelection()
                break;
            }
        }
    }, 500);
}
