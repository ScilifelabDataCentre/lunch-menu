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
  components: {
    'restaurant-entry': RestaurantEntry
  },
  data () {
    return {
      list_type: null,
      active: []
    }
  },
  computed: {
    ...mapGetters(['restaurants', 'sortedSolna', 'sortedUppsala'])
  },
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
