
class Geometry extends Materials {

    constructor() {
        super();
        this.geometry = {};
    }

    initGeometry() {
       this.geometry.field = new BoxGeometry(
           this.cellSize,
           this.height,
           this.cellSize
       );
       this.geometry.edge = new EdgesGeometry(this.geometry.field, 15);
    }

}