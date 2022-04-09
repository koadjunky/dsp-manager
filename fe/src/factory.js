import React from 'react';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import CardActionArea from '@mui/material/CardActionArea';
import Avatar from '@mui/material/Avatar';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormControl from '@mui/material/FormControl';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import { ThemeProvider } from '@emotion/react';
import { createTheme } from '@mui/material/styles';
import { recipes } from './recipes';
import { machines } from './machines';
import CombinedEntityCardContent from './components/entity_card_content_combined';

const theme = createTheme();

theme.typography.h6 = {
    fontSize: '1.0rem'
};

theme.typography.body1 = {
    fontSize: '0.8rem'
};

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
                    <Card variant="outlined" sx={{ maxWidth: 240, minWidth: 240, m: 3 }}>
                        <CardActionArea onClick={() => this.openDialog()}>
                            <CardMedia component="div" image="/images/factory.png" sx={{ minHeight: 120, maxHeight: 120 }} alt="Factory">
                                <Typography variant="h6" component="div" color="common.white">{this.props.factory.name}</Typography>
                                <Stack direction="row" spacing={1} sx={{ marginTop: 7 }}>
                                    <Avatar alt="Assembler 1" src={"/images/" + this.props.factory.machine + ".webp"} sx={{ bgcolor: "white" }} />
                                    <Avatar alt={this.props.factory.count} sx={{ bgcolor: "white", color: "black" }}>{this.props.factory.count}</Avatar>
                                </Stack>
                            </CardMedia>
                            <CombinedEntityCardContent map={this.props.factory.production} />
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
