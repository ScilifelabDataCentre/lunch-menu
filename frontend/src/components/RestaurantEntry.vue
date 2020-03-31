<template>
<div class="restaurant">
  <div class="title is-5"><a :href="restaurant_info.url">{{ restaurant_info.name }}</a>
    <a :href="restaurant_info.osm"><img :src="require('../assets/img/map-marker.svg')" class="map"/></a>
  </div>
  <div v-for="entry in dishes" :key="entry">
    {{ entry.dish }}
  </div>
</div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RestaurantEntry',
  props: ["restaurant_info"],
  data () {
    return {
      dishes: null
    }
  },
  mounted () {
    axios
      .get(process.env.VUE_APP_API_URL + '/restaurant/' +
           this.restaurant_info['identifier'] + '/')
      .then(response => (this.dishes = response.data.restaurant.menu))
  }
}
</script>

<style scoped>
.restaurant {
    Margin: 10px 0px 10px 0px;
}
.map {
    height: 1em;
    padding: 0.1em 0em 0em 0.15em;
}

</style>
