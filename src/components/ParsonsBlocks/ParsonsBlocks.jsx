import React, {Component} from 'react';
import {
	Row,
	Col
} from 'reactstrap';
import Block from './Block.jsx';

/**
 * Your Component
 */
export default class ParsonsBlocks extends Component {
	
	constructor(props){
		super(props);
	}	

    // Render editor
    render(){
		
		const blocks = this.props.blockInfo.map( (fields, id) => {
			console.log(fields);
			return( 
				<React.Fragment>
					<Block indent={fields.indent} text={fields.text} pos={fields.position}> </Block>
				</React.Fragment>
				);
		});

		return(
			<React.Fragment>
				<Row>			
					<Col>
						<h3 style={{textAlign: 'center'}} >Correct Blocks</h3>
						<div className="text-white bg-lightrounded-3">
							{blocks}
						</div>
					</Col>
					<Col>
						<h3 style={{textAlign: 'center'}} >Distractor Blocks</h3>
						<div className="text-white bg-lightrounded-3">
						</div>
					</Col>
				</Row>
			</React.Fragment>
		);
    }
}
