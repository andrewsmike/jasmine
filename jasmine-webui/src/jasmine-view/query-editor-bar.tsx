import { gql, useLazyQuery } from "@apollo/client";
import { makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import FeedbackIcon from "@material-ui/icons/Feedback";
import FlashAuto from "@material-ui/icons/FlashAuto";
import SaveIcon from "@material-ui/icons/Save";
import SettingsIcon from "@material-ui/icons/Settings";
import { useDispatch, useSelector } from "react-redux";

import {
    selectEditorQueryFullPath,
    selectEditorQueryText,
    selectEditorQueryUnchanged,
    selectEditorQueryValid,
    setEditorQueryFullPath,
    setEditorQueryText,
    toggleFeedback,
    toggleSettings,
} from "jasmine-view/state";
import { fullPath } from "utils/path-utils";

const useStyles = makeStyles((theme) => ({
    queryPathBox: {
        flexGrow: 1,
    },
    saveButton: {
        [theme.breakpoints.up("md")]: {
            marginLeft: "auto",
        },
    },
    button: {
        [theme.breakpoints.up("md")]: {
            marginLeft: theme.spacing(1),
        },
        [theme.breakpoints.down("sm")]: {
            flexGrow: 1,
            marginLeft: theme.spacing(0.5),
            marginRight: theme.spacing(0.5),
        },
    },
    queryBar: {
        [theme.breakpoints.up("sm")]: {
            display: "flex",
            flexDirection: "row",
            marginBottom: theme.spacing(1),
        },
        [theme.breakpoints.down("sm")]: {
            display: "flex",
            flexDirection: "column",
            marginBottom: theme.spacing(1),
        },
    },
    queryButtonBar: {
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        [theme.breakpoints.up("md")]: {
            marginLeft: theme.spacing(1),
        },
        [theme.breakpoints.down("sm")]: {
            marginTop: theme.spacing(1),
        },
    },
}));

const formattedSqlQueryTextQuery = gql`
    query formattedQueryText($queryText: String!) {
        formatted_query_text(query_text: $queryText)
    }
`;

export default function QueryEditorBar({
    queryId,
    updateQuery,
    refetchQueries,
}: {
    queryId: number;
    updateQuery: () => void;
    refetchQueries: any[];
}) {
    const dispatch = useDispatch();
    const classes = useStyles();

    const narrowButtonMode = useMediaQuery("(max-width: 420px)");

    const editorQueryFullPath = useSelector(selectEditorQueryFullPath);
    const editorQueryText = useSelector(selectEditorQueryText);

    const editorQueryUnchanged = useSelector(selectEditorQueryUnchanged);
    const editorQueryValid = useSelector(selectEditorQueryValid);

    const [formatQuery] = useLazyQuery(formattedSqlQueryTextQuery, {
        onCompleted: (data) =>
            dispatch(setEditorQueryText(data.formatted_query_text)),
    });

    return (
        <div className={classes.queryBar}>
            <TextField
                className={classes.queryPathBox}
                onChange={(event) =>
                    dispatch(setEditorQueryFullPath(event.target.value))
                }
                variant="outlined"
                label="Name"
                value={editorQueryFullPath}
                error={!editorQueryValid}
                helperText={
                    editorQueryValid
                        ? undefined
                        : "Invalid path. Format: [project]/path/to/query."
                }
                size="small"
            />
            <div className={classes.queryButtonBar}>
                <Button
                    className={classes.button}
                    variant="contained"
                    color="primary"
                    disabled={editorQueryUnchanged || !editorQueryValid}
                    onClick={() => updateQuery()}
                    startIcon={narrowButtonMode ? "" : <SaveIcon />}
                >
                    {narrowButtonMode ? <SaveIcon /> : "Save"}
                </Button>
                <Button
                    className={classes.button}
                    variant="contained"
                    color="secondary"
                    onClick={() =>
                        formatQuery({
                            variables: { queryText: editorQueryText },
                        })
                    }
                    startIcon={narrowButtonMode ? "" : <FlashAuto />}
                >
                    {narrowButtonMode ? <FlashAuto /> : "Autoformat"}
                </Button>
                <Button
                    className={classes.button}
                    variant="contained"
                    onClick={() => dispatch(toggleSettings())}
                >
                    <SettingsIcon fontSize="medium" />
                </Button>
                <Button
                    className={classes.button}
                    variant="contained"
                    onClick={() => dispatch(toggleFeedback())}
                >
                    <FeedbackIcon fontSize="medium" />
                </Button>
            </div>
        </div>
    );
}
