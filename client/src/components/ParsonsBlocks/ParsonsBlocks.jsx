import React, {Component} from 'react';
import {
	Row,
	Col
} from 'reactstrap';
import './ParsonsBlocks.css';
import Block from './Block.jsx';
import axios from 'axios';

/**
 * Your Component
 */
export default class ParsonsBlocks extends Component {


	
    // Render editor
    render(){
		
		const blocks = this.props.blockInfo.map( (fields) => {
			console.log(fields);
			return( 
				<React.Fragment>
                    <Block 
						type="codeBlock"
						color={fields.color}
                        indent={fields.indent} 
                        text={fields.text}
                        pos={fields.position}
                        clickHandler={this.props.distractorSelector} 
                    /> 
				</React.Fragment>
				);
		});

		const distractors = this.props.distractorSet.map( (fields, i) => {
			return( 
				<React.Fragment>
                    <Block 
						type="distractorOption"
						color='grey'
						indent={0} 
						text={fields.text} 
						pos={i}
						clickHandler={this.props.addDistractor} 
					/> 
				</React.Fragment>
				);
        });

		const selected = this.props.selectedDistractors.map( (text, i) => {
			return( 
				<React.Fragment>
                    <Block 
						type="distractorSelected"
						color='grey'
                        indent={0} 
                        text={text} 
						pos={i}
                        clickHandler={this.props.removeDistractor} 
                    />
				</React.Fragment>
				);
		});

		return(
			<React.Fragment>
				<Col>
					<h3 style={{textAlign: 'center'}} >Correct Blocks</h3>
					<div className="text-white bg-darkrounded-3">
						{blocks}
					</div>
				</Col>
				<Col>
					<h3 style={{textAlign: 'center'}} >Distractor Blocks</h3>
					<div className="text-white bg-lightrounded-3">
						{distractors}
					</div>
				</Col>
				<Col>
					<h3 style={{textAlign: 'center'}} >Selected Distractors</h3>
					<div className="text-white bg-lightrounded-3 selected-distractors">
						{selected}
					</div>
				</Col>
			</React.Fragment>
		);
    }
}
