import "bootstrap/dist/css/bootstrap.min.css";
import "../assets/main.css";

import { createApp } from "vue";
import { createBootstrap } from "bootstrap-vue-next";
import App from "../App.vue";
import router from "../router";

const app = createApp(App);
const bootstrap = createBootstrap();

app.use(router);
app.use(bootstrap);
app.mount("#app");
