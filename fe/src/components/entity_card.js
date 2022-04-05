import React from 'react';
import Card from '@mui/material/Card';
import CardActionArea from '@mui/material/CardActionArea';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { Link } from "react-router-dom";
import { createTheme } from '@mui/material/styles';
import { ThemeProvider } from '@emotion/react';
import SplitEntityCardContent from './entity_card_content_split';

const theme = createTheme();

theme.typography.h6 = {
    fontSize: '1.0rem'
};

theme.typography.body1 = {
    fontSize: '0.8rem'
};

class EntityCard extends React.Component {
    render() {
        return (
            <ThemeProvider theme={theme}>
                <Card variant="outlined" sx={{ maxWidth: 240, minWidth: 240, m: 3}}>
                    <CardActionArea component={Link} to={this.props.link}>
                        <CardMedia component="div" image={this.props.image} sx={{ minHeight: 120, maxHeight: 120 }} alt={this.props.alt}>
                            <Typography variant="h6" component="div" color="common.white">{this.props.name}</Typography>
                        </CardMedia>
                        {this.props.variant === 'split' && <SplitEntityCardContent map={this.props.map} />}
                    </CardActionArea>
                </Card>
            </ThemeProvider>
        );
    }
}

export default EntityCard;