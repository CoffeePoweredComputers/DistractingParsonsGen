import React, {Component} from 'react';
import {
	Row,
	Col
} from 'reactstrap';
import Block from './Block.jsx';
import axios from 'axios';

/**
 * Your Component
 */
export default class ParsonsBlocks extends Component {
	
    // Render editor
    render(){
		
		const blocks = this.props.blockInfo.map( (fields, id) => {
			console.log(fields);
			return( 
				<React.Fragment>
					<Block indent={fields.indent} text={fields.text} pos={fields.position} clickHandler={this.props.distractorSelector}> </Block>
				</React.Fragment>
				);
		});

		const distractors = this.props.distractorSet.map( (fields, id) => {
			console.log(fields);
			return( 
				<React.Fragment>
					<Block indent={0} text={fields.text} clickHandler={this.props.distractorToggle}> </Block>
				</React.Fragment>
				);
		});

		return(
			<React.Fragment>
				<Row>			
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
				</Row>
			</React.Fragment>
		);
    }
}
