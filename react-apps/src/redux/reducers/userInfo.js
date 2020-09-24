const initialState = [
      { value: '1', label: 'Jane Doe' }
    ]

const userInfo = (state = initialState, { type, payload }) => {
    switch (type) {
      case 'FETCH_ALL_USERS': {
        return state = payload
      }
      default:
        return state
    }   
  }

export default userInfo  