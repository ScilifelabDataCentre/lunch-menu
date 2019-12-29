import Vue from 'vue';
import VueRouter from 'vue-router';
import RestaurantList from '../components/RestaurantList.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  base: '/',
  routes: [
    {
      name: 'solna',
      path: '/solna',
      component: RestaurantList,
      props: { list_type: 'solna' },
      alias: ['/ki']
    },
    {
      name: 'uppsala',
      path: '/uppsala',
      component: RestaurantList,
      props: { list_type: 'uppsala' },
      alias: ['/uu', '/bmc']
    },
    {
      name: 'all',
      path: '/',
      component: RestaurantList,
      props: { list_type: 'both' },
      alias: ['*']
    },
  ]
});

export default router;
