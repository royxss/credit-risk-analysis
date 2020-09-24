import React, {useState} from "react";
import {
  CWidgetIcon,
  CCol,
  CCardFooter,
  CRow,
  CCard,
  CCardHeader,
  CCardBody,
  CButton,
  CCollapse
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import MainDropdownTable from '../common/MainDropdownTable'

// Static values
var high_val = 4
var medium_val = 10
var no_information = 6

const OverallMemberValue = () => {

  const [collapse, setCollapse] = useState(false)
  const toggle = (e) => {
    setCollapse(!collapse)
    e.preventDefault()
  }
  
  return (

    <CCard borderColor="light">
    <CCardHeader color="dark" className="text-white">
      Customer Value
      <div className="card-header-actions">
            <CIcon name="cil-check" className="float-right"/>
      </div>
    </CCardHeader>
    <CCardBody color="light">
        <CRow>
            <CCol xl lg md sm="4">
            <CWidgetIcon 
                text="customers are high valued" 
                header={high_val+''} 
                color="success" 
                iconPadding={false}
                footerSlot={
                <CCardFooter className="card-footer px-3 py-2">
                    <CButton
                      block 
                      color="link" 
                      className="text-left m-0 p-0 font-weight-bold font-xs" 
                      onClick={toggle}
                    >
                      View All
                      <CIcon name="cil-arrow-right" className="float-right" width="16"/>  
                    </CButton>
                 </CCardFooter>
                }
            >
                <CIcon width={24} name="cil-user-follow" className="mx-5"/>
            </CWidgetIcon>
            </CCol>
            <CCol xl lg md sm="4">
            <CWidgetIcon 
                text="customers are medium valued" 
                header={medium_val+''} 
                color="warning" 
                iconPadding={false}
                footerSlot={
                <CCardFooter className="card-footer px-3 py-2">
                    <CButton
                      block 
                      color="link" 
                      className="text-left m-0 p-0 font-weight-bold font-xs" 
                      onClick={toggle}
                    >
                      View All
                      <CIcon name="cil-arrow-right" className="float-right" width="16"/>  
                    </CButton>
                 </CCardFooter>
                }
            >
                <CIcon width={24} name="cil-user-unfollow" className="mx-5"/>
            </CWidgetIcon>
            </CCol>
            <CCol xl lg md sm="4">
            <CWidgetIcon 
                text="customers are uncategorized" 
                header={no_information+''} 
                color="info" 
                iconPadding={false}
                footerSlot={
                <CCardFooter className="card-footer px-3 py-2">
                    <CButton
                      block 
                      color="link" 
                      className="text-left m-0 p-0 font-weight-bold font-xs" 
                      onClick={toggle}
                    >
                      View All
                      <CIcon name="cil-arrow-right" className="float-right" width="16"/>  
                    </CButton>
                 </CCardFooter>
                }
            >
                <CIcon width={24} name="cil-bell" className="mx-5"/>
            </CWidgetIcon>
            </CCol>
        </CRow>
    </CCardBody>
        <CCollapse show={collapse}>
          <MainDropdownTable data = {[]} />
        </CCollapse>
  </CCard>
  
);
}

export default OverallMemberValue

