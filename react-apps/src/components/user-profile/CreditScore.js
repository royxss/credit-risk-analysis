import React from 'react'
import {
  CCard,
  CCardBody,
  CCardHeader
} from '@coreui/react'
import CIcon from '@coreui/icons-react'

import GaugeChart from 'react-gauge-chart'
import { useSelector } from 'react-redux'

const CreditScore = () => {
  var score = useSelector(state => state.userModel[0].credit_score)
  if (typeof score === 'string' ){
    score = 0
  }

  return (

      <CCard accentColor="dark">
        <CCardHeader>
          Credit Score
          <div className="card-header-actions">
                <CIcon name="cil-check" className="float-right"/>
          </div>
        </CCardHeader>
        <CCardBody>
        <GaugeChart id="gauge-chart2" 
          nrOfLevels={20} 
          percent={score/1000} 
          textColor= '#464A4F'
          formatTextValue={value => value*10 + '/850'}
          
        />
        </CCardBody>
      </CCard>
  )
}

export default CreditScore
