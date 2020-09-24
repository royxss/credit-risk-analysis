import React from 'react'
import {
  CCard,
  CCardHeader,
  CCardBody,
  CWidgetProgressIcon,
  CProgress
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import {useSelector} from 'react-redux'

const OtherIndicators = () => {
  var userObj = useSelector(state => state.userModel[0].other_indicators)
  var debt_ratio = userObj.debt_ratio.value
  var credit_utilization = userObj.credit_utilization.value
  // render
  return (
    <CCard accentColor="dark">
      <CCardHeader>
        Other Indicators
          <div className="card-header-actions">
                <CIcon name="cil-credit-card" className="float-right"/>
          </div>
      </CCardHeader>

      <CCardBody>
      <CWidgetProgressIcon
            header={debt_ratio+'%'}
            text="Debt to Income Ratio - Recommended < 43%"
            color="gradient-dark"
            inverse
            progressSlot={
              <>
              <CProgress color="success" style={{height: "15px"}} value={debt_ratio} animated className="my-3" size="xs" />
              <CProgress color="warning" style={{height: "3px"}} value={43} className="mb-3" />
              </>
            }
      >
      </CWidgetProgressIcon>
      <CWidgetProgressIcon
            header={credit_utilization+'%'}
            text="Credit Utilization - Recommended < 10%"
            color="gradient-dark"
            inverse
            progressSlot={
            <>
            <CProgress color="success" style={{height: "15px"}} value={credit_utilization} animated className="my-3" size="xs" />
            <CProgress color="warning" style={{height: "3px"}} value={10} className="mb-3" />
            </>
          }
      >
      </CWidgetProgressIcon>

      </CCardBody>
    </CCard>  

  )
}

export default OtherIndicators
