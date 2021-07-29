import React, { Component, Fragment } from 'react';

import UploadView from './pages/uploadview/UploadView'
import Button from '@material-ui/core/Button';
import ResultView from './pages/resultview/ResultView'
import NewStatusView from './pages/resultview/ResultView'
import StepperBar from './components/stepperBar/StepperBar'
import logo from './logo.svg';
import GroupWorkIcon from '@material-ui/icons/GroupWork';
import { PrivateRoute } from "./PrivateRoute.jsx";
import './App.css';
import './Main.scss'
import './stylesheets/_globalimports.scss';
import UserProfile from './UserProfile';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';
import { getUserName, getToken } from './auth.js';
import ExitToAppIcon from '@material-ui/icons/ExitToApp';
import { options } from './pages/uploadview/UploadView'
import axios from 'axios';
import Loader from "./components/common/loader/Loader"
import { useHistory } from "react-router-dom";


import { connect } from 'react-redux'
import { Route, Redirect, Switch, withRouter, RouteComponentProps } from 'react-router-dom'
import store from './redux/store';
import PeopleIcon from '@material-ui/icons/People';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';

class Main extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeStep: 0,
      results: { 'data': [] },
      loading: false,
      selectedModel: "",
      allDocsLoaded: false,
      jds: [],
      cvs: [],
      sessionId: ''
    }
  }

  changeActiveStep = () => {

    const {
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

    const {
      loading
    } = this.state
    this.setState({
      loading: !loading
    })

  }
  handleModelSelection = (model) => {
    const {
      selectedModel
    } = this.state

    this.setState({
      selectedModel: model
    })
  }

  addJds = (jd) => {
    this.setState({
      jds: jd
    })
  }

  addCvs = (cv) => {
    this.setState({
      cvs: cv
    })
  }

  setSessionId = (session_id) => {
    this.setState({
      sessionId: session_id
    })
  }

  handleUploadImage = () => {
    const { cvs, jds, sessionId, selectedModel } = this.state

    var formData = new FormData();
    cvs.map(cv => {
      formData.append("cv", cv)
    })

    jds.map(jd => {
      formData.append("jd", jd)
    })
    formData.append("session_id", sessionId)
    this.toggleLoading()
    axios.post(`http://127.0.0.1:4000/${selectedModel}`, formData, {
      headers: {
        'Authorization': `Bearer ${getToken()}`,
        'Content-Type': 'multipart/form-data',
        'X-Requested-With': 'XMLHttpRequest',//CORS fixes client side
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
      }
    }).then(res => {
      if (res.status === 200) {
        this.setResults(res['data'])
        this.toggleLoading()

      }
    })
}

render() {

  const {
    storeState
  } = this.props

  const {
    activeStep,
    results,
    loading,
    selectedModel,
    allDocsLoaded,
    jds,
    cvs,
    sessionId
  } = this.state

  //console.log(storeState)

  return (
    <div className="Main">

      <div className="header">
        <StepperBar
          activeStep={activeStep}
          changeActiveStep={this.changeActiveStep}
        />
      </div>


      <div className="body" style={{ height: "100%" }}>
        <div className="user-profile-header">
          <AccountCircleIcon /><span>{getUserName()}</span>
          {/* <ExitToAppIcon onClick={deleteTokens(), window.location.reload()}/> */}
        </div>
        {
          activeStep === 0 ? <UploadView
            changeActiveStep={this.changeActiveStep}
            viewType={"JD"}
            key={"JD"}
            jds={jds}
            addJds={this.addJds}
            setResults={this.setResults}
            sessionId={sessionId}
            setSessionId={this.setSessionId}
            toggleLoading={this.toggleLoading}
            loading={loading}
            selectedModel={selectedModel}
            handleModelSelection={this.handleModelSelection}
            allDocsLoaded={allDocsLoaded}
            toggleAllDocsLoaded={() => {
              this.setState({
                allDocsLoaded: !allDocsLoaded
              })
            }}
          /> : activeStep === 1 ? <UploadView
            changeActiveStep={this.changeActiveStep}
            setResults={this.setResults}
            toggleLoading={this.toggleLoading}
            viewType={"CV"}
            key={"CV"}
            addCvs={this.addCvs}
            cvs={cvs}
            jds={jds}
            sessionId={sessionId}
            setSessionId={this.setSessionId}
            selectedModel={selectedModel}
            handleModelSelection={this.handleModelSelection}
            allDocsLoaded={allDocsLoaded}
            toggleAllDocsLoaded={() => console.log("lol")}
            loading={loading}
          /> : <Fragment>
                <div className="upload-bar-main">
                  <FormControl>
                    <InputLabel id="demo-simple-select-label">Models</InputLabel>
                    <Select
                      labelId="demo-simple-select-label"
                      id="demo-simple-select"
                      classes={{ root: "model-select" }}
                      value={selectedModel}
                      onChange={(event) => {
                        this.handleModelSelection(event.target.value)
                      }}
                    >
                      {
                        options.map(option => {
                          return <MenuItem key={option.id} value={option.id}>{option.name}</MenuItem>
                        })
                      }
                    </Select>
                  </FormControl>

                  <div className="process-button-container">
                    <Button


                      variant="contained"
                      //disabled={jds.length > 0 ? false: true}
                      classes={jds.length > 0 ? { root: "process-button-active" } : { root: "process-button-inactive" }}
                      onClick={(e) => this.handleUploadImage()}
                    >
                      Process
              </Button>

                  </div>
                </div>
                {loading ? <Loader/>:<ResultView
                  results={results}
                  jds={jds}
                  cvs={cvs}
                />}
                </Fragment>
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
