let vlayout = {};
let hlayout = {};
let current_book = null;
let player = null;
let first_book = null;
let second_book = null;
let catalog = null;
let reader = null;
let link_catalog = null;
let link_reader = null;
let links = null;
let tabs = null;

let first_timer = null;
let rus_position = 0;
let eng_position = 0;
let current_lang = "eng";
let rus_selection = null;
let eng_selection = null;
let span_timer = null;
let data_list_key = null;
let data_list_value = null;
let buffer_result = {"resp": {}};
let first_book_insert_sync = null;
let second_book_insert_sync = null;

function init() {
    player = document.getElementById("player");
    first_book = document.getElementById("first_book");
    second_book = document.getElementById("second_book");
    link_catalog = document.getElementById("link_catalog");
    link_reader = document.getElementById("link_reader");
    catalog = document.getElementById("catalog");
    reader = document.getElementById("reader");
    links = document.getElementsByClassName("links")[0];
    tabs = document.getElementsByClassName("tabs")[0];
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// function getElementByXpath(path) {
//     return document.evaluate(path, document, null,
//         XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
// }

let getTEXT = function (url, callback, timeout) {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.timeout = timeout;
    xhr.responseType = 'text';
    xhr.onload = function () {
        let status = xhr.status;
        if (status === 200) {
            callback(null, xhr.response);
        } else {
            callback(status, xhr.response);
        }
    };
    xhr.send();
    return xhr;
};

let getTEXT2 = function (url, callback, _) {
    let xhr = {};
    xhr.timeout = 0;
    xhr.status = 1;
    xhr.readyState = 4;
    xhr.response = "responseData";
    callback(null, xhr.response);
    return xhr;
};

function getList() {
    getTEXT('data/list.json',
        function (err, data) {
            if (err !== null) {
                alert('Something went wrong: ' + err);
            } else {
                let jsonobj = JSON.parse(data.toString())
                data_list_key = jsonobj["key"].reverse();
                data_list_value = jsonobj["value"].reverse();
                let buffer = "";
                let doed = [];
                for (let i = data_list_key.length - 1; i >= 0; i--) {
                    let spl = data_list_key[i].split("/")[2];
                    if (doed.indexOf(spl) === -1)
                        buffer = buffer +
                            "<a onclick='clickCover(" + '"' +
                            spl + '"' +
                            ")' href='#'><img src='data/eng/" +
                            spl + "/cover.jpg' alt='" + spl + "'></a>";
                    doed.push(spl);
                }
                catalog.innerHTML = buffer;
            }
        }, 3000);
}
