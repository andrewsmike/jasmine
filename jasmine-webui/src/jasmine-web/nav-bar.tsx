import { makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import SwipeableDrawer from "@material-ui/core/SwipeableDrawer";
import { useDispatch, useSelector } from "react-redux";

import { selectNavbarCollapsed, toggleNavbar } from "jasmine-web/state";

import NavBarSections from "jasmine-web/nav-bar-sections";

const useStyles = makeStyles((theme) => ({
    drawer: {
        top: 64,
        minWidth: "min(280px, 34vw)",
    },
    narrowDrawer: {
        top: 0,
        minWidth: "max(300px, 60vw)",
    },
    drawerPaper: {
        top: 64,
        position: "static",
        minWidth: "min(280px, 34vw)",
    },
    narrowDrawerPaper: {
        top: 0,
        minWidth: "max(300px, 60vw)",
    },
    sectionName: {
        marginLeft: theme.spacing(1),
        marginTop: theme.spacing(0.5),
    },
}));

export default function JasmineNavBar() {
    const classes = useStyles();
    const dispatch = useDispatch();

    const narrowMode = useMediaQuery((theme: any) =>
        theme.breakpoints.down("xs")
    );
    const navbarCollapsed = useSelector(selectNavbarCollapsed);
    const drawerVisible = !(navbarCollapsed && narrowMode);

    let drawerClass = classes.drawer;
    let drawerPaperClass = classes.drawerPaper;
    if (narrowMode) {
        drawerClass = classes.narrowDrawer;
        drawerPaperClass = classes.narrowDrawerPaper;
    }

    return (
        <SwipeableDrawer
            variant={narrowMode ? "temporary" : "permanent"}
            anchor="left"
            open={drawerVisible}
            onOpen={() => dispatch(toggleNavbar())}
            onClose={() => dispatch(toggleNavbar())}
            className={drawerClass}
            classes={{ paper: drawerPaperClass }}
        >
            <NavBarSections />
        </SwipeableDrawer>
    );
}
