import React from 'react'
import {
  CCard,
  CCardHeader,
  CCardBody,
  CWidgetBrand,
  CWidgetProgressIcon,
  CProgress,
  CBadge
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import {useSelector} from 'react-redux'

//style={{display:'flex', flexDirection: 'row'}}
const customcolors = {
  'text-type': {
    'Yes': 'danger',
    'No': 'success',
    'NA': 'warning'
  }
}

const PredictedScore = () => {
  var userObj = useSelector(state => state.userModel[0].user_predictions)
  var proba_score = userObj.DefaultScore
  var threshold = userObj.ProbabilisticCutoff
  var tpr = userObj.TruePositiveRate
  var fnr = userObj.FalseNegativeRate
  var verdict

  if (proba_score === 0){
    verdict = 'NA'
  } else if (proba_score > threshold) {
    verdict = 'Yes'
  } else {
    verdict = 'No'
  }

  // render
  return (
    <CCard accentColor="dark">
      <CCardHeader>
        Predictive Score
          <div className="card-header-actions">
                <CIcon name="cil-graph" className="float-right"/>
          </div>
      </CCardHeader>

      <CCardBody>
      <CWidgetProgressIcon
            header={
            <CBadge shape="pill" color={customcolors['text-type'][verdict]} className="float-right">{verdict}</CBadge>
            }
            text="Chance of Defaulting"
            color="gradient-dark"
            inverse
            progressSlot={
            <CProgress color={customcolors['text-type'][verdict]} size="xs" value={proba_score} animated className="my-3"
            />}
      >
      </CWidgetProgressIcon>
      <CWidgetBrand
        // the '' has been added simply to remove console warnings for data types
        rightHeader={tpr+''}
        rightFooter="True positive rate"
        leftHeader={fnr+''}
        leftFooter="false negative rate"
        style = {{display:'flex', height: '5 px'}}
      >
      </CWidgetBrand>
      </CCardBody>
    </CCard>  

  )
}

export default PredictedScore
