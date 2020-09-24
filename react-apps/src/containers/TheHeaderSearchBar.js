import React from "react";
import Select from 'react-select';
import {
  CButton,
  CInputGroup,
  CInputGroupPrepend
} from '@coreui/react'
import CIcon from '@coreui/icons-react'

import { getAllUsers, initLandDashboard, asyncGetUserModel } from '../redux/actions/actionCreator'
import { connect } from "react-redux"


class TheHeaderSearchBar extends React.Component {
  state = {
    selectedOption: null,
  };

  handleChange = selectedOption => {
    this.setState({ selectedOption });
    //console.log(`Option selected:`, selectedOption);
  };

  componentDidUpdate = () => {
    this.props.initLandDash()
    this.props.fetchUserPred(this.state.selectedOption['Id'])
  }

  render() {
    const { selectedOption } = this.state;
    return (
      <CInputGroup>
      <CInputGroupPrepend className="pt-2" >
        <CButton type="button" disabled><CIcon name="cil-magnifying-glass" /> </CButton>
      </CInputGroupPrepend>
      <Select
        className="border-none border-white form-control"
        placeholder="Start typing here..."
        value={selectedOption}
        onChange={this.handleChange}
        options={this.props.fetchUsers()['payload']}
        openMenuOnClick={false}
      />
    </CInputGroup>
    );
  }
}

// Connect Redux Store

const mapDispatchToProps = (dispatch) => {
  return {
    fetchUsers: () => dispatch(getAllUsers()),
    fetchUserPred: (id) => dispatch(asyncGetUserModel(id)),
    initLandDash: () => dispatch(initLandDashboard(1))
  }
}

export default connect(
  null,
  mapDispatchToProps
)(TheHeaderSearchBar)