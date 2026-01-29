
class Scenes extends Cameras {

    constructor(){
        super();
        this.scene = null;
    }

    initScene() {
        this.scene = new Scene();
        this.scene.background = new Color(this.backgroundColor);
        this.scene.add(this.board);
    }

}
