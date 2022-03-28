import React from 'react';
import './Block.css';
import { ItemTypes } from './Constants';
import { useDrag } from 'react-dnd';
import {
    Button
} from 'reactstrap';

export default function Block ({type, color, indent, text, op, group, pos, clickHandler}){

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
            group={group}
            onClick={clickHandler} 
            style={{
                backgroundColor: color,
                opacity: isDragging ? 0.5 : 1,
                marginLeft: indent * 50,
                width: 'calc(100% - ' + (indent * 50).toString()  + 'px)' 
            }}
        >
            {text}
        </button>
    );


}
