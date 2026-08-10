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
        this.left_div = null;
        this.board_div = null;
        this.select_game = null;
    }

    initConfig() {
        this.left_div = document.getElementsByClassName("left")[0];
        this.board_div = document.getElementsByClassName("board")[0];
        this.select_game = document.querySelector('#select_game');
        this.select_game.addEventListener('change',
        () => {
            document.querySelectorAll('.rules_game').forEach(
                block => {
                    block.classList.remove('active');
                }
            );
            const target = document.getElementById("rules_" + this.select_game.value);
            if (target) {
                target.classList.add('active');
                window.location.href = "#" + this.select_game.value;
            }
        });
        this.initLayouts();
    }

    initLayouts() {
        this.vertical_layout["this.left_div.style.width"] = "100%";
        this.vertical_layout["this.left_div.style.height"] = "25%";
        this.vertical_layout["this.board_div.style.width"] = "100%";
        this.vertical_layout["this.board_div.style.height"] = "75%";
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
}
