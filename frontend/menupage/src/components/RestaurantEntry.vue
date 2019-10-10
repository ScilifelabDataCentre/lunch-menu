<template>
<div class="restaurant">
  <h2>{{ restaurant_info.name }}</h2>
  <menu-entry v-for="dish in dishes" :key="dish" :dish="dish">
  </menu-entry>
</div>
</template>

<script>
import axios from 'axios';
import MenuEntry from './MenuEntry.vue'

export default {
  name: 'RestaurantEntry',
  props: ["restaurant_info"],
  components: {
    'menu-entry': MenuEntry
  },
  data () {
    return {
      dishes: null
    }
  },
  mounted () {
    axios
      .get('http://localhost:3333/api/restaurant/' +
           this.restaurant_info['identifier'])
      .then(response => (this.dishes = response.data.menu))
  }

}
</script>
