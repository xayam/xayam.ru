
let state = null;

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

        this.init_layouts();

        state = new State(this.board_center);
    }

    init_layouts() {
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

    load_layout(layout) {
        for (let key in layout) {
            const execute = key + " = '" + layout[key] + "';";
            eval(execute);
        }
    }

    resize_window(_) {
        if (window.innerWidth > window.innerHeight) {
            this.load_layout(this.horizontal_layout);
        } else {
            this.load_layout(this.vertical_layout);
        }

        state.update_state();

        setTimeout(state.update_state, 500);
        setTimeout(state.update_state, 1000);
    }

}
