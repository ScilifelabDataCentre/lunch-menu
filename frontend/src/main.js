import Vue from 'vue'
import App from './App.vue'
import router from './router';
import store from './store';
import VueCookies from 'vue-cookies'

Vue.use(VueCookies)

import '../node_modules/bulma/css/bulma.css';

Vue.config.productionTip = false

new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app')
