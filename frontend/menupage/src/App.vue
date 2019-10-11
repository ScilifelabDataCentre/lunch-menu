<template>
<div id="app">
  <div v-if="!restaurants">Waiting for data from API...</div>
  <restaurant-entry v-for="restaurant in sortedSolna" :key="restaurant.name" :restaurant_info="restaurant">
  </restaurant-entry>
  <restaurant-entry v-for="restaurant in sortedUppsala" :key="restaurant.name" :restaurant_info="restaurant">
  </restaurant-entry>
  <div class="endnote">Code available at <a href="https://github.com/talavis/lunch-menu">Github</a>.
    Patches are very welcome.
  </div>
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
  computed: {
    sortedSolna () {
      let chosen = this.restaurants.filter((rest) => rest.campus == 'Solna')
      return chosen.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
    },
    sortedUppsala () {
      let chosen = this.restaurants.filter((rest) => rest.campus == 'Uppsala')
      return chosen.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
    }
  },

  mounted () {
    axios
      .get('http://scilifelab-lunches.herokuapp.com/api/restaurants')
      .then(response => (this.restaurants = response.data))
  }
}
</script>

<style>
#app {
    height:100%;
    font-size:14px;
    font-family:'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    letter-spacing: 0.01em;

    .endnote {
        font-size: 10px;
        padding: 25px 0px 0px 0px;
    }

    font-family: 
}
</style>
