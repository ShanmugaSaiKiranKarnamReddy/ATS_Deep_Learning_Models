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
import { Document, Page } from 'react-pdf';


class ResultView extends Component {
  constructor(props){
    super(props);
    this.state = {
      selectedModel: "dict_result"
    }
  }

  // const [numPages, setNumPages] = useState(null);
  // const [pageNumber, setPageNumber] = useState(1);

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


    // if(results['data'].length > 0){
    //   Object.keys(results['data']).map(result => {
    //     dictResults.push({ name: result.name, score: result.score })
    //   })
    // }

    console.log(results['data'].sort((a, b) => parseFloat(b.result) - parseFloat(a.result)));
    return results['data']
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


    return <div className={"result-view-container"}>
      <Paper classes={{root: "table-container"}} elevation={3}>
        <TableContainer  classes={{root: "result-table"}}>
          <Table aria-label="customized table">
            <TableHead classes={{root: "result-table-header"}}>
              <TableRow>
                <TableCell>Name</TableCell>
                <TableCell align="right">File Type</TableCell>
                <TableCell align="right">Score(per 100)</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.length > 0 && rows.map((row, index) => (
                <TableRow key={index}>
                  <TableCell component="th" scope="row">
                    {row.filename}
                  </TableCell>
                  <TableCell align="right">{"PDF"}</TableCell>
                  <TableCell align="right">{row.result}</TableCell>
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