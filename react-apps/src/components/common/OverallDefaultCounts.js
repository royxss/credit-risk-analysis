import React, {useEffect, useState} from "react";
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
import { useSelector, useDispatch} from 'react-redux'
import { asyncGetOverallStats} from '../../redux/actions/actionCreator'

import MainDropdownTable from '../common/MainDropdownTable'

var usersData = []
const OverallDefaultCounts = () => {

  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(asyncGetOverallStats())
  }, [dispatch])
  

  var userObj = useSelector(state => state.overallDefaultingStat['all_count'])
  var num_default = userObj.num_default
  var good_standing = userObj.good_standing
  var no_information = userObj.no_information

  var data_def = useSelector(state => state.overallDefaultingStat['all_def'])
  var data_non_def = useSelector(state => state.overallDefaultingStat['all_non_def'])
  var data_noinfo_def = useSelector(state => state.overallDefaultingStat['all_noinfo_def'])

  const [left, setleft] = useState(false)
  const [middle, setmiddle] = useState(false)
  const [right, setright] = useState(false)

  var collapse = false
  var datatype = 'def'

  if (left || middle || right) {
    collapse = true
  }


  const lefttoggle = (e) => {
    e.preventDefault()

    // Set others to false
    setmiddle(false)
    setright(false)

    if (left === false && collapse === false) {
      usersData = data_def
      datatype = 'def'

      }
    setleft(!left)  
  }


  const middletoggle = (e) => { 
    e.preventDefault() 

    // Set others to false
    setleft(false)
    setright(false)
    
    if (middle === false && collapse === false) {
      usersData = data_non_def
      datatype = 'ndef'
    }
    setmiddle(!middle)
  }


  const righttoggle = (e) => {  
    e.preventDefault()  

    // Set others to false
    setmiddle(false)
    setleft(false)
    
    if (right === false && collapse === false) {
      usersData = data_noinfo_def
      datatype = 'ninfo'
    }
    setright(!right)
  }

  //console.log("left: "+left+"; middle: "+middle+"; right: "+right)
  //console.log("collapse: "+collapse)
  //console.log(usersData)
  
  return (
    <CCard borderColor="light">
    <CCardHeader color="dark" className="text-white">
      Customer Default Behaviour
      <div className="card-header-actions">
            <CIcon name="cil-check" className="float-right"/>
      </div>
    </CCardHeader>
    <CCardBody color="light">
      <CRow>
          <CCol xl lg md sm="4">
            <CWidgetIcon 
              text="customers may default" 
              header={num_default+''} 
              color="danger" 
              iconPadding={false}
              footerSlot={
                <CCardFooter className="card-footer px-3 py-2">
                    <CButton
                      block 
                      color="link" 
                      className="text-left m-0 p-0 font-weight-bold font-xs" 
                      onClick={lefttoggle}
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
              header={good_standing+''} 
              color="success" 
              iconPadding={false}
              footerSlot={
                <CCardFooter className="card-footer px-3 py-2">
                    <CButton
                      block 
                      color="link" 
                      className="text-left m-0 p-0 font-weight-bold font-xs" 
                      onClick={middletoggle}
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
                      onClick={righttoggle}
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
          <MainDropdownTable data = {usersData} datatype = {datatype} />
      </CCollapse>
  </CCard>
  
);
}

export default OverallDefaultCounts

