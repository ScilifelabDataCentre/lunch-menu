<template>
  <div class="flex justify-center">
    <div ref="map-root" style="width: 100%; height: 50vh; max-height: 50em">
    </div>
    <res-entry v-if="selectedRestaurant.length > 0" :restaurantBase="selectedRestaurantBase" />
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

import 'ol/ol.css'

import RestaurantEntry from 'components/RestaurantEntry.vue'

export default {
  name: 'MenuMap',

  computed: {
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
        for (entry of this.restaurants) {
          if (entry.identifier == this.selectedRestaurant)
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
      let tmp = this.mapObject.getLayers()
      console.log(this.mapObject.getFeaturesAtPixel(event.pixel, {hitTolerance: 20}))
      this.selectedRestaurant = ''
      this.mapObject.forEachFeatureAtPixel(event.pixel, this.updateSelectedRes);
    },

    updateSelectedRes(feature, layer) {
      console.log('inside')
      this.selectedRestaurant = feature.get('name');
    }
  },
  
  watch: {
    visibleRestaurants() {
      this.updateResSource();
      this.mapObject.getView().fit(this.resSource.getExtent(), {padding: [70, 70, 70, 70]});
    },
  }, 
  
  data () {
    return {
      coordinates: [],
      solnaCenter: fromLonLat([18.02588, 59.34864]),
      uppsalaCenter: fromLonLat([17.63807, 59.84353]),
      mapObject: null,
      selectedRestaurant: '',
      resSource: {},
    }
  },

  mounted() {
    this.mapObject = new Map({
      target: this.$refs['map-root'],
      layers: [ new TileLayer({ source: new OSM() }) ],
    })
    this.resSource = new Vector({features: []});
    this.updateResSource();
    let layer = new VectorLayer({source: this.resSource,
                                 style: new Style({
                                   image: new Icon({
                                     anchor: [0.5, 50],
                                     anchorXUnits: 'fraction',
                                     anchorYUnits: 'pixels',
                                     src: require('assets/map-marker.png'),
                                   })
                                 })
                                });

    this.mapObject.addLayer(layer);
    this.mapObject.getView().fit(this.resSource.getExtent(), {padding: [70, 70, 70, 70]});
    this.mapObject.on('click', this.handleMapClick);
    this.mapObject.updateSize();
    this.mapObject.renderSync();
  },
}
</script>
