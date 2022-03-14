import React, { Component } from 'react';
import { render } from "react-dom";
import AceEditor from "react-ace"; 

import "ace-builds/src-noconflict/mode-html";
import "ace-builds/src-noconflict/mode-markdown";

import "ace-builds/src-noconflict/theme-tomorrow";
import "ace-builds/src-noconflict/theme-xcode";
import "ace-builds/src-noconflict/theme-terminal";

export default class GeneratedProblem extends Component {

	logText = (newValue) => {
        console.log(newValue);
	}

    // Render editor
    render(){
        return(
            <React.Fragment>
                <AceEditor
					width='1000px'
					height='250px'
                    theme='tomorrow'
                    mode='html'
                    onChange={this.logText}
                    name='UNIQUE_ID_OF_DIV1'
                    ref='aceEditor2'
                    editorProps={{ $blockScrolling: true }}
                />
            </React.Fragment>
        );
    }
}

