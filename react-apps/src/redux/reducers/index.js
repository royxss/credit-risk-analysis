import { combineReducers } from "redux"

import collapseNav from "./collapseNav"
import userInfo from "./userInfo"
import userModel from './userModel'
import initLandDashboard from './initLandDashboard'
import pageLoading from './pageLoading'
import overallDefaultingStat from './overallDefaultingStat'

export default combineReducers({
    collapseNav,
    userInfo,
    userModel,
    initLandDashboard,
    pageLoading,
    overallDefaultingStat
})