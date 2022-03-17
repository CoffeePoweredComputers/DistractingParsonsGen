import React, {Component} from 'react';

export default function Block ({indent, text, position}){
    
    // Render editor
    return(
        <div 
            style={{
                backgroundColor: 'grey',
                color: 'white',
                width: '100%'
            }}
        >
        {text}
        </div>
        );


}
