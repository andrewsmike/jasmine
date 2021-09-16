import { gql, useQuery } from "@apollo/client";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import ExpandLessIcon from "@material-ui/icons/ExpandLess";
import TreeView from "@material-ui/lab/TreeView";
import TreeItem from "@material-ui/lab/TreeItem";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import { useHistory } from "react-router-dom";
import { ReactNode } from "react";
import { useDispatch } from "react-redux";

import { toggleNavbar } from "jasmine-web/state";
import {
    arrayFromMap,
    mapFromArray,
    unflattenedMap,
    RecursiveMap,
} from "utils/map-utils";

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
        marginLeft: theme.spacing(1),
    },
    treeItem: {
        [theme.breakpoints.down("xs")]: {
            fontSize: theme.typography.pxToRem(22),
            padding: theme.spacing(0.25),
        },
        [theme.breakpoints.only("sm")]: {
            fontSize: theme.typography.pxToRem(16),
            padding: theme.spacing(0.15),
        },
        [theme.breakpoints.up("md")]: {
            fontSize: theme.typography.pxToRem(16),
        },
    },
}));

interface QueryDirectoryArgs {
    organizationId: number;
}

interface QueryDirectoryProject {
    name: string;
    queries: {
        query_id: number;
        path: string;
    }[];
}
interface QueryDirectoryData {
    organization: {
        projects: QueryDirectoryProject[];
    };
}

const queryDirectoryQueries = gql`
    query orgQueryDirectory($organizationId: ID!) {
        organization(id: $organizationId) {
            projects {
                name
                queries {
                    query_id
                    path
                }
            }
        }
    }
`;
function treeViewFromDirectory(
    directory: RecursiveMap<number>,
    path: string[],
    className: string
): ReactNode {
    const name = path.at(-1);
    const pathStr = path.join("/");

    const label = <Typography className={className}> {name} </Typography>;

    if (directory instanceof Map) {
        const children = arrayFromMap(directory, (subdir, subdirItems) =>
            treeViewFromDirectory(subdirItems, path.concat([subdir]), className)
        );
        return (
            <TreeItem
                classes={{ label: className }}
                key={pathStr}
                nodeId={"dir:" + pathStr}
                label={label}
            >
                {" "}
                {children}{" "}
            </TreeItem>
        );
    } else {
        return (
            <TreeItem
                classes={{ label: className }}
                key={pathStr}
                nodeId={"leaf:" + pathStr}
                label={label}
            />
        );
    }
}

function projectDirectoryTreeItems(
    project: QueryDirectoryProject,
    className: string
): ReactNode {
    const queryIdDirectory = unflattenedMap(
        mapFromArray(project.queries, (query) => [query.path, query.query_id])
    );
    const projectName = "[" + project.name + "]";

    return treeViewFromDirectory(queryIdDirectory, [projectName], className);
}

export default function JasmineNavBar() {
    const classes = useStyles();
    const history = useHistory();
    const dispatch = useDispatch();

    const organizationId = 1;

    const { loading, error, data } = useQuery<
        QueryDirectoryData,
        QueryDirectoryArgs
    >(queryDirectoryQueries, { variables: { organizationId } });

    const directoryOpenQuery = (event: any, queryDirPath: string) => {
        if (queryDirPath.startsWith("leaf:")) {
            history.push(
                "/console/query/" + queryDirPath.slice("leaf:".length)
            );
            dispatch(toggleNavbar());
        }
    };

    if (loading) return <div> Loading... </div>;
    else if (error)
        return (
            <div> Could not load organization with ID {organizationId}. </div>
        );

    return (
        <TreeView
            className={classes.root}
            defaultCollapseIcon={<ExpandMoreIcon />}
            defaultExpandIcon={<ExpandLessIcon />}
            onNodeSelect={directoryOpenQuery}
        >
            {data &&
                data.organization.projects.map((item) =>
                    projectDirectoryTreeItems(item, classes.treeItem)
                )}
        </TreeView>
    );
}
