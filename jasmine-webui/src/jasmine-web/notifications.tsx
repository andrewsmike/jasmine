import React from "react";
import { useDispatch, useSelector } from "react-redux";
import Snackbar from "@material-ui/core/Snackbar";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";

import { resetNotification, selectNotification } from "jasmine-web/state";

export default function Notifications() {
    const notification = useSelector(selectNotification);
    const dispatch = useDispatch();

    const handleClose = () => dispatch(resetNotification());

    return (
        <Snackbar
            anchorOrigin={{
                vertical: "bottom",
                horizontal: "left",
            }}
            open={notification !== undefined}
            autoHideDuration={6000}
            onClose={handleClose}
            message={notification}
            action={
                <>
                    <IconButton
                        size="small"
                        color="inherit"
                        onClick={handleClose}
                    >
                        <CloseIcon fontSize="small" />
                    </IconButton>
                </>
            }
        />
    );
}
