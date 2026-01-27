let camera = null;
let renderer = null;
//let three = three_module();

function resize_window(_) {
    if (window.innerWidth > window.innerHeight) {
        load_layout(hlayout);
    } else {
        load_layout(vlayout);
    }
    if (camera && renderer) {
        camera.aspect = board_center.innerWidth / board_center.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(board_center.innerWidth, board_center.innerHeight);
    }
}

function update_state() {
    // === Сцена
    const scene = new Scene();
    scene.background = new Color(0xffffff);

    // === Камера (перспективная)
    const camera = new PerspectiveCamera(
        50,
        board_center.innerWidth / board_center.innerHeight,
        0.1, 1000
    );
    camera.position.set(150, 150, 200); // ваша (x, y, z)
    camera.lookAt(50, 50, 5);           // центр объекта

    // === Рендерер
    const renderer = new WebGLRenderer({ antialias: true });
    renderer.setSize(board_center.innerWidth, board_center.innerHeight);
    board_center.appendChild(renderer.domElement);

    // === Параллелепипед 100×100×10
    const geometry = new BoxGeometry(100, 100, 10);
    const edges = new EdgesGeometry(geometry, 15); // только рёбра
    const material = new LineBasicMaterial({ color: 0x000000 });
    const wireframe = new LineSegments(edges, material);
    scene.add(wireframe);

    // === Анимация (опционально)
    function animate() {
        requestAnimationFrame(animate);
        wireframe.rotation.y += 0.005; // вращение
        renderer.render(scene, camera);
    }
    animate();
}
