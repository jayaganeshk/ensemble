<template>
  <div>
    <div class="font-weight-medium text-h6 ma-2">X-Ray History</div>
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
  }),
  methods: {
    onUpload() {
      console.log("this.files ", this.files);
      this.isLoading = true;
      let file = this.files[0];
      let de = this.details;
      getCredentials.getCredentials().then(function (credentials) {
        console.log("credentials from upload: ", credentials);
        const s3 = new AWS.S3({
          accessKeyId: credentials.key,
          secretAccessKey: credentials.secretkey,
        });

        var datetime = moment().format("YYYY-MM-DDThh:mm:ss.ms");

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
        var options = { partSize: 10 * 1024 * 1024, queueSize: 1 };
        s3.upload(params, options, function (err, data) {
          if (err) {
            console.log(err);
          } else {
            console.log("Data :", data);

            let postBody = {};
            postBody["URI"] = "s3://ab-sagemaker-bucket/" + data.Key;

            let IDToken = UserInfoAPI.getIDToken();
            // console.log("ID TOken ", IDToken);

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
                this.isLoading = false;
              })
              .catch((error) => {
                console.error("Error ", error);
                this.isLoading = false;
              });
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
};
</script>
