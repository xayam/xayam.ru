
class App extends Config {

    constructor() {
        super();
        this.state = null;
    }

    init() {
        this.initConfig();
        this.state = new State(this.board_center);
        this.onReSizeFunction = (e) => {
            this.reSizeWindow();
        }
        window.addEventListener('resize', this.onReSizeFunction);
        this.reSizeWindow(null);
        this.state.update();
        animate();
    }

    run() {
        this.onLoadFunction = () => {
            this.init();
        }
        window.addEventListener("load", this.onLoadFunction);
    }

    reSizeWindow(e) {
        if (window.innerWidth > window.innerHeight) {
            this.loadLayout(this.horizontal_layout);
        } else {
            this.loadLayout(this.vertical_layout);
        }
        this.state.update();
        setTimeout(this.state.update, 500);
        setTimeout(this.state.update, 1000);
    }
}

