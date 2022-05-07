import React from 'react';
import {
	Navbar,
	NavbarBrand,
	Row,
	Col
} from 'reactstrap';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

import OptionsMenu from "./components/OptionsMenu/OptionsMenu.jsx";
import TextEditor from "./components/TextEditor/TextEditor.jsx";
import ParsonsBlocks from "./components/ParsonsBlocks/ParsonsBlocks.jsx";
import GeneratedProblem from "./components/GeneratedProblem/GeneratedProblem.jsx";

import { DndProvider } from 'react-dnd'
import { HTML5Backend } from 'react-dnd-html5-backend'

export default class App extends React.Component{

	constructor(props){
		super(props);
		this.state = {
			title: "",
			prompt: "",
			topic: "",
			qid: "",
			tags: [],
			blockInfo: [],
			distractorSet: [],
			activeParent: ""
		}
	}

	matchDistractor = async (line) => {

		const requestParams = {
			params : {
				text: line
			}
		};

		return await axios.get('http://localhost:8000/match_distractor', requestParams)
			.then( (response) => response.data )
			.catch((error) => {
				console.error(error);
			});
		
	}


    processText = async (newValue) => {

        var blocks = {};
		const lines = newValue.split('\n');

		for(var i = 0; i < lines.length; i++){

			const spaces = lines[i].search(/\S/);
			lines[i] += (i < lines.length - 1) ? '\n' : '';
			if(spaces < 0){
				continue;
			} 

			const indent_level = Math.floor(spaces/4);
			var distractorData = null;

			if(lines[i].trim() in this.state.blockInfo){
				const fields = this.state.blockInfo[lines[i].trim()];
				distractorData = {
					op: fields.op,
					type: fields.type,
					matchFound: fields.color == 'darkgreen'
				};
			} else{
				distractorData = await this.matchDistractor(lines[i].trim());
			}

			blocks[lines[i].trim()] = {
                    op: distractorData.op,
					type: distractorData.type,
					text: lines[i].trim(),
					indent: indent_level,
					position: i + 1,
					color:  distractorData.matchFound ? 'darkgreen' : 'grey',
					distractors: (lines[i].trim() in this.state.blockInfo) ? this.state.blockInfo[lines[i].trim()].distractors: [],
					};
		}

		this.setState({
			blockInfo: blocks 
		});
    }

	getDistractors = (event) => {

		const requestParams = {
			params : {
				text: event.target.innerHTML,
				type: event.target.getAttribute("group"),
                operation: event.target.getAttribute("op")
			}
		};
		
		axios.get('http://localhost:8000/get_distractors', requestParams)
			.then((response) => this.setState({
				distractorSet: response.data,
				activeParent: event.target.innerHTML
			})
			)
			.catch((error) => {
				console.error(error);
			});

		event.preventDefault();
	}

	addDistractor = (event) => {

		var newBlockInfo = { ...this.state.blockInfo };
		newBlockInfo[this.state.activeParent].distractors.push(event.target.innerHTML);
		this.setState({
			blockInfo: newBlockInfo
		})			
		event.preventDefault();
    }

	removeDistractor = (event) => {
		
		const parentBlock = event.target.getAttribute("parentblock");
		var newBlockInfo = { ...this.state.blockInfo };
		var distractorIndex = newBlockInfo[parentBlock].distractors.indexOf(event.target.innerHTML);
		newBlockInfo[parentBlock].distractors.splice(distractorIndex, 1);
		this.setState({
			blockInfo: newBlockInfo
		})			
		event.preventDefault();

	}

	setTitle = (event) => {
		this.setState({
			title: event.target.value.trim()
		});
		event.preventDefault();
	}

	setPrompt = (event) => {
		this.setState({
			prompt: event.target.value.trim()
		});
		event.preventDefault();
	}

	setTopic = (event) => {
		this.setState({
			topic: event.target.value.trim()
		});
		event.preventDefault();
	}

	setQID = (event) => {
		this.setState({
			qid: event.target.value
		});
		event.preventDefault();
	}

	setTags = (event) => {
		this.setState({
			tags: event.target.value.split(",").map( (x) => x.trim() )
		});
		event.preventDefault();
	}

	render(){

		return (
			<React.Fragment>
				<Navbar color="dark" dark expand="md" light >
					<NavbarBrand href="/">
						Parson's Problem: Automatic Distractor Gen
					</NavbarBrand>
				</Navbar>
				<Row className="bg-light border">
					<Col className="editor">
                        <TextEditor updateTextInfo={this.processText} />
					</Col>
					<Col>
                        <OptionsMenu 
							setTitle={this.setTitle} 
							setPrompt={this.setPrompt}
                            setTopic={this.setTopic} 
                            setQID={this.setQID} 
                            setTags={this.setTags}
                        />
					</Col>
					<DndProvider backend={HTML5Backend}>
						<ParsonsBlocks 
							blockInfo={this.state.blockInfo} 
							distractorSet={this.state.distractorSet} 
							distractorSelector={this.getDistractors} 
							addDistractor={this.addDistractor}
							removeDistractor={this.removeDistractor}
						/>
					</DndProvider>
				</Row>
				<Row className="bg-light border">
					<center>
						<h2> Generated Problem </h2>
						<GeneratedProblem 
							qid={this.state.qid} 
							title={this.state.title} 
							prompt={this.state.prompt}
							topic={this.state.topic}
							tags={this.state.tags} 
							blockInfo={this.state.blockInfo} 
						/>
					</center>
				</Row>
			</React.Fragment>
			);
	}
}
