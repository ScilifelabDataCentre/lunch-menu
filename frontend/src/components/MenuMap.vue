<template>
  <div class="flex justify-center">
    <div ref="map-root" style="width: 95%; height: 40vh; max-width: 100em; max-height: 80em">
    </div>
  </div>
</template>

<script>
import View from 'ol/View'
import Map from 'ol/Map'
import TileLayer from 'ol/layer/Tile'
import OSM from 'ol/source/OSM'
import {fromLonLat} from 'ol/proj'

import 'ol/ol.css'

export default {
  name: 'MenuMap',
  components: {},
  props: {},

  watch: {
    region() {
      if (this.region === 'solna') {
        this.mapObject.getView().setCenter(this.solnaCenter);
        this.mapObject.getView().setZoom(17)
      }
      else if (this.region === 'uppsala') {
        this.mapObject.getView().setZoom(16)
        this.mapObject.getView().setCenter(this.uppsalaCenter);
      }
      else
        this.mapObject.getView().setCenter([0, 0]);
    },
  }, 
  
  data () {
    return {
      solnaCenter: fromLonLat([18.02588, 59.34864]),
      uppsalaCenter: fromLonLat([17.63807, 59.84353]),
      mapObject: null,
    }
  },

  mounted() {
    this.mapObject = new Map({
      target: this.$refs['map-root'],
      layers: [ new TileLayer({ source: new OSM() }) ],
      view: new View({zoom: 17, center: this.solnaCenter})
    })
  },
}
</script>
