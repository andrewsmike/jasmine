import { gql, useLazyQuery, useMutation } from "@apollo/client";
import grey from "@material-ui/core/colors/grey";
import { makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import Button from "@material-ui/core/Button";
import Paper from "@material-ui/core/Paper";
import TextField from "@material-ui/core/TextField";
import FlashAuto from "@material-ui/icons/FlashAuto";
import SaveIcon from "@material-ui/icons/Save";
import SettingsIcon from "@material-ui/icons/Settings";
import { useState } from "react";
import { Prompt } from "react-router";

import SqlEditor from "jasmine-query/sql-editor";

const useStyles = makeStyles((theme) => ({
    editorPaper: {
        display: "flex",
        flexDirection: "column",
        flexGrow: 1,
        margin: "10px",
        padding: "10px",
        /*flexBasis: 'auto',*/
    },
    queryPathBox: {
        flexGrow: 1,
        marginRight: theme.spacing(2),
    },
    saveButton: {
        marginLeft: "auto",
        //marginLeft: theme.spacing(2),
    },
    formatButton: {
        marginLeft: theme.spacing(1.5),
    },
    settingsButton: {
        marginLeft: theme.spacing(1.5),
        backgroundColor: grey[200],
        paddingLeft: theme.spacing(2),
        paddingRight: theme.spacing(2),
        minWidth: "0%",
    },
    queryBar: {
        display: "flex",
        flexDirection: "row",
        marginBottom: theme.spacing(1),
    },
}));

const saveSqlQueryText = gql`
    mutation saveSqlQueryText($queryId: ID!, $queryText: String!) {
        update_query_text(id: $queryId, query_text: $queryText) {
            success
            error
            result {
                query_id
                project {
                    name
                }
                path
                query_text
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
    const classes = useStyles();
    const narrowMode = useMediaQuery((theme: any) =>
        theme.breakpoints.down("sm")
    );

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
                    <Button
                        className={classes.saveButton}
                        variant="contained"
                        color="primary"
                        disabled={codeUnchanged}
                        onClick={() => saveQueryTextMutation()}
                        startIcon={narrowMode ? "" : <SaveIcon />}
                    >
                        {narrowMode ? <SaveIcon /> : "Save"}
                    </Button>
                    <Button
                        className={classes.formatButton}
                        variant="contained"
                        color="secondary"
                        onClick={() =>
                            formatQuery({ variables: { queryText: code } })
                        }
                        startIcon={narrowMode ? "" : <FlashAuto />}
                    >
                        {narrowMode ? <FlashAuto /> : "Autoformat"}
                    </Button>
                    <Button
                        className={classes.settingsButton}
                        variant="contained"
                    >
                        <SettingsIcon fontSize="medium" />
                    </Button>
                </div>

                <SqlEditor code={code || ""} setCode={setCode} />
            </Paper>
        </>
    );
}
