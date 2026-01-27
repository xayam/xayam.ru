let vlayout = {};
let hlayout = {};
let left = null;
let center = null;
let right = null;
let board_center = null;


function init() {
    left = document.getElementsByClassName("left")[0];
    center = document.getElementsByClassName("center")[0];
    right = document.getElementsByClassName("right")[0];
    board_center = document.getElementsByClassName("board_center")[0];
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}