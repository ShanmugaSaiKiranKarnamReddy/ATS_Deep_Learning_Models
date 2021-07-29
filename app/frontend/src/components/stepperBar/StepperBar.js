import React, {Component} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';


import './stepper-bar.scss'

class StepperBar extends Component {
  constructor(props){
    super(props);
    this.state = {
      
    }
  }
  

  render(){

    const{
      activeStep
    } = this.props
    return(
      <Paper classes={{root: "stepper-bar-container"}}>
        <Stepper activeStep={activeStep} classes={{root:"custom-stepper"}}>
          <Step >
            <StepLabel>{"Upload a JD"}</StepLabel>
          </Step>
          <Step >
            <StepLabel>{"Upload the CVs"}</StepLabel>
          </Step>
          <Step >
            <StepLabel>{"Result"}</StepLabel>
          </Step>
 
        </Stepper>
      </Paper>
    )
  }
}

export default StepperBar 
