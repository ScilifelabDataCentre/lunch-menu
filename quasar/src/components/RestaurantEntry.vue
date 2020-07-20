<template>
<q-item v-if="!loading && Object.keys(restaurantData).length > 0">
  <q-item-section v-if="failed">
    <q-chip>
      <q-avatar text-color="negative" icon="error" />
      Failed to retrieve data for {{ restaurantId }}
    </q-chip>
  </q-item-section>
  
  <q-item-section v-else>
    <q-item-label>
      <q-btn flat>
        {{ restaurantData.title }}
      </q-btn>
      <q-list>
        <q-item v-for="dish in restaurantData.dishes" :key="dish">
          {{ dish }}
        </q-item>
      </q-list>
    </q-item-label>
  </q-item-section>
</q-item>
</template>

<script>
export default {
  name: 'RestaurantEntry',
  props: ["restaurantId"],
  data () {
    return {
      dishes: null,
      loading: true,
      failed: false,
      restaurantData: {},
    }
  },
  mounted () {
    this.$store.dispatch('main/getRestaurant', this.restaurantId)
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
