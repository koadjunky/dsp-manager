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
        this.state = {trade: []};
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
    render() {
        return (
            <div className="system">
                <div className='id'>{this.state.id}</div>
                <div className="name">{this.state.name}</div>
                <div className="title">Imports</div>
                    {this.state.trade.map(item => item[1] < 0 ? <div>{item[0]}:{item[1]}</div> : "")}
                <div className="title">Exports</div>
                    {this.state.trade.map(item => item[1] > 0 ? <div>{item[0]}:{item[1]}</div> : "")}
            </div>
        )
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
