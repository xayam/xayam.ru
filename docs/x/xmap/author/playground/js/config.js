
let config = null;
let state = null;

const SIZE = 8;
const CELL_SIZE = 10;
const HEIGHT = 2;
const LIGHT_COLOR = 0xdddddd;
const DARK_COLOR = 0x666666;
const BACKGROUND_COLOR = 0xffffff;

class Config {

    constructor() {
        this.vertical_layout = {};
        this.horizontal_layout = {};
        this.left = null;
        this.center = null;
        this.right = null;
        this.board_center = null;

        this.init();
    }

    init() {
        this.left = document.getElementsByClassName("left")[0];
        this.center = document.getElementsByClassName("center")[0];
        this.right = document.getElementsByClassName("right")[0];
        this.board_center = document.getElementsByClassName("board_center")[0];

        this.initLayouts();

        state = new State(this.board_center);
    }

    initLayouts() {
        this.vertical_layout["this.left.style.display"] = "none";
        this.vertical_layout["this.center.style.width"] = "100%";
        this.vertical_layout["this.center.style.height"] = "calc(var(--cell-size) * 11.0 + 24px)";
        this.vertical_layout["this.right.style.width"] = "100%";
        this.vertical_layout["this.right.style.height"] = "calc(var(--cell-size) * 2.0)";

        for (let key in this.vertical_layout) {
            const execute = "this.horizontal_layout['"+ key + "'] = " + key + ';';
            eval(execute);
        }
    }

    loadLayout(layout) {
        for (let key in layout) {
            const execute = key + " = '" + layout[key] + "';";
            eval(execute);
        }
    }

    reSizeWindow(_) {
        if (window.innerWidth > window.innerHeight) {
            this.loadLayout(this.horizontal_layout);
        } else {
            this.loadLayout(this.vertical_layout);
        }
        state.update();
        setTimeout(state.update, 500);
        setTimeout(state.update, 1000);
    }
}
