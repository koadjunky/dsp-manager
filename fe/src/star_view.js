import React from 'react';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import EntityCard from './components/entity_card';
import { useParams, Link } from "react-router-dom";
import { styled } from '@mui/material/styles';

class Planet extends React.Component {
    render() {
        return (
            <EntityCard link={`/stars/${this.props.star_name}/planets/${this.props.planet.name}`}
                        image="/images/planet.png"
                        alt="Planet"
                        name={this.props.planet.name}
                        map={this.props.planet.trade}
                        variant="split" />
        );
    }
}

const Item = styled(Paper)(({theme}) => ({
    padding: theme.spacing(1),
}));

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
            <Grid container spacing={1}>
                <Grid item xs={12}>
                    <Item>
                        <Link to={'/'}>Back to System</Link>
                    </Item>
                </Grid>
                <Grid item xs={12}>
                    <Item>{this.state.name}</Item>
                </Grid>
                <Grid item xs={6}>
                    <Item>
                        <Typography>Imports</Typography>
                        {Object.entries(this.state.trade).map(([key, value], index) => {
                            return (value < 0 ? <Typography>{key}: {value}</Typography> : "");
                        })}
                    </Item>
                </Grid>
                <Grid item xs={6}>
                    <Item>
                        <Typography>Exports</Typography>
                        {Object.entries(this.state.trade).map(([key, value], index) => {
                            return (value > 0 ? <Typography>{key}: {value}</Typography> : "");
                        })}
                    </Item>
                </Grid>
                <Grid item xs={12}>
                    <Box sx={{display: 'flex', flexWrap: 'wrap', m: '10'}}>
                        {this.state.planets.map(item => <Planet key={item.name} star_name={this.props.star_name} planet={item}/> )}
                    </Box>
                </Grid>
            </Grid>
        );
    }
}

export default function StarViewWrapper() {
    const { star_name } = useParams();
    return (<StarView star_name={star_name} /> );
}
