import React from 'react';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import EntityCard from "./components/entity_card";

class Star extends React.Component {
    render() {
        return (
            <EntityCard link={`/stars/${this.props.star.name}`}
                        image='/images/star.png'
                        alt='Star'
                        name={this.props.star.name}
                        map={this.props.star.trade}
                        variant="split" />
        );
    }
}

export default class SystemView extends React.Component {
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
            <Grid container spacing={1}>
                <Grid item xs={12}>
                    <Box sx={{display: 'flex', flexWrap: 'wrap', m: '10'}}>
                        {this.state.stars.map(item => <Star key={item.name} star={item}/>)}
                    </Box>
                </Grid>
            </Grid>
        );
    }
}
