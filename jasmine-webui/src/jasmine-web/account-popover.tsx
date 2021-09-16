import Popover from "@material-ui/core/Popover";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import { useDispatch } from "react-redux";

import { toggleAccountPopover } from "jasmine-web/state";

const useStyles = makeStyles((theme) => ({
    popoverText: {
        padding: theme.spacing(2),
    },
}));

export default function AccountPopover({
    hidden,
    account,
    elem,
}: {
    hidden: boolean;
    account: string;
    elem: any;
}) {
    const dispatch = useDispatch();
    const classes = useStyles();

    const userName = account;

    return (
        <Popover
            open={!hidden}
            onClose={() => dispatch(toggleAccountPopover())}
            anchorOrigin={{
                vertical: "bottom",
                horizontal: "right",
            }}
            transformOrigin={{
                vertical: "top",
                horizontal: "right",
            }}
            anchorEl={elem}
        >
            <Typography className={classes.popoverText} variant="body2">
                Hello {userName}!
            </Typography>
        </Popover>
    );
}
