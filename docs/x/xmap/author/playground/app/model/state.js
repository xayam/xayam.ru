
class State extends User {

    constructor(canvas) {
        super();
        this.size = SIZE;
        this.cellSize = CELL_SIZE;
        this.height = HEIGHT;
        this.halfBoard = this.size * this.cellSize / 2;
        this.lightColor = LIGHT_COLOR;
        this.darkColor = DARK_COLOR;
        this.backgroundColor = BACKGROUND_COLOR;
        this.renderer = null;
        this.canvas = canvas;
        this.init();
    }

    update() {
        if (this.camera && this.renderer) {
            this.camera.aspect = this.canvas.clientWidth / this.canvas.clientHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        }
    }

    initState() {
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        this.canvas.appendChild(this.renderer.domElement);
    }

    init() {
        this.initMaterial()
        this.initGeometry();
        this.initBoard();
        this.initFigure();
        this.initCamera();
        this.initScene();
        this.initKeyBoard();
        this.initMouse();
        this.initTouche();
        this.initAction();
        this.initRule();
        this.initGame();
        this.initUser();
        this.initState();
    }
}

function animate() {
    requestAnimationFrame(animate);
    app.state.board.rotation.y += 0.001;
    app.state.renderer.render(app.state.scene, app.state.camera);
}
