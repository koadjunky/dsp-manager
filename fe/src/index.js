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


class Interface extends React.Component {
    render() {
        return (
            <div className="main">
                <System name="Sun"/>
                <System name="Alpha Centauri"/>
            </div>
        );
    }
}

// =====================================================

ReactDOM.render(
    <Interface />,
    document.getElementById('root')
);
