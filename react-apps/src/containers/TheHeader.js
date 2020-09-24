import React from 'react'
import { useSelector, useDispatch } from 'react-redux'
import {
  CHeader,
  CToggler,
  CHeaderNav,
  CSubheader,
  CBreadcrumbRouter,
  CLink,
  CHeaderNavItem
} from '@coreui/react'
import CIcon from '@coreui/icons-react'

// routes config
import allroutes from '../routes'

import { 
  TheHeaderDropdown,
  TheHeaderDropdownMssg,
  TheHeaderDropdownNotif,
  TheHeaderSearchBar
}  from './index'

// subscribe to store
//import store from '../redux/store'
//store.subscribe(() => {
//  console.log(store.getState())
//})
import {collapseNav} from '../redux/actions/actionCreator'


const TheHeader = () => {
  const dispatch = useDispatch()
  const sidebarShow = useSelector(state => state.collapseNav.sidebarShow)
  

  const toggleSidebar = () => {
    const val = [true, 'responsive'].includes(sidebarShow) ? false : 'responsive'
    //dispatch({type: 'set', sidebarShow: val })
    dispatch(collapseNav(val))
  }

  const toggleSidebarMobile = () => {
    const val = [false, 'responsive'].includes(sidebarShow) ? true : 'responsive'
    //dispatch({type: 'set', sidebarShow: val })
    dispatch(collapseNav(val))
  }

  return (
    <CHeader withSubheader>
      <CToggler
        inHeader
        className="ml-md-3 d-lg-none"
        onClick={toggleSidebarMobile}
      />
      <CToggler
        inHeader
        className="ml-3 d-md-down-none"
        onClick={toggleSidebar}
      />

      <CHeaderNav className="mr-auto d-inline w-50">
        <CHeaderNavItem >
          <TheHeaderSearchBar />
        </CHeaderNavItem>
      </CHeaderNav>

      <CHeaderNav className="px-3">
        <TheHeaderDropdownNotif/>
        <TheHeaderDropdownMssg/>
        <TheHeaderDropdown/>
      </CHeaderNav>

      <CSubheader className="px-3 justify-content-between">
        <CBreadcrumbRouter 
          className="border-0 c-subheader-nav m-0 px-0 px-md-3" 
          routes={allroutes} 
        />
          <div className="d-md-down-none mfe-2 c-subheader-nav">
            <CLink className="c-subheader-nav-link"href="#">
              <CIcon name="cil-speech" alt="Settings" />
            </CLink>
            <CLink 
              className="c-subheader-nav-link" 
              aria-current="page" 
              to="/dashboard"
            >
              <CIcon name="cil-graph" alt="Dashboard" />&nbsp;Dashboard
            </CLink>
            <CLink className="c-subheader-nav-link" href="#">
              <CIcon name="cil-settings" alt="Settings" />&nbsp;Settings
            </CLink>
          </div>
      </CSubheader>
    </CHeader>
  )
}

export default TheHeader
