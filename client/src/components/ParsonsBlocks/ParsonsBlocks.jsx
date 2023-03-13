import React, {Component, useState} from 'react';
import {
    Alert,
	Row,
    Col,
    Accordion,
    AccordionItem,
    AccordionHeader,
    AccordinToggle,
    AccordionBody,
    UncontrolledAccordion
} from 'reactstrap';
import './ParsonsBlocks.css';
import Block from './Block.jsx';
import axios from 'axios';

/**
 * Your Component
 */
export default class ParsonsBlocks extends Component {

    constructor(props) {
        super(props);
        this.state = {
            open: ''
        };
    }

    toggle = (id) => {
        console.log(id);
        const item = Object.values(this.props.blockInfo).find((element) => element.position  === (id  + 1)) ;
        console.log(item.color) ;
        if ((this.state.open === id) || (item.color === "grey")) {
            this.setState({ open: '' });
        } else{
            this.setState({ open: id });
        }
    }


	
    // Render editor
    render(){

		const distractors = this.props.distractorSet.map( (fields, i) => {
			return( 
                <React.Fragment>
                    <Block 
						type="distractorOption"
						parentBlock={fields.parentBlock}
                        color="rgba(220, 53, 69, .2)"
                        bordercolor="#f5c6cb"
						indent={0} 
						text={fields.text} 
						pos={i}
						clickHandler={this.props.toggleDistractor} 
                        style={{
                            borderColor: "#f5c6cb;"
                        }}
                /> 
				</React.Fragment>
				);
        });

		const blocks = Object.keys(this.props.blockInfo).map( (key, i) => {
            const fields = this.props.blockInfo[key];
			return( 
                <React.Fragment>
                    <AccordionItem  className="element" 
                            style={{
                                marginLeft: fields.indent * 50,
                                width: 'calc(100% - ' + (fields.indent * 50).toString()  + 'px)' 
                            }}
                    >
                        <AccordionHeader targetId={i} >
                            <Block 
                                type="codeBlock"
                                color={fields.color}
                                bordercolor="grey"
                                indent={fields.indent} 
                                text={fields.text}
                                op={fields.op}
                                group={fields.type}
                                pos={fields.position}
                                clickHandler={this.props.distractorSelector} 
                            /> 
                        </AccordionHeader>
                        <AccordionBody accordionId={i}>
                            {distractors}
                        </AccordionBody>
                    </AccordionItem>
				</React.Fragment>
				);
		});

		return(
			<React.Fragment>
				<Col>
                    <div className="text-white bg-darkrounded-3 blocks">
                    <Accordion flush open={this.state.open} toggle={this.toggle}>
                            {blocks}
                    </Accordion>
					</div>
				</Col>
			</React.Fragment>
		);
    }
}
