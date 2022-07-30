<template>
  <div>
    <v-app-bar flat>
      <v-app-bar-title class="font-weight-bold text-h4 ma-2 Apptitle">
        Ensemble
      </v-app-bar-title>
    </v-app-bar>
    <!-- <div class="ma-2 font-weight-medium text-h5">Hello, {{ userName }} !</div> -->
  </div>
</template>
<script>
import UserInfoStore from "../app/user-info-store";

export default {
  name: "AppTitle",
  data() {
    return {
      userInfo: UserInfoStore.state.cognitoInfo,
    };
  },
  computed: {
    userName: {
      get() {
        return (
          this.userInfo.username[0].toUpperCase() +
          this.userInfo.username.slice(1)
        );
      },
    },
  },
};
</script>
<style>
Apptitle {
  color: #262d4c !important;
}
</style>
