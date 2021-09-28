import { rootState } from "store";
export * from "jasmine-view/state-reducers";

export const selectFeedbackCollapsed = (state: rootState) =>
    state.view.feedbackCollapsed;
export const selectSettingsVisible = (state: rootState) =>
    state.view.settingsVisible;
