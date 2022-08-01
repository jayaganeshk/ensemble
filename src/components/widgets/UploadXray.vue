<template>
  <div>
    <div class="font-weight-medium text-h6 ma-2">Diagnostics</div>
    <v-row class="ma-2">
      <v-col cols="12" sm="6"> </v-col>
      <v-col cols="12" sm="6">
        <v-row>
          <v-col cols="12" sm="8">
            <v-file-input
              v-model="files"
              color="#262D4C"
              counter
              dense
              label="Upload new XRay"
              multiple
              placeholder="Select your files"
              prepend-icon="mdi-paperclip"
              outlined
              :show-size="1000"
            >
              <template v-slot:selection="{ index, text }">
                <v-chip v-if="index < 2" color="#262D4C" dark label small>
                  {{ text }}
                </v-chip>

                <span
                  v-else-if="index === 2"
                  class="text-overline grey--text text--darken-3 mx-2"
                >
                  +{{ files.length - 2 }} File(s)
                </span>
              </template>
            </v-file-input>
          </v-col>
          <v-col>
            <v-btn
              color="#262D4C"
              class="white--text"
              @click="onUpload"
              :disabled="files.length == 0"
              :loading="isLoading"
            >
              Upload
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-row class="ma-2" justify="center" v-if="showDialog">
      <v-alert outlined type="success" text v-if="resultCode == 0">
        {{ apiResult }}
      </v-alert>
      <v-alert outlined type="error" text v-if="resultCode == 1">
        {{ apiResult }}
      </v-alert>
    </v-row>
    <v-row class="ma-2">
      <v-data-table
        :headers="headers"
        :items="XRayHistory"
        :items-per-page="10"
        :loading="XRayLoading"
        loading-text="Loading... Please wait"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
      >
        <template v-slot:[`item.actions`]="{ item }">
          <v-icon medium class="mr-2" @click="editItem(item)">
            mdi-open-in-new
          </v-icon>
        </template>
      </v-data-table>
    </v-row>
  </div>
</template>

<script>
import getCredentials from "@/getCred";
const AWS = require("aws-sdk");
var moment = require("moment");
import UserInfoAPI from "@/app/user-info-api";
import axios from "axios";

export default {
  name: "UploadXray",
  props: ["uploadDetailsProp"],
  data: () => ({
    files: [],
    isLoading: false,
    XRayHistory: [],
    sortBy: "id",
    sortDesc: true,
    headers: [
      {
        text: "ID",
        align: "start",
        value: "id",
      },
      { text: "File Name", value: "pneumonia_action" },
      { text: "Result", value: "result" },
      { text: "Date", value: "created_on" },
    ],
    showDialog: false,
    apiResult: "",
    resultCode: 0,
    XRayLoading: false,
  }),
  methods: {
    async onUpload() {
      console.log("this.files ", this.files);
      this.isLoading = true;

      let postBody = await this.uploadtoS3();

      let IDToken = UserInfoAPI.getIDToken();

      const headers = {
        "Content-Type": "application/json",
        Authorization: IDToken,
      };
      const apiURL = process.env.VUE_APP_API_URL + "/pneumoniaaction ";
      console.log("apiURL ", apiURL);
      axios
        .post(apiURL, postBody, {
          headers: headers,
        })
        .then((response) => {
          console.log("API Response :", response);
          this.apiResult = response.data.Inference;
          this.resultCode = response.data.Result;
          this.showDialog = true;
          console.log("result :", this.apiResult);
          console.log("showDialog :", this.showDialog);
          this.isLoading = false;
          this.files = [];
          this.getXrayHistory();
        })
        .catch((error) => {
          console.error("Error ", error);
          this.isLoading = false;
        });
    },
    getXrayHistory() {
      this.XRayLoading = true;
      let IDToken = UserInfoAPI.getIDToken();
      const headers = {
        "Content-Type": "application/json",
        Authorization: IDToken,
      };
      const apiURL =
        process.env.VUE_APP_API_URL + "/xrayhistory?id=" + this.details.id;
      console.log("apiURL ", apiURL);
      axios
        .get(apiURL, {
          headers: headers,
        })
        .then((response) => {
          console.log("API Response :", response);
          this.XRayHistory = response.data;
          this.XRayLoading = false;
        })
        .catch((error) => {
          console.error("Error ", error);
          this.XRayLoading = false;
        });
    },
    async uploadtoS3() {
      let file = this.files[0];
      let de = this.details;

      let credentials = await getCredentials.getCredentials();
      console.log("credentials from upload: ", credentials);

      const s3 = new AWS.S3({
        accessKeyId: credentials.key,
        secretAccessKey: credentials.secretkey,
      });

      var datetime = moment().format("YYYY-MM-DDThh:mm:ss.ms");

      var options = { partSize: 10 * 1024 * 1024, queueSize: 1 };
      var params = {
        Bucket: "ab-sagemaker-bucket",
        Key:
          "chest_xray/patients/" +
          de.user_name +
          "_" +
          de.id +
          "/" +
          datetime +
          "/" +
          file.name,
        Body: file,
      };

      return new Promise((resolve, reject) => {
        s3.upload(params, options, function (err, data) {
          if (err) {
            console.log(err);
            reject(err);
          } else {
            console.log("Data :", data);

            let postBody = {};
            postBody["URI"] = "s3://ab-sagemaker-bucket/" + data.Key;
            postBody["ID"] = de.id;
            resolve(postBody);
          }
        });
      });
    },
  },
  computed: {
    details: {
      get() {
        return this.uploadDetailsProp;
      },
    },
  },
  created: function () {
    this.getXrayHistory();
  },
};
</script>
