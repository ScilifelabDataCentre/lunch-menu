<template>
<div id="app" class="container">
  <div class="notification is-info" v-if="!loaded && !error">Waiting for data from API...</div>
  <div class="notification is-danger" v-if="(loaded && restaurants.length === 0) || error">Failed to load data from API: {{ error }}</div>
  <router-view></router-view>
  <div class="endnote">Provided by <a href="https://www.scilifelab.se/data/">SciLifeLab Data Centre</a>. Code, issues, and requests for new restaurants at <a href="https://github.com/ScilifelabDataCentre/lunch-menu">Github</a>.
  </div>
</div>
</template>

<script>
import {mapGetters} from 'vuex';

export default {
  name: 'app',
  data () {
    return {
      active: ['bikupan', 'hjulet'],
      loaded: false,
      error: null,
    }
  },
  computed: {
    ...mapGetters(['restaurants']),
  },
  created () {
    this.$store.dispatch('getRestaurants')
      .then(() => this.loaded = true)
      .catch((err) => this.error = err);
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
