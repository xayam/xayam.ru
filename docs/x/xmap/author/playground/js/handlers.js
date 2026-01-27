let camera = null;
let renderer = null;
let state = {};

function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj);
    if (obj instanceof Array) return obj.map(item => deepClone(item));
    if (obj instanceof Object) {
        return Object.keys(obj).reduce((acc, key) => {
            acc[key] = deepClone(obj[key]);
            return acc;
        }, {});
    }
    return obj;
}

function update_state() {
    if (camera && renderer) {
        camera.aspect = board_center.clientWidth / board_center.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(board_center.clientWidth, board_center.clientHeight);
    }
}

function resize_window(_) {
    if (window.innerWidth > window.innerHeight) {
        load_layout(hlayout);
    } else {
        load_layout(vlayout);
    }
    update_state();
    setTimeout(update_state, 500);
    setTimeout(update_state, 1000);
}

function create_state() {
    const scene = new Scene();
    scene.background = new Color(0xffffff);
    camera = new PerspectiveCamera(
        50,
        board_center.clientWidth / board_center.clientHeight,
        0.1,
        1000
    );

    const size = 8;          // 8×8
    const cellSize = 10;     // ширина/глубина клетки
    const height = 2;        // толщина плитки
    const halfBoard = size * cellSize / 2;
    camera.position.set(0, (size + 2) * cellSize * 1.41, 0);
    camera.lookAt(0, 0, 0);
    const lightColor = 0xdddddd; // светлая клетка
    const darkColor  = 0x666666; // тёмная клетка
    const boardGroup = new Group();
    scene.add(boardGroup);
    const geometry = new BoxGeometry(cellSize, height, cellSize);
    const board = {}
    for (let row = 0; row < size; row++) {
        for (let col = 0; col < size; col++) {
            const isLight = (row + col) % 2 === 0;
            const color = isLight ? lightColor : darkColor;
            const x = (col - 3.5) * cellSize;
            const z = (row - 3.5) * cellSize;
            const y = height / 2;

            const material = new MeshBasicMaterial({ color: color });
            const field = new Mesh(geometry, material);
            field.position.set(x, y, z);
            board['field:' + col + ':' + row] = field;
            boardGroup.add(field);
            const colorEdge = isLight ? darkColor : lightColor;
            const edges = new EdgesGeometry(geometry, 15);
            const edgeMat = new LineBasicMaterial({color: colorEdge});
            const wireframe = new LineSegments(edges, edgeMat);
            wireframe.position.set(x, y, z);
            board['wireframe:' + col + ':' + row] = field;
            boardGroup.add(wireframe);
        }
    }
    boardGroup.position.set(0, 0, 0);
    renderer = new WebGLRenderer({ antialias: true });
    renderer.setSize(board_center.clientWidth, board_center.clientHeight);
    board_center.appendChild(renderer.domElement);
    state.boardGroup = boardGroup;
    state.board = board;
//    console.log(state.board)
    update_state();

    function animate() {
        requestAnimationFrame(animate);
        state.boardGroup.rotation.y += 0.005;
        renderer.render(scene, camera);
    }
    animate();
}
