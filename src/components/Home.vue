<template>
  <div>
    <SideNavigationDrawer />
    <router-view></router-view>
  </div>
</template>
<script>
import UserInfoStore from "../app/user-info-store";
import getCredentials from "../getCred.js";

import SideNavigationDrawer from "@/components/SideNavigationDrawer.vue";

export default {
  name: "HomePage",
  components: {
    SideNavigationDrawer,
  },
  data: function () {
    return {
      userInfo: UserInfoStore.state.cognitoInfo,
    };
  },
  created: function () {
    getCredentials.getCredentials().then(function (credentials) {
      console.log("credentials from created: ", credentials);
    });
  },
};
</script>
<style></style>
