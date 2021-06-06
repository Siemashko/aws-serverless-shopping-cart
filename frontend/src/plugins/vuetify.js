import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)

const opts = {
    theme: {
      themes: {
        light: {
            primary: '#c1ddc8',
            secondary: '#363732',
            accent: '#047e00'
        },
      },
    },
  }

export default new Vuetify(opts)