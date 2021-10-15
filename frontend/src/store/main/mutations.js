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

export function updateRegion (state, payload) {
  state.currentRegion = payload;
}

// expects payload to be {'restaurant': name, 'favourite': state}
export function updateFavourite (state, payload) {
  let index = state.favourites.indexOf(payload.restaurant);
  if (payload.favourite) {
    if (index === -1) {
      state.favourites.push(payload.restaurant);
    }
  }
  else {
    if (index > -1) {
      state.favourites.splice(index, 1);
    }
  }
}
