<template>
<div id="app">
  <h1>Restaurants</h1>
  <restaurant-entry v-for="restaurant in restaurants" :key="restaurant.name" :restaurant_info="restaurant" :is_active="isActive(restaurant)">
  </restaurant-entry>
</div>
</template>

<script>
import axios from 'axios';
import RestaurantEntry from './components/RestaurantEntry.vue'

export default {
  name: 'app',
  components: {
    'restaurant-entry': RestaurantEntry
  },
  data () {
    return {
      restaurants: null,
      active: ['bikupan', 'hjulet']
    }
  },
  methods: {
    isActive: function (restaurant) {
      return this.active.includes(restaurant.identifier)
    }
  },
  mounted () {
    axios
      .get('http://localhost:3333/api/restaurants')
      .then(response => (this.restaurants = response.data))
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
