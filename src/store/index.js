import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    currentUser: {},
  },
  mutations: {
    setcurrentUser(state, payload) {
      state.currentUser = payload;
    },
  },
  actions: {
    async setcurrentUser(state, payload) {
      state.commit("currentUser", payload);
    },
  },

  modules: {},
  getters: {
    gettercurrentUser: (state) => state.currentUser,
  },
});
