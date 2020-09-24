import React from 'react';
import { Redirect } from "react-router-dom";

const Dashboard = React.lazy(() => import('./views/dashboard/Dashboard'));

const routes = [
  { path: '/', exact:true, name: 'Home', component: () => <Redirect to="/dashboard" />},
  { path: '/dashboard', name: 'Dashboard', component: Dashboard }
];

export default routes;
