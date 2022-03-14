import React, { Component } from 'react';
import { render } from "react-dom";
import AceEditor from "react-ace"; 

import "ace-builds/src-noconflict/mode-python";
import "ace-builds/src-noconflict/mode-java";

import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/theme-tomorrow";
import "ace-builds/src-noconflict/theme-xcode";
import "ace-builds/src-noconflict/theme-terminal";

export default class TextEditor extends Component {

	processText = (newValue) => {
		this.props.updateTextInfo(newValue);
	}

    // Render editor
    render(){
        return(
            <React.Fragment>
                <AceEditor
					height='500px'
					mode="python"
					theme="terminal"
					onChange={this.processText}
					name="UNIQUE_ID_OF_DIV2"
					ref="aceEditor1"
					editorProps={{ $blockScrolling: true }}
            />
			</React.Fragment>
		);
    }
}
