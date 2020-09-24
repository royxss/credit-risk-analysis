
import React from 'react'
import {
  CCard,
  CCardBody,
  CCol,
  CDataTable,
  CRow,
  CButton,
  CProgress
} from '@coreui/react'
import { initLandDashboard, asyncGetUserModel } from '../../redux/actions/actionCreator'
import { useDispatch} from 'react-redux'

//const fields = ['id', 'name', 'state', 'score', 'profile']
const fields = [
  { key: 'id', _style: { width: '5%'} },
  { key: 'name', _style: { width: '20%'} },
  { key: 'address', _style: { width: '20%'} },
  { key: 'default_score', _style: { width: '30%'} },
  {
    key: 'show_details',
    label: '',
    _style: { width: '10%' },
    sorter: false,
    filter: false,
  }
]

const getColor = (status)=>{
  switch (status) {
    case 'ndef': return 'success'
    case 'ninfo': return 'warning'
    case 'def': return 'danger'
    default: return 'primary'
  }
}

const MainDropdownTable = (props) => {

  var data = props.data
  var datatype = props.datatype
  //console.log(props)

  var userData = []

  data.map((itm) => {
    return (
      userData.push(
        {
          'id': itm.id,
          'name': itm.name,
          'address': itm.address,
          'score': itm.prob
        }
      )
    )
  })

  const dispatch = useDispatch()

  const viewProfile = (id) => {  
    dispatch(asyncGetUserModel(id)) 
    dispatch(initLandDashboard(1))
    //console.log("View Profile id: "+id)
  }

    return (
        <CRow>
            <CCol>
                <CCard>
                    <CCardBody>
                    <CDataTable
                    items={userData}
                    fields={fields}
                    columnFilter
                    tableFilter
                    
                    itemsPerPageSelect
                    itemsPerPage={5}
                    hover
                    
                    
                    
                    
                    bordered
                    size="sm"
                    
                    pagination
                    scopedSlots = {{
                      'default_score':
                      (item)=>(
                            <td>
                              <div className="clearfix">
                                <div className="float-right">
                                  <strong className="text-muted">{item.score+'%'}</strong>
                                </div>
                              </div>
                              <CProgress className="progress-xs" color={getColor(datatype)} value={item.score+''} animated/>
                            </td>
                      ),
                        'show_details':
                        (item)=>{
                          return (
                            <td className="py-2">
                              <CButton
                                color="primary"
                                //variant="outline"
                                shape="badge"
                                size="sm"
                                className="float-right"
                                onClick={()=>{viewProfile(item.id)}}
                              >
                                View Profile
                              </CButton>
                            </td>
                            )
                        }
                    }}
                    />
                    </CCardBody>
                </CCard>
            </CCol>
        </CRow>
    )
                }

export default MainDropdownTable