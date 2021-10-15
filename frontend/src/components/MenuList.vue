<template>
<div class="justify-center">
  <div class="flex justify-center">
    <q-list class="flex-center">
      <res-entry v-for="restaurant in visibleRestaurants"
                 :key="restaurant.identifier"
                 :restaurantBase="restaurant" />
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
        let current = JSON.parse(JSON.stringify(this.restaurants));
        if (this.currentRegion === "favourites") {
          current = current.filter((entry) => this.favourites.includes(entry.identifier));
        }
        else {
          current = current.filter((value) => value.region.toLowerCase() === this.currentRegion);
          current = current.sort((a,b) => {
            return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0);
          });
        }
        return current;
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
