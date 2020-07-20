<template>
<q-page class="flex justify-center">
  <q-list class="flex-center">
    <res-entry v-for="restaurant in visRes"
               :key="restaurant.identifier"
               :restaurantBase="restaurant" />
  </q-list>

  <q-inner-loading :showing="loading">
    <q-spinner-dots color="primary"
                    size="2em" />
  </q-inner-loading>
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

    showSolna: {
      get () {
        return this.$store.state.main.showSolna;
      },
    },

    showUppsala: {
      get () {
        return this.$store.state.main.showUppsala;
      },
    },

    favourites: {
      get () {
        return this.$store.state.main.favourites;
      },
    },

    onlyFavourites: {
      get () {
        return this.$store.state.main.onlyFavourites;
      },
    },

    visRes: {
      get () {
        let current = this.restaurants;
        if (this.onlyFavourites) {
          current = current.filter((value) => this.favourites.includes(value.identifier));
        }
        if (!this.showSolna) {
          current = current.filter((value) => value.campus !== 'Solna');
        }
        if (!this.showUppsala) {
          current = current.filter((value) => value.campus !== 'Uppsala');
        }
        return current;
      }
    },
  },
  
  data () {
    return {
      visibleRestaurants: [],
      error: false,
      loading: true,
    }
  },

  created () {
    this.$store.dispatch('main/getRestaurants')
      .then(() => this.loading = false);
  }
}
</script>
