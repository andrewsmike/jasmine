import { gql, useQuery } from "@apollo/client";
import { useLocation } from "react-router-dom";

import QueryEditor from "jasmine-query/query-editor";
import QueryFeedbackBar from "jasmine-query/query-feedback-bar";

const sqlQueryFromPathQuery = gql`
    query SqlQuery(
        $projectName: String!
        $queryPath: String!
        $organizationId: ID
    ) {
        sql_query_from_path(
            project_name: $projectName
            query_path: $queryPath
            organization_id: $organizationId
        ) {
            query_id
            project {
                name
            }
            path
            query_text
        }
    }
`;

const sqlQueryFromIdQuery = gql`
    query SqlQuery($queryId: ID!) {
        sql_query(id: $queryId) {
            query_id
            project {
                name
            }
            path
            query_text
        }
    }
`;

function isIn(elem: any, values: any): boolean {
    return values.indexOf(elem) >= 0;
}

function queryAttrsFromPath(urlPath: string) {
    const prefix = "/console/query/";
    console.assert(urlPath.startsWith(prefix));

    const queryFullPath = urlPath.slice(prefix.length);
    if (isIn("/", queryFullPath)) {
        const fullPathRegex = /\[([^/\]]+)\]\/(.+)/;
        const [, projectName, queryPath] = queryFullPath.match(
            fullPathRegex
        ) as RegExpMatchArray;
        return { pathType: "queryPath", projectName, queryPath };
    } else {
        return { pathType: "queryId", queryId: parseInt(queryFullPath) };
    }
}

export default function JasmineQuery() {
    const { pathname: pathName } = useLocation();

    var {
        pathType,
        queryId: urlQueryId,
        projectName: urlProjectName,
        queryPath: urlQueryPath,
    } = queryAttrsFromPath(pathName);

    // Two paths: Resolve by path, or resolve by ID.
    const queryByPathResults = useQuery(sqlQueryFromPathQuery, {
        skip: pathType !== "queryPath",
        variables: {
            organizationId: 1,
            projectName: urlProjectName,
            queryPath: urlQueryPath,
        },
    });
    const queryByIdResults = useQuery(sqlQueryFromIdQuery, {
        skip: pathType !== "queryId",
        variables: { queryId: urlQueryId },
    });

    var loading, error, data;
    if (pathType === "queryPath") {
        ({ loading, error, data } = queryByPathResults);
    } else if (pathType === "queryId") {
        ({ loading, error, data } = queryByIdResults);
    } else {
        console.assert(false);
    }

    if (loading) return <div> Loading... </div>;
    else if (error) {
        return <div> Could not load query at {pathName}. </div>;
    }

    var queryData;
    if (pathType === "queryPath") {
        queryData = data.sql_query_from_path;
    } else if (pathType === "queryId") {
        queryData = data.sql_query;
    } else {
        console.assert(false);
    }

    // Fill in missing fields.
    var {
        query_id: queryId,
        project: { name: projectName },
        path: queryPath,
        query_text: queryText,
    } = queryData;

    return (
        <>
            <QueryEditor
                queryId={queryId}
                projectName={projectName}
                queryPath={queryPath}
                queryText={queryText}
                refetchQueries={[sqlQueryFromIdQuery, sqlQueryFromPathQuery]}
            />
            <QueryFeedbackBar queryId={queryId} queryText={queryText} />
        </>
    );
}
