import React, { Component, Fragment } from 'react';
import TextField from '@material-ui/core/TextField'
import Button from '@material-ui/core/Button';
import "./upload-bar.scss"
import { DropzoneArea } from 'material-ui-dropzone'
import { getUserName, getToken } from '../../auth.js';

import { DropzoneDialog } from 'material-ui-dropzone'
import { makeStyles } from '@material-ui/core/styles';
import axios from 'axios';
import UserProfile from '../../UserProfile';
import ButtonGroup from '@material-ui/core/ButtonGroup';


class UploadBar extends Component {

  constructor(props) {
    super(props);
    this.state = {
      jds: [],
      cvs: [],
      sessionId: ''
    };
  }


  handleUploadImage(ev) {

    const {
      
    } = this.state

    const {
      changeActiveStep,
      viewType,
      setResults,
      toggleLoading,
      loading,
      toggleAllDocsLoaded,
      selectedModel,
      jds,
      cvs,
      sessionId,
      setSessionId
    } = this.props
    //ev.preventDefault();

    if (viewType === "JD") {
      changeActiveStep()
    } else if (viewType === "CV"){




      // toggleLoading()
      toggleAllDocsLoaded()

      var formData = new FormData();
      cvs.map(cv => {
        formData.append("cv", cv)
      })

      jds.map(jd => {
        formData.append("jd", jd)
      })
      axios.get('http://127.0.0.1:4000/start', {
        headers: {
          'Authorization': `Bearer ${getToken()}`,
          'Content-Type': 'multipart/form-data',
          'X-Requested-With': 'XMLHttpRequest',//CORS fixes client side
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
        }
      }).then(res => {
        if (res.status === 200) {
          // this.setState({sessionId: res['data']['session_id']})
          formData.append("session_id", res['data']['session_id'])
          setSessionId(res['data']['session_id'])
          toggleLoading()
          console.log(formData)
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
              setResults(res['data'])
              changeActiveStep()
              toggleLoading()
            }
          })
        }

      })

    }

  }


  handleDropboxChange = (files) => {
    const {
      viewType,
      changeActiveStep,
      jds,
      cvs,
      addJds,
      addCvs
    } = this.props
    console.log(files,viewType)

    if (viewType === "JD") {
      addJds(files)
    }else if(viewType === "CV"){
      addCvs(files)
    }
    



  }

  // handleJdDropboxChange = (files) => {
  //   console.log(files)
  //   this.setState({
  //     jds: files
  //   });
  // }


  getDropZoneText = () => {
    // const {
    //   jds,
    //   cvs
    // } = this.state

    const {
      viewType,
      jds,
      cvs
    } = this.props

    if (viewType == "JD") {
      if (jds.length > 0) {
        return "JD Uploaded"
      } else {
        return "Drop JD here/Click to browse for JD"
      }
    } else if (viewType == "CV") {
      if (cvs.length > 0) {
        return "CVs Uploaded, you can add more"
      } else {
        return "Drop CVs here/Click to browse for CVs"
      }
    }

  }


  render() {
    // const {
    //   jds,
    //   cvs
    // } = this.state

    const {
      viewType,
      changeActiveStep,
      jds,
      cvs
    } = this.props

    return (

      <div className="upload-bar-main">

        <Fragment>
          <DropzoneArea
            key={viewType}
            onChange={this.handleDropboxChange}
            classes={{ root: "drop-zone-main" }}
            dropzoneText={this.getDropZoneText()}
            filesLimit={viewType === "JD" ? 1 : 50}
          />


          <div className="process-button-container">
            <Button
              key={viewType}

              variant="contained"
              classes={jds.length > 0 ? { root: "process-button-active" } : { root: "process-button-inactive" }}
              onClick={(e) => this.handleUploadImage()}
            >
              Process
              </Button>

          </div>
        </Fragment>

      </div>

    )
  }

}

export default UploadBar