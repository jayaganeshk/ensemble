<template>
  <div>
    <v-row class="ma-2 pa-2">
      <v-card-title class="font-weight-bold text--h4">
        Patient History
      </v-card-title>
      {{ showItem }}
      <v-spacer></v-spacer>
      <v-col cols="12" sm="4">
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search Patient History"
          single-line
          hide-details
          outlined
          dense
        ></v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-data-table
        :headers="headers"
        :items="patientDetails"
        :items-per-page="10"
        :search="search"
        :loading="isloading"
        loading-text="Loading... Please wait"
      >
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon medium class="mr-2" @click="editItem(item)">
            mdi-open-in-new
          </v-icon>
        </template>
      </v-data-table></v-row
    >
    <PatientDetail
      :dialogProp="showItem"
      :detailsProp="selectedItem"
      v-if="showItem"
      @onClose="onClose"
    />
  </div>
</template>
<script>
import UserInfoAPI from "@/app/user-info-api";
import axios from "axios";

import PatientDetail from "@/components/Pages/PatientDetail.vue";
export default {
  name: "PatientHistoryTable",
  components: { PatientDetail },
  data() {
    return {
      search: "",
      headers: [
        {
          text: "ID",
          align: "start",

          value: "id",
        },
        { text: "Patient's Name", value: "user_name" },
        { text: "Patient's Mail", value: "user_mail" },
        { text: "Patient's Phonenumber", value: "user_phone" },
        { text: "symptoms", value: "symptoms" },
        { text: "Prognosis", value: "prognosis" },
        { text: "Created on", value: "created_on" },
        { text: "Updated on", value: "updated_on" },
        { text: "Actions", value: "actions", sortable: false },
      ],
      patientDetails: [],
      isloading: true,
      selectedItem: {},
      showItem: false,
    };
  },
  methods: {
    editItem(item) {
      console.log("Edit Item :", item);
      this.selectedItem = item;
      this.showItem = true;
    },
    fetchAllPatients() {
      this.isloading = true;
      let IDToken = UserInfoAPI.getIDToken();
      const headers = {
        "Content-Type": "application/json",
        Authorization: IDToken,
      };
      const apiURL = process.env.VUE_APP_API_URL + "/patienthistory";
      console.log("apiURL ", apiURL);
      axios
        .get(apiURL, {
          headers: headers,
        })
        .then((response) => {
          console.log("API Response :", response);
          this.patientDetails = response.data;
          this.isloading = false;
        })
        .catch((error) => {
          console.error("Error ", error);
          this.isloading = false;
        });
    },
    onClose() {
      this.selectedItem = {};
      this.showItem = false;
    },
  },
  created() {
    console.log("Created ");
    this.fetchAllPatients();
  },
};
</script>

<style>
th {
  font-size: 20px;
  background-color: #262d4c;
  color: white !important;
}
/* td {
  background-color: #f1f2f7 !important;
} */
</style>
