
class Figure extends Board {

    constructor() {
        super();
        this.figure = null;
        this.figures = []
    }

    initFigure() {

        let pieces = this.chessboard.position();
        let piecesList = [];

        for (let square in pieces) {
            if (pieces.hasOwnProperty(square)) {
                piecesList.push({
                    square: square,
                    piece: pieces[square],
                    type: pieces[square][1], // 'P', 'R', 'N', 'B', 'Q', 'K'
                    color: pieces[square][0] === 'w' ? 'white' : 'black'
                });
            }
        }
        console.log(piecesList);
        // for (let row = 0; row < this.size; row++) {
        //     for (let col = 0; col < this.size; col++) {
        //         const isLight = (row + col) % 2 === 0;
        //         const x = (col - 3.5) * this.cellSize;
        //         const z = (row - 3.5) * this.cellSize;
        //         const y = this.height / 2;
        //
        //         const geometry = this.geometry.field
        //         const material = isLight ? this.material.lightField : this.material.darkField
        //         const field = new Mesh(geometry, material);
        //         field.position.set(x, y, z);
        //
        //         const edge = this.geometry.edge;
        //         const edgeMaterial = isLight ? this.material.darkEdge : this.material.lightEdge;
        //         const wireframe = new LineSegments(edge, edgeMaterial);
        //         wireframe.position.set(x, y, z);
        //
        //     }
        // }
        // this.board.position.set(0, 0, 0);
    }

}
