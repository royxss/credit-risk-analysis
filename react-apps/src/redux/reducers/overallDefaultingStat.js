var initialState = 
  { 'all_count':
    {
      "num_default": 0,
      "good_standing": 0,
      "no_information": 0
    }
  }


const overallDefaultingStat = (state = initialState, { type, payload }) => {
  switch (type) {
    case 'FETCH_ALL_STATS': {
      return {...state, 'all_count': payload[0]}
    }
    case 'FETCH_ALL_DEF_STATS': {
      return {...state, 'all_def': payload}
    }
    case 'FETCH_ALL_NONDEF_STATS': {
      return {...state, 'all_non_def': payload}
    }
    case 'FETCH_ALL_NOINFO_STATS': {
      return {...state, 'all_noinfo_def': payload}
    }
    default:
      return state
  }   
}

export default overallDefaultingStat  