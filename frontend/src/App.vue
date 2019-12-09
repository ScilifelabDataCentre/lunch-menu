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
          <router-link :to="{name: 'all'}" :class="{'navbar-item': true, 'is-active':this.$route.name === 'all'}">All</router-link>
          <router-link :to="{name: 'solna'}" :class="{'navbar-item': true, 'is-active':this.$route.name === 'solna'}">Solna</router-link>
          <router-link :to="{name: 'uppsala'}" :class="{'navbar-item': true, 'is-active':this.$route.name === 'uppsala'}">Uppsala (BMC)</router-link>
          <hr class="navbar-divider">
          <a class="navbar-item" @click="saveLocation">Remember location</a>
        </div>
      </div>
    </nav>

    <div v-if="notification" :class="{notification: true, 'is-info': !error, 'is-danger': error}">
      {{ notification }}
    </div>
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
      error: false,
      today: null,
      notification: "Waiting for data from API...",
    }
  },

  computed: {
    ...mapGetters(['restaurants']),
    
  },

  created () {
    let location = this.$cookies.get("location");
    if (location) {
      if (['all', 'solna', 'uppsala'].includes(location)) {
        if (this.$route.name != location) {
          this.$router.push({name: location});
        }
      }
    }
    
    this.$store.dispatch('getRestaurants')
      .then(() => this.notification = "")
      .catch((error) => {
        this.error = true;
        this.notification = "Failed to load data from API: " + error;
      });

    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const months = ['January', 'February', 'March',
                    'April', 'May', 'June',
                    'July', 'August', 'September',
                    'October', 'November', 'December'];
    let day = new Date();
    this.today = days[day.getDay()] + ' ' + day.getDate() + ' ' + months[day.getMonth()];
  },

  methods: {
    saveLocation() {
      this.$cookies.set("location", this.$route.name, '5y');
      this.notification = "Location saved";
      window.setTimeout(() => this.notification = "", 3000);
    },
  }
}
</script>

<style>
#app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
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
