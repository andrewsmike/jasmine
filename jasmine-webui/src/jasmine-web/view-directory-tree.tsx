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

interface ViewDirectoryArgs {
    organizationId: number;
}

type ViewType = "query";

interface ViewDirectoryProject {
    name: string;
    views: {
        view_id: number;
        view_type: ViewType;
        path: string;
    }[];
}
interface ViewDirectoryData {
    organization: {
        projects: ViewDirectoryProject[];
    };
}

const viewDirectoryQuery = gql`
    query orgViewDirectory($organizationId: ID!) {
        organization(id: $organizationId) {
            projects {
                name
                views {
                    view_id
                    view_type
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
    project: ViewDirectoryProject,
    className: string
): ReactNode {
    const viewIdDirectory = unflattenedMap(
        mapFromArray(project.views, (view) => [view.path, view.view_id])
    );
    const projectName = "[" + project.name + "]";

    return treeViewFromDirectory(viewIdDirectory, [projectName], className);
}

export default function JasmineNavBar() {
    const classes = useStyles();
    const history = useHistory();
    const dispatch = useDispatch();

    const organizationId = 1;

    const { loading, error, data } = useQuery<
        ViewDirectoryData,
        ViewDirectoryArgs
    >(viewDirectoryQuery, { variables: { organizationId } });

    const directoryOpenView = (event: any, viewDirPath: string) => {
        if (viewDirPath.startsWith("leaf:")) {
            history.push("/console/view/" + viewDirPath.slice("leaf:".length));
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
            onNodeSelect={directoryOpenView}
        >
            {data &&
                data.organization.projects.map((item) =>
                    projectDirectoryTreeItems(item, classes.treeItem)
                )}
        </TreeView>
    );
}
