import React from "react";
import { useSelector, useDispatch } from "react-redux";
import {
  CCreateElement,
  CSidebar,
  CSidebarBrand,
  CSidebarNav,
  CSidebarNavDivider,
  CSidebarNavTitle,
  CSidebarMinimizer,
  CSidebarNavDropdown,
  CSidebarNavItem,
} from "@coreui/react";

import { collapseNav } from "../redux/actions/actionCreator";
import CIcon from "@coreui/icons-react";

// sidebar nav config
//width:"256px", height:"56px"
import navigation from "./_nav";

const TheSidebar = () => {
  const dispatch = useDispatch();
  const show = useSelector((state) => state.collapseNav.sidebarShow);

  return (
    <CSidebar
      show={show}
      //onShowChange={(val) => dispatch({type: 'set', sidebarShow: val })}
      onShowChange={(val) => dispatch(collapseNav(val))}
    >
      <CSidebarBrand className="d-md-down-none" to="/">
        <CIcon
          className="c-sidebar-brand-full"
          name="logo-negative"
          height={35}
        />
        <CIcon
          className="c-sidebar-brand-minimized"
          name="sygnet"
          height={35}
        />
      </CSidebarBrand>
      <CSidebarNav>
        <CCreateElement
          items={navigation}
          components={{
            CSidebarNavDivider,
            CSidebarNavDropdown,
            CSidebarNavItem,
            CSidebarNavTitle,
          }}
        />
      </CSidebarNav>
      <CSidebarMinimizer className="c-d-md-down-none" />
    </CSidebar>
  );
};

export default React.memo(TheSidebar);
