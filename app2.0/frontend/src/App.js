import React, {Component} from 'react';

import UploadView from './pages/uploadview/UploadView'
import Button from '@material-ui/core/Button';
import ResultView from './pages/resultview/ResultView'
import NewStatusView from './pages/resultview/ResultView'
import StepperBar from './components/stepperBar/StepperBar'
import logo from './logo.svg';
import GroupWorkIcon from '@material-ui/icons/GroupWork';
import { PrivateRoute } from "./PrivateRoute.jsx";
import './App.css';
import './stylesheets/_globalimports.scss'
import {isLoggedIn} from './auth.js';

import Login from './login.jsx';
import Main from './Main'

import { connect } from 'react-redux'
import { Route, Redirect, Switch, withRouter, RouteComponentProps, BrowserRouter as Router } from 'react-router-dom'
import store from './redux/store';
import PeopleIcon from '@material-ui/icons/People';

const Home = ()=> <h3>Logged in as {localStorage.getItem("username")}</h3>


export default class App extends Component{
  render(){
    return(
      <Router>
        <div className="route">
          <PrivateRoute exact isloggedin={isLoggedIn()} path="/" component={Main} />
          <Route exact path="/login" component={Login} />
      </div>
    </Router>
      )
  }
}