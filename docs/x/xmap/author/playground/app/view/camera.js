
class Cameras extends Figure {

    constructor(){
        super();
        this.camera = null;
    }

    initCamera() {
        this.camera = new THREE.PerspectiveCamera(
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

}
