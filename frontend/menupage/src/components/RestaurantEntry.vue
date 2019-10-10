<template>
<div class="restaurant" v-if="is_active">
  <h2>{{ restaurant_info.name }}</h2>
  <ul>
  </ul>
  </div>
</template>

<script>
import MenuEntry from './MenuEntry.vue'

export default {
  name: 'RestaurantEntry',
  props: ["restaurant_info", "is_active"],
  components: {
    'menu-entry': MenuEntry
  }
}
</script>
