export function updateRestaurants (state, payload) {
  state.restaurants = payload;
}


export function updateSolna (state, payload) {
  state.showSolna = payload;
}


export function updateUppsala (state, payload) {
  state.showUppsala = payload;
}


export function updateOnlyFavourites (state, payload) {
  state.onlyFavourites = payload;
}


// expects payload to be {'restaurant': name, 'favourite': state}
export function updateFavourite (state, payload) {
  let index = state.favourites.index(payload['restaurant']);
  if (!payload[favourite]) {
    if (index > -1) {
      state.favourites.splice(index);
    }
  }
  else {
    if (index > -1) {
      state.favourites.push(payload['restaurant']);
    }
  }
}
