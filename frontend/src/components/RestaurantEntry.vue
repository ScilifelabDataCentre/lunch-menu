<template>
<div class="restaurant">
  <div class="title is-5"><a :href="restaurant_info.url">{{ restaurant_info.name }}</a>
    (<a :href="restaurant_info.osm">{{ restaurant_info.campus }}</a>)
  </div>
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
      .get('http://scilifelab-lunches.herokuapp.com/api/restaurant/' +
           this.restaurant_info['identifier'])
      .then(response => (this.dishes = response.data.menu))
  }

}
</script>

<style scoped>
.restaurant {
    padding: 5px 0px 10px 0px;
    color: #2c3e50;
}

a {
    color: #2c3e50;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

a:active {
    text-decoration: underline;
}
    
div.title {
    font-weight: bold;
    color: black;
    padding: 0px 0px 10px 0px;
}

</style>
