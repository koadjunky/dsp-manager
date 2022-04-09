import React from 'react';
import CardContent from '@mui/material/CardContent';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableRow from '@mui/material/TableRow';
import TableCell from '@mui/material/TableCell';

class CombinedEntityCardContent extends React.Component {
    render() {
        return (
            <CardContent>
                <Table size="small">
                    <TableBody>
                        {Object.entries(this.props.map).map(([key, value], index) => {
                            return (<TableRow>
                                        <TableCell style={{borderBottom: "none"}}>{key}:</TableCell>
                                        <TableCell align="right" style={{borderBottom: "none"}}>{value}</TableCell>
                                    </TableRow>);
                        })}
                    </TableBody>
                </Table>
            </CardContent>
        );
    }
}

export default CombinedEntityCardContent;
