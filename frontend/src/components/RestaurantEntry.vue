<template>
<q-card>
  <q-card-section>
    <div class="row">
      <q-btn flat
             dense
             no-wrap
             text-color="info"
             type="a"
             :href="restaurantBase.homepage"
             icon-right="las la-external-link-alt"
             :label="restaurantBase.name" />
      <q-space />
      
      <q-btn @click="isFavourite = !isFavourite"
	     flat
	     dense
	     round
	     color="white"
	     text-color="info"
	     :icon="isFavourite ? 'las la-heart' : 'lar la-heart'" />
    </div>
    <div v-if="loading"
         class="flex justify-center">
      <q-spinner-dots 
        color="info"
        size="2em"
        />
    </div>
    <div v-else-if="failed"
         class="justify-center">
      <q-avatar text-color="negative" icon="error" />
      Failed to retrieve data for {{ restaurantBase.name }}
    </div>
    <q-list v-else>
      <q-item
        v-for="menuEntry in restaurantData.menu"
        :key="menuEntry['dish']">
        {{ menuEntry['dish'] }}
      </q-item>
    </q-list>
  </q-card-section>
</q-card>
</template>

<script>
export default {
  name: 'RestaurantEntry',

  props: ["restaurantBase"],

  computed: {
    favourites: {
      get () {
        return this.$store.state.main.favourites;
      },
    },
    isFavourite: {
      get () {
        return this.favourites.includes(this.restaurantBase.identifier);
      },
      set (value) {
        this.$store.dispatch('main/setFavourite', {
          'favourite': value,
          'restaurant': this.restaurantBase.identifier
        });
      }
    }
  },

  watch: {
    restaurantBase() {
      this.$store.dispatch('main/getRestaurant', this.restaurantBase.identifier)
        .then((response) => {
          this.restaurantData = response.data.restaurant;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
          this.failed = true;
        });
    },
  },

  data () {
    return {
      dishes: null,
      loading: true,
      failed: false,
      restaurantData: {},
    }
  },
  
  mounted () {
    this.isFavourite = this.favourites.includes(this.restaurantBase.identifier);
    this.$store.dispatch('main/getRestaurant', this.restaurantBase.identifier)
      .then((response) => {
        this.restaurantData = response.data.restaurant;
        this.loading = false;
      })
      .catch(() => {
        this.loading = false;
        this.failed = true;
      });
  }
}
</script>
