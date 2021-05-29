<template>
  <v-container grid-list-md fluid class="mt-0" pt-0>
    <h1>Example payment form</h1>
    <v-layout row wrap>
      <v-flex xs12 lg4 sm6>
        <v-card>
          <v-container>
            <v-form pa-2 ma-2>
              <v-text-field
                  color="secondary"
                  outlined
                  required
                  @input="$v.customerName.$touch()"
                  @blur="$v.customerName.$touch()"
                  label="Name"
                  v-model="customerName"
                  :error-messages="cardCustomerNameErrors"
              ></v-text-field>
              <v-text-field
                  color="secondary"
                  outlined
                  required
                  @input="$v.customerSurname.$touch()"
                  @blur="$v.customerSurname.$touch()"
                  label="Surname"
                  v-model="customerSurname"
                  :error-messages="cardCustomerSurnameErrors"
              ></v-text-field>
              <v-text-field
                  color="secondary"
                  outlined
                  required
                  @input="$v.customerEmail.$touch()"
                  @blur="$v.customerEmail.$touch()"
                  label="Customer E-mail"
                  v-model="customerEmail"
                  :error-messages="cardCustomerEmailErrors"
                  :disabled="emailDisabled"
              ></v-text-field>
              <v-text-field
                  color="secondary"
                  outlined
                  required
                  @input="$v.cardNumber.$touch()"
                  @blur="$v.cardNumber.$touch()"
                  v-model="cardNumber"
                  label="Card Number"
                  v-mask="'#### #### #### ####'"
                  :error-messages="cardNumberErrors"
              ></v-text-field>
              <v-text-field
                  color="secondary"
                  outlined
                  required
                  @input="$v.cardName.$touch()"
                  @blur="$v.cardName.$touch()"
                  label="Cardholder Name"
                  v-model="cardName"
                  :error-messages="cardNameErrors"
              ></v-text-field>
              <v-text-field
                  color="secondary"
                  outlined
                  required
                  @input="$v.cardExpiry.$touch()"
                  @blur="$v.cardExpiry.$touch()"
                  label="Card Expiry"
                  v-model="cardExpiry"
                  :error-messages="cardExpiryErrors"
              ></v-text-field>
              <v-text-field
                  color="secondary"
                  outlined
                  required
                  @input="$v.cardCVC.$touch()"
                  @blur="$v.cardCVC.$touch()"
                  label="Card CVC"
                  v-model="cardCVC"
                  :error-messages="cardCVCErrors"
              ></v-text-field>
              <v-btn block color="accent" @click="submit">Submit</v-btn>
            </v-form>
          </v-container>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import {mapGetters, mapState} from "vuex";
import {validationMixin} from "vuelidate";
import {helpers, required} from "vuelidate/lib/validators";


const ccvalidate = helpers.regex(
    "alpha",
    /(\d{4} *\d{4} *\d{4} *\d{4})/
); /* I know, I know... */

export default {
  data() {
    let user = this.$store.state.user
    let email = null;
    let emailDisabled = false;
    if(user) {
      email = user.getSignInUserSession().getIdToken().decodePayload()["email"];
      emailDisabled = true;
    }
    return {
      customerName: null,
      customerSurname: null,
      customerEmail: email,
      emailDisabled: emailDisabled,
      cardNumber: null,
      cardExpiry: null,
      cardName: null,
      cardCVC: null
    };
  },
  mixins: [validationMixin],
  validations: {
    customerName: {
      required
    },
    customerSurname: {
      required
    },
    customerEmail: {
      required
    },
    cardNumber: {
      required,
      ccvalidate: ccvalidate
    },
    cardExpiry: {
      required
    },
    cardCVC: {
      required
    },
    cardName: {
      required
    }
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) {
        console.log("invalid form"); // eslint-disable-line no-console
      } else {
        this.$store.dispatch("checkoutCart")
        // TODO: redirect to confirmation
      }
    }
  },
  computed: {
    ...mapGetters(["cartTotalAmount", "getCart"]),
    ...mapState(["cart"]),
    cardCustomerNameErrors() {
      const errors = [];
      if (!this.$v.customerName.$dirty) return errors;
      !this.$v.customerName.required && errors.push("Customer name is required.");
      return errors;
    },
    cardCustomerSurnameErrors() {
      const errors = [];
      if (!this.$v.customerSurname.$dirty) return errors;
      !this.$v.customerSurname.required && errors.push("Customer surname is required.");
      return errors;
    },
    cardCustomerEmailErrors() {
      const errors = [];
      if (!this.$v.customerEmail.$dirty) return errors;
      !this.$v.customerEmail.required && errors.push("Customer e-mail is required.");
      return errors;
    },
    cardNumberErrors() {
      const errors = [];
      if (!this.$v.cardNumber.$dirty) return errors;
      !this.$v.cardNumber.ccvalidate &&
      errors.push("Valid card number is required.");
      !this.$v.cardNumber.required && errors.push("Card number is required.");
      return errors;
    },
    cardNameErrors() {
      const errors = [];
      if (!this.$v.cardName.$dirty) return errors;
      !this.$v.cardName.required && errors.push("Cardholder name is required.");
      return errors;
    },
    cardExpiryErrors() {
      const errors = [];
      if (!this.$v.cardExpiry.$dirty) return errors;
      !this.$v.cardExpiry.required && errors.push("Cart expiry is required.");
      return errors;
    },
    cardCVCErrors() {
      const errors = [];
      if (!this.$v.cardCVC.$dirty) return errors;
      !this.$v.cardCVC.required && errors.push("Card CVC is required.");
      return errors;
    }
  }
};
</script>

