import React from 'react';
import './Block.css';
import { ItemTypes } from './Constants';
import { useDrag } from 'react-dnd';
import {
    Button
} from 'reactstrap';

export default function Block ({type, color, bordercolor, indent, text, op, group, pos, parentBlock, clickHandler}){

    const [{isDragging}, drag] = useDrag(() => ({
        type: ItemTypes.BLOCK,
        collect: monitor => ({
            isDragging: !!monitor.isDragging(),
        }),
    }))

    const blockID = type + pos.toString();


    return(
        <button
            id={blockID}
            pos={pos}
            ref={drag} 
            op={op}
            parentBlock={parentBlock}
            group={group}
            onClick={clickHandler} 
            style={{
                backgroundColor: color,
                borderColor: bordercolor,
                width: '100%'
            }}
        >
            {text}
        </button>
    );


}
