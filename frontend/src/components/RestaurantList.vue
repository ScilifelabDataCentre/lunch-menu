<template>
<div id="restaurant-list">
  <div id="solna-restaurants" v-if="list_type === 'both' || list_type === 'solna'">
    <restaurant-entry v-for="restaurant in sortedSolna"
                      :key="restaurant.name"
                      :restaurant_info="restaurant">
    </restaurant-entry>
  </div>
  <div id="spacer" v-if="list_type === 'both'">
    <hr id="location_divider" />
  </div>
  <div id="uppsala-restaurants" v-if="list_type === 'both' || list_type === 'uppsala'">
    <restaurant-entry v-for="restaurant in sortedUppsala"
                      :key="restaurant.name"
                      :restaurant_info="restaurant">
    </restaurant-entry>
  </div>
</div>
</template>

<script>
import {mapGetters} from 'vuex';
import RestaurantEntry from './RestaurantEntry.vue'

export default {
  name: 'RestaurantList',
  props: ['list_type'],
  components: {
    'restaurant-entry': RestaurantEntry
  },
  computed: {
    ...mapGetters(['restaurants']),
    
    sortedSolna () {
      let chosen = this.restaurants.filter((rest) => rest.campus == 'Solna')
      return chosen.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
    },

    sortedUppsala () {
      let chosen = this.restaurants.filter((rest) => rest.campus == 'Uppsala')
      return chosen.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
    }
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
    margin-top: 50px;
    letter-spacing: 0.01em;
}

.endnote {
    font-size: 10px;
    padding: 25px 0px 0px 0px;
}


#spacer {
    padding: 25px 0px;
}

#location_divider {
    width: 120px;
}

</style>
