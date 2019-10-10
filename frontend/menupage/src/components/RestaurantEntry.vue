<template>
  <h1> Restaurants </h1>
  <div class="restaurant">
    {{ restaurant-info }}
  </div>
</template>

<script>
export default {
  name: 'RestaurantEntry',
  props: ['restaurant-info']
}
</script>
