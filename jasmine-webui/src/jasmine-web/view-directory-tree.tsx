import { gql, useQuery } from "@apollo/client";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import ExpandLessIcon from "@material-ui/icons/ExpandLess";
import DescriptionOutlinedIcon from "@material-ui/icons/DescriptionOutlined";
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
    classTypeIcon: {
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

function treeViewFromDirectory(
    directory: RecursiveMap<[string, number]>,
    path: string[],
    labelClassName: string,
    iconClassName: string
): ReactNode {
    const name = path.at(-1);
    const pathStr = path.join("/");

    if (directory instanceof Map) {
        const children = arrayFromMap(directory, (subdir, subdirItems) =>
            treeViewFromDirectory(
                subdirItems,
                path.concat([subdir]),
                labelClassName,
                iconClassName
            )
        );
        const label = (
            <Typography className={labelClassName}> {name} </Typography>
        );
        return (
            <TreeItem
                classes={{ label: labelClassName }}
                key={pathStr}
                nodeId={"dir:" + pathStr}
                label={label}
            >
                {" "}
                {children}{" "}
            </TreeItem>
        );
    } else {
        const [viewType] = directory;

        const viewTypeIcon = {
            query: (
                <DescriptionOutlinedIcon
                    className={iconClassName}
                    color="primary"
                />
            ),
        }[viewType];

        const label = (
            <Typography className={labelClassName}>
                {viewTypeIcon}
                {name}
            </Typography>
        );

        return (
            <TreeItem
                classes={{ label: labelClassName }}
                key={pathStr}
                nodeId={"leaf:" + pathStr}
                label={label}
            />
        );
    }
}

function projectDirectoryTreeItems(
    project: ViewDirectoryProject,
    labelClassName: string,
    iconClassName: string
): ReactNode {
    const viewNodeDirectory = unflattenedMap<RecursiveMap<[string, number]>>(
        mapFromArray(project.views, (view) => [
            view.path,
            [view.view_type, view.view_id],
        ])
    );
    const projectName = "[" + project.name + "]";

    return treeViewFromDirectory(
        viewNodeDirectory,
        [projectName],
        labelClassName,
        iconClassName
    );
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

    return (
        <TreeView
            className={classes.root}
            defaultCollapseIcon={<ExpandMoreIcon />}
            defaultExpandIcon={<ExpandLessIcon />}
            onNodeSelect={directoryOpenView}
        >
            {data &&
                data.organization.projects.map((item) =>
                    projectDirectoryTreeItems(
                        item,
                        classes.treeItem,
                        classes.classTypeIcon
                    )
                )}
        </TreeView>
    );
}
