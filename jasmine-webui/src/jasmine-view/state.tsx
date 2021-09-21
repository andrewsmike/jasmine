import { rootState } from "store";
export * from "jasmine-view/state-reducers";

export const selectFeedbackCollapsed = (state: rootState) =>
    state.view.feedbackCollapsed;
