export type viewState = {
    feedbackCollapsed: boolean;
    settingsVisible: boolean;
};

export const toggleFeedback = () => ({ type: "view/toggle_feedback" } as const);
export const toggleSettings = () => ({ type: "view/toggle_settings" } as const);

export type viewAction = ReturnType<
    typeof toggleFeedback | typeof toggleSettings
>;

export const defaultViewState: viewState = {
    feedbackCollapsed: true,
    settingsVisible: false,
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
        case "view/toggle_settings":
            return {
                ...state,
                settingsVisible: !state.settingsVisible,
            };
        default:
            return state;
    }
}
