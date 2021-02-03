import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ant from "./utils/ant";
import "./assets/less/common.less";

createApp(App)
  .use(router)
  .use(store)
  .use(ant)
  .mount("#app");
