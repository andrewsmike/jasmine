import CssBaseline from "@material-ui/core/CssBaseline";
import {
    createTheme,
    makeStyles,
    ThemeProvider,
} from "@material-ui/core/styles";
import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import HomePage from "home-page";
import JasmineAppBar from "jasmine-web/app-bar";
import JasmineNavBar from "jasmine-web/nav-bar";
import JasmineView from "jasmine-view/jasmine-view";

const useStyles = makeStyles((theme) => ({
    navBarSplit: {
        display: "flex",
        height: "calc(100vh - 64px)",
    },
}));

const jasmineTheme = {
    primary: {
        main: "#8862a8", // '#8e83ba', // '#627da8', // 8db3f1
        contrastText: "#FFF",
    },
    secondary: {
        main: "#ffea00", // '#ba8e83', //f1998d',
        contrastText: "#000",
    },
};

export default function App() {
    const classes = useStyles();
    /* const preferredTheme = useSelector(selectAppTheme); */
    /* {type: preferredTheme} */

    const theme = React.useMemo(
        () =>
            createTheme({
                palette: jasmineTheme,
            }),
        []
    );

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Router>
                <JasmineAppBar />
                <div className={classes.navBarSplit}>
                    <JasmineNavBar />
                    <Switch>
                        <Route path="/console/about">About!</Route>
                        <Route path="/console/view/:id">
                            <JasmineView />
                        </Route>
                        <Route path="/console">
                            <HomePage />
                        </Route>
                    </Switch>
                </div>
            </Router>
        </ThemeProvider>
    );
}
