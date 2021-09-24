import { gql, useLazyQuery, useMutation } from "@apollo/client";
import { makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import Button from "@material-ui/core/Button";
import Paper from "@material-ui/core/Paper";
import TextField from "@material-ui/core/TextField";
import FeedbackIcon from "@material-ui/icons/Feedback";
import FlashAuto from "@material-ui/icons/FlashAuto";
import SaveIcon from "@material-ui/icons/Save";
import SettingsIcon from "@material-ui/icons/Settings";
import { useState } from "react";
import { useDispatch } from "react-redux";
import { Prompt } from "react-router";

import SqlEditor from "jasmine-view/sql-editor";
import { toggleFeedback } from "jasmine-view/state";

const useStyles = makeStyles((theme) => ({
    editorPaper: {
        display: "flex",
        flexDirection: "column",
        flexGrow: 1,
        margin: "10px",
        padding: "10px",
        minWidth: "1px",
    },
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

const saveSqlQueryText = gql`
    mutation saveSqlQueryText($queryId: ID!, $queryText: String!) {
        update_query_text(id: $queryId, query_text: $queryText) {
            success
            error
            result {
                view_id
                project {
                    name
                }
                path
                spec {
                    ... on QuerySpec {
                        query_text
                    }
                }
            }
        }
    }
`;

const formattedSqlQueryTextQuery = gql`
    query formattedQueryText($queryText: String!) {
        formatted_query_text(query_text: $queryText)
    }
`;

export default function JasmineQuery({
    queryId,
    projectName,
    queryPath,
    queryText,
    refetchQueries,
}: {
    queryId: number;
    projectName: string;
    queryPath: string;
    queryText: string;
    refetchQueries: any[];
}) {
    const dispatch = useDispatch();
    const classes = useStyles();

    /*
    const narrowMode = useMediaQuery((theme: any) =>
        theme.breakpoints.down("xs")
    );
    */
    const narrowButtonMode = useMediaQuery("(max-width: 420px)");

    const [code, setCode] = useState(queryText);

    const [saveQueryTextMutation] = useMutation(saveSqlQueryText, {
        refetchQueries: refetchQueries,
        variables: { queryId, queryText: code },
    });
    const [formatQuery] = useLazyQuery(formattedSqlQueryTextQuery, {
        onCompleted: (data) => setCode(data.formatted_query_text),
    });

    const codeUnchanged = queryText === code;

    const fullPath = "[" + projectName + "]/" + queryPath;

    return (
        <>
            <Prompt
                when={!codeUnchanged}
                message="You have unsaved changes. Discard and continue?"
            />
            <Paper className={classes.editorPaper} elevation={6}>
                <div className={classes.queryBar}>
                    <TextField
                        className={classes.queryPathBox}
                        variant="outlined"
                        label="Name"
                        value={fullPath}
                        size="small"
                    />
                    <div className={classes.queryButtonBar}>
                        <Button
                            className={classes.button}
                            variant="contained"
                            color="primary"
                            disabled={codeUnchanged}
                            onClick={() => saveQueryTextMutation()}
                            startIcon={narrowButtonMode ? "" : <SaveIcon />}
                        >
                            {narrowButtonMode ? <SaveIcon /> : "Save"}
                        </Button>
                        <Button
                            className={classes.button}
                            variant="contained"
                            color="secondary"
                            onClick={() =>
                                formatQuery({ variables: { queryText: code } })
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

                <SqlEditor code={code || ""} setCode={setCode} />
            </Paper>
        </>
    );
}
