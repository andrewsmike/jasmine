export type queryState = {
    feedbackCollapsed: boolean;
};

export const toggleFeedback = () =>
    ({ type: "query/toggle_feedback" } as const);

export type queryAction = ReturnType<typeof toggleFeedback>;

export const defaultQueryState: queryState = {
    feedbackCollapsed: true,
};

export function queryReducer(
    state: queryState = defaultQueryState,
    action: queryAction
) {
    switch (action.type) {
        case "query/toggle_feedback":
            return {
                ...state,
                feedbackCollapsed: !state.feedbackCollapsed,
            };
        default:
            return state;
    }
}
