import React, { Component } from 'react';
import { render } from "react-dom";
import { split as SplitEditor} from "react-ace"; 

import "ace-builds/src-noconflict/mode-html";
import "ace-builds/src-noconflict/mode-markdown";

import "ace-builds/src-noconflict/theme-tomorrow";
import "ace-builds/src-noconflict/theme-xcode";
import "ace-builds/src-noconflict/theme-terminal";

export default class GeneratedProblem extends Component {

    // Render editor
    render(){
        return(
            <SplitEditor
                width='1500px'
                height='400px'
                theme='tomorrow'
                mode='html'
                name='UNIQUE_ID_OF_DIV1'
                splits={3} 
                editorProps={{ $blockScrolling: true }}
            />
        );
    }
}

