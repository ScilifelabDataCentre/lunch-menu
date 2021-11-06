<template>
<q-page class="justify-center">
  <div class="flex justify-center">
    <q-btn-toggle class="q-ma-md"
                  v-model="selectedRegion"
                  toggle-color="info"
                  :options="regionChoices" />
  </div>
  <div v-if="selectedRegion != 'favourites'">
    <div class="flex justify-center">
      <q-btn-toggle
        v-model="showMapList"
        rounded
        unelevated
        toggle-color="primary"
        color="white"
        text-color="primary"
        :options="[
          {label: 'Map', value: 'map'},
          {label: 'List', value: 'list'}
          ]"
        />
    </div>
    <div v-if="showMapList === 'map'" class="q-my-lg q-mx-md">
      <menu-map />
    </div>
    <div v-show="showMapList === 'list'" class="q-my-lg q-mx-md">
      <menu-list />
    </div>
  </div>
  <menu-list v-else/>
</q-page>
</template>

<script>
import MenuList from 'components/MenuList.vue'
import MenuMap from 'components/MenuMap.vue'

export default {
  name: 'PageIndex',
  
  components: {
    'menu-list': MenuList,
    'menu-map': MenuMap,
  },

  computed: {
    regionChoices: {
      get () {
        let regions = [];
        for (let entry of this.$store.state.main.restaurants)
          if (!regions.includes(entry.region.toLowerCase()))
            regions.push(entry.region.toLowerCase())
        regions = regions.sort()
        regions.forEach(function (value, i) {
          regions[i] = {label: value, value: value}
        });
        regions.push({icon: 'las la-heart', value: 'favourites'})
        return regions;
      }
    },

    selectedRegion: {
      get () {
        return this.$store.state.main.currentRegion
      },
      set (newValue) {
        this.$store.dispatch('main/setRegion', newValue)
          .then(this.$store.dispatch('main/updateVisRes'));
      }
    },

    showMapList: {
      get () {
        return this.$store.state.main.showMapList
      },
      set (newValue) {
        this.$store.dispatch('main/setShowMapList', newValue)
      }
    },

    restaurants: {
      get () {
        return this.$store.state.main.restaurants;
      },
    },
  },
  
  data () {
    return {
      error: false,
      loading: true,
      constTrue: true,
    }
  },

  created () {
    this.$store.dispatch('main/getRestaurants')
      .then(() => this.loading = false);
    this.$store.dispatch('main/updateVisRes');
  }
}
</script>
