<template>
  <div class="flex justify-center">
    <div ref="map-root" style="width: 100%; height: 60vh; max-height: 80em">
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

    visibleRestaurants: {
      get () {
        let current = JSON.parse(JSON.stringify(this.restaurants));
        if (this.currentRegion === "favourites") {
          current = current.filter((entry) => this.favourites.includes(entry.identifier));
        }
        else {
          current = current.filter((value) => value.region.toLowerCase() === this.currentRegion);
          current = current.sort((a,b) => {
            return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0);
          });
        }
        return current;
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

    restaurants: {
      get () {
        return this.$store.state.main.restaurants;
      },
    },
  },
  
  components: {
    'res-entry': RestaurantEntry,
  },

  props: {},

  methods: {
    genResLayer() {
      let features = [];
      for (let entry of this.restaurants) {
        features.push(new Feature({
          geometry: new Point(fromLonLat([entry.coordinate[1], entry.coordinate[0]])),
          name: entry.identifier,
        }))
      }
      this.resSource = new Vector({features: features})
      let layer = new VectorLayer({source: this.resSource,
                                   style: new Style({
                                     image: new Icon({
                                       anchor: [0.5, 64],
                                       anchorXUnits: 'fraction',
                                       anchorYUnits: 'pixels',
                                       src: require('assets/map-marker.png'),
                                     }),
                                   })
                                  });
      return layer;
    },

    handleMapClick(event) {
      let tmp = this.mapObject.getLayers()
      console.log(this.mapObject.getFeaturesAtPixel(event.pixel, {hitTolerance: 20}))
      this.selectedRestaurant = ''
      this.mapObject.forEachFeatureAtPixel(event.pixel, updateSelectedRes);
    },

    updateSelectedRes(feature, layer) {
      console.log('inside')
      this.selectedRestaurant = feature.get('name');
    }
  },
  
  watch: {
    restaurants() {
      let layer = this.genResLayer()
      this.mapObject.addLayer(layer);
      this.mapObject.updateSize();
      this.mapObject.renderSync();
    },
    
    region() {
      
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
      view: new View({zoom: 17, center: this.solnaCenter})
    })
    let layer = this.genResLayer()

    this.mapObject.addLayer(layer);
    
    this.mapObject.on('click', this.handleMapClick);
    this.mapObject.updateSize();
    this.mapObject.renderSync();
  },
}
</script>
