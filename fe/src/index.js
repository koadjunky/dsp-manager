import React from 'react';
import ReactDOM from 'react-dom';
import "./index.css";

class System extends React.Component {
    render() {
        return (
            <div className="system">
                <div className="name">{this.props.name}</div>
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
