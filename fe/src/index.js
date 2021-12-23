import React from 'react';
import ReactDOM from 'react-dom';
import "./index.css";


class System extends React.Component {
    constructor(props) {
        super(props);
        this.state = {stars: [{'name': 'Unknown'}]};
    }
    componentDidMount() {
        fetch('/dsp/api/stars')
        .then(res => res.json())
        .then((data) => {
            this.setState({stars: data});
        })
        .catch(console.log);
        console.log(this.state.stars);
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

class Planet extends React.Component {
    constructor(props) {
        super(props);
        this.state = {name: "", trade: [], factories: []};
    }
    componentDidMount() {
        fetch('/dsp/api/stars/1/planets/1')
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
                        {this.state.trade.map(item => item.value < 0 ? <div>{item.name}:{item.value}</div> : "")}
                    <div className="title">Exports</div>
                        {this.state.trade.map(item => item.value > 0 ? <div>{item.name}:{item.value}</div> : "")}
                </div>
                <div className='wrapper'>
                    {this.state.factories.map(item => <Factory factory={item}/> )}
                </div>
            </div>
        );
    }
}

class Factory extends React.Component {
    render() {
        return (
            <div className="factory">
                <div>Name: {this.props.factory.name}</div>
                <div>Recipe: {this.props.factory.recipe}</div>
                <div>Machine: {this.props.factory.machine}</div>
                <div>Count: {this.props.factory.count}</div>
                <div>Production:</div>
                {Object.entries(this.props.factory.production).map((key, value) => {
                    return (<div>{key}: {value}</div>);
                })}
            </div>
        );
    }
}

class Interface extends React.Component {
    render() {
        return (
            <div className="main">
                <System/>
                <Planet/>
            </div>
        );
    }
}

// =====================================================

ReactDOM.render(
    <Interface />,
    document.getElementById('root')
);
