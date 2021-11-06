import axios from 'axios';

export function getRestaurants ({ commit }) {
  return new Promise((resolve, reject) => {
    axios
      .get('/api/restaurant')
      .then((response) => {
        commit('updateRestaurants', response.data.restaurants);
        commit('updateVisRes', response.data.restaurants);
        resolve(response);
      })
      .catch((err) => {
        reject(err);        
      });
  });
}

export function getRestaurant ({ commit }, identifier) {
  return new Promise((resolve, reject) => {
    axios
      .get('/api/restaurant/' + identifier)
      .then((response) => {
        resolve(response);
      })
      .catch((err) => {
        reject(err);        
      });
  });
}

export function setRegion ({ commit }, value) {
  commit('updateRegion', value);
}

export function setShowMapList ({ commit }, value) {
  commit('updateShowMapList', value);
}

// expects payload to be {'restaurant': name, 'favourite': state}
export function setFavourite ({ commit }, payload) {
  commit('updateFavourite', payload);
}

export function updateVisRes ({ commit }) {
  commit('updateVisRes');
}
