import Vue from 'vue';
import VueRouter from 'vue-router';
import RestaurantList from '../components/RestaurantList.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'hash',
  base: '/menu/',
  routes: [
    {
      path: '/solna',
      component: RestaurantList,
      props: { list_type: 'solna' },
      alias: ['/ki']
    },
    {
      path: '/uppsala',
      component: RestaurantList,
      props: { list_type: 'uppsala' },
      alias: ['/uu', '/bmc']
    },
    {
      path: '/',
      component: RestaurantList,
      props: { list_type: 'both' },
      alias: ['*']
    },
  ]
});

export default router;
