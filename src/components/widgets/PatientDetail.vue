<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" persistent scrollable>
      <v-card>
        <v-card-title class="text-h5 mb-2" style="background-color: #f1f2f7">
          Details of: {{ details.user_name }}
          <v-spacer></v-spacer>
          <v-icon @click="onClose"> mdi-close </v-icon>
        </v-card-title>

        <v-card-text>
          <v-row class="mt-2">
            <v-container>
              <v-row>
                <v-col
                  cols="12"
                  sm="4"
                  class="pa-1"
                  v-for="key in keys"
                  :key="key"
                >
                  <v-text-field
                    dense
                    outlined
                    v-model="details[key]"
                    :label="key"
                    disabled
                    required
                    v-if="key != 'symptoms'"
                  ></v-text-field>
                  <div v-else>
                    <v-autocomplete
                      v-model="selectedSymptoms"
                      :items="selectedSymptoms"
                      chips
                      label="Symptoms"
                      multiple
                      outlined
                      disabled
                    ></v-autocomplete>
                  </div>
                </v-col>
              </v-row>
            </v-container>
          </v-row>
          <v-divider></v-divider>

          <UploadXray :uploadDetailsProp="details" />
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <!-- <v-btn color="green darken-1" text @click="dialog = false">
            Disagree
          </v-btn> -->

          <v-btn color="green darken-1" text @click="onClose"> Ok </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import UploadXray from "@/components/widgets/UploadXray.vue";
export default {
  name: "PatientDetail",
  props: ["dialogProp", "detailsProp"],
  components: { UploadXray },
  data() {
    return {
      keys: [
        "id",
        "user_name",
        "user_mail",
        "user_phone",
        "symptoms",
        "prognosis",
        "created_on",
        "updated_on",
      ],
    };
  },
  computed: {
    dialog: {
      get() {
        return this.dialogProp;
      },
    },
    details: {
      get() {
        // let detail = this.detailsProp;
        // let symptoms = detail["symptoms"];
        // delete detail.symptoms;
        // detail["detail"] = symptoms;
        return this.detailsProp;
      },
    },
    selectedSymptoms: {
      get() {
        let symptom = this.details["symptoms"].replace(/'/g, '"');
        return JSON.parse(symptom);
      },
    },
  },
  methods: {
    onClose: function (item) {
      this.$emit("onClose", item);
    },
  },
};
</script>
