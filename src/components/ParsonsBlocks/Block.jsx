import React from 'react';
import './Block.css';
import { ItemTypes } from './Constants';
import { useDrag } from 'react-dnd';

function getDistractors(event){
    event.preventDefault();
    console.log(event.target.innerHTML);
}

export default function Block ({indent, text, pos}){
    

    const [{isDragging}, drag] = useDrag(() => ({
        type: ItemTypes.BLOCK,
        collect: monitor => ({
            isDragging: !!monitor.isDragging(),
        }),
    }))

    return(
        <button
            ref={drag} 
            onClick={getDistractors} 
            style={{
                backgroundColor: 'grey',
                textAlign: 'left',
                opacity: isDragging ? 0.5 : 1,
                color: 'black',
                padding: '5px',
                margin: '3px',
                marginLeft: indent * 50,
                borderRadius: '5px',
                display: 'block'
            }}
        >
        {text}
        </button>
    );


}
