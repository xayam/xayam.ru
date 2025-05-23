let rus_sync = null;
let eng_sync = null;
let eng2rus = null;
let rus2eng = null;

function leftSpan() {
    first_book.innerHTML = first_book_insert_sync
    second_book.innerHTML = second_book_insert_sync
}

function rightSpan(book, end) {
    let span =
        document.querySelector('#' + book + ' span');
    let textAfterSpan;
    while (span.nextSibling) {
        if (span.contains(end)) break;
        textAfterSpan = span.nextSibling;
        span.appendChild(textAfterSpan);
    }
}

function setSelection() {
    // let root1 = document.getElementById('first_book');
    // let start1 =
    //     root1.getElementsByTagName('a')[0];
    let end1 = eng_selection.firstChild;
    // let root2 = document.getElementById('second_book');
    // let start2 =
    //     root2.getElementsByTagName('a')[0];
    let end2 = rus_selection.firstChild;
    rightSpan('first_book', end1);
    rightSpan('second_book', end2);
}


function insertSync(data, sync, lang) {
    let position = 0
    let s = "<span><a class='a_book_first'>1</a></span>"
    let eng__rus = eng2rus
    if (lang === "r")
        eng__rus = rus2eng
    for (let i = 0; i < sync.length; i++) {
        s += data.substring(position, sync[i][4]);
        let time = parseInt((sync[i][0] * 100).toString());
        let content0 = "";
        let content1 = "";
        for (let key in eng__rus) {
            let value = eng__rus[key];
            if (value[0] > position) {
                content0 = value[0].toString();
                content1 = value[1].toString();
                break;
            }
        }
        s += "<a id='" + lang + "a" + time + "'>" +
            content1 + "</a>";
        position = sync[i][4];
    }
    s += data.substring(position, data.length);
    return s.replace(/\n/g, "<br>");
}

function getResult(url, method, timeout) {
    return getTEXT(url,
        function (err, data) {
            if (err !== null) {
                alert('Something went wrong: ' + err);
            } else {
                buffer_result["resp"][method] = data.toString()
            }
        }, timeout);
}

async function sendRequest(book, method) {
    let try_count_delay =
        [150, 200, 400, 800, 1000, 1500, 2000, 5000, 10000]
    for (let i = 0; i < try_count_delay.length; i++) {
        let xhr = getResult(book, method, try_count_delay[i]);
        await sleep(try_count_delay[i]);
        console.log(book + "|" + method + "|" + try_count_delay[i])
        if (xhr.status === 0)
            continue
        if (xhr.readyState === 4)
            break;
    }
}

async function clickCover0(data) {
    for (let key = 0; key < data_list_key.length; key++) {
        let spl = data_list_key[key].split("/");
        let lang = spl[1];
        let book = spl[2];
        if (book !== data)
            continue;
        let do_break = {}
        do_break[key] = false
        let filename = spl[3];
        if (filename === "sync.json")
            await sendRequest(data_list_key[key], "sync" + lang + 1);
        else if (filename === "eng2rus.json")
            await sendRequest(data_list_key[key], "eng2rus");
        else if (filename === "rus2eng.json")
            await sendRequest(data_list_key[key], "rus2eng");
        else if (filename === "book.txt" && lang === "eng")
            await sendRequest(data_list_key[key], "engbook");
        else if (filename === "book.txt" && lang === "rus")
            await sendRequest(data_list_key[key], "rusbook");
    }
}

async function clickCover(book_folder) {
    current_book = book_folder;
    document.title = book_folder.replaceAll("_", " ")
    buffer_result["resp"] = {}
    clearInterval(span_timer)
    clearInterval(first_timer)
    player.src = "";
    first_book.innerHTML = "Loading book...";
    second_book.innerHTML = "Загрузка книги...";
    eng_sync = null;
    rus_sync = null;
    rus_position = 0;
    eng_position = 0;
    eng2rus = null;
    rus2eng = null;

    link_reader.click();
    await clickCover0(current_book);

    first_book.innerHTML = "Prepare book...";
    second_book.innerHTML = "Подготовка книги...";

    try {
        eng_sync = JSON.parse(buffer_result["resp"]["synceng1"]);
        rus_sync = JSON.parse(buffer_result["resp"]["syncrus1"]);
        eng2rus = JSON.parse(buffer_result["resp"]["eng2rus"]);
        rus2eng = JSON.parse(buffer_result["resp"]["rus2eng"]);
        first_book_insert_sync =
            insertSync(buffer_result["resp"]["engbook"], eng_sync, "e");
        second_book_insert_sync =
            insertSync(buffer_result["resp"]["rusbook"], rus_sync, "r");
        leftSpan()
        player.src = "data/eng/" + current_book + "/all.mp3";
    }
    catch (e) {
        console.log(e)
        first_book.innerHTML = "Error loading book.";
        second_book.innerHTML = "Ошибка при загрузке книги.";
        alert("Ошибка загрузки книги. Попробуйте выбрать книгу в каталоге еще раз.")
    }
}
