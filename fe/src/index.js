import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useParams, Link } from "react-router-dom";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormControl from '@mui/material/FormControl';
import "./index.css";


const recipes = [
    {
        label: 'Fractinator',
        value: 'fractinator'
    },
    {
        label: 'Water Pump',
        value: 'water_pump'
    },
    {
        label: 'Water Pump',
        value: 'water_pump'
    },
    {
        label: 'Sulfric Acid Pump',
        value: 'sulfric_acid_pump'
    },
    {
        label: 'Oil Extractor',
        value: 'oil_extractor'
    },
    {
        label: 'Orbital Collector',
        value: 'orbital_collector'
    },
    {
        label: 'Coal Vein',
        value: 'coal_vein'
    },
    {
        label: 'Copper Ore Vein',
        value: 'copper_ore_vein'
    },
    {
        label: 'Fire Ice Vein',
        value: 'fire_ice_vein'
    },
    {
        label: 'Fractal Silicon Vein',
        value: 'fractal_silicon_vein'
    },
    {
        label: 'Iron Ore Vein',
        value: 'iron_ore_vein'
    },
    {
        label: 'Kimberlite Ore Vein',
        value: 'kimberlite_ore_vein'
    },
    {
        label: 'Optical Grating Crystal Vein',
        value: 'optical_grating_crystal_vein'
    },
    {
        label: 'Organic Crystal Vein',
        value: 'organic_crystal_vein'
    },
    {
        label: 'Silicon Ore Vein',
        value: 'silicon_ore_vein'
    },
    {
        label: 'Spinform Stalagmite Crystal Vein',
        value: 'spinform_stalagmite_crystal_vein'
    },
    {
        label: 'Stone Vein',
        value: 'stone_vein'
    },
    {
        label: 'Titanium Ore Vein',
        value: 'titanium_ore_vein'
    },
    {
        label: 'Unipolar Magnet Vein',
        value: 'unipolar_magnet_vein'
    },
    {
        label: 'Gear',
        value: 'gear'
    },
    {
        label: 'Magnetic Coil',
        value: 'magnetic_coil'
    },
    {
        label: 'Prism',
        value: 'prism'
    },
    {
        label: 'Plasma Exciter',
        value: 'plasma_exciter'
    },
    {
        label: 'Titanium Crystal',
        value: 'titanium_crystal'
    },
    {
        label: 'Casimir Crystal',
        value: 'casimir_crystal'
    },
    {
        label: 'Casimir Crystal *',
        value: 'casimir_crystal_plus'
    },
    {
        label: 'Titanium Glass',
        value: 'titanium_glass'
    },
    {
        label: 'Patricle Broadband',
        value: 'patricle_broadband'
    },
    {
        label: 'Plane Filter',
        value: 'plane_filter'
    },
    {
        label: 'Deuteron Fuel Rod',
        value: 'deuteron_fuel_rod'
    },
    {
        label: 'Annihilation Constraint Sphere',
        value: 'annihilation_constraint_sphere'
    },
    {
        label: 'Circuit Board',
        value: 'circuit_board'
    },
    {
        label: 'Processor',
        value: 'processor'
    },
    {
        label: 'Quantum Chip',
        value: 'quantum_chip'
    },
    {
        label: 'Microcrystalline Component',
        value: 'microcrystalline_component'
    },
    {
        label: 'Crystal Silicon *',
        value: 'crystal_silicon_plus'
    },
    {
        label: 'Photon Combiner',
        value: 'photon_combiner'
    },
    {
        label: 'Photon Combiner *',
        value: 'photon_combiner_plus'
    },
    {
        label: 'Solar Sail',
        value: 'solar_sail'
    },
    {
        label: 'Frame Material',
        value: 'frame_material'
    },
    {
        label: 'Dyson Sphere Component',
        value: 'dyson_sphere_component'
    },
    {
        label: 'Small Carrier Rocket',
        value: 'small_carrier_rocket'
    },
    {
        label: 'Electric Motor',
        value: 'electric_motor'
    },
    {
        label: 'Electromagnetic Turbine',
        value: 'electromagnetic_turbine'
    },
    {
        label: 'Patricle Container',
        value: 'patricle_container'
    },
    {
        label: 'Patricle Container *',
        value: 'patricle_container_plus'
    },
    {
        label: 'Graviton Lens',
        value: 'graviton_lens'
    },
    {
        label: 'Super Magnetic Ring',
        value: 'super_magnetic_ring'
    },
    {
        label: 'Iron Ingot',
        value: 'iron_ingot'
    },
    {
        label: 'Magnet',
        value: 'magnet'
    },
    {
        label: 'Copper Ingot',
        value: 'copper_ingot'
    },
    {
        label: 'Stone Brick',
        value: 'stone_brick'
    },
    {
        label: 'Energetic Graphite',
        value: 'energetic_graphite'
    },
    {
        label: 'Silicon Ore',
        value: 'silicon_ore'
    },
    {
        label: 'Crystal Silicon',
        value: 'crystal_silicon'
    },
    {
        label: 'Glass',
        value: 'glass'
    },
    {
        label: 'High Purity Silicon',
        value: 'high_purity_silicon'
    },
    {
        label: 'Diamond',
        value: 'diamond'
    },
    {
        label: 'Diamond *',
        value: 'diamond_plus'
    },
    {
        label: 'Steel',
        value: 'steel'
    },
    {
        label: 'Titanium Ingot',
        value: 'titanium_ingot'
    },
    {
        label: 'Titanium Alloy',
        value: 'titanium_alloy'
    },
    {
        label: 'Oil Refining',
        value: 'refining'
    },
    {
        label: 'X-Ray Cracking',
        value: 'x_ray_cracking'
    },
    {
        label: 'Deuterium',
        value: 'deuterium'
    },
    {
        label: 'Antimatter',
        value: 'antimatter'
    },
    {
        label: 'Strange Matter',
        value: 'strange_matter'
    },
    {
        label: 'Plastic',
        value: 'plastic'
    },
    {
        label: 'Sulfric Acid',
        value: 'sulfric_acid'
    },
    {
        label: 'Organic Crystal',
        value: 'organic_crystal'
    },
    {
        label: 'Graphene',
        value: 'graphene'
    },
    {
        label: 'Graphene *',
        value: 'graphene_plus'
    },
    {
        label: 'Carbon Nanotube',
        value: 'carbon_nanotube'
    },
    {
        label: 'Carbon Nanotube *',
        value: 'carbon_nanotube_plus'
    },
    {
        label: 'Blue Science',
        value: 'blue_science'
    },
    {
        label: 'Red Science',
        value: 'red_science'
    },
    {
        label: 'Yellow Science',
        value: 'yellow_science'
    },
    {
        label: 'Purple Science',
        value: 'purple_science'
    },
    {
        label: 'Green Science',
        value: 'green_science'
    },
    {
        label: 'White Science',
        value: 'white_science'
    }
];

