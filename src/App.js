import React from 'react';
import {
	Navbar,
	NavbarBrand,
	NavbarText,
	Row,
	Col
} from 'reactstrap';
import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

import TextEditor from "./components/TextEditor/TextEditor.jsx";
import ParsonsBlocks from "./components/ParsonsBlocks/ParsonsBlocks.jsx";
import GeneratedProblem from "./components/GeneratedProblem/GeneratedProblem.jsx";

import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'

export default class App extends React.Component{

	constructor(props){
		super(props);
		this.state = {
			blockInfo: [],
			distractorSet: [],
			selectedDistractors: []
		}
	}

    processText = (newValue) => {
        var blocks = [];
		const lines = newValue.split('\n');
		for(var i = 0; i < lines.length; i++){

			const spaces = lines[i].search(/\S/);
			if(spaces < 0){
				continue;
			} 

			const indent_level = Math.floor(spaces/4);
			const data = {
					text: lines[i].trim(),
					indent: indent_level,
					position: blocks.length + 1
					}

			blocks.push(data);
		}

		this.setState({
			blockInfo: blocks 
		});
    }

	getDistractors = (event) => {
		
		const requestParams = {
			params : {
				text: event.target.innerHTML,
				type: "list",
				operation: "append"
			}
		};
		
		axios.get('http://localhost:8000/get_distractors', requestParams)
			.then( (response) => this.setState({
				distractorSet: response.data
			})
			)
			.catch((error) => {
				console.error(error);
			});
		
		event.preventDefault();
	}

	toggleDistractor = (event) => {
		
		if(this.state.selectedDistractors.includes(event.target.innerHTML)){
			console.log("implement removing from state array");
		} else {
			this.setState({
				selectedDistractors: [...this.state.selectedDistractors, event.target.innerHTML]
			});
		}
		event.preventDefault();
	}

	render(){

		const cards = this.state.blockInfo.map( (fields, id) => {
			return (
				<React.Fragment>
					<li><b> {fields.indent}, {fields.text}, {fields.position} </b></li>
				</React.Fragment>
			);
		});

		return (
			<React.Fragment>
				<Navbar color="dark" dark expand="md" light >
					<NavbarBrand href="/">
						Parson's Problem: Automatic Distractor Gen
					</NavbarBrand>
				</Navbar>
				<Row>
					<Col className = "editor">
						<TextEditor updateTextInfo={this.processText} ></TextEditor>
					</Col>
					<Col className = "cards">
						<DndProvider backend={HTML5Backend}>
							<ParsonsBlocks blockInfo={this.state.blockInfo} distractorSet={this.state.distractorSet} distractorSelector={this.getDistractors} distractorToggle={this.toggleDistractor}></ParsonsBlocks>
						</DndProvider>
					</Col>
				</Row>
				<Row>
					<center>
						<h2> Generated Problem </h2>
						<GeneratedProblem></GeneratedProblem>
					</center>
				</Row>
			</React.Fragment>
			);
	}
}
