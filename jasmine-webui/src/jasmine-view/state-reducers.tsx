export type viewState = {
    feedbackCollapsed: boolean;
};

export const toggleFeedback = () => ({ type: "view/toggle_feedback" } as const);

export type viewAction = ReturnType<typeof toggleFeedback>;

export const defaultViewState: viewState = {
    feedbackCollapsed: true,
};

export function viewReducer(
    state: viewState = defaultViewState,
    action: viewAction
) {
    switch (action.type) {
        case "view/toggle_feedback":
            return {
                ...state,
                feedbackCollapsed: !state.feedbackCollapsed,
            };
        default:
            return state;
    }
}
