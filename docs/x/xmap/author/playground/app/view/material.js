
class Materials {

    constructor() {
       this.material = {}
       this.material.lightField = null;
       this.material.darkField = null;
    }

    initMaterial() {
       this.material.lightField = new THREE.MeshBasicMaterial({color: this.lightColor});
       this.material.darkField = new THREE.MeshBasicMaterial({color: this.darkColor});

       this.material.lightEdge = new THREE.LineBasicMaterial({color: this.lightColor});
       this.material.darkEdge = new THREE.LineBasicMaterial({color: this.darkColor});
    }

}
