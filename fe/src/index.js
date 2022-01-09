import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useParams } from "react-router-dom";
import "./index.css";


class Factory extends React.Component {
    render() {
        return (
            <div className="factory">
                <div>Name: {this.props.factory.name}</div>
                <div>Recipe: {this.props.factory.recipe}</div>
                <div>Machine: {this.props.factory.machine}</div>
                <div>Count: {this.props.factory.count}</div>
                <div>Production:</div>
                {Object.entries(this.props.factory.production).map(([key, value], index) => {
                    return (<div>{key}: {value}</div>);
                })}
            </div>
        );
    }
}

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
        })
        .catch(console.log);
        console.log(this.state);
    }
    renderFactory(i) {
        return <Factory factory={this.state.factories[i]} />;
    }
    render() {
        return (
            <div>
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

function PlanetViewWrapper() {
    const { star_name, planet_name } = useParams();
    return (<PlanetView star_name={star_name} planet_name={planet_name} /> );
}

class Planet extends React.Component {
    render() {
        return (
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
        })
        .catch(console.log);
        console.log(this.state);
    }
    render() {
        return (
            <div>
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
                    {this.state.planets.map(item => <Planet planet={item}/> )}
                </div>
            </div>
        );
    }
}

function StarViewWrapper() {
    const { star_name } = useParams();
    return (<StarView star_name={star_name} /> );
}

class SystemView extends React.Component {
    constructor(props) {
        super(props);
        this.state = {stars: [{'name': 'Unknown'}]};
    }
    componentDidMount() {
        fetch('/dsp/api/stars')
        .then(res => res.json())
        .then((data) => {
            this.setState(data);
        })
        .catch(console.log);
        console.log(this.state);
    }
    render() {
        return (
            <div className="system">
                <div className="name">{this.state.stars[0].name}</div>
                <div className="title">Imports</div>
                <div className="title">Exports</div>
            </div>
        )
    }
}

// =====================================================

ReactDOM.render(
    <div className="main">
        <Router>
            <Routes>
                <Route path="/" element={<SystemView /> } />
                <Route path="/star/:star_name" element={ <StarViewWrapper /> } />
                <Route path="/star/:star_name/planet/:planet_name" element={ <PlanetViewWrapper /> } />
            </Routes>
        </Router>
    </div>,
    document.getElementById('root')
);
