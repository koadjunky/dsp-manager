import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import CardActionArea from '@mui/material/CardActionArea';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import Typography from '@mui/material/Typography';
import TableRow from '@mui/material/TableRow';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import { Link } from "react-router-dom";
import { createTheme } from '@mui/material/styles';
import { ThemeProvider } from '@emotion/react';

const theme = createTheme();

theme.typography.h6 = {
    fontSize: '1.0rem'
};

theme.typography.body1 = {
    fontSize: '0.8rem'
};
class Star extends React.Component {
    render() {
        return (
            <ThemeProvider theme={theme}>
                <Card variant="outlined" sx={{ maxWidth: 240, minWidth: 240, m: 3}}>
                    <CardActionArea component={Link} to={`/stars/${this.props.star.name}`}>
                        <CardMedia component="div" image="/images/star.png" sx={{ minHeight: 120, maxHeight: 120 }} alt="Star">
                            <Typography variant="h6" component="div" color="common.white">{this.props.star.name}</Typography>
                        </CardMedia>
                        <CardContent>
                            <Typography variant="h6" component="div" color="common.white">Imports:</Typography>
                            <Table size="small">
                                <TableBody>
                                    {Object.entries(this.props.star.trade).map(([key, value], index) => {
                                        return (value < 0 ? 
                                            <TableRow>
                                                <TableCell style={{borderBottom: "none"}}>{key}:</TableCell>
                                                <TableCell align="right" style={{borderBottom: "none"}}>{value}</TableCell>
                                            </TableRow>
                                        : "");
                                    })}
                                </TableBody>
                            </Table>
                            <Typography variant="h6" component="div" color="common.white">Exports:</Typography>
                            <Table size="small">
                                <TableBody>
                                    {Object.entries(this.props.star.trade).map(([key, value], index) => {
                                        return (value > 0 ? 
                                            <TableRow>
                                                <TableCell style={{borderBottom: "none"}}>{key}:</TableCell>
                                                <TableCell align="right" style={{borderBottom: "none"}}>{value}</TableCell>
                                            </TableRow>
                                        : "");
                                    })}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </CardActionArea>
                </Card>
            </ThemeProvider>
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
