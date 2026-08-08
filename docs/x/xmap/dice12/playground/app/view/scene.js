
class Scenes extends Cameras {

    constructor(){
        super();
        this.scene = null;
    }

    initScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(this.backgroundColor);
        this.scene.add(this.board);
        for (let figure in this.figures) {
            this.scene.add(figure);
        }
    }

}
