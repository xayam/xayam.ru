
class Geometry extends Materials {

    constructor() {
        super();
        this.geometry = {};
    }

    initGeometry() {
       this.geometry.field = new THREE.BoxGeometry(
           this.cellSize,
           this.height,
           this.cellSize
       );
       this.geometry.edge = new THREE.EdgesGeometry(this.geometry.field, 15);
    }

}