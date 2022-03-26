import React from 'react';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormControl from '@mui/material/FormControl';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import { recipes } from './recipes';
import { machines } from './machines';

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
