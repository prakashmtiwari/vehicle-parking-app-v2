import { createApp } from "https://unpkg.com/vue@3/dist/vue.esm-browser.js";
import App from "./App.vue";     // root component
import router from "./router.js"; // router config

const app = createApp(App);
app.use(router);
app.mount("#app");
