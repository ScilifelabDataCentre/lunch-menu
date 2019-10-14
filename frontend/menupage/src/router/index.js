import Vue from 'vue';
import VueRouter from 'vue-router';
import RestaurantEntry from '../components/RestaurantEntry.vue'

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/solna',
      component: RestaurantEntry,
      props: { restaurantInfo: sortedSolna },
      alias: ['/ki']
    },
    {
      path: '/uppsala',
      component: RestaurantEntry,
      props: { restaurantInfo: sortedUppsala },
      alias: ['/uu', '/bmc']
    },
    {
      path: '/',
      components: {
        solna: RestaurantEntry,
        bmc: RestaurantEntry
      },
      props: {
        solna: { restaurantInfo: sortedSolna },
        bmc: { restaurantInfo: sortedUppsala }
      }
    },
  ]
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");
  if (!token && to.path !== '/login') next('/login');
  else next();
});

export default router;
