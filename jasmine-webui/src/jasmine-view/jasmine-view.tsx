import { gql, useQuery } from "@apollo/client";
import { useLocation } from "react-router-dom";

import QueryEditor from "jasmine-view/query-editor";
import ViewFeedbackBar from "jasmine-view/view-feedback-bar";
import ViewSettingsDrawer from "jasmine-view/view-settings-drawer";

const viewFromPathQuery = gql`
    query ViewFromPath(
        $projectName: String!
        $viewPath: String!
        $organizationId: ID
    ) {
        view_from_path(
            project_name: $projectName
            view_path: $viewPath
            organization_id: $organizationId
        ) {
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
`;

const viewFromIdQuery = gql`
    query ViewFromId($viewId: ID!) {
        view(id: $viewId) {
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
`;

function isIn(elem: any, values: any): boolean {
    return values.indexOf(elem) >= 0;
}

function viewAttrsFromPath(urlPath: string) {
    const prefix = "/console/view/";
    console.assert(urlPath.startsWith(prefix));

    const viewFullPath = urlPath.slice(prefix.length);
    if (isIn("/", viewFullPath)) {
        const fullPathRegex = /\[([^/\]]+)\]\/(.+)/;
        const [, projectName, viewPath] = viewFullPath.match(
            fullPathRegex
        ) as RegExpMatchArray;
        return { pathType: "viewPath", projectName, viewPath };
    } else {
        return { pathType: "viewId", viewId: parseInt(viewFullPath) };
    }
}

export default function JasmineView() {
    const { pathname: pathName } = useLocation();

    var {
        pathType,
        viewId: urlViewId,
        projectName: urlProjectName,
        viewPath: urlViewPath,
    } = viewAttrsFromPath(pathName);

    // Two paths: Resolve by path, or resolve by ID.
    const viewByPathResults = useQuery(viewFromPathQuery, {
        skip: pathType !== "viewPath",
        variables: {
            organizationId: 1,
            projectName: urlProjectName,
            viewPath: urlViewPath,
        },
    });
    const viewByIdResults = useQuery(viewFromIdQuery, {
        skip: pathType !== "viewId",
        variables: { viewId: urlViewId },
    });

    var loading, error, data;
    if (pathType === "viewPath") {
        ({ loading, error, data } = viewByPathResults);
    } else if (pathType === "viewId") {
        ({ loading, error, data } = viewByIdResults);
    } else {
        console.assert(false);
    }

    const urlLocation =
        pathType === "viewPath"
            ? `at [${urlProjectName}]/${urlViewPath}`
            : `with ID ${urlViewId}`;
    if (loading) {
        return <div> Loading... </div>;
    } else if (pathType === "viewPath" && !data.view_from_path) {
        return <div> There are no views {urlLocation}. </div>;
    } else if (pathType === "viewId" && (!data || !data.view)) {
        return <div> There is no view {urlLocation}. </div>;
    } else if (error) {
        return <div> Could not load view {urlLocation}. </div>;
    }

    var viewData;
    if (pathType === "viewPath") {
        viewData = data.view_from_path;
    } else if (pathType === "viewId") {
        viewData = data.view;
    } else {
        console.assert(false);
    }

    // Fill in missing fields.
    var {
        view_id: viewId,
        project: { name: projectName },
        path: viewPath,
        spec: { query_text: queryText },
    } = viewData;

    return (
        <>
            <QueryEditor
                queryId={viewId}
                projectName={projectName}
                queryPath={viewPath}
                queryText={queryText}
                refetchQueries={[viewFromIdQuery, viewFromPathQuery]}
            />
            <ViewFeedbackBar viewId={viewId} />
            <ViewSettingsDrawer
                viewProject={projectName}
                viewPath={viewPath}
                viewId={viewId}
            />
        </>
    );
}
