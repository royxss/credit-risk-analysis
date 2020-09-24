import React from "react";

import {
  CWidgetProgressIcon,
  CCard,
  CCardBody,
  CCardHeader,
  CCol,
  CRow,
  CCallout,
  CBadge
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import {useSelector} from 'react-redux'

const ImportantFeatures = () => {

  var userObj = useSelector(state => state.userModel[0].feature_importance)

  if (userObj.length === 0) {

      return (
        <>
          <CCard accentColor="dark">
            <CCardHeader>
              Important Features
                <div className="card-header-actions">
                      <CIcon name="cil-applications-settings" className="float-right"/>
                </div>
            </CCardHeader>
            <CCardBody color="gradient-light">
              <div className="float-center">No information available...</div>
            </CCardBody>
            </CCard>
        </>
      )

  } else {

      // create chunks of 2 from a list to arrange fragments into 2 columns and 3 rows
      const chunk = (arr, size) =>
      Array.from({ length: Math.ceil(arr.length / size) }, (v, i) =>
        arr.slice(i * size, i * size + size)
      );
      const nuserObj = chunk(userObj, 2)

      // set colors
      const customcolors = {
        'text-type': {
          'high': 'danger',
          'medium': 'warning',
          'low': 'info',
          'bad': 'danger',
          'good': 'success'
        }
      }
      
      return (
      <>
        <CCard accentColor="dark">
          <CCardHeader>
            Important Features
              <div className="card-header-actions">
                    <CIcon name="cil-applications-settings" className="float-right"/>
              </div>
          </CCardHeader>
          <CCardBody color="gradient-light">
            {nuserObj.map((itm, index) => (
              <React.Fragment key={index}>
                <CRow>
                  <CCol xs="12" md="6" xl="6">
                  <CWidgetProgressIcon
                  // the '' has been added simply to remove console warnings for data types
                  header={
                    <>
                    {itm[0].value+''}
                    <CBadge 
                    color={customcolors['text-type'][itm[0].impact]} className="float-right"
                    >
                      {itm[0].impact[0].toUpperCase() + itm[0].impact.substr(1) + " Impact"}
                      </CBadge>
                    </>
                  }
                  text={itm[0].feature}
                  progressSlot = {
                    <CCallout color={customcolors['text-type'][itm[0].performance]}>
                      <h5 style={{color: "#928693"}}>{itm[0].text}</h5>
                    </CCallout>
                  }
                >
                  </CWidgetProgressIcon>
                  </CCol>

                  <CCol xs="12" md="6" xl="6">
                  <CWidgetProgressIcon
                  // the '' has been added simply to remove console warnings for data types
                  header={
                    <>
                    {itm[1].value+''}
                    <CBadge 
                    color={customcolors['text-type'][itm[1].impact]} className="float-right"
                    >
                      {itm[1].impact[0].toUpperCase() + itm[1].impact.substr(1) + " Impact"}
                      </CBadge>
                    </>
                  }
                  text={itm[1].feature}
                  progressSlot = {
                    <CCallout color={customcolors['text-type'][itm[1].performance]}>
                      <h5 style={{color: "#928693"}}>{itm[1].text}</h5>
                    </CCallout>
                  }
                >
                </CWidgetProgressIcon>
                  </CCol>
                  
                </CRow>

            </React.Fragment>
          ))}
            </CCardBody>
          </CCard>
      </>
    );
    }
}

export default ImportantFeatures;
