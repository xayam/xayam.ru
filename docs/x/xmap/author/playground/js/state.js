
class State extends Figure {

    constructor(canvas) {
        super();
        this.size = SIZE;
        this.cellSize = CELL_SIZE;
        this.height = HEIGHT;
        this.halfBoard = this.size * this.cellSize / 2;
        this.lightColor = LIGHT_COLOR;
        this.darkColor = DARK_COLOR;
        this.backgroundColor = BACKGROUND_COLOR;

        this.scene = null;
        this.camera = null;
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

    initScene() {
        this.scene = new Scene();
        this.scene.background = new Color(this.backgroundColor);
        this.scene.add(this.board);
    }

    initCamera() {
        this.camera = new PerspectiveCamera(
            50,
            this.canvas.clientWidth / this.canvas.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(- this.size * this.cellSize * 1.41,
                                   this.size * this.cellSize * 1.41, 0
        );
        this.camera.lookAt(0, 0, 0);
    }

    initState() {
        this.renderer = new WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        this.canvas.appendChild(this.renderer.domElement);
    }

    init() {
        this.initMaterial()
        this.initGeometry();
        this.initBoard();
        this.initFigure();
        this.initScene();
        this.initCamera();
        this.initState();
    }
}

function animate() {
    requestAnimationFrame(animate);
    state.board.rotation.y += 0.001;
    state.renderer.render(state.scene, state.camera);
}
