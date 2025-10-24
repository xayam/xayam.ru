
function get_layer(layer) {
    for (let y = 0; y < 13; y += 1) {
        for (let x = 0; x < 12; x += 1) {
            // if (!((x % 2 === 1 && y % 2 === 1) || (x % 2 === 0 && y % 2 === 0)))
            //     continue;
            if (x % 2 === 1 && y % 2 === 0) continue;
            if (x % 2 === 0 && y % 2 === 1) continue;
            let buffer = layer;
            let xx = "x" + x.toString();
            let yy = "y" + y.toString();
            buffer += "_" + xx + yy;
            if (!state[layer]) state[layer] = {};
            if (!state[layer][xx]) state[layer][xx] = {};
            if (!state[layer][xx][yy]) state[layer][xx][yy] = {};
            state[layer][xx][yy].x = xx;
            state[layer][xx][yy].y = yy;
            state[layer][xx][yy]["element"] = document.getElementById(buffer);
            if (state[layer][xx][yy]["element"])
                state[layer][xx][yy]["content"] =
                    state[layer][xx][yy]["element"].innerText;
            state[layer][xx][yy]["layer_class"] = layer;
        }
    }
}

function init_state() {
    state = {};
    get_layer(L_FIELD);
    get_layer(L_WHITE);
    get_layer(L_BLACK);
    console.log(state);
}

function possible_move() {
    if (phase !== 3) return false;
    if (!from_move || !to_move) return false;
    let layers = [to_move["my_layer"], to_move["op_layer"]];
    to_move["orig"] = to_move["element"].innerText;
    // if (turn === L_BLACK) {
    //     console.log(to_move["my_layer"]);
    //     to_move["element"] =
    //         state[to_move["my_layer"]][to_move.x][to_move.y]["element"];
    // }
    console.log(to_move);
    // console.log("-------------");
    // console.log(state[layer][to_move.x][to_move.y]);
    // console.log("'" + state[layer][to_move.x][to_move.y].content + "'");
    // console.log("-------------");
    let b = state[to_move["layer_class"]][to_move.x][to_move.y]["element"].innerText;
    if (b === "1" || b === "2" || b === "3" || b === "4" || b === "5" || b === "6")
        return true;
    for (let i = 0; i < layers.length; i++)
        if (state[layers[i]][to_move.x][to_move.y].content !== "")
            return false;
    return true;
}

function update_state(new_value) {
    to_move["element"].innerText = new_value.toString();
    to_move["content"] = to_move["element"].innerText;
    alert(to_move["op_layer"])
    state[to_move["op_layer"]][to_move.x][to_move.y]["content"] =
        to_move["element"]["content"];

    from_move["element"].innerText = "";
    from_move["content"] = "";

    state[from_move["my_layer"]][from_move.x][from_move.y]["content"] =
        from_move["element"]["content"];

    from_move["element"].style.outline = "0px solid green";
    to_move["element"].style.outline = "0px solid green";
    from_move = {};
    to_move = {};
    phase = 0;
    if (turn === L_BLACK) turn = L_WHITE; else turn = L_BLACK;
}

function self_collision(new_value) {
    let b = state[to_move["layer_class"]][to_move.x][to_move.y]["element"].innerText;
    if (b === "1" || b === "2" || b === "3" || b === "4" || b === "5" || b === "6") {
        new_value += parseInt(to_move["element"].innerText);
        // alert(new_value)
        update_state(new_value);
        return true;
    }
}

function push_move() {
    if (possible_move()) {
        let new_value;
        if (from_move["element"].innerText === "")
            new_value = 0;
        else
            new_value = parseInt(from_move["element"].innerText);
        if (self_collision(new_value)) return;
        if (to_move["orig"] === C_PLUS) {
            new_value += 1;
            if (new_value === 7) new_value = 1;
        } else {
            new_value -= 1;
            if (new_value === 0) new_value = 6;
        }
        update_state(new_value);
    }
    else {
        from_move["element"].style.outline = "0px solid green"
        to_move["element"].style.outline = "0px solid green"
        phase = 0;
    }
}

function update_to_layer(layer_class, self) {
    to_move["my_layer"] = layer_class;
    to_move["op_layer"] = layer_class;
    if (turn === L_WHITE) {
        if (layer_class === L_WHITE) {
            to_move["my_layer"] = L_WHITE;
            to_move["op_layer"] = L_BLACK;
            if (self)
                to_move["op_layer"] = L_WHITE;
        }
    } else {
        if (layer_class === L_BLACK) {
            to_move["my_layer"] = L_BLACK;
            to_move["op_layer"] = L_WHITE;
            if (self)
                to_move["op_layer"] = L_BLACK;
        }
    }
}

function make_move(element, layer_class, c, x, y, self) {
    if (phase === 2) {
        to_move["element"] = element;
        to_move["layer_class"] = layer_class;
        to_move["content"] = to_move["element"].innerText;
        to_move.x = x;
        to_move.y = y;
        to_move["color"] = turn;
        console.log(layer_class)
        update_to_layer(layer_class, self);
        phase = 3;
        push_move();
    }
    return true;
}

function update_from_layer(layer_class) {
    from_move["my_layer"] = layer_class;
    from_move["op_layer"] = layer_class;
    if (turn === L_WHITE) {
        if (layer_class === L_WHITE) {
            from_move["my_layer"] = L_WHITE;
            from_move["op_layer"] = L_BLACK;
        }
    } else {
        if (layer_class === L_BLACK) {
            from_move["my_layer"] = L_BLACK;
            from_move["op_layer"] = L_WHITE;
        }
    }
}

function click_from_cell(lclass, x, y) {
    let result = true;
    let layer_class = L_WHITE;
    console.log(layer_class + x + y);
    let element = state[layer_class][x][y]["element"];
    let c = parseInt(element.innerText);
    if (c > 0 && c < 7) {
        console.log(c + "|" + layer_class + "|" + x + "|" + y);
    } else {
        layer_class = L_BLACK;
        element = state[layer_class][x][y]["element"];
        try {
            c = parseInt(element.innerText);
        } catch (e) {c = -256;}
        if (c > 0) {
            console.log(c + "|" + layer_class + "|" + x + "|" + y);
        } else {
                result = false;
        }
    }
    if (result && phase === 0) {
        if ((turn === L_BLACK && layer_class === L_BLACK) ||
            (turn === L_WHITE && layer_class === L_WHITE)) {
            from_move["element"] = element;
            from_move["layer_class"] = layer_class;
            from_move["content"] = from_move["element"].innerText;
            from_move.x = x;
            from_move.y = y;
            from_move["element"].style.outline = "2px solid " + L_COLOR[turn];
            from_move["color"] = turn;
            update_from_layer(layer_class);
            phase = 1;
        } else {
            alert("Error: code '1001'.")
        }
    } else if (phase === 1) {
        return click_to_cell(lclass, x, y);
    }
}

function click_to_cell(layer_class, x, y) {
    let result = true;
    let self = false;
    let lclass = turn;
    let element = state[lclass][x][y]["element"];
    let c;
    if (element.innerText === "") c = 0;
    else c = parseInt(element.innerText);
    if (c > 0) {
        self = true;
        console.log(c + "|" + lclass + "|" + x + "|" + y);
    } else {
        layer_class = L_FIELD;
        let element = state[layer_class][x][y]["element"];
        let c = element.innerText;
        if (c === C_PLUS || c === C_MINUS) {
            console.log(c + "|" + layer_class + "|" + x + "|" + y);
        } else
            result = false;
    }
    if (result) {
        phase = 2;
        return make_move(element, layer_class, c, x, y, self);
    }
}
