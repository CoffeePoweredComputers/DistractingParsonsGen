import React from 'react';
import {
	Navbar,
	NavbarBrand,
	NavbarText,
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
			topic: "",
			qid: "",
			tags: [],
			blockInfo: [],
			distractorSet: [],
			selectedDistractors: []
		}
	}

	matchDistractor = async (line) => {

		const requestParams = {
			params : {
				text: line
			}
		};

		return await axios.get('http://18.189.184.37:80/match_distractor', requestParams)
			.then( (response) => response.data.matchFound );
			//.catch((error) => {
			//	console.error(error);
			//});
		
	}


    processText = async (newValue) => {
        var blocks = [];
		const lines = newValue.split('\n');
		for(var i = 0; i < lines.length; i++){

			const spaces = lines[i].search(/\S/);
			lines[i] += (i < lines.length - 1) ? '\n' : '';
			if(spaces < 0){
				continue;
			} 

			const indent_level = Math.floor(spaces/4);
			const distractorMatched = (lines[i].endsWith('\n')) ? (await this.matchDistractor(lines[i].trim())) : false;
			const data = {
					text: lines[i].trim(),
					indent: indent_level,
					position: blocks.length + 1,
					color:  distractorMatched ? 'darkgreen' : 'grey',
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
		
		axios.get('http://18.189.184.37:80/get_distractors', requestParams)
			.then( (response) => this.setState({
				distractorSet: response.data
			})
			)
			.catch((error) => {
				console.error(error);
			});
		
		event.preventDefault();
	}

	addDistractor = (event) => {
		
        this.setState({
            selectedDistractors: [...this.state.selectedDistractors, event.target.innerHTML]
        });

		event.preventDefault();
    }

	removeDistractor = (event) => {
		const blockIndex = event.target.getAttribute("pos");
		var selectedDistractorsCopy = [ ...this.state.selectedDistractors ];
		selectedDistractorsCopy.splice(blockIndex, 1)
		this.setState({
			selectedDistractors: selectedDistractorsCopy

		});

		event.preventDefault();
	}

	setTitle = (event) => {
		this.setState({
			title: event.target.value.trim()
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
                            setTopic={this.setTopic} 
                            setQID={this.setQID} 
                            setTags={this.setTags}
                        />
					</Col>
					<DndProvider backend={HTML5Backend}>
						<ParsonsBlocks 
							blockInfo={this.state.blockInfo} 
							distractorSet={this.state.distractorSet} 
							selectedDistractors={this.state.selectedDistractors} 
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
							topic={this.state.topic}
							tags={this.state.tags} 
							correct={this.state.blockInfo} 
							distractors={this.state.selectedDistractors} 
						/>
					</center>
				</Row>
			</React.Fragment>
			);
	}
}
