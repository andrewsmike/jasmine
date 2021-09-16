import { gql, useQuery } from "@apollo/client";
import Avatar from "@material-ui/core/Avatar";
import Hidden from "@material-ui/core/Hidden";
import Paper from "@material-ui/core/Paper";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";

import { useRef } from "react";
import { useDispatch, useSelector } from "react-redux";

import AccountPopover from "jasmine-web/account-popover";
import {
    selectAccountPopoverHidden,
    toggleAccountPopover,
} from "jasmine-web/state";

const useStyles = makeStyles((theme) => ({
    accountBox: {
        display: "flex",
        alignItems: "center",
        padding: theme.spacing(0.5),
        paddingLeft: theme.spacing(1),
        paddingRight: theme.spacing(1),
        marginLeft: theme.spacing(2),
        marginRight: theme.spacing(2),
    },
    accountAvatar: {
        //flexGrow: 80,
        //color: theme.palette.getContrastText("#6fa8dcff"),
        //backgroundColor: "#6fa8dcff",
    },
    accountText: {
        marginLeft: theme.spacing(2),
        paddingRight: theme.spacing(1),
    },
}));

const accountInfoQuery = gql`
    {
        user(id: 1) {
            organization {
                name
            }
            name
        }
    }
`;

export default function AccountBox() {
    const classes = useStyles();
    const dispatch = useDispatch();

    const { loading, error, data } = useQuery(accountInfoQuery);

    const accountBoxRef = useRef<HTMLElement | null>(null);

    const accountPopoverHidden = useSelector(selectAccountPopoverHidden);

    if (loading) {
        return <div> </div>;
    }

    const userOrg = error ? "Error fetching data" : data.user.organization.name;
    const userName = error ? "Error fetching data" : data.user.name;

    return (
        <>
            <Paper
                elevation={4}
                className={classes.accountBox}
                onClick={() => dispatch(toggleAccountPopover())}
                ref={accountBoxRef}
            >
                <Avatar alt={userName} className={classes.accountAvatar} />
                <Hidden xsDown={true}>
                    <Typography variant="body2" className={classes.accountText}>
                        {userOrg}
                    </Typography>
                </Hidden>
            </Paper>
            <AccountPopover
                hidden={accountPopoverHidden}
                account={userName}
                elem={() => accountBoxRef.current}
            />
        </>
    );
}
