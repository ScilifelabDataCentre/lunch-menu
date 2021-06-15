<template>
<q-layout view="lHh Lpr lFf">
  <q-header elevated>
    <q-toolbar class="bg-grey-2  text-primary">
      <q-btn type="a"
             href="https://www.scilifelab.se/data/"
             flat>
	<q-avatar square>
          <img :src="require('assets/sll-logo.svg')"
	       alt="Data Centre logo"/>
	</q-avatar>
      </q-btn>      
      <q-toolbar-title>
	{{ today }}
      </q-toolbar-title>

      <q-space />

      <q-btn flat
             round
             icon="fab fa-github"
             type="a"
             href="https://github.com/ScilifelabDataCentre/lunch-menu"/>
    </q-toolbar>
  </q-header>
  <q-page-container>
    <router-view />
  </q-page-container>
</q-layout>
</template>

<script>
export default {
  name: 'MainLayout',

  computed: {  
    showSolna: {
      get () {
        return this.$store.state.main.showSolna;
      },
      set (val) {
        this.$store.dispatch('main/setShowSolna', val)
      }
    },

    showUppsala: {
      get () {
        return this.$store.state.main.showUppsala;
      },
      set (val) {
        this.$store.dispatch('main/setShowUppsala', val)
      }
    },

    onlyFavourites: {
      get () {
        return this.$store.state.main.onlyFavourites;
      },
      set (val) {
        this.$store.dispatch('main/setOnlyFavourites', val)
      }
    }
  },

  data () {
    return {
      today: '',
    }
  },
  
  created () {
    const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                  'Thursday', 'Friday', 'Saturday'];
    const months = ['January', 'February', 'March',
                    'April', 'May', 'June',
                    'July', 'August', 'September',
                    'October', 'November', 'December'];
    let day = new Date();
    this.today = days[day.getDay()] + ' ' + day.getDate() + ' ' + months[day.getMonth()];
  }
    
}
</script>
