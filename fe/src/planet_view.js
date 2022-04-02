import React from 'react';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import { styled } from '@mui/material/styles';
import { useParams, Link } from "react-router-dom";
import Factory from './factory'

const Item = styled(Paper)(({theme}) => ({
    padding: theme.spacing(1),
}));

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
            <Grid container spacing={1}>
                <Grid item xs={12}>
                    <Item>
                        <Link to={`/stars/${this.props.star_name}`}>Back to {this.props.star_name}</Link>
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
                        {this.state.factories.map(item => <Factory factory={item}/> )}
                    </Box>
                </Grid>
            </Grid>
        );
    }
}

export default function PlanetViewWrapper() {
    const { star_name, planet_name } = useParams();
    return (<PlanetView star_name={star_name} planet_name={planet_name} /> );
}
