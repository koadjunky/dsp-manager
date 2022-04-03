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
import Paper from '@mui/material/Paper';
import { useParams, Link } from "react-router-dom";
import { createTheme, styled } from '@mui/material/styles';
import { ThemeProvider } from '@emotion/react';

const theme = createTheme();

theme.typography.h6 = {
    fontSize: '1.0rem'
};

theme.typography.body1 = {
    fontSize: '0.8rem'
};
class Planet extends React.Component {
    render() {
        return (
            // TODO: Extract common Card
            <ThemeProvider theme={theme}>
            <Card variant="outlined" sx={{ maxWidth: 240, minWidth: 240, m: 3}}>
                <CardActionArea component={Link} to={`/stars/${this.props.star_name}/planets/${this.props.planet.name}`}>
                    <CardMedia component="div" image="/images/planet.png" sx={{ minHeight: 120, maxHeight: 120 }} alt="Planet">
                        <Typography variant="h6" component="div" color="common.white">{this.props.planet.name}</Typography>
                    </CardMedia>
                    <CardContent>
                        <Typography variant="h6" component="div" color="common.white">Imports:</Typography>
                        <Table size="small">
                            <TableBody>
                                {Object.entries(this.props.planet.trade).map(([key, value], index) => {
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
                                {Object.entries(this.props.planet.trade).map(([key, value], index) => {
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
