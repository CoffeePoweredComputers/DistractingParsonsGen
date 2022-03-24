import React, { Component } from 'react';
import { render } from "react-dom";
import { split as SplitEditor} from "react-ace"; 
//import { v5 as uuidv5 } from 'uuid';
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
			uuid: uuid()
		}
	}

	downloadContents = () => {}


    // Render editor
    render(){

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
					splits={2} 
					value={[infoJson, generatedHTML]}
					editorProps={{ $blockScrolling: true }}
				/>
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

