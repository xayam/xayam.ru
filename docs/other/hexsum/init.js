const L_FIELD = "l_field";
const L_WHITE = "l_white";
const L_BLACK = "l_black";

const L_COLOR = {L_WHITE: "red", L_BLACK: "blue"}
const C_PLUS = "⁺";
const C_MINUS = "‾";

let turn = L_WHITE;
let from_move = {};
let to_move = {};
let board = null;
let debug = null;
let state = {};
let phase = 0;

function init() {
    board = document.getElementById("board");
    debug = document.getElementById("debug");

    create_board();
}

function random_plus_minus() {
    return (Math.random()>=0.5)? C_PLUS : C_MINUS;
}

function random_1_6() {
    const list = [1, 2, 3, 4, 5, 6];
    return list[Math.floor(Math.random() * list.length)];
}

function create_board() {
    create_board_layers();
}

 function create_board_layers() {
    for (let y = 0; y < 7; y++) {
        for (let x = 0; x < 6; x++) {
            let l_back =
                "<img id='l_back_x" + (2 * x) + "y" + (2 * y) +
                "' class='l_back' src='hexcell.svg' alt='hexcell' " +
                "style='left:" + (x * 137) + "px;top:" + (y * 80) + "px'" +
                "/>";
            let content = random_plus_minus();
            // if (y === 0 || y === 6) content = "";
            let l_field =
                "<div onclick='click_to_cell(\"x" + (2 * x) +
                "\", \"y" + (2 * y) + "\")'" +
                " id='l_field_x" + (2 * x) + "y" + (2 * y) +
                "' class='l_field' " +
                "style='" +
                "left:" + (x * 137) + "px;top:" + (y * 80) + "px'" +
                ">" + content + "</div>";
            content = random_1_6();
            if (y !== 0) content = "";
            let l_black =
                "<div id='l_black_x" + (2 * x) + "y" + (2 * y) +
                "' class='l_black' " +
                "style='" +
                "left:" + (x * 137) + "px;top:" + (y * 80) + "px'" +
                ">" + content + "</div>";
            content = random_1_6();
            if (y !== 6) content = "";
            l_black += "<div onclick='click_from_cell(" + '"' +
                "l_white" + '"' + ", \"x" +
                (2 * x) + "\", \"y" + (2 * y) + "\")'" +
                " id='l_white_x" + (2 * x) + "y" + (2 * y) +
                "' class='l_white' " +
                "style='" +
                "left:" + (x * 137) + "px;top:" + (y * 80) + "px'" +
                ">" + content + "</div>";
            board.innerHTML += l_back + l_field + l_black;
        }
        for (let x = 0; x < 5; x++) {
            let l_back =
                "<img id='l_back_x" + (2 * x) + "y" + (2 * y) +
                "' class='l_back' src='hexcell.svg' alt='hexcell' " +
                "style='left:" + (68 + x * 137) + "px;top:" + (40 + y * 80) + "px'" +
                "/>";
            if (y === 6) l_back = "";
            let content = random_plus_minus();
            let l_field = "";
            if (y !== 6)
                l_field =
                    "<div onclick='click_to_cell(\"x" +
                    (2 * x + 1) + "\", \"y" + (2 * y + 1) + "\")'" +
                    " id='l_field_x" + (2 * x + 1) + "y" + (2 * y + 1) +
                    "' class='l_field' " +
                    "style='left:" + (68 + x * 137) + "px;top:" + (40 + y * 80) + "px'" +
                    ">" + content + "</div>";
            if (y !== 6)
                l_field +=
                    "<div id='l_black_x" + (2 * x + 1) + "y" + (2 * y + 1) +
                    "' class='l_black' " +
                    "style='left:" + (68 + x * 137) + "px;top:" + (40 + y * 80) + "px'" +
                    "></div>";
            let  l_white =
                "<div onclick='click_from_cell(" + '"' + "l_white42" + '"' + ", \"x" +
                (2 * x + 1) + "\", \"y" + (2 * y + 1) + "\"" + ")'" +
                " id='l_white_x" + (2 * x + 1) + "y" + (2 * y + 1) +
                "' class='l_white' " +
                "style='left:" + (68 + x * 137) + "px;top:" + (40 + y * 80) + "px'" +
                "></div>";
            if (y === 6) l_white = "";
            board.innerHTML += l_back + l_field + l_white;
        }
        board.innerHTML += "<br>";
    }
}
