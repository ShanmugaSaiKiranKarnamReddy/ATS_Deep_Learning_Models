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
import './stylesheets/_globalimports.scss';
import UserProfile from './UserProfile';


import { connect } from 'react-redux'
import { Route, Redirect, Switch, withRouter, RouteComponentProps } from 'react-router-dom'
import store from './redux/store';
import PeopleIcon from '@material-ui/icons/People';
import { v4 as uuidv4 } from 'uuid';


class Main extends Component {
  constructor(props){
    super(props);
    this.state = {
      activeStep: 0,
      results:null,
      loading: false,
      userName: "Vicky"
    }
    //this.id = _.uniqueId("prefix-");
    // if (window.performance) {
    //   if (performance.navigation.type == 1) {
    //     alert( "This page is reloaded" );
    //   } else {
    //     alert( "This page is not reloaded");
    //   }
    // }
    UserProfile.setName(this.state.userName, uuidv4());
  }

  changeActiveStep = () =>{

    const{
      activeStep
    } = this.state
    this.setState({
      activeStep: activeStep + 1 
    })
  }

  setResults = (results) => {
    

    this.setState({
      results: results 
    })

  }

  toggleLoading = () => {

    const{
      loading
    } = this.state
    this.setState({
      loading: !loading
    })
    
  }

  render(){

    const{
      storeState
    } = this.props

    const{
      activeStep,
      results,
      loading
    } = this.state

    //console.log(storeState)

    return (
      <div className="App">

        <div className="header">
          <StepperBar
            activeStep={activeStep}
            changeActiveStep={this.changeActiveStep}
          />
        </div>


        {/* <Button onClick={this.changeActiveStep}>
          Next
        </Button> */}


        <div className="body" style={{ height: "100%" }}>
          {/* <div style={{ display: "flex", float: "right", marginTop: "-20px", marginRight: "30px" }}>
            <PeopleIcon /><span style={{ marginLeft: "10px" }}>Team AVSRF</span>
          </div> */}
          {
            activeStep === 0 ? <UploadView
              changeActiveStep={this.changeActiveStep}
              viewType={"JD"}
              setResults={this.setResults}
              toggleLoading={this.toggleLoading}
              loading={loading}
            /> : activeStep === 1 ? <UploadView
              changeActiveStep={this.changeActiveStep}
              setResults={this.setResults}
              toggleLoading={this.toggleLoading}
              viewType={"CV"}
              loading={loading}
            /> : <ResultView
                  results={results}
                />
          }

        </div>



      </div>
    );
  }
  
}

// const mapStateToProps = (state) => {
//   return {
//     storeState: state
//   }
// }

// const mapDispatchToProps = (dispatch) => {
//   return {
    
//   }
// }

export default Main
