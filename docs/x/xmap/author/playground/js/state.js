
class State {

    constructor(canvas) {
        this.size = 8;
        this.cellSize = 10;
        this.height = 2;
        this.halfBoard = this.size * this.cellSize / 2;
        this.lightColor = 0xdddddd;
        this.darkColor  = 0x666666;
        this.backgroundColor = 0xffffff;

        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.boardGroup= null;
        this.board3d= {};
        this.canvas = canvas;

        this.init()
    }

    update_state() {
        if (this.camera && this.renderer) {
            this.camera.aspect = this.canvas.clientWidth / this.canvas.clientHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        }
    }

    init_scene() {
        this.scene = new Scene();
        this.scene.background = new Color(this.backgroundColor);
    }

    init_camera() {
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

    init_state() {
        this.boardGroup = new Group();
        this.scene.add(this.boardGroup);
        const geometry = new BoxGeometry(this.cellSize, this.height, this.cellSize);
        for (let row = 0; row < this.size; row++) {
            for (let col = 0; col < this.size; col++) {
                const isLight = (row + col) % 2 === 0;
                const color = isLight ? this.lightColor : this.darkColor;
                const x = (col - 3.5) * this.cellSize;
                const z = (row - 3.5) * this.cellSize;
                const y = this.height / 2;
                const material = new MeshBasicMaterial({ color: color });
                const field = new Mesh(geometry, material);
                field.position.set(x, y, z);
                this.board3d['field:' + col + ':' + row] = field;
                this.boardGroup.add(field);
                const colorEdge = isLight ? this.darkColor : this.lightColor;
                const edges = new EdgesGeometry(geometry, 15);
                const edgeMat = new LineBasicMaterial({color: colorEdge});
                const wireframe = new LineSegments(edges, edgeMat);
                wireframe.position.set(x, y, z);
                this.board3d['wireframe:' + col + ':' + row] = wireframe;
                this.boardGroup.add(wireframe);
            }
        }
        this.boardGroup.position.set(0, 0, 0);
        this.renderer = new WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.canvas.clientWidth, this.canvas.clientHeight);
        this.canvas.appendChild(this.renderer.domElement);
    }

    init() {
        this.init_scene();
        this.init_camera();
        this.init_state();
    }
}

function animate() {
    requestAnimationFrame(animate);
    state.boardGroup.rotation.y += 0.005;
    state.renderer.render(state.scene, state.camera);
}
