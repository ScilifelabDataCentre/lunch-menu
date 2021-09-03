<template>
<q-layout view="lHh Lpr lFf">
  <q-header elevated reveal>
    <q-toolbar>
      <q-btn type="a"
             href="https://www.scilifelab.se/data/"
             flat>
	<q-avatar square>
          <img :src="require('assets/sll-logo.svg')"
	       alt="SciLifeLab logo"/>
	</q-avatar>
      </q-btn>      
      <q-toolbar-title>
	{{ today }}
      </q-toolbar-title>

      <q-space />

      <q-btn flat
             round
             dense
             :icon="$q.dark.isActive ? 'las la-sun' : 'las la-moon'"
             @click="toggleDark" />
      
      <q-btn flat
             round
             dense
             icon="lab la-github"
             type="a"
             href="https://github.com/ScilifelabDataCentre/lunch-menu" />
    </q-toolbar>
  </q-header>
  <q-page-container>
    <router-view />
  </q-page-container>
</q-layout>
</template>

<script>
import { setCssVar } from 'quasar'

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

  methods: {
    toggleDark () {
      console.log("here")
      this.$q.dark.toggle();
      if (this.$q.dark.isActive)
        setCssVar('info', '#A7C947');
      else
        setCssVar('info', '#3F3F3F');
    },
  },
  
  created () {
    if (this.$q.dark.isActive)
      setCssVar('info', '#A7C947');

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
