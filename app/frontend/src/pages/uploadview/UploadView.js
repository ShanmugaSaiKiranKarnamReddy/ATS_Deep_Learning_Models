import React, {Component} from 'react';
import UploadBar from "../../components/upload/UploadBar"
import TextField from '@material-ui/core/TextField'
import Loader from "../../components/common/loader/Loader"
import './upload-view.scss'

import Snackbar from '@material-ui/core/Snackbar';
//import MuiAlert from '@material-ui/lab/Alert';


class UploadView extends Component {


  // Alert =(props) => {
  //   return <MuiAlert elevation={6} variant="filled" {...props} />;
  // }

  render (){
    const{
      changeActiveStep,
      viewType,
      setResults,
      toggleLoading,
      loading
    }=this.props
    return (

      <div className="upload-view-container">
        {
          loading ? <Loader/>: <div className={"bar-container"}>

          <UploadBar 
            changeActiveStep={changeActiveStep}
            viewType={viewType}
            setResults={setResults}
            toggleLoading={toggleLoading}
            loading={loading}
          />

        </div>
        }
        

        {/* // <div className={"status-container"}>

        //  <div className={"status"}>
        //    <span className="title">File Name:</span> {viewType === "JD"?<span>JD Name</span>: <span>CV</span>}
        //  </div>

        //  <div className={"status"}>
        //    <span className="title">File type:</span> <span style={{color: "green"}}>PDF</span>
        //  </div>

        // </div> */}
     


      </div>
    )
  }

}

export default UploadView