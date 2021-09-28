import { gql, useMutation } from "@apollo/client";
import red from "@material-ui/core/colors/red";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import DeleteIcon from "@material-ui/icons/Delete";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";

import { setNotification } from "jasmine-web/state";

const useStyles = makeStyles((theme) => ({
    deleteViewButton: {
        backgroundColor: red[300],
        margin: theme.spacing(2),
        "&:hover": {
            backgroundColor: red[400],
        },
    },
}));

const deleteView = gql`
    mutation deleteView($viewId: ID!) {
        delete_view(id: $viewId) {
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

    const [deleteViewMutation] = useMutation(deleteView, {
        refetchQueries: ["orgViewDirectory", "ViewFromPath", "ViewFromId"],
        variables: { viewId },
        onCompleted: (data) => {
            dispatch(
                setNotification(`Deleted view at [${viewProject}]/${viewPath}.`)
            );
            history.push("/console");
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
