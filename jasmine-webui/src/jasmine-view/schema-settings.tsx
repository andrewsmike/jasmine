import { gql, useMutation } from "@apollo/client";
import red from "@material-ui/core/colors/red";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import DeleteIcon from "@material-ui/icons/Delete";

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

export default function SchemaSettings({ viewId }: { viewId: number }) {
    const classes = useStyles();

    const [deleteViewMutation] = useMutation(deleteView, {
        refetchQueries: ["orgViewDirectory", "ViewFromPath", "ViewFromId"],
        variables: { viewId },
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
