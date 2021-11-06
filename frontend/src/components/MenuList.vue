<template>
<div class="justify-center">
  <div class="flex justify-center">
    <q-list class="flex-center">
      <q-item v-for="restaurant in visibleRestaurants"
              :key="restaurant.identifier">
        <q-item-section>
          <res-entry :restaurantBase="restaurant" />
        </q-item-section>
      </q-item>
    </q-list>

    <q-inner-loading :showing="loading">
      <q-spinner-dots color="primary"
                      size="2em" />
    </q-inner-loading>
  </div>
</div>
</template>

<script>
import RestaurantEntry from 'components/RestaurantEntry.vue'

export default {
  name: 'MenuList',
  
  components: {
    'res-entry': RestaurantEntry,
  },
  
  computed: {
    restaurants: {
      get () {
        return this.$store.state.main.restaurants;
      },
    },

    favourites: {
      get () {
        return this.$store.state.main.favourites;
      },
    },

    currentRegion: {
      get () {
        return this.$store.state.main.currentRegion;
      }
    },

    visibleRestaurants: {
      get () {
        return this.$store.state.main.visibleRestaurants;
      }
    },
  },
  
  data () {
    return {
      error: false,
      loading: true,
      constTrue: true,
    }
  },

  created () {
    this.$store.dispatch('main/getRestaurants')
      .then(() => this.loading = false);
  }
}
</script>
