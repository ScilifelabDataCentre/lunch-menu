<template>
<div id="app">
  <div v-if="restaurants.length == 0">Waiting for data from API...</div>
  <router-view></router-view>
  <div class="endnote">Provided by <a href="https://www.scilifelab.se/data/">SciLifeLab Data Centre</a>. Code available at <a href="https://github.com/ScilifelabDataCentre/lunch-menu">Github</a>.
  </div>
</div>
</template>

<script>
import {mapGetters} from 'vuex';

export default {
  name: 'app',
  data () {
    return {
      active: ['bikupan', 'hjulet']
    }
  },
  computed: {
    ...mapGetters(['restaurants']),
  },
  created () {
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

a {
    color: #2c3e50;
    text-decoration: none;
    font-weight: bold;
}

a:hover {
    text-decoration: underline;
    font-weight: bold;
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
