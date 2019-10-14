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
      .then((response) => {
        commit('UPDATE_RESTAURANTS', response.data);
      });
  }
}

const getters = {
  restaurants: state => state.restaurants
}

const store = new Vuex.Store({
  state,
  mutations,
  actions,
  getters
})

export default store
