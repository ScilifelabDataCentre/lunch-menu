<template>
  <div class="flex justify-center">
    <div ref="map-root" style="width: 100%; height: 50vh; max-height: 50em">
    </div>
    <res-entry v-if="selectedRestaurant.length > 0"
               class="q-my-md"
               :restaurantBase="selectedRestaurantBase" />
    <q-card v-else
            class="q-my-md">
      <q-card-section class="text-center text-weight-medium">
        Click a marker to show information about the restaurant
      </q-card-section>
    </q-card>
  </div>
</template>

<script>
import View from 'ol/View'
import Map from 'ol/Map'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import OSM from 'ol/source/OSM'
import Vector from 'ol/source/Vector'
import Feature from 'ol/Feature'
import Point from 'ol/geom/Point'
import {fromLonLat} from 'ol/proj'
import {Icon, Style} from 'ol/style';
import {getDistance} from 'ol/sphere';

import 'ol/ol.css'

import RestaurantEntry from 'components/RestaurantEntry.vue'

export default {
  name: 'MenuMap',
  
  computed: {
    restaurants: {
      get () {
        return this.$store.state.main.restaurants;
      },
    },
    
    selectedRegion: {
      get () {
        return this.$store.state.main.currentRegion
      },
      set (newValue) {
        this.$store.dispatch('main/setRegion', newValue)
      }
    },
    
    selectedRestaurantBase: {
      get () {
        for (let entry of this.restaurants) {
          if (entry.identifier === this.selectedRestaurant)
            return entry
        }
        return {}
      }
    },
    
    showMap: {
      get () {
        return this.$store.state.main.showMap
      },
      set (newValue) {
        this.$store.dispatch('main/setShowMap', newValue)
      }
    },
    
    visibleRestaurants: {
      get () {
        return this.$store.state.main.visibleRestaurants;
      },
    },
  },
  
  components: {
    'res-entry': RestaurantEntry,
  },
  
  props: {},
  
  methods: {
    updateResSource() {
      this.resSource.clear()
      for (let entry of this.visibleRestaurants) {
        this.resSource.addFeature(new Feature({
          geometry: new Point(fromLonLat([entry.coordinate[1], entry.coordinate[0]])),
          name: entry.identifier,
        }))
      }
    },
    
    handleMapClick(event) {
      let res = this.resSource.getClosestFeatureToCoordinate(event.coordinate)
      if (this.currRes !== null)
        this.currRes.setStyle(undefined)
      this.currRes = res
      if (this.currRes !== null) {
        this.currRes.setStyle(new Style({
          image: new Icon({
            anchor: [0.5, 50],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: require('assets/map-marker-solid-sel.png'),
          })
        }))
        this.selectedRestaurant = res.get('name')
      }
      else
        this.selectedRestaurant = '';
    },
  },
  
  watch: {
    visibleRestaurants() {
      this.selectedRestaurant = '',
      this.currRes = null;
      this.updateResSource();
      if (this.resSource.getFeatures().length > 0)
        this.mapObject.getView().fit(this.resSource.getExtent(), {padding: [70, 70, 70, 70]});
      else
      this.mapObject.setView(new View({center: fromLonLat([18.02588, 59.34864]), zoom:15}))
    },
  }, 
  
  data () {
    return {
      mapObject: null,
      selectedRestaurant: '',
      currRes: null,
      resSource: null,
    }
  },

  mounted() {
    this.mapObject = new Map({
      target: this.$refs['map-root'],
      layers: [ new TileLayer({ source: new OSM() }) ],
      view: new View({center: fromLonLat([18.02588, 59.34864]), zoom:15})
    })
    this.resSource = new Vector({features: []});
    this.updateResSource();
    let layer = new VectorLayer({source: this.resSource,
                                 style: new Style({
                                   image: new Icon({
                                     anchor: [0.5, 50],
                                     anchorXUnits: 'fraction',
                                     anchorYUnits: 'pixels',
                                     src: require('assets/map-marker-solid.png'),
                                   })
                                 })
                                });

    this.mapObject.addLayer(layer);
    if (this.resSource.getFeatures().length > 0) {
      this.mapObject.getView().fit(this.resSource.getExtent(), {padding: [70, 70, 70, 70]});
    }
    this.mapObject.on('click', this.handleMapClick);
  },
}
</script>
