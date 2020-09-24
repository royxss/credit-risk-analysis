var initialState = 0;
const pageLoading = (state = initialState, { type, payload }) => {
    switch (type) {
      case 'PAGE_LOADING': {
        return state = payload
      }
      default:
        return state
    }   
  }

export default pageLoading  