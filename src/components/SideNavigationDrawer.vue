<template>
  <nav>
    <v-navigation-drawer
      app
      clipped
      height="100%"
      v-model="drawer"
      permanent
      :mini-variant.sync="mini"
      color="#262D4C"
    >
      <v-list-item v-if="!mini">
        <v-spacer></v-spacer>
        <v-list-item-action>
          <v-btn icon @click.stop="mini = !mini" dark>
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
      <v-list-item v-if="mini">
        <v-list-item-action>
          <v-btn icon @click.stop="mini = !mini" dark>
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>

      <v-list dense>
        <v-list-item v-for="item in items" :key="item.title" link>
          <v-list-item-icon>
            <v-icon color="white">{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <router-link
              :to="item.route"
              style="text-decoration: none; color: inherit"
            >
              <v-list-item-title class="white--text text-subtitle-2">
                {{ item.title }}
              </v-list-item-title>
            </router-link>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </nav>
</template>
<script>
import UserInfoStore from "../app/user-info-store";

export default {
  name: "SideNavigationDrawer",
  data() {
    return {
      drawer: true,
      items: [
        { title: "Home", icon: "mdi-home", route: "/CreateCase" },
        {
          title: "Patient History",
          icon: "mdi-account-multiple",
          route: "/CaseHistory",
        },
        { title: "Logout", icon: "mdi-logout-variant", route: "/logout" },
      ],
      mini: false,
      userInfo: UserInfoStore.state.cognitoInfo,
    };
  },
  computed: {
    userAvatar: {
      get() {
        return this.userInfo.username[0].toUpperCase();
      },
    },
  },
};
</script>
