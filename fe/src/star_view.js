import React from 'react';
import { useParams, Link } from "react-router-dom";

class Planet extends React.Component {
    render() {
        return (
            <Link to={`/stars/${this.props.star_name}/planets/${this.props.planet.name}`}>
                <div>
                    <div className="name">Name: {this.props.planet.name}</div>
                    <div className="title">Imports:</div>
                        {Object.entries(this.props.planet.trade).map(([key, value], index) => {
                            return (value < 0 ? <div>{key}: {value}</div> : "");
                        })}
                    <div className="title">Exports:</div>
                        {Object.entries(this.props.planet.trade).map(([key, value], index) => {
                            return (value > 0 ? <div>{key}: {value}</div> : "");
                        })}
                </div>
            </Link>
        );
    }
}

class StarView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {name: "", trade: [], planets: []};
    }
    componentDidMount() {
        fetch(`/dsp/api/stars/${this.props.star_name}`)
        .then(res => res.json())
        .then((data) => {
            this.setState(data);
            console.log(this.state);
        })
        .catch(console.log);
    }
    render() {
        return (
            <div>
                <Link to={'/'}>Back to System</Link>
                <div className="system">
                    <div className="name">{this.state.name}</div>
                    <div className="title">Imports</div>
                        {Object.entries(this.state.trade).map(([key, value], index) => {
                            return (value < 0 ? <div>{key}: {value}</div> : "");
                        })}
                    <div className="title">Exports</div>
                        {Object.entries(this.state.trade).map(([key, value], index) => {
                            return (value > 0 ? <div>{key}: {value}</div> : "");
                        })}
                </div>
                <div className="wrapper">
                    {this.state.planets.map(item => <Planet key={item.name} star_name={this.props.star_name} planet={item}/> )}
                </div>
            </div>
        );
    }
}

export default function StarViewWrapper() {
    const { star_name } = useParams();
    return (<StarView star_name={star_name} /> );
}
