<template>
  <v-card outlined class="flexcard mt-4" height="100%" :href="enableLink ? '/product/'+product.productId : ''">
    <v-row align="center" justify="center" class="center">
      <v-col :cols="12" align="center" justify="center" class="mt-10 mb-10"><img v-bind:src="product.pictures[0]"/>
      </v-col>
    </v-row>
    <v-row class="pt-2" dense>
      <v-col :cols="8" class="mb-5">
        <v-card-title primary-title class="pb-0 pt-2">
          <p class="subtitle-2">{{ product.name }}</p>
        </v-card-title>
      </v-col>
      <v-col>
        <p class="text-truncate body-2 pt-2 pb-0 pr-2 grow text-right mb-1">{{ product.category }}</p>
      </v-col>
    </v-row>
    <v-card-text class="pt-0 pl-4 pb-0">
      <p class="pt-0 pb-0 mb-0 body-2">"{{ product.description }}"</p>
      <p class="price pt-0 pb-0 grow accent--text mb-1">${{ getPrice(product) }}</p>
    </v-card-text>
    <v-row align="center" justify="center" class="center">
      <v-card-actions class="card-actions pa-0 mb-2 mt-2 align-center justify-center">
        <v-row class="pa-4" v-if="endDate>now">
          {{ hour }}:{{ min }}:{{ sec }}
        </v-row>
        <v-row class="pa-4" v-if="endDate<=now">
          <v-btn
              icon
              small
              :disabled="cartItemCount(product.productId) < 1"
              @click.stop.prevent="removeProductFromCart(product)"
              :loading="product.removeLoading"
          >
            <v-icon>mdi-minus</v-icon>
          </v-btn>
          <cart-quantity-editor @input="updateCart" :product="product"
                                :value="cartItemCount(product.productId)"></cart-quantity-editor>
          <v-btn icon small depressed @click.stop.prevent="addProductToCart(product)" :loading="product.addLoading">
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-row>
      </v-card-actions>
    </v-row>
  </v-card>
</template>

<script>
import {Decimal} from "decimal.js";

export default {
  props:
      {
        product: {
          type: Object
        },
        enableLink: {
          type: Boolean,
          default: true
        },
        endDate: {  // pass date object till when you want to run the timer
          type: Date,
          default() {
            return new Date()
          }
        },
        negative: {  // optional, should countdown after 0 to negative
          type: Boolean,
          default: true
        }
      },
  name: "product",
  data() {
    return {
      now: new Date(),
      timer: null
    };
  },
  computed: {
    hour() {
      let h = Math.trunc((this.endDate - this.now) / 1000 / 3600);
      return h > 9 ? h : '0' + h;
    },
    min() {
      let m = Math.trunc((this.endDate - this.now) / 1000 / 60) % 60;
      return m > 9 ? m : '0' + m;
    },
    sec() {
      let s = Math.trunc((this.endDate - this.now) / 1000) % 60
      return s > 9 ? s : '0' + s;
    }
  },
  watch: {
    endDate: {
      immediate: true,
      handler(newVal) {
        if (this.timer) {
          clearInterval(this.timer)
        }
        this.timer = setInterval(() => {
          this.now = new Date()
          if (this.negative)
            return
          if (this.now > newVal) {
            this.now = newVal
            this.$emit('endTime')
            clearInterval(this.timer)
          }
        }, 1000)
      }
    }
  },
  beforeDestroy() {
    clearInterval(this.timer)
  },
  methods: {
    cartItemCount(id) {
      let item = this.$store.state.cart.find(obj => obj.sk === id);
      if (item) {
        return item.quantity;
      } else {
        return 0;
      }
    },
    addProductToCart(product) {
      this.$store.dispatch("addToCart", product);
    },
    removeProductFromCart(product) {
      this.$store.dispatch("removeFromCart", product);
    },
    getPrice(product) {
      return new Decimal(product.price / 100).toFixed(2);
    },
    updateCart(event) {
      this.$store.dispatch("updateCart", event)
    }
  }
};
</script>

<style scoped>
.flexcard {
  position: relative;
  padding-bottom: 50px;
}

.card-actions {
  position: absolute;
  bottom: 0;
  border: 1px solid;
  border-radius: 15px !important;
  border-color: #dce1e9;
}

img {
  height: 80%;
  width: 60%;
}
</style>