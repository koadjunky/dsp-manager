import React from 'react';
import { Link } from "react-router-dom";

class Star extends React.Component {
    render() {
        return (
            <Link to={`/stars/${this.props.star.name}`}>
                <div>
                    <div className="name">{this.props.star.name}</div>
                    <div className="title">Imports:</div>
                        {Object.entries(this.props.star.trade).map(([key, value], index) => {
                            return (value < 0 ? <div>{key}: {value}</div> : "");
                        })}
                    <div className="title">Exports:</div>
                        {Object.entries(this.props.star.trade).map(([key, value], index) => {
                            return (value > 0 ? <div>{key}: {value}</div> : "");
                        })}
                </div>
            </Link>
        );
    }
}

export default class SystemView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {stars: [{name: 'Unknown', trade: [], planets: []}]};
    }
    componentDidMount() {
        fetch('/dsp/api/stars')
        .then(res => res.json())
        .then((data) => {
            this.setState(data);
            console.log(this.state);
        })
        .catch(console.log);
    }
    render() {
        return (
            <div className="wrapper">
                {this.state.stars.map(item => <Star key={item.name} star={item}/>)}
            </div>
        )
    }
}
