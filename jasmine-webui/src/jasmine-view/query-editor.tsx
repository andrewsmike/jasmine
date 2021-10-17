import { gql, useMutation } from "@apollo/client";
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Prompt } from "react-router";
import { useHistory } from "react-router-dom";

import SqlEditor from "jasmine-view/sql-editor";
import QueryEditorBar from "jasmine-view/query-editor-bar";
import ViewResultPreview from "jasmine-view/view-result-preview";
import {
    queryEditorPartialReset,
    selectEditorQuery,
    selectEditorQueryUnchanged,
    selectEditorQueryValid,
    selectOriginalQuery,
    setEditorQueryFullPath,
    setEditorQueryText,
} from "jasmine-view/state";
import { setNotification } from "jasmine-web/state";
import { fullPath, fullPathParts, fullPathValid } from "utils/path-utils";

const useStyles = makeStyles((theme) => ({
    editorPaper: {
        display: "flex",
        flexDirection: "column",
        flexGrow: 1,
        margin: "10px",
        padding: "10px",
        minWidth: "1px",
    },
}));

const updateQueryTextMutation = gql`
    mutation updateQueryText($queryId: ID!, $queryText: String!) {
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

const moveQueryMutation = gql`
    mutation moveQuery(
        $queryId: ID!
        $projectName: String!
        $queryPath: String!
    ) {
        move_view(
            id: $queryId
            project_name: $projectName
            view_path: $queryPath
        ) {
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

export default function QueryEditor({
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
    const dispatch = useDispatch();
    const history = useHistory();

    /* When the original query gets created/updated, update both the original and editor queries. */
    useEffect(() => {
        dispatch(
            queryEditorPartialReset({
                fullPath: fullPath(projectName, queryPath),
            })
        );
    }, [projectName, queryPath]);
    useEffect(() => {
        dispatch(queryEditorPartialReset({ queryText }));
    }, [queryText]);

    /* updateQuery: Convert query updates into a sequence of delta-applying mutations. */
    const editorQueryValid = useSelector(selectEditorQueryValid);

    const originalQuery = useSelector(selectOriginalQuery);
    const editorQuery = useSelector(selectEditorQuery);

    /* Parse out arguments for the updateQueryText mutation. */
    var editorQueryProjectName, editorQueryPath;
    if (editorQueryValid)
        [editorQueryProjectName, editorQueryPath] = fullPathParts(
            editorQuery?.fullPath as string
        );
    else [editorQueryProjectName, editorQueryPath] = [undefined, undefined];

    const [updateQueryText] = useMutation(updateQueryTextMutation, {
        refetchQueries: refetchQueries,
        variables: { queryId, queryText: editorQuery?.queryText },
        onCompleted: (data) => {
            dispatch(
                setNotification(`Saved view at ${originalQuery?.fullPath}.`)
            );
            dispatch(
                queryEditorPartialReset({ queryText: editorQuery?.queryText })
            );
        },
    });

    const [moveQuery] = useMutation(moveQueryMutation, {
        refetchQueries: refetchQueries,
        variables: {
            queryId,
            projectName: editorQueryProjectName,
            queryPath: editorQueryPath,
        },
        onCompleted: (data) => {
            dispatch(
                setNotification(`Moved view to ${editorQuery?.fullPath}.`)
            );
            dispatch(
                queryEditorPartialReset({ fullPath: editorQuery?.fullPath })
            );
            history.push(`/console/view/${editorQuery?.fullPath}`);
        },
    });

    const updateQuery = () => {
        if (originalQuery === undefined || editorQuery === undefined)
            // For typechecking.
            return;

        if (!editorQueryValid) return;

        if (originalQuery.queryText !== editorQuery.queryText)
            updateQueryText();

        if (originalQuery.fullPath !== editorQuery.fullPath) {
            moveQuery();
        }
    };

    /* These should be pushed into subcomponents at some point.
     * They're not relevant to the top-level form logic.
     */
    const editorQueryUnchanged = useSelector(selectEditorQueryUnchanged);
    const setEditorCode = (queryText: string) => {
        dispatch(setEditorQueryText(queryText));
    };

    return (
        <>
            <Prompt
                when={!editorQueryUnchanged}
                message="You have unsaved changes. Discard and continue?"
            />
            <Paper className={classes.editorPaper} elevation={6}>
                <QueryEditorBar
                    queryId={queryId}
                    updateQuery={updateQuery}
                    refetchQueries={refetchQueries}
                />
                <SqlEditor
                    code={editorQuery?.queryText || ""}
                    setCode={setEditorCode}
                />
                <ViewResultPreview
                    viewId={queryId}
                    disabled={!editorQueryUnchanged}
                />
            </Paper>
        </>
    );
}
