
class Board extends Geometry {

    constructor() {
        super();
        this.board = null;
        this.fields = [];
        this.wireframes = [];
    }

    initBoard() {
        this.board = new Group();
        for (let row = 0; row < this.size; row++) {
            this.fields.push([]);
            this.wireframes.push([]);
            for (let col = 0; col < this.size; col++) {
                const isLight = (row + col) % 2 === 0;
                const x = (col - 3.5) * this.cellSize;
                const z = (row - 3.5) * this.cellSize;
                const y = this.height / 2;

                const geometry = this.geometry.field
                const material = isLight ? this.material.lightField : this.material.darkField
                const field = new Mesh(geometry, material);
                field.position.set(x, y, z);

                const edge = this.geometry.edge;
                const edgeMaterial = isLight ? this.material.darkEdge : this.material.lightEdge;
                const wireframe = new LineSegments(edge, edgeMaterial);
                wireframe.position.set(x, y, z);

                this.fields[row].push(field);
                this.wireframes[row].push(wireframe);
                this.board.add(field);
                this.board.add(wireframe);
            }
        }
        this.board.position.set(0, 0, 0);
    }

}
