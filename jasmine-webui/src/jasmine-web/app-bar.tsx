import AppBar from "@material-ui/core/AppBar";
import EmojiFoodBeverageIcon from "@material-ui/icons/EmojiFoodBeverage";
import MenuIcon from "@material-ui/icons/Menu";
import IconButton from "@material-ui/core/IconButton";
import Hidden from "@material-ui/core/Hidden";
import { makeStyles } from "@material-ui/core/styles";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import { useDispatch } from "react-redux";
import { Link } from "react-router-dom";

import AccountBox from "jasmine-web/account-box";
import { toggleNavbar } from "jasmine-web/state";

const useStyles = makeStyles((theme) => ({
    appBar: {
        maxHeight: 64,
        position: "relative",
    },
    logoText: {
        flexGrow: 1,
    },
}));

export default function JasmineAppBar() {
    const classes = useStyles();
    const dispatch = useDispatch();

    return (
        <AppBar className={classes.appBar} position="static" color="primary">
            <Toolbar variant="regular">
                <Hidden smUp>
                    <IconButton
                        color="inherit"
                        size="medium"
                        onClick={() => dispatch(toggleNavbar())}
                    >
                        <MenuIcon fontSize="large" />
                    </IconButton>
                </Hidden>
                <IconButton
                    color="inherit"
                    component={Link}
                    to="/console"
                    size="medium"
                >
                    <EmojiFoodBeverageIcon fontSize="large" />
                </IconButton>
                <Typography variant="h6" className={classes.logoText}>
                    Jasmine ETL
                </Typography>
                <AccountBox />
            </Toolbar>
        </AppBar>
    );
}
