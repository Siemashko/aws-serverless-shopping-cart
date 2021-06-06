<template>
    <v-container grid-list-md fluid class="mt-0" pt-0>
      <v-layout row wrap>
        <v-flex v-for="product in products" :key="product.productId" xs12 lg3 sm6 xl3>
            <product :product="product" :enableLink="true" :key="product.productId" />
        </v-flex>
      </v-layout>
    </v-container>
</template>

<script>
export default {
  computed: {
    products() {
      return this.$store.state.products;
    }
  },
  created() {
    this.$store.dispatch("fetchProducts");
  }
};
</script>