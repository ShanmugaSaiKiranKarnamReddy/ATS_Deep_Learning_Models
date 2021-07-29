import React from 'react'
import './loader.scss'

function Loader(props) {
  return	<div className={'loading-container'}>
    <div>
      <img className={'loading-image'} src={require('../../../media/icons/loading.gif')}/>
    </div>
    {props.text ? <div className={'loading-text'}>
      {props.text}
    </div> : null}
  </div>
}

export default Loader