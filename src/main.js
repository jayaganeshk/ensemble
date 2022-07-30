import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import store from "./store";

Vue.config.productionTip = false;

Vue.use(vuetify, {
  theme: {
    primary: "#B4C592",
    accent: "#F1F2F7",
    secondary: "#F1F2F7",
    success: "#56617C",
  },
});

// require("../public/main.scss");
new Vue({
  render: (h) => h(App),
  router,
  store,
  vuetify,
}).$mount("#app");
