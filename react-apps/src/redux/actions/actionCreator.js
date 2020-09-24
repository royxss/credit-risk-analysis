//////////////////////////////////////////////////////////////////////////////////////////
//                        Import Libraries
//////////////////////////////////////////////////////////////////////////////////////////
import axios from 'axios';
const user_info = require('../../data/user-data.json')
const dummy_defaulted_users = require('../../data/data-backend-alldefaulted.json')
const data_backend = require('../../data/data-backend.json')
const data_def_count = require('../../data/data-backend-stat.json')

//////////////////////////////////////////////////////////////////////////////////////////
//                        API and action for backend user queries
//////////////////////////////////////////////////////////////////////////////////////////

export function asyncGetUserModel(id) {

  const API = '/iv/?id='+id
  //const API = 'https://jsonplaceholder.typicode.com/users'

  return (dispatch) => {
      axios.get(API)
      .then(dispatch(pageLoading(1)))
      .then(response => {
          const user_pred = response.data
          dispatch(getUserModel(user_pred))
          dispatch(pageLoading(0))
          //setTimeout(() => {
          //  dispatch(getUserModel(user_pred))
          //}, 3000)             
    })
    .catch(() => {
      dispatch(pageLoading(0)) 
      // Default to initial state
      //console.log("API cannot be called. Defaulting to a dummy user...")
      dispatch(getUserModel(data_backend))
    })
}
}

export function getUserModel(user_pred) {
      return {
        type: "FETCH_USER_PRED",
        payload: user_pred
      }
  }

//////////////////////////////////////////////////////////////////////////////////////////
//                        API and action for over statistics
//////////////////////////////////////////////////////////////////////////////////////////

export function asyncGetOverallStats() {
    const API_OverallStat = '/overall_stat/'

    return (dispatch) => {
      axios.get(API_OverallStat)
      //axios.get('https://jsonplaceholder.typicode.com/users')
      .then(response => {
            const stat = response.data
            dispatch({
              type: "FETCH_ALL_STATS",
              payload: stat
            })        
      })
      // Call subsequent dispatches in sequence
      .then(dispatch(asyncGetAllDefaulters()))
      .then(dispatch(asyncGetAllNonDefaulters()))
      .then(dispatch(asyncGetAllMissingInfo()))
      .catch(() => {
          //console.log("API cannot be called. Defaulting to dummy stats...")
          dispatch({
            type: "FETCH_ALL_STATS",
            payload: data_def_count
          })
      })
  }
}


export function asyncGetAllDefaulters() {
    const API_alldef = '/defaulter_info/'

    return (dispatch) => {
      axios.get(API_alldef)
        .then(response => {
            const stat_default = response.data
            dispatch({
                type: "FETCH_ALL_DEF_STATS",
                payload: stat_default
              })             
      })
      .catch(() => {
        // Default to initial state
        //console.log("API cannot be called. Defaulting to dummy defaulted values...")
        dispatch({
            type: "FETCH_ALL_DEF_STATS",
            payload: dummy_defaulted_users
          })
        
      })
  }
  } 

  export function asyncGetAllNonDefaulters() {
    const API_allnondef = '/good_standing_info/'

    return (dispatch) => {
      axios.get(API_allnondef)
        .then(response => {
            const stat_default = response.data
            dispatch({
                type: "FETCH_ALL_NONDEF_STATS",
                payload: stat_default
              })             
      })
      .catch(() => {
        // Default to initial state
        //console.log("API cannot be called. Defaulting to dummy defaulted values...")
        dispatch({
            type: "FETCH_ALL_NONDEF_STATS",
            payload: dummy_defaulted_users
          })
        
      })
  }
  } 

  export function asyncGetAllMissingInfo() {
    const API_allmissinfo = '/no_information_info/'

    return (dispatch) => {
      axios.get(API_allmissinfo)
        .then(response => {
            const stat_default = response.data
            dispatch({
                type: "FETCH_ALL_NOINFO_STATS",
                payload: stat_default
              })             
      })
      .catch(() => {
        // Default to initial state
        //console.log("API cannot be called. Defaulting to dummy defaulted values...")
        dispatch({
            type: "FETCH_ALL_NOINFO_STATS",
            payload: dummy_defaulted_users
          })
        
      })
  }
  } 
   

//////////////////////////////////////////////////////////////////////////////////////////
//                        Action for fetching all local users
//////////////////////////////////////////////////////////////////////////////////////////    

export function getAllUsers() {
  // do axios get for component will mount

  user_info.forEach((user_info) => {
    user_info['value']=user_info['Id'];
    user_info['label']=user_info['First Name'] + " " + user_info['Last Name'];
  })

  return {
    type: "FETCH_ALL_USERS",
    payload: user_info
  }
}


//////////////////////////////////////////////////////////////////////////////////////////
//                        Action for miscellaneous
//////////////////////////////////////////////////////////////////////////////////////////

export function collapseNav(val) {
  return {
    type: "set",
    sidebarShow: val
  }
}


export function initLandDashboard(val) {
  return {
    type: "SHOW_EMPTY_DASH",
    payload: val
  }
}

export function pageLoading(val) {
  return {
    type: "PAGE_LOADING",
    payload: val
  }
}
