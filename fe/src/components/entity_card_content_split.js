import React from 'react';
import CardContent from '@mui/material/CardContent';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableRow from '@mui/material/TableRow';
import TableCell from '@mui/material/TableCell';
import Typography from '@mui/material/Typography';

class SplitEntityCardContent extends React.Component {
    render() {
        return (
            <CardContent>
                <Typography variant="h6" component="div">Imports:</Typography>
                <Table size="small">
                    <TableBody>
                        {Object.entries(this.props.map).map(([key, value], index) => {
                            return (value < 0 ? 
                                <TableRow>
                                    <TableCell style={{borderBottom: "none"}}>{key}:</TableCell>
                                    <TableCell align="right" style={{borderBottom: "none"}}>{value}</TableCell>
                                </TableRow> 
                            : "");
                        })}
                    </TableBody>
                </Table>
                <Typography variant="h6" component="div">Exports:</Typography>
                <Table size="small">
                    <TableBody>
                        {Object.entries(this.props.map).map(([key, value], index) => {
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
        );
    }
}

export default SplitEntityCardContent;