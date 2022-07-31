<template>
  <div>
    <AppTitle />

    <v-card class="ma-2 pa-2">
      <v-card-text>
        <PatientHistoryTable class="ma-2" />
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import AppTitle from "@/components/AppTitle.vue";
import PatientHistoryTable from "@/components/widgets/PatientHistoryTable.vue";
export default {
  name: "CaseHistory",
  components: { AppTitle, PatientHistoryTable },
  methods: {},
};
</script>
