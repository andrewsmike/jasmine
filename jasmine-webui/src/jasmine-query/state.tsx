import { rootState } from "store";
export * from "jasmine-query/state-reducers";

export const selectFeedbackCollapsed = (state: rootState) =>
    state.query.feedbackCollapsed;
