
class App extends Config {

    constructor() {
        super();
        this.state = null;
        this.onReSizeFunction = (e) => {
            this.reSizeWindow();
        }
        this.onLoadFunction = () => {
            this.init();
        }
    }

    init() {
        this.initConfig();
        this.state = new State(this.board_center);
        window.addEventListener('resize', this.onReSizeFunction);
        this.fullScreen();
        this.onReSizeFunction(null);
        this.state.update();
        animate();
    }

    run() {
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

    fullScreen() {
//        document.addEventListener('fullscreenchange', () => {
//        if (document.fullscreenElement) {
//            console.log('Переход в полноэкранный режим (через requestFullscreen)');
//        } else {
//            console.log('Выход из полноэкранного режима');
//        }
//        });
//        document.documentElement.requestFullscreen();
    }
}
