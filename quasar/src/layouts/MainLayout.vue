<template>
<q-layout view="lHh Lpr lFf">
  <q-header elevated>
    <q-toolbar class="bg-grey-2">
      <span class="text-primary">
        {{ today }}
      </span>
      <q-space />
      <q-btn-dropdown dense
                      flat
                      no-wrap
                      no-caps
		      text-color="secondary"
                      icon="location_on"
                      class="q-ml-sm pull-right">
        <q-list>
          <q-item>
            <q-item-section avatar>
              <q-btn round
                     :icon="showSolna ? 'location_on' : 'location_off'"
                     :color="showSolna ? 'positive' : 'grey-2'"
                     :text-color="showSolna ? 'white' : 'black'"
                     @click="showSolna = !showSolna" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Solna</q-item-label>
              <q-item-label caption>Show restaurants at KI Solna</q-item-label>
            </q-item-section>
          </q-item>

          <q-item>
            <q-item-section avatar>
              <q-btn round
                     :icon="showUppsala ? 'location_on' : 'location_off'"
                     :color="showUppsala ? 'positive' : 'grey-2'"
                     :text-color="showUppsala ? 'white' : 'black'"
                     @click="showUppsala = !showUppsala" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Uppsala</q-item-label>
              <q-item-label caption>Show restaurants at BMC</q-item-label>
            </q-item-section>
          </q-item>

          <q-separator inset spaced />

          <q-item>
            <q-item-section avatar>
              <q-btn round
                     :icon="onlyFavourites ? 'favorite' : 'favorite_border'"
                     :color="onlyFavourites ? 'positive' : 'grey-2'"
                     :text-color="onlyFavourites ? 'white' : 'black'"
                     @click="onlyFavourites = !onlyFavourites" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Favourites Only</q-item-label>
              <q-item-label caption>Show only favourited restaurants</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>

      <q-separator vertical />
      <q-btn-dropdown flat
                      label="About"
                      class="text-primary">
        <q-list>
          <q-item tag="a"
                  href="https://www.scilifelab.se/data/"
                  target="_blank">
            <q-item-section>
              <q-item-label>SciLifeLab Data Centre</q-item-label>
              <q-item-label caption>Developers of the menu page</q-item-label>
            </q-item-section>
          </q-item>
          <q-item tag="a"
                  href="https://github.com/ScilifelabDataCentre/lunch-menu"
                  target="_blank">
            <q-item-section>
              <q-item-label>Github</q-item-label>
              <q-item-label caption>Code, issues, requests</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
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
