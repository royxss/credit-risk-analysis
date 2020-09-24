import React from 'react'
import {
  CCol,
  CContainer,
  CRow
} from '@coreui/react'

const EmptyDashboard = () => {
  return (
    <div className="align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md="6">
              <h4 className="pt-3">Please search for a customer...</h4>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default EmptyDashboard
