import React from "react";
import {
  CCard,
  CCardBody,
  CCardHeader,
  CForm,
  CFormGroup,
  CInput,
  CInputGroup,
  CInputGroupPrepend,
  CInputGroupText
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { useSelector } from 'react-redux'

const UserAccountDetails = () => {
  var userObj = useSelector(state => state.userModel[0])
  var fname = userObj.first_name
  var lname = userObj.last_name
  var address1 = userObj.address_1
  var address2 = userObj.address_2
  var dob = userObj.dob

  return (
    <CCard accentColor="dark">
    <CCardHeader>
      Account Details
          <div className="card-header-actions">
                <CIcon name="cil-user-follow" className="float-right"/>
          </div>
    </CCardHeader>
    <CCardBody>
      <CForm action="" method="post">
        <CFormGroup>
          <CInputGroup>
            <CInputGroupPrepend>
              <CInputGroupText><CIcon name="cil-user" /></CInputGroupText>
            </CInputGroupPrepend>
            <CInput id="firstname" name="firstname" placeholder={fname} />
            <CInput id="lastname" name="lastname" placeholder={lname}/>
          </CInputGroup>
        </CFormGroup>
        <CFormGroup>
          <CInputGroup>
            <CInputGroupPrepend>
              <CInputGroupText><CIcon name="cil-envelope-closed" /></CInputGroupText>
            </CInputGroupPrepend>
            <CInput type="address" id="address" name="address" placeholder={address1}/>
          </CInputGroup>
        </CFormGroup>
        <CFormGroup>
          <CInputGroup>
            <CInputGroupPrepend>
              <CInputGroupText><CIcon name="cil-location-pin" /></CInputGroupText>
            </CInputGroupPrepend>
            <CInput type="city" id="city" name="city" placeholder={address2}/>
          </CInputGroup>
        </CFormGroup>
        <CFormGroup>
          <CInputGroup>
            <CInputGroupPrepend>
              <CInputGroupText><CIcon name="cil-calendar" /></CInputGroupText>
            </CInputGroupPrepend>
            <CInput type="dob" id="dob" name="dob" placeholder={dob}/>
          </CInputGroup>
        </CFormGroup>
      </CForm>
    </CCardBody>
  </CCard>
  );
}

export default UserAccountDetails;
