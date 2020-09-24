const initialState = require('../../data/data-backend-init.json')

const userModel = (state = initialState, { type, payload }) => {
  switch (type) {
    case 'FETCH_USER_PRED': {
      return state = payload
    }
    default:
      return state
  }   
}

export default userModel  