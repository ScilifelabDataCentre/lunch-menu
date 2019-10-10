<template>
  <div id="app">
    <restaurant-entry v-for="restaurant in restaurants" :key="restaurant.name" :restaurant-info="restaurant"/>
  </div>
</template>

<script>
import axios from 'axios';
import RestaurantEntry from './components/RestaurantEntry.vue'

export default {
  name: 'app',
  components: {
    'restaruant-entry': RestaurantEntry
  },
  data () {
    return {
      restaurants: null
    }
  },
  mounted () {
    axios
      .get('https://api.coindesk.com/v1/bpi/currentprice.json')
      .then(response => (this.restaurants = response))
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