const machines = [
    {
        label: "Assembler Mk.1",
        value: "assembler1"
    },
    {
        label: "Assembler Mk.2",
        value: "assembler2"
    },
    {
        label: "Assembler Mk.3",
        value: "assembler3"
    },
    {
        label: "Arc Smelter",
        value: "arc_smelter"
    },
    {
        label: "Plane Smelter",
        value: "plane_smelter"
    },
    {
        label: "Refinery",
        value: "refinery"
    },
    {
        label: "Chemical Plant",
        value: "chemical_plant"
    },
    {
        label: "Fractinator",
        value: "fractinator"
    },
    {
        label: "Particle Collider",
        value: "particle_collider"
    },
    {
        label: "Matrix Lab",
        value: "matrix_lab"
    },
    {
        label: "Mine",
        value: "mine"
    },
    {
        label: "Pump",
        value: "water_pump"
    },
    {
        label: "Oil Extractor",
        value: "oil_extractor"
    },
    {
        label: "Orbital Collector",
        value: "orbital_collector"
    }
];

class Factory extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            name: props.factory.name,
            recipe: props.factory.recipe,
            machine: props.factory.machine,
            count: props.factory.count,
            dialogOpen: false
        };
    }

    openDialog() {
        this.setState({...this.state, dialogOpen: true } );
    }

    closeDialog() {
        this.setState({...this.state, dialogOpen: false });
    }

    changeRecipe(arg) {
        this.setState({...this.state, recipe: arg.target.value});
    }

    changeMachine(arg) {
        this.setState({...this.state, machine: arg.target.value});
    }

    render() {
        return (
            <div>
                <div className="factory" onClick={() => this.openDialog()}>
                    <div>Name: {this.props.factory.name}</div>
                    <div>Recipe: {this.props.factory.recipe}</div>
                    <div>Machine: {this.props.factory.machine}</div>
                    <div>Count: {this.props.factory.count}</div>
                    <div>Production:</div>
                    {Object.entries(this.props.factory.production).map(([key, value], index) => {
                        return (<div>{key}: {value}</div>);
                    })}
                </div>
                <Dialog open={this.state.dialogOpen} onClose={() => this.closeDialog()}>
                <DialogTitle>Configure Factory</DialogTitle>
                <DialogContent>
                    <Box component="form" noValidate autoComplete="off" sx={{ display: 'flex', flexDirection: 'column', m:'auto', width:'fit-content' }}>
                    <FormControl sx={{ mt: 2 }}>
                        <TextField required label="Name" defaultValue={this.state.name}/>
                    </FormControl>
                    <FormControl sx={{ mt: 2 }}>
                        <TextField select label="Recipe" value={this.state.recipe} onChange={(arg) => this.changeRecipe(arg)}>
                            {recipes.map((option) => (
                                <MenuItem key={option.value} value={option.value}>
                                    {option.label}
                                </MenuItem>
                            ))}
                        </TextField>
                    </FormControl>
                    <FormControl sx={{ mt: 2 }}>
                        <TextField select label="Machine" value={this.state.machine} onChange={(arg) => this.changeMachine(arg)}>
                            {machines.map((option) => (
                                <MenuItem key={option.value} value={option.value}>
                                    {option.label}
                                </MenuItem>
                            ))}
                        </TextField>
                    </FormControl>
                    <FormControl sx={{ mt: 2 }}>
                        <TextField required label="Count" defaultValue={this.state.count}/>
                    </FormControl>
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => this.closeDialog()}>Submit</Button>
                    <Button onClick={() => this.closeDialog()}>Cancel</Button>
                </DialogActions>
            </Dialog>
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

function PlanetViewWrapper() {
    const { star_name, planet_name } = useParams();
    return (<PlanetView star_name={star_name} planet_name={planet_name} /> );
}

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

function StarViewWrapper() {
    const { star_name } = useParams();
    return (<StarView star_name={star_name} /> );
}

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

class SystemView extends React.Component {
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
