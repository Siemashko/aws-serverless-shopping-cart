<template>
  <v-container grid-list-md fluid class="mt-0" pt-0>
    <v-layout row wrap>
      <v-flex  xs12 lg3 sm6 xl3>
        <v-card outlined class="flexcard mt-4" height="100%">

          <v-toolbar flat color="transparent">
            <v-toolbar-title>Price range</v-toolbar-title>
          </v-toolbar>

          <v-container class="py-0">
            <v-row align-center justify-start wrap>
              <v-col :cols="3"><v-text-field
                :value="filterParams.p[0]"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @change="$set(filterParams.p, 0, $event)"
              ></v-text-field></v-col>
              <v-col :cols="6"><v-range-slider v-model="filterParams.p"
                              :max="100"
                              :min="0"
                              hide-details
                              @change="filterProducts"
                              class="align-center">

              </v-range-slider></v-col>
              <v-col :cols="3"><v-text-field
                :value="filterParams.p[1]"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px"
                @change="$set(filterParams.p, 1, $event)"
              ></v-text-field></v-col>
            </v-row>
          </v-container>

          <v-toolbar flat color="transparent">
            <v-toolbar-title>Categories</v-toolbar-title>
          </v-toolbar>

          <v-container class="py-0">
            <v-row align-center justify-start wrap>
              <v-col v-for="(selection, i) in selections" :key="selection" class="shrink">
                <v-chip :disabled="loading" close @click:close="remove(selection)">
                  {{ selection }}
                </v-chip>
              </v-col>
              <v-col v-if="!allSelected" :cols="12">
              </v-col>
            </v-row>
          </v-container>

          <v-divider v-if="!allSelected"></v-divider>

          <v-list>
            <template v-for="item in categories">
              <v-list-item
                  v-if="!filterParams.c.includes(item)"
                  :key="item"
                  :disabled="loading"
                  @click="add(item)"
              >
                <v-list-item-title v-text="item"></v-list-item-title>
              </v-list-item>
            </template>
          </v-list>

          <v-divider></v-divider>
        </v-card>
      </v-flex>
      <v-flex v-for="product in products" :key="product.productId" xs12 lg3 sm6 xl3>
        <product :product="product" :enableLink="true" :end-date="new Date(product.availableSince)"
                 :key="product.productId"/>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script defer>

export default {
  data() {
    return {
      filterParams: {
        c: [],
        p: [0, 100]
      },
      loading: false
    }
  },
  computed: {
    products() {
      return this.$store.state.products;
    },
    categories() {
      return this.$store.state.categories;
    },
    // maxPrice() {
    //   return this.$store.state.maxPrice;
    // },
    allSelected() {
      return this.filterParams.c.length === this.$store.state.categories;
    },
    selections() {
      const selections = [];

      for (const selection of this.filterParams.c) {
        selections.push(selection)
      }

      return selections;
    }
  },
  created() {
    this.$store.dispatch("fetchProducts", this.filterParams);
    this.$store.dispatch("fetchCategories");
  },
  methods: {
    remove(item) {
      this.filterParams.c.splice(this.filterParams.c.indexOf(item), 1);
      this.filterParams.c = [...this.filterParams.c];
      this.$store.dispatch("fetchProducts", this.filterParams);
    },
    add(item) {
      this.filterParams.c.push(item);
      this.$store.dispatch("fetchProducts", this.filterParams);
    },
    filterProducts() {
      this.$store.dispatch("fetchProducts", this.filterParams);
    }
  }
};
</script>