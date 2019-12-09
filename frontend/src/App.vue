<template>
<div id="app">  
  <div class="container">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-start">
        <div class="navbar-item"> 
          {{today}}
        </div>
      </div>
      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link">
          Location
        </a>

        <div class="navbar-dropdown">
          <router-link to="/" class="navbar-item">All</router-link>
          <router-link to="/solna" class="navbar-item">Solna</router-link>
          <router-link to="/bmc" class="navbar-item">Uppsala (BMC)</router-link>
        </div>
      </div>
    +</nav>

    <div class="notification is-info" v-if="!loaded && !error">Waiting for data from API...</div>
    <div class="notification is-danger" v-if="(loaded && restaurants.length === 0) || error">Failed to load data from API: {{ error }}</div>
    <router-view></router-view>
    <footer class="footer">
      <div>
        Provided by <a href="https://www.scilifelab.se/data/">SciLifeLab Data Centre</a>
      </div>.
      <div>
        Code, issues, and requests for new restaurants at <a href="https://github.com/ScilifelabDataCentre/lunch-menu">Github</a>
      </div>
    </footer>
  </div>

</div>
</template>

<script>
import {mapGetters} from 'vuex';

export default {
  name: 'app',
  data () {
    return {
      loaded: false,
      error: null,
      today: null,
    }
  },
  computed: {
    ...mapGetters(['restaurants']),
  },
  created () {
    this.$store.dispatch('getRestaurants')
      .then(() => this.loaded = true)
      .catch((err) => this.error = err);

    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const months = ['January', 'February', 'March',
                    'April', 'May', 'June',
                    'July', 'August', 'September',
                    'October', 'November', 'December'];
    let day = new Date();
    this.today = days[day.getDay()] + ' ' + day.getDate() + ' ' + months[day.getMonth()];
  },
}
</script>

<style>
#app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
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
