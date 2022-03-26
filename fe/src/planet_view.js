import React from 'react';
import { useParams, Link } from "react-router-dom";
import Factory from './factory'

class PlanetView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {name: "", trade: [], factories: []};
    }
    componentDidMount() {
        fetch(`/dsp/api/stars/${this.props.star_name}/planets/${this.props.planet_name}`)
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
                <Link to={`/stars/${this.props.star_name}`}>Back to {this.props.star_name}</Link>
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
                <div className='wrapper'>
                    {this.state.factories.map(item => <Factory factory={item}/> )}
                </div>
            </div>
        );
    }
}

export default function PlanetViewWrapper() {
    const { star_name, planet_name } = useParams();
    return (<PlanetView star_name={star_name} planet_name={planet_name} /> );
}
