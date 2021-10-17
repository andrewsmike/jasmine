export type query = {
    queryId: number;
    fullPath: string;
    queryText: string;
};

export type viewState = {
    feedbackCollapsed: boolean;
    settingsVisible: boolean;
    originalQuery?: query;
    editorQuery?: query;
};

export const toggleFeedback = () => ({ type: "view/toggle_feedback" } as const);
export const toggleSettings = () => ({ type: "view/toggle_settings" } as const);

export const setEditorQueryText = (queryText: string) =>
    ({ type: "view/set_editor_query_text", queryText } as const);
export const setEditorQueryFullPath = (fullPath: string) =>
    ({ type: "view/set_editor_query_full_path", fullPath } as const);

export const queryEditorPartialReset = (partialQuery: Partial<query>) =>
    ({ type: "view/query_editor_partial_reset", partialQuery } as const);

export type viewAction = ReturnType<
    | typeof toggleFeedback
    | typeof toggleSettings
    | typeof setEditorQueryText
    | typeof setEditorQueryFullPath
    | typeof queryEditorPartialReset
>;

export const defaultViewState: viewState = {
    feedbackCollapsed: true,
    settingsVisible: false,
    originalQuery: undefined,
    editorQuery: undefined,
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
        case "view/set_editor_query_text":
            return {
                ...state,
                editorQuery: {
                    ...state.editorQuery,
                    queryText: action.queryText,
                },
            };
        case "view/set_editor_query_full_path":
            return {
                ...state,
                editorQuery: {
                    ...state.editorQuery,
                    fullPath: action.fullPath,
                },
            };
        case "view/query_editor_partial_reset":
            return {
                ...state,
                originalQuery: {
                    ...(state.originalQuery || {}), // May not be initialized at this point.
                    ...action.partialQuery,
                },
                editorQuery: {
                    ...(state.editorQuery || {}), // May not be initialized at this point.
                    ...action.partialQuery,
                },
            };
        default:
            return state;
    }
}
