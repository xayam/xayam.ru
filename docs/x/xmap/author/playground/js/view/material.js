
class Materials {

    constructor() {
       this.material = {}
       this.material.lightField = null;
       this.material.darkField = null;
    }

    initMaterial() {
       this.material.lightField = new MeshBasicMaterial({color: this.lightColor});
       this.material.darkField = new MeshBasicMaterial({color: this.darkColor});

       this.material.lightEdge = new LineBasicMaterial({color: this.lightColor});
       this.material.darkEdge = new LineBasicMaterial({color: this.darkColor});
    }

}
