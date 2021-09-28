export type ColorThemeType = "dark" | "light";

export type appState = {
    theme: ColorThemeType;
    navbarCollapsed: boolean;
    accountPopoverHidden: boolean;
    notification?: string;
};

export const toggleNavbar = () => ({ type: "app/toggle_navbar" } as const);

export const toggleAccountPopover = () =>
    ({ type: "app/toggle_account_popover" } as const);

export const setTheme = (theme: ColorThemeType) =>
    ({ type: "app/set_theme", theme } as const);

export const setNotification = (notification: string) =>
    ({ type: "app/set_notification", notification } as const);
export const resetNotification = () =>
    ({ type: "app/reset_notification" } as const);

export type appAction = ReturnType<
    | typeof toggleNavbar
    | typeof toggleAccountPopover
    | typeof setTheme
    | typeof setNotification
    | typeof resetNotification
>;

export const defaultAppState: appState = {
    theme: "light",
    navbarCollapsed: true,
    accountPopoverHidden: true,
    notification: undefined,
};

export function appReducer(
    state: appState = defaultAppState,
    action: appAction
) {
    switch (action.type) {
        case "app/toggle_navbar":
            return {
                ...state,
                navbarCollapsed: !state.navbarCollapsed,
            };
        case "app/toggle_account_popover":
            return {
                ...state,
                accountPopoverHidden: !state.accountPopoverHidden,
            };
        case "app/set_notification":
            return {
                ...state,
                notification: action.notification,
            };
        case "app/reset_notification":
            return {
                ...state,
                notification: undefined,
            };
        case "app/set_theme":
            return {
                ...state,
                theme: action.theme,
            };
        default:
            return state;
    }
}
