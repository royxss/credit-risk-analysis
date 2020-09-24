import React from 'react'
import {
  CCol,
  CRow
} from '@coreui/react'

import OverallDefaultCounts from '../../components/common/OverallDefaultCounts'
import OverallMemberChurn from '../../components/common/OverallMemberChurn'
import OverallMemberValue from '../../components/common/OverallMemberValue'
import UserAccountDetails from '../../components/user-profile/UserAccountDetails'
import CreditScore from '../../components/user-profile/CreditScore'
import TopSpendings from '../../components/user-profile/TopSpendings'
import ImportantFeatures from '../../components/user-profile/ImportantFeatures'
import PredictedScore from '../../components/user-profile/PredictedScore'
import OtherIndicators from '../../components/user-profile/OtherIndicators'
//import EmptyDashboard from '../../components/utils/EmptyDashboard'
import { useSelector } from 'react-redux'
import { CubeGrid } from 'styled-loaders-react'

//style={{display:'flex', flexDirection: 'row'}}

const Dashboard = () => {

  var initState = useSelector(state => state.initLandDashboard)
  var pageLoad = useSelector(state => state.pageLoading)

  if (initState === 0) {
    return (
      <>
      <OverallDefaultCounts />
      <OverallMemberChurn />
      <OverallMemberValue />
      </>
    )
  }
  else {

    return (
        <>
        {
        pageLoad === 1 ? <CubeGrid color="#0254a1"/> :
          <>
            <CRow>
              <CCol lg xl = "8" sm="12" md="9">
                <CRow>
                  <CCol lg xl = "6" md="4"><UserAccountDetails /></CCol>
                  <CCol lg xl = "6" md="8"><CreditScore /></CCol>
                </CRow>
                <CRow>
                  <CCol><ImportantFeatures/></CCol>
                </CRow>
              </CCol>
              <CCol lg xl = "4" md="3">
                <PredictedScore />
                <OtherIndicators />
                <TopSpendings />
              </CCol>
            </CRow>
          </>
        }
        </>     
    )
}
}  

export default Dashboard
