
import { initLandDashboard } from '../../redux/actions/actionCreator'
import { useDispatch} from 'react-redux'


const ResetDashboardState = () => {

  const dispatch = useDispatch()
  dispatch(initLandDashboard(0))
  //console.log("Here")
  return null
}

export default ResetDashboardState