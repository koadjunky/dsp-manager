import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActionArea from '@mui/material/CardActionArea';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import Typography from '@mui/material/Typography';
import TableRow from '@mui/material/TableRow';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormControl from '@mui/material/FormControl';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import { createTheme } from '@mui/material/styles';
import { recipes } from './recipes';
import { machines } from './machines';
import { ThemeProvider } from '@emotion/react';


const theme = createTheme();

theme.typography.h6 = {
    fontSize: '1.0rem'
};

theme.typography.body1 = {
    fontSize: '0.8rem'
}

export default class Factory extends React.Component {

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
                <ThemeProvider theme={theme}>
                <Card variant="outlined">
                    <CardActionArea onClick={() => this.openDialog()}>
                        <CardContent>
                            <Typography variant="h6" component="div">
                                Name:
                            </Typography>
                            <Typography variant="body1" component="div">
                                {this.props.factory.name}
                            </Typography>
                            <Typography variant="h6" component="div">
                                Recipe:
                            </Typography>
                            <Typography variant="body1" component="div">
                                {this.props.factory.recipe}
                            </Typography>
                            <Typography variant="h6" component="div">
                                Machine:
                            </Typography>
                            <Typography variant="body1" component="div">
                                {this.props.factory.machine}
                            </Typography>
                            <Typography variant="h6" component="div">
                                Count:
                            </Typography>
                            <Typography variant="body1" component="div">
                                {this.props.factory.count}
                            </Typography>
                            <Typography variant="h6" component="div">
                                Production:
                            </Typography>
                            <Table size="small">
                                <TableBody>
                                    {Object.entries(this.props.factory.production).map(([key, value], index) => {
                                        return (<TableRow>
                                                    <TableCell>{key}:</TableCell>
                                                    <TableCell>{value}</TableCell>
                                                </TableRow>);
                                    })}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </CardActionArea>
                </Card>
                </ThemeProvider>
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
