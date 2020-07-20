<template>
<q-item>
  <q-item-section>
    <q-card>
      <q-card-section v-if="failed">
        <q-avatar text-color="negative" icon="error" />
        Failed to retrieve data for {{ restaurantData }}
      </q-card-section>
      <q-card-section v-else>
        <div class="row">
        <q-btn flat
               text-color="primary">
          {{ restaurantBase.name }}
        </q-btn>
        <q-space />
        <q-btn @click="setFavourite"
               flat
               round
               color="white"
               text-color="red"
               :icon="isFavourite ? 'favorite' : 'favorite_border'" />
        </div>
        <div v-if="loading"
             class="flex justify-center">
          <q-spinner-dots 
            color="primary"
            size="2em"
            />
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
  </q-item-section>
</q-item>
</template>

<script>
export default {
  name: 'RestaurantEntry',

  props: ["restaurantBase"],

  computed: {
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
  },

  data () {
    return {
      dishes: null,
      loading: true,
      failed: false,
      isFavourite: false,
      restaurantData: {},
    }
  },

  methods: {
    setFavourite () {
      this.isFavourite = !this.isFavourite;
      this.$store.dispatch('main/setFavourite', {
        'favourite': this.isFavourite,
        'restaurant': this.restaurantBase.identifier
      });
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
