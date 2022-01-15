import { gql, useQuery } from "@apollo/client";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import ExpandLessIcon from "@material-ui/icons/ExpandLess";
import DescriptionOutlinedIcon from "@material-ui/icons/DescriptionOutlined";
import RestoreIcon from "@material-ui/icons/Restore";
import TreeView from "@material-ui/lab/TreeView";
import TreeItem from "@material-ui/lab/TreeItem";
import { useHistory } from "react-router-dom";
import { ReactNode } from "react";
import { useDispatch } from "react-redux";

import { setNavbarCollapsed } from "jasmine-web/state";
import {
    arrayFromMap,
    mapFromArray,
    unflattenedMap,
    RecursiveMap,
} from "utils/map-utils";
import { fullPath, pathDirectories } from "utils/path-utils";
import { mapFromSet } from "utils/set-utils";

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
    viewTypeIcon: {
        fontSize: "1em",
        marginRight: theme.spacing(0.5),
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

interface DirectoryViewNode {
    path: string;
    icon: ReactNode;
}

export function DirectoryView({
    classes,
    onClick,
    nodes,
}: {
    classes: { root?: string; treeItem?: string };
    onClick: (event: object, nodeId: string) => void;
    nodes: DirectoryViewNode[];
}) {
    const nodeDirectories = new Set(
        nodes.map((node) => Array.from(pathDirectories(node.path))).flat()
    );
    const nodeDirectoryIds = mapFromSet(
        nodeDirectories,
        (dir_path) => `dir:${dir_path}`
    );

    const nodeDirectory = unflattenedMap<RecursiveMap<DirectoryViewNode>>(
        mapFromArray(nodes, (node) => [node.path, node])
    );

    const children = treeViewFromDirectory(
        nodeDirectory,
        [],
        classes.treeItem,
        true
    );

    return (
        <TreeView
            className={classes.root}
            defaultCollapseIcon={<ExpandMoreIcon />}
            defaultExpandIcon={<ExpandLessIcon />}
            onNodeSelect={onClick}
            defaultExpanded={nodeDirectoryIds}
        >
            {children}
        </TreeView>
    );
}

function treeViewFromDirectory(
    directory: RecursiveMap<DirectoryViewNode>,
    path: string[],
    className: string | undefined,
    topLevel: boolean
): ReactNode {
    var children, nodeType, icon;
    if (directory instanceof Map) {
        children = arrayFromMap(directory, (subdir, subdirItems) =>
            treeViewFromDirectory(
                subdirItems,
                path.concat([subdir]),
                className,
                false
            )
        );
        nodeType = "dir";
        icon = undefined;
    } else {
        children = undefined;
        nodeType = "leaf";
        icon = directory.icon;
    }

    const name = path.at(-1);
    const label = (
        <Typography className={className}>
            {" "}
            {icon}
            {name}{" "}
        </Typography>
    );

    const pathStr = path.join("/");
    const nodeId = `${nodeType}:${pathStr}`;

    if (topLevel) {
        return <> {children} </>;
    } else {
        return (
            <TreeItem
                classes={{ label: className }}
                key={pathStr}
                nodeId={nodeId}
                label={label}
            >
                {children}
            </TreeItem>
        );
    }
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
            dispatch(setNavbarCollapsed(true));
        }
    };

    if (loading) return <div> Loading... </div>;
    else if (error)
        return (
            <div> Could not load organization with ID {organizationId}. </div>
        );

    const viewTypeIcon = {
        query: (
            <DescriptionOutlinedIcon
                className={classes.viewTypeIcon}
                color="primary"
            />
        ),
        history_table: (
            <RestoreIcon className={classes.viewTypeIcon} color="primary" />
        ),
    };

    const viewNodes = (data as ViewDirectoryData).organization.projects
        .map((project) =>
            project.views.map((view) => ({
                path: fullPath(project.name, view.path),
                icon: viewTypeIcon[view.view_type],
            }))
        )
        .flat() as DirectoryViewNode[];

    return (
        <DirectoryView
            classes={{ root: classes.root, treeItem: classes.treeItem }}
            onClick={directoryOpenView}
            nodes={viewNodes}
        />
    );
}
