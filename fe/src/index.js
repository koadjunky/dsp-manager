import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./index.css";
import PlanetViewWrapper from './planet_view'
import StarViewWrapper from './star_view';
import SystemView from './system_view';


// =====================================================

ReactDOM.render(
    <div className="main">
        <Router>
            <Routes>
                <Route path="/" element={<SystemView /> } />
                <Route path="/stars/:star_name" element={ <StarViewWrapper /> } />
                <Route path="/stars/:star_name/planets/:planet_name" element={ <PlanetViewWrapper /> } />
            </Routes>
        </Router>
    </div>,
    document.getElementById('root')
);
