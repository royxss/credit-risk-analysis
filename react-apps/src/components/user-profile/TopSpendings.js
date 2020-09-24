import React from "react";
import {
  CCard,
  CCardBody,
  CCardHeader,
  CProgress
} from '@coreui/react'
import { useSelector } from 'react-redux'
import CIcon from '@coreui/icons-react'

const TopSpendings = () => {
  var userObj = useSelector(state => state.userModel[0].top_spendings)
  var sumValues = Object.values(userObj).reduce((a, b) => a + b)

  // Avoid division by zero
  if (sumValues===0){
      sumValues = 0.00001
  }
  
  return (
  <CCard accentColor="dark">
    <CCardHeader>
      Top Spendings
          <div className="card-header-actions">
                <CIcon name="cil-dollar" className="float-right"/>
          </div>
    </CCardHeader>
    <CCardBody>
      {Object.entries(userObj).map(([spend_item, spend_amt], id) => (
        
        <React.Fragment key={id}>

          <div className="progress-group">
            <div className="progress-group-header">
              <span className="title">{spend_item }</span>
              <span className="ml-auto font-weight-bold">{spend_amt} <span className="text-muted small">{"("+(spend_amt*100/sumValues).toFixed(1)+"%)"}</span></span>
            </div>
            <div className="progress-group-bars">
              <CProgress className="progress-xs" color="success" value={spend_amt*100/sumValues} style={{height: "5px"}} animated/>
            </div>
          </div>

        </React.Fragment>
      ))}

    </CCardBody>
  </CCard>
);
}

export default TopSpendings;

