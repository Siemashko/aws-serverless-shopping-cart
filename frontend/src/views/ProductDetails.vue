<template>
  <v-container grid-list-md fluid class="mt-0" pt-0>
      <v-layout align-center justify-center row wrap>
        <v-flex xs12 lg7 sm7 xl7>
          <product :product="product" :enableLink="false" :key="this.$route.params.id"/>
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
export default {
  name: "productDetails",
  computed: {
    product() {
      return this.$store.state.activeProduct;
    }
  },
  created() {
    this.$store.dispatch("fetchProduct", this.$route.params.id);
    this.$store.dispatch("fetchProducts");
  }
}
</script>

<style scoped>

</style>