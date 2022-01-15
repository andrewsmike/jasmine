import { gql, useMutation } from "@apollo/client";
import red from "@material-ui/core/colors/red";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import DeleteIcon from "@material-ui/icons/Delete";
import HighlightOffIcon from "@material-ui/icons/HighlightOff";
import RestoreIcon from "@material-ui/icons/Restore";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";

import { setNotification } from "jasmine-web/state";
import { toggleSettings } from "jasmine-view/state";

const useStyles = makeStyles((theme) => ({
    deleteViewButton: {
        backgroundColor: red[300],
        margin: theme.spacing(2),
        "&:hover": {
            backgroundColor: red[400],
        },
    },
}));

const createHistoryTable = gql`
    mutation createHistoryTable(
        $sourceDbName: String!
        $sourceTableName: String!
    ) {
        delete_view(id: $viewId) {
            success
            error
        }
    }
`;

const deleteView = gql`
    mutation deleteView($viewId: ID!, $force: boolean!) {
        delete_view(id: $viewId, force_no_cleanup: $force) {
            success
            error
        }
    }
`;

export default function SchemaSettings({
    viewProject,
    viewPath,
    viewId,
}: {
    viewProject: string;
    viewPath: string;
    viewId: number;
}) {
    const classes = useStyles();
    const dispatch = useDispatch();
    const history = useHistory();

    // Adding create-history-table button, force-kill button.
    const [addHistoryTableViewMutation] = useMutation(deleteView, {
        refetchQueries: ["orgViewDirectory", "ViewFromPath", "ViewFromId"],
        variables: { viewId },
        onCompleted: (data) => {
            if (data.create_view.success) {
                dispatch(
                    setNotification(
                        `Created history table at [${viewProject}]/${viewPath}_history.`
                    )
                );
                dispatch(toggleSettings());
                history.push("/console");
            } else {
                dispatch(
                    setNotification(
                        `Failed to deleted view: ` + data.delete_view.error
                    )
                );
            }
        },
    });

    const [deleteViewMutation] = useMutation(deleteView, {
        refetchQueries: ["orgViewDirectory", "ViewFromPath", "ViewFromId"],
        variables: { viewId, force: false },
        onCompleted: (data) => {
            if (data.delete_view.success) {
                dispatch(
                    setNotification(
                        `Deleted view at [${viewProject}]/${viewPath}.`
                    )
                );
                dispatch(toggleSettings());
                history.push("/console");
            } else {
                dispatch(
                    setNotification(
                        `Failed to deleted view: ` + data.delete_view.error
                    )
                );
            }
        },
    });

    return (
        <div>
            <Button
                className={classes.deleteViewButton}
                variant="contained"
                startIcon={<DeleteIcon />}
                onClick={() => deleteViewMutation()}
            >
                Delete View
            </Button>
        </div>
    );
}
