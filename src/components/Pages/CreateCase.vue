<template>
  <div>
    <AppTitle />
    <div>
      <v-card class="ma-2">
        <v-card-title>Create New Case</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-container>
              <v-row v-for="item in items" :key="item.model">
                <v-col cols="12" sm="5" class="pa-1">
                  <v-text-field
                    dense
                    outlined
                    v-model="pateientData[item.model]"
                    :rules="item.rules"
                    :label="item.label"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12" sm="5" class="pa-1">
                  <v-autocomplete
                    v-model="pateientData['symptoms']"
                    :items="symptoms"
                    chips
                    label="Symptoms"
                    multiple
                    outlined
                  ></v-autocomplete>
                </v-col>
              </v-row>
              <v-row>
                <v-btn
                  @click="onSubmit"
                  color="#262D4C"
                  class="white--text"
                  :disabled="isLoading"
                  :loading="isLoading"
                >
                  Create
                </v-btn>
              </v-row>
            </v-container>
          </v-form>
        </v-card-text>
        <v-card-actions> </v-card-actions>
      </v-card>
    </div>
    <v-dialog v-model="showDialog" max-width="290">
      <v-card>
        <v-card-title class="text-h5"> Prediction Completed </v-card-title>

        <v-card-text>
          We have predicted that the patient has {{ predictedDisease }}
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="green darken-1" text @click="dialog = false">
            close
          </v-btn>
          <v-btn color="green darken-1" text @click="dialog = false">
            continue
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import AppTitle from "@/components/AppTitle.vue";
import UserInfoAPI from "@/app/user-info-api";
import axios from "axios";
export default {
  name: "CreateCase",
  components: { AppTitle },
  data: () => ({
    valid: false,
    pateientData: {},
    items: [
      {
        label: "Patient's Name",
        model: "user_name",
        rules: [(v) => !!v || "Name is required"],
      },
      {
        label: "Patient's Phone Number",
        model: "user_phone",
        rules: [(v) => !!v || "Phone Number is required"],
      },
      {
        label: "Email",
        model: "user_mail",
      },
    ],
    autocompleteItems: [
      "itching",
      "skin_rash",
      "nodal_skin_eruptions",
      "continuous_sneezing",
      "shivering",
      "chills",
      "joint_pain",
      "stomach_pain",
      "acidity",
      "ulcers_on_tongue",
      "muscle_wasting",
      "vomiting",
      "burning_micturition",
      "spotting_urination",
      "fatigue",
      "weight_gain",
      "anxiety",
      "cold_hands_and_feets",
      "mood_swings",
      "weight_loss",
      "restlessness",
      "lethargy",
      "patches_in_throat",
      "irregular_sugar_level",
      "cough",
      "high_fever",
      "sunken_eyes",
      "breathlessness",
      "sweating",
      "dehydration",
      "indigestion",
      "headache",
      "yellowish_skin",
      "dark_urine",
      "nausea",
      "loss_of_appetite",
      "pain_behind_the_eyes",
      "back_pain",
      "constipation",
      "abdominal_pain",
      "diarrhoea",
      "mild_fever",
      "yellow_urine",
      "yellowing_of_eyes",
      "acute_liver_failure",
      "fluid_overload",
      "swelling_of_stomach",
      "swelled_lymph_nodes",
      "malaise",
      "blurred_and_distorted_vision",
      "phlegm",
      "throat_irritation",
      "redness_of_eyes",
      "sinus_pressure",
      "runny_nose",
      "congestion",
      "chest_pain",
      "weakness_in_limbs",
      "fast_heart_rate",
      "pain_during_bowel_movements",
      "pain_in_anal_region",
      "bloody_stool",
      "irritation_in_anus",
      "neck_pain",
      "dizziness",
      "cramps",
      "bruising",
      "obesity",
      "swollen_legs",
      "swollen_blood_vessels",
      "puffy_face_and_eyes",
      "enlarged_thyroid",
      "brittle_nails",
      "swollen_extremeties",
      "excessive_hunger",
      "extra_marital_contacts",
      "drying_and_tingling_lips",
      "slurred_speech",
      "knee_pain",
      "hip_joint_pain",
      "muscle_weakness",
      "stiff_neck",
      "swelling_joints",
      "movement_stiffness",
      "spinning_movements",
      "loss_of_balance",
      "unsteadiness",
      "weakness_of_one_body_side",
      "loss_of_smell",
      "bladder_discomfort",
      "foul_smell_of_urine",
      "continuous_feel_of_urine",
      "passage_of_gases",
      "internal_itching",
      "toxic_look_(typhos)",
      "depression",
      "irritability",
      "muscle_pain",
      "altered_sensorium",
      "red_spots_over_body",
      "belly_pain",
      "abnormal_menstruation",
      "dischromic_patches",
      "watering_from_eyes",
      "increased_appetite",
      "polyuria",
      "family_history",
      "mucoid_sputum",
      "rusty_sputum",
      "lack_of_concentration",
      "visual_disturbances",
      "receiving_blood_transfusion",
      "receiving_unsterile_injections",
      "coma",
      "stomach_bleeding",
      "distention_of_abdomen",
      "history_of_alcohol_consumption",
      "fluid_overload",
      "blood_in_sputum",
      "prominent_veins_on_calf",
      "palpitations",
      "painful_walking",
      "pus_filled_pimples",
      "blackheads",
      "scurring",
      "skin_peeling",
      "silver_like_dusting",
      "small_dents_in_nails",
      "inflammatory_nails",
      "blister",
      "red_sore_around_nose",
      "yellow_crust_ooze",
    ],
    values: [],
    value: null,
    isLoading: false,
    showDialog: false,
    predictedDisease: "",
  }),
  computed: {
    symptoms: {
      get() {
        let newArray = [];
        this.autocompleteItems.forEach((autocompleteItem) => {
          let val = this.capitalizeWords(autocompleteItem.replace(/_/g, " "));
          newArray.push(val);
        });

        return newArray;
      },
    },
  },
  methods: {
    onSubmit() {
      this.$refs.form.validate();
      if (this.valid) {
        this.isLoading = true;
        console.log("this.pateientData :", this.pateientData);

        let IDToken = UserInfoAPI.getIDToken();
        // console.log("ID TOken ", IDToken);

        const headers = {
          "Content-Type": "application/json",
          Authorization: IDToken,
        };
        const apiURL = process.env.VUE_APP_API_URL + "/diseaseprediction ";
        console.log("apiURL ", apiURL);
        axios
          .post(apiURL, this.pateientData, {
            headers: headers,
          })
          .then((response) => {
            console.log("API Response :", response);
            this.predictedDisease = response.data;
            this.showDialog = true;
            this.isLoading = false;
          })
          .catch((error) => {
            console.error("Error ", error);
            this.isLoading = false;
          });
      }
    },
    capitalizeWords(string) {
      return string.replace(/(?:^|\s)\S/g, function (a) {
        return a.toUpperCase();
      });
    },
  },
};
</script>
