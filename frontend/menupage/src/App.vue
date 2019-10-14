<template>
<div id="app">
  <div v-if="restaurants.length == 0">Waiting for data from API...</div>
  <router-view></router-view>
  <div class="endnote">Code available at <a href="https://github.com/talavis/lunch-menu">Github</a>.
    Patches are very welcome.
  </div>
</div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      restaurants: [],
      active: ['bikupan', 'hjulet']
    }
  },
  created() {
    this.$store.dispatch('getRestaurants');
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
