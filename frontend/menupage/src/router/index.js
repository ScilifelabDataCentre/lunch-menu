import Vue from 'vue';
import VueRouter from 'vue-router';
import RestaurantList from '../components/RestaurantList.vue'

Vue.use(VueRouter);

const router = new VueRouter({
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
    },
  ]
});

export default router;
