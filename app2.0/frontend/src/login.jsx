import React, { Component } from "react";
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import FormGroup from '@material-ui/core/FormGroup';


import Paper from '@material-ui/core/Paper';
import './Main.scss'

// function FieldGroup({ id, label, help, ...props }) {
//   return (
//     <FormGroup controlId={id}>
//       <ControlLabel>{label}</ControlLabel>
//       <FormControl {...props} />
//       {help && <HelpBlock>{help}</HelpBlock>}
//     </FormGroup>
//   );
// }

export default class Login extends Component{
  constructor(props){
    super(props);

    this.state = {
      email:"",
      password:""
    }

 }

  handleChange=event=>{
    const target = event.target;
    const value = target.value;
    const name = target.name;
    this.setState({
      [name]: value
    });
  }

  handleRegistration = e =>{
    e.preventDefault() ;
    let url = "localhost:4000/register"
    let formData  = new FormData();
    let data = this.state;
    for(let name in data) {
      formData.append(name, data[name]);
    }

    fetch(url, {
      method: 'POST',
      body: formData
    }).then( res => res.json())
    .then(data=>{
      console.log(data)
      localStorage.setItem('access_token', data.access_token);
      
      localStorage.setItem('username', data.username);

      if (localStorage.getItem("access_token") !== null && localStorage.getItem("access_token")!=="undefined") {
        window.location.replace("/")
      }else{
          alert(data.error)
      }
    }).catch(err => console.log(err));
  }

  handleSignIn = e =>{
    e.preventDefault() ;
    let url = "http://localhost:4000/auth"
    let formData  = new FormData();
    let data = this.state;
    // for(let name in data) {
    //   formData.append(name, data[name]);
    // }
    // console.log(formData)

    console.log(JSON.stringify({
      "email": data.email,
      "password": data.password,
    }))

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        "email": data.email,
        "password": data.password,
      })
    }).then( res => res.json())
    .then(data=>{
      console.log(data)
      localStorage.setItem('access_token', data.data.token);
      
      localStorage.setItem('username', data.data.name);

      if (localStorage.getItem("access_token") !== null && localStorage.getItem("access_token")!=="undefined") {
        window.location.replace("/")
      }else{
          alert(data.message);
      }
    }).catch(err => console.log(err));
  }
  render(){
    return (
      <Paper elevation={3} classes={{root: "login"}}>
        <FormGroup>
          <TextField
          required
          id="outlined-required"
          type="email"
          name="email"
          label="Required"
          variant="outlined"
          label="Email address"
          value={this.state.username}
          onChange={this.handleChange}
          placeholder="Enter email"
        />
         

          <TextField
            required
            type="password"
            name="password"
            id="outlined-required"
            label="Required"
            variant="outlined"
            label="Password"
            value={this.state.password}
            onChange={this.handleChange}
            placeholder="Password"
          />

          {/* <Button onClick={this.handleSignIn}>Log in</Button> */}
          <Button
            variant="contained"
            onClick={this.handleSignIn}
            >
              Log in
              </Button>
        </FormGroup>
      </Paper>
    );
  }
}