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
        this.games_div = null;
        this.games_label = null;
        this.games_select = null;
        this.menus_div = null;
        this.menus_label = null;
        this.menus_select = null;
        this.rules_div = null;
    }

    initConfig() {
        this.left_div = document.getElementsByClassName("left")[0];
        this.board_div = document.getElementsByClassName("board")[0];
        this.games_div = document.getElementsByClassName("games")[0];
        this.games_label = document.querySelector('.games label');
        this.games_select = document.querySelector('.games select');
        this.menus_div = document.getElementsByClassName("menus")[0];
        this.menus_label = document.querySelector('.menus label');
        this.menus_select = document.querySelector('.menus select');
        this.rules_div = document.querySelector('.rules');
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
        this.vertical_layout["this.left_div.style.height"] = "30%";
        this.vertical_layout["this.left_div.style.borderRightWidth"] = "0";
        this.vertical_layout["this.left_div.style.borderBottom"] = "1px solid gray";
        this.vertical_layout["this.board_div.style.width"] = "100%";
        this.vertical_layout["this.board_div.style.height"] = "70%";
        this.vertical_layout["this.games_div.style.height"] = "10%";
        this.vertical_layout["this.games_div.style.display"] = "flex";
        this.vertical_layout["this.games_div.style.alignItems"] = "center";
        this.vertical_layout["this.games_div.style.gap"] = "8px";
        this.vertical_layout["this.games_label.style.fontSize"] = "80cqb";
        this.vertical_layout["this.games_label.style.whiteSpace"] = "nowrap";
        this.vertical_layout["this.games_label.style.flexShrink"] = "0";
        this.vertical_layout["this.games_select.style.fontSize"] = "80cqb";
        this.vertical_layout["this.games_select.style.flex"] = "1";
        this.vertical_layout["this.menus_div.style.height"] = "10%";
        this.vertical_layout["this.menus_div.style.display"] = "flex";
        this.vertical_layout["this.menus_div.style.alignItems"] = "center";
        this.vertical_layout["this.menus_div.style.gap"] = "8px";
        this.vertical_layout["this.menus_label.style.fontSize"] = "80cqb";
        this.vertical_layout["this.menus_label.style.lineHeight"] = "1";
        this.vertical_layout["this.menus_label.style.whiteSpace"] = "nowrap";
        this.vertical_layout["this.menus_label.style.flexShrink"] = "0";
        this.vertical_layout["this.menus_select.style.fontSize"] = "80cqb";
        this.vertical_layout["this.menus_select.style.lineHeight"] = "1";
        this.vertical_layout["this.menus_select.style.flex"] = "1";
        this.vertical_layout["this.rules_div.style.height"] = "calc(100% - 20%)";

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
