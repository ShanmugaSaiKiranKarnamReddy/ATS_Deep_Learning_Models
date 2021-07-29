import React, {Component} from 'react';
import TextField from '@material-ui/core/TextField'
import Button from '@material-ui/core/Button';
import "./upload-bar.scss"
import {DropzoneArea} from 'material-ui-dropzone'

import {DropzoneDialog} from 'material-ui-dropzone'
import { makeStyles } from '@material-ui/core/styles';
import axios from 'axios';
import UserProfile from '../../UserProfile';


class UploadBar extends Component {

  constructor(props){
    super(props);
    this.state = {
      files: []
    };
  }

  // componentDidMount = () => {
  //   axios.defaults.withCredentials = true
  //   axios.get(`http://127.0.0.1:8000/get_time`)
  //     .then(res => {
  //       console.log(res.data)
  //     }).catch(() => console.log("Can’t access "  + " response. Blocked by browser?"))
  // }

  handleUploadImage(ev) {

    const{
      files
    } = this.state

    const{
      changeActiveStep,
      viewType,
      setResults,
      toggleLoading,
      loading
    }= this.props

    ev.preventDefault();

    toggleLoading()

    var formData = new FormData();
    files.map(file => {
      formData.append("file", file)
    })

    if(viewType === "JD"){
      axios.post('http://127.0.0.1:3001/uploadJD', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Requested-With': 'XMLHttpRequest',//CORS fixes client side
          'Access-Control-Allow-Origin' : '*',
          'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
          'Session-Id': UserProfile.getSessionId()
        }
      }).then(res => {
        console.log(res.data);
        toggleLoading()
        changeActiveStep()
      })
    }else{
      axios.post('http://127.0.0.1:3001/uploadCV', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'X-Requested-With': 'XMLHttpRequest',//CORS fixes client side
          'Access-Control-Allow-Origin' : '*',
          'Access-Control-Allow-Methods' : 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
          'Session-Id': UserProfile.getSessionId()
        }
      }).then(res => {
        console.log(res.data);
        toggleLoading()

        setResults(res.data)
        changeActiveStep()
      })
    }
    
  }


  handleChange(files){
    this.setState({
      files: files
    });
  }

  handleClose() {
    this.setState({
        open: false
    });
  }

  handleOpen() {
    this.setState({
        open: true,
    });
}

handleSave(files) {
  //Saving files to state for further use and closing Modal.
  this.setState({
      files: files,
      open: false
  });
}

getDropZoneText = () => {
  const {
    files
  }= this.state

  const{
    viewType
  }= this.props

  if(viewType == "JD"){
    if(files.length > 0){
      return "JD Uploaded"
    }else{
      return "Drop JD here/Click to browse for JD"
    }
  }else if(viewType == "CV"){
    if(files.length > 0){
      return "CVs Uploaded, you can add more"
    }else{
      return "Drop CVs here/Click to browse for CVs"
    }
  }

}

  
  render (){
    const {
      files
    }= this.state

    const{
      viewType
    }= this.props

    return (

      <div className="upload-bar-main">

        <DropzoneArea
          onChange={this.handleChange.bind(this)}
          classes={{root: "drop-zone-main"}}
          dropzoneText={this.getDropZoneText()}
          filesLimit={viewType == "JD"? 1: 50}
        />

            <div className="process-button-container">
              <Button 
                variant="contained" 
                disabled={files.length > 0 ? false: true}
                classes={files.length > 0 ? {root:"process-button-active"}: {root:"process-button-inactive"}}
                onClick={(e) => this.handleUploadImage(e)}
              >
                Process
              </Button>
            </div>
        </div>

    )
  }

}

export default UploadBar