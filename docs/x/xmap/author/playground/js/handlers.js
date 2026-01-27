let camera = null;
let renderer = null;

function update() {
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
    update();
    setTimeout(update, 500);
    setTimeout(update, 1000);
}

function update_state() {
    const scene = new Scene();
    scene.background = new Color(0xffffff);

    camera = new PerspectiveCamera(
        50,
        board_center.clientWidth / board_center.clientHeight,
        0.1,
        1000
    );
    camera.position.set(150, 150, 200);
    camera.lookAt(0, 0, 0);

    renderer = new WebGLRenderer({ antialias: true });
    renderer.setSize(board_center.clientWidth, board_center.clientHeight);
    board_center.appendChild(renderer.domElement);

    const geometry = new BoxGeometry(100, 100, 10);
    const edges = new EdgesGeometry(geometry, 15);
    const material = new LineBasicMaterial({ color: 0x000000 });
    const wireframe = new LineSegments(edges, material);
    scene.add(wireframe);

    update();

    function animate() {
        requestAnimationFrame(animate);
        wireframe.rotation.y += 0.01;
        renderer.render(scene, camera);
    }
    animate();
}
