import axios from 'axios';


export function getRestaurants ({ commit }) {
  return new Promise((resolve, reject) => {
    axios
      .get('/api/restaurant')
      .then((response) => {
        commit('updateRestaurants', response.data.restaurants);
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


export function setShowSolna ({ commit }, status) {
  commit('updateSolna', status);
}


export function setShowUppsala ({ commit }, status) {
  commit('updateUppsala', status);
}


export function setOnlyFavourites ({ commit }, status) {
  commit('updateOnlyFavourites', status);
}

export function setRegion ({ commit }, value) {
  commit('updateRegion', value);
}


// expects payload to be {'restaurant': name, 'favourite': state}
export function setFavourite ({ commit }, payload) {
  commit('updateFavourite', payload);
}
