export function updateRestaurants (state, payload) {
  state.restaurants = payload;
}

export function updateRegion (state, payload) {
  state.currentRegion = payload;
}

export function updateShowMapList (state, payload) {
  state.showMapList = payload;
}

export function updateVisRes (state) {
  let current = JSON.parse(JSON.stringify(state.restaurants));
  if (state.currentRegion === "favourites") {
    current = current.filter((entry) => state.favourites.includes(entry.identifier));
  }
  else {
    current = current.filter((value) => value.region.toLowerCase() === state.currentRegion);
  }
  state.visibleRestaurants = current.sort((a,b) => {
    return (a.name > b.name) ? 1 : ((b.name > a.name) ? -1 : 0);
  });
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
