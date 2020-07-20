<template>
<q-page class="flex flex-center">
  <q-list>
    <res-entry v-for="restaurant in restaurants"
               :key="restaurant"
               :restaurantId="restaurant" />
  </q-list>
</q-page>
</template>

<script>
import axios from 'axios';

import RestaurantEntry from 'components/RestaurantEntry.vue'

export default {
  name: 'PageIndex',

  components: {
    'res-entry': RestaurantEntry,
  },
  
  computed: {
    restaurants: {
      get () {
        return this.$store.state.main.restaurants;
      },
    },
  },

  data () {
    return {
      error: false,
      loading: true,
    }
  },

  created () {
    this.$store.dispatch('main/getRestaurants');
  }
}
</script>
