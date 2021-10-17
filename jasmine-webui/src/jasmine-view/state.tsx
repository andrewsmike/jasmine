import _ from "lodash";

import { rootState } from "store";
import { fullPathValid } from "utils/path-utils";

export * from "jasmine-view/state-reducers";

export const selectFeedbackCollapsed = (state: rootState) =>
    state.view.feedbackCollapsed;
export const selectSettingsVisible = (state: rootState) =>
    state.view.settingsVisible;

export const selectOriginalQuery = (state: rootState) =>
    state.view.originalQuery;
export const selectEditorQuery = (state: rootState) => state.view.editorQuery;

export const selectEditorQueryFullPath = (state: rootState) =>
    state.view.editorQuery?.fullPath;
export const selectEditorQueryText = (state: rootState) =>
    state.view.editorQuery?.queryText;

export const selectEditorQueryUnchanged = (state: rootState) =>
    _.isEqual(state.view.originalQuery, state.view.editorQuery);

export const selectEditorQueryValid = (state: rootState) =>
    state.view.editorQuery !== undefined &&
    fullPathValid(state.view.editorQuery.fullPath);
