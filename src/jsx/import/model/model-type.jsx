/**
 * model-type.jsx: append list of model types.
 *
 * Note: this script implements jsx (reactjs) syntax.
 */

import React, { Component } from 'react';
import checkValidString from './../validator/valid-string.js';

class ModelType extends Component {
    // initial 'state properties'
    constructor() {
        super();
        this.state = {
            value_model_type: '--Select--',
        };
        this.changeModelType = this.changeModelType.bind(this);
    }
    // update 'state properties': pass property to parent component
    changeModelType(event) {
        if (checkValidString(event.target.value)) {
            this.setState({ value_model_type: event.target.value });
            this.props.onChange({ value_model_type: event.target.value });
        } else {
            this.setState({ value_model_type: '--Select--' });
        }
    }
    // triggered when 'state properties' change
    render() {
        // display result
        return (
            <select
                className='form-control fullspan'
                name='model_type'
                autoComplete='off'
                onChange={this.changeModelType}
                value={this.state.value_model_type}
            >

                <option value='' defaultValue>--Select--</option>
                <option value='svm'>Classification</option>
                <option value='svr'>Regression</option>

            </select>
        );
    }
}

// indicate which class can be exported, and instantiated via 'require'
export default ModelType;
