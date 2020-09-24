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

// Static value
var pos_churn = 2
var neg_churn = 16
var no_information = 2

const OverallMemberChurn = () => {

  const [collapse, setCollapse] = useState(false)
  const toggle = (e) => {
    setCollapse(!collapse)
    e.preventDefault()
  }
  
  return (
    <CCard borderColor="light">
    <CCardHeader color="dark" className="text-white">
      Customer Churn Behaviour
      <div className="card-header-actions">
            <CIcon name="cil-check" className="float-right"/>
      </div>
    </CCardHeader>
    <CCardBody color="light">
        <CRow>
            <CCol xl lg md sm="4">
            <CWidgetIcon 
                text="customers may churn" 
                header={pos_churn+''} 
                color="danger" 
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
                <CIcon width={24} name="cil-warning" className="mx-5"/>
            </CWidgetIcon>
            </CCol>
            <CCol xl lg md sm="4">
            <CWidgetIcon 
                text="customers have good standing" 
                header={neg_churn+''} 
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
                <CIcon width={24} name="cil-bell" className="mx-5"/>
            </CWidgetIcon>
            </CCol>
            <CCol xl lg md sm="4">
            <CWidgetIcon 
                text="customers with no information" 
                header={no_information+''} 
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

export default OverallMemberChurn

