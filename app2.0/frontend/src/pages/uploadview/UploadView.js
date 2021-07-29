import React, {Component} from 'react';
import UploadBar from "../../components/upload/UploadBar"
import Loader from "../../components/common/loader/Loader"
import './upload-view.scss'
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';

export const options = [
  {
    "name" : "Malstm",
    "id":"result_malstm"
  },
  {
    "name" : "Rnn",
    "id":"result_rnn"
  },
  {
    "name" : "BiLstm",
    "id":"result_bi_lstm"
  },
  {
    "name" : "Keyword Matching",
    "id":"result_keywordmatching"
  },
  {
    "name" : "Tfidf",
    "id":"result_tfidf"
  },
  {
    "name" : "Text Tranformation(Roberta)",
    "id":"result_text_tranformers"
  },
];
class UploadView extends Component {

  render (){
    const{
      changeActiveStep,
      viewType,
      setResults,
      toggleLoading,
      loading,
      handleModelSelection,
      selectedModel,
      toggleAllDocsLoaded,
      allDocsLoaded,
      jds,
      cvs,
      addJds,
      addCvs,
      sessionId,
      setSessionId
    }=this.props
    return (

      <div className="upload-view-container">
        {
          loading ? <Loader/>: 
          <div className={"bar-container"}>
          <UploadBar 
            changeActiveStep={changeActiveStep}
            viewType={viewType}
            setResults={setResults}
            toggleLoading={toggleLoading}
            loading={loading}
            jds={jds}
            cvs={cvs}
            addJds={addJds}
            addCvs={addCvs}
            sessionId={sessionId}
            setSessionId={setSessionId}
            selectedModel={selectedModel}
            toggleAllDocsLoaded={toggleAllDocsLoaded}
          />
            {viewType === "CV" &&
              <FormControl>
                <InputLabel id="demo-simple-select-label">Models</InputLabel>
                <Select
                  labelId="demo-simple-select-label"
                  id="demo-simple-select"
                  classes={{ root: "model-select" }}
                  value={selectedModel}
                  onChange={(event) => {
                    handleModelSelection(event.target.value)
                  }}
                >
                  {
                    options.map(option => {
                      return <MenuItem key={option.id} value={option.id}>{option.name}</MenuItem>
                    })
                  }
                </Select>
              </FormControl>
            }
        </div>
  }


      </div>
    )
  }

}

export default UploadView