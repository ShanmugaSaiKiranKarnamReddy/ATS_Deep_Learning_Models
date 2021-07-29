import React, {Component} from 'react';
import { withStyles, makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

import './result-view.scss'



class ResultView extends Component {
  constructor(props){
    super(props);
    this.state = {
      selectedModel: "dict_result"
    }
  }

  sortAndNormalize = (results) => {
    let finalResult = [];
    let maxScore = 0
    
    finalResult  = results.sort((a,b) => {
      return parseFloat(b.score) - parseFloat(a.score);
    });



    finalResult.map(item=>{
      if(item.score > maxScore){
        maxScore = item.score
      }
    })

    finalResult.map(item => {
      item.score = Math.round((item.score/maxScore)*5)
    })

    // finalResult.map(item=>{
    //   item.score = item.score/
    // })
    return finalResult
  }

  getDictResults = () => {
    const {
      results
    } = this.props
    let dictResults = []

    const {
      selectedModel
    } = this.state


    console.log(selectedModel)
    if(results && selectedModel){
      Object.keys(results[selectedModel]).map(result => {
        dictResults.push({ name: result, score: results[selectedModel][result] })
      })
    }
    return dictResults
  }




  render(){
    
    const {
      results
    } = this.props

    const {
      selectedModel
    } = this.state

    let rows = []
    let sortedRows = []
    rows = this.getDictResults()
    sortedRows = this.sortAndNormalize(rows)
    console.log(sortedRows)




    return <div className={"result-view-container"}>
       <FormControl classes={{root: "model-selection"}}>
        <InputLabel id="demo-simple-select-label">Model</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={selectedModel}
          onChange={(event) => {
            this.setState({
              selectedModel: event.target.value
            });
          }}
        >
          <MenuItem value={"dict_result"}>Keyword matching</MenuItem>
          <MenuItem value={"tfidf_result"}>Tfidf</MenuItem>
        </Select>
      </FormControl>
      <Paper classes={{root: "table-container"}} elevation={3}>
        <TableContainer  classes={{root: "result-table"}}>
          <Table aria-label="customized table">
            <TableHead classes={{root: "result-table-header"}}>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell align="right">File Type</TableCell>
                <TableCell align="right">Score</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.length > 0 && rows.map((row) => (
                <TableRow key={row.name}>
                  <TableCell component="th" scope="row">
                    {row.name}
                  </TableCell>
                  <TableCell align="right">{"PDF"}</TableCell>
                  <TableCell align="right">{row.score}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </div>
  }
}


export default ResultView