import React, { Component } from 'react';
import { split as SplitEditor} from "react-ace"; 
import {
	Dropdown,
	DropdownItem,
	DropdownToggle,
	DropdownMenu,
	Form,
	FormGroup,
	Label,
	Input 
} from 'reactstrap';
import uuid from 'react-uuid'


import "ace-builds/src-noconflict/mode-html";
import "ace-builds/src-noconflict/mode-markdown";

import "ace-builds/src-noconflict/theme-tomorrow";
import "ace-builds/src-noconflict/theme-xcode";
import "ace-builds/src-noconflict/theme-terminal";

export default class GeneratedProblem extends Component {

	constructor(props){
		super(props)
		this.state = {
			uuid: uuid(),
			isOpen: false,
			outputMode: "PrairieLearn"
		}
	}

	downloadContents = () => {}

	toggle = () =>{
		this.setState({
			isOpen: !this.state.isOpen
		})
	}

	setOutputMode = (event) => {
		this.setState({
			outputMode: event.target.innerText
		})
	}

	generatePrairieLearnOutput = () =>{
        //Generate the server.py

        //Generate the info.json
		const infoJson= JSON.stringify({
			uuid: this.state.uuid,
			title: this.props.title,
			topic: this.props.topic,
			tags: this.props.tags,
			singleVariant: true,
			type: "v3"
		}, null, 4)



		const blocks = Object.keys(this.props.blockInfo).map( (key) => {

			const block = this.props.blockInfo[key];

			const elements = [
                "    <pl-answer correct=\"true\" indent=\"" + 
                block.indent.toString() + "\" ranking=\"" +
                block.position.toString() +"\"> " + 
                block.text + 
                " </pl-answer>"
			]

			if(block.distractors.length > 0){
				const formattedDistractors = block.distractors.map( (distractor) => {
					return(
						"    <pl-answer correct=\"false\"> " + distractor + " </pl-answer>"
					);
				});
				elements.push(...formattedDistractors);
			}

			return(elements.join("\n"));
		}).join("\n");

		const generatedHTML = "<pl-parsons-blocks answers-name=\"answers\" indentation=true grading-method=\"ranking\">\n"  + blocks + "\n</pl-parsons-blocks>"

		return(<SplitEditor
			width='1500px'
			height='400px'
			theme='tomorrow'
			fontSize='10pt'
			mode='html'
			name='UNIQUE_ID_OF_DIV1'
			splits={2} 
			value={[infoJson, generatedHTML]}
			editorProps={{ $blockScrolling: true }}
		/>);


	}

	/*generateRuneStoneOutput = () => {

        this.props.correct.map( (field, id) => {
            return( 
                "    <pl-answer correct=\"true\" indent=\"" + 
                field.indent.toString() + "\" ranking=\"" +
                field.position.toString() +"\"> " + 
                field.text + 
                " </pl-answer>"
                );
        }).join("\n");

        // Generate the HTML
        const correct = this.props.correct.map( (field, id) => {
            return( 
                "    <pl-answer correct=\"true\" indent=\"" + 
                field.indent.toString() + "\" ranking=\"" +
                field.position.toString() +"\"> " + 
                field.text + 
                " </pl-answer>"
                );
        }).join("\n");

        const distractors = this.props.distractors.map( (x) => {
            return( 
                "    <pl-answer correct=\"false\"> " + x + " </pl-answer>"
                );
        }).join("\n");

		const generatedHTML = "<pl-parsons-blocks answers-name=\"answers\" indentation=true grading-method=\"ranking\">\n"  + correct + "\n" + distractors + "\n</pl-parsons-blocks>"

		return(
			<React.Fragment>
				<SplitEditor
					width='1500px'
					height='400px'
					theme='tomorrow'
					fontSize='10pt'
					mode='html'
					name='UNIQUE_ID_OF_DIV1'
					splits={1} 
					value={[generatedHTML]}
					editorProps={{ $blockScrolling: true }}
				/>
			</React.Fragment>
		);


	}*/


    // Render editor
    render(){

		const outputMap = {
			"PrairieLearn": this.generatePrairieLearnOutput,
			//"RuneStone": this.generateRuneStoneOutput,
			null: () => {}
		}


        return(
			<React.Fragment>
				<Dropdown isOpen={this.state.isOpen} toggle={this.toggle}>
					<DropdownToggle caret>Select Output Type</DropdownToggle>
					<DropdownMenu>
						<DropdownItem onClick={this.setOutputMode}>RuneStone</DropdownItem>
						<DropdownItem onClick={this.setOutputMode}>PrairieLearn</DropdownItem>
					</DropdownMenu>
				</Dropdown>
				{outputMap[this.state.outputMode]()}
				<button
					id='downloadContent'
					onClick={this.downloadContents} 
					>
					Download ZIP
				</button>
			</React.Fragment>
        );
    }
}

