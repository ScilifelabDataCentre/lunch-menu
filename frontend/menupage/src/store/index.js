import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

const state = {
  restaurants: []
}

const mutations = {
  UPDATE_RESTAURANTS (state, payload) {
    state.restaurants = payload;
  }
}

const actions = {
  getRestaurants ({ commit }) {
    axios
      .get('http://scilifelab-lunches.herokuapp.com/api/restaurants')
      .then(commit('UPDATE_RESTAURANTS', response.data))
  },
}

const getters = {
  restaurants: state => state.restaurants,
  sortedSolna () {
    let chosen = this.restaurants.filter((rest) => rest.campus == 'Solna')
    return chosen.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
  },
  sortedUppsala () {
    let chosen = this.restaurants.filter((rest) => rest.campus == 'Uppsala')
    return chosen.sort((a,b) => (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0))
  }
}

const store = new Vuex.Store({
  state,
  mutations,
  actions,
  getters
})
