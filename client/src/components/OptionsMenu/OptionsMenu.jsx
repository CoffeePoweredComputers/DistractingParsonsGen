import React from 'react';
import {
    Button, 
    Form, 
    FormGroup, 
    Label, 
    Input, 
    FormText 
} from 'reactstrap';

export default class OptionsMenu extends React.Component{

	render(){

        return (
            <Form>
                <FormGroup>
                    <Label for="title">Title</Label>
                    <Input type="text" name="title" id="title" placeholder="title here" onChange={this.props.setTitle} />
                </FormGroup>
                <FormGroup>
                    <Label for="qid">QID</Label>
                    <Input type="text" name="qid" id="qid" placeholder="qid here" onChange={this.props.setQID} />
                </FormGroup>
                <FormGroup>
                    <Label for="tags">Topic</Label>
                    <Input type="text" name="topic" id="topic" placeholder="topic here" onChange={this.props.setTopic} />
                </FormGroup>
                <FormGroup>
                    <Label for="tags">Tags</Label>
                    <Input type="text" name="tags" id="title" placeholder="(e.g., tag1, tag2, tag3, ...)" onChange={this.props.setTags} />
                </FormGroup>
			</Form>
			);
	}
}

