import { makeStyles } from "@material-ui/core/styles";
import SwipeableDrawer from "@material-ui/core/SwipeableDrawer";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import AssessmentIcon from "@material-ui/icons/Assessment";
import AccountTreeIcon from "@material-ui/icons/AccountTree";
import FolderOpenIcon from "@material-ui/icons/FolderOpen";
import ListIcon from "@material-ui/icons/List";
import LockIcon from "@material-ui/icons/Lock";
import FastForwardIcon from "@material-ui/icons/FastForward";
import React from "react";
import { useDispatch, useSelector } from "react-redux";

import DataSettings from "jasmine-view/data-settings";
import LogSettings from "jasmine-view/log-settings";
import MaterializationSettings from "jasmine-view/materialization-settings";
import PerformanceSettings from "jasmine-view/performance-settings";
import PermissionSettings from "jasmine-view/permission-settings";
import SchemaSettings from "jasmine-view/schema-settings";
import { selectSettingsVisible, toggleSettings } from "jasmine-view/state";

const useStyles = makeStyles((theme) => ({
    drawer: {
        minHeight: "max(300px, 70vh)",
    },
    drawerPaper: {
        minHeight: "max(300px, 70vh)",
    },
}));

export default function ViewSettingsDrawer({
    viewProject,
    viewPath,
    viewId,
}: {
    viewProject: string;
    viewPath: string;
    viewId: number;
}) {
    const classes = useStyles();
    const dispatch = useDispatch();

    const [currentTab, setCurrentTab] = React.useState(0);
    const onClickTab = (event: any, clickedTab: any) =>
        setCurrentTab(clickedTab);

    const settingsVisible = useSelector(selectSettingsVisible);

    const settingsTabBar = (
        <Tabs
            value={currentTab}
            onChange={onClickTab}
            indicatorColor="primary"
            textColor="primary"
            variant="scrollable"
            scrollButtons="auto"
        >
            <Tab
                icon={<FolderOpenIcon />}
                label="Schema"
                id="settings-panel-performance"
            />
            <Tab
                icon={<LockIcon />}
                label="Permissions"
                id="settings-panel-permissions"
            />
            <Tab
                icon={<AccountTreeIcon />}
                label="Data"
                id="settings-panel-data"
            />
            <Tab
                icon={<AssessmentIcon />}
                label="Performance"
                id="settings-panel-performance"
            />
            <Tab
                icon={<FastForwardIcon />}
                label="Materializations"
                id="settings-panel-materializations"
            />
            <Tab icon={<ListIcon />} label="Logs" id="settings-panel-log" />
        </Tabs>
    );

    const settingsContent = [
        <SchemaSettings
            viewProject={viewProject}
            viewPath={viewPath}
            viewId={viewId}
        />,
        <PermissionSettings />,
        <DataSettings />,
        <PerformanceSettings />,
        <MaterializationSettings />,
        <LogSettings viewId={viewId} />,
    ][currentTab];

    return (
        <SwipeableDrawer
            variant="temporary"
            anchor="bottom"
            open={settingsVisible}
            onOpen={() => dispatch(toggleSettings())}
            onClose={() => dispatch(toggleSettings())}
            className={classes.drawer}
            classes={{ paper: classes.drawerPaper }}
        >
            {settingsTabBar}
            {settingsContent}
        </SwipeableDrawer>
    );
}
