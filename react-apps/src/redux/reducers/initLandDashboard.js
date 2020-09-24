var initialState = 0;
const initLandDashboard = (state = initialState, { type, payload }) => {
    switch (type) {
      case 'SHOW_EMPTY_DASH': {
        return state = payload
      }
      default:
        return state
    }   
  }

export default initLandDashboard  