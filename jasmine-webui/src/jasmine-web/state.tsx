import { rootState } from "store";
export * from "jasmine-web/state-reducers";

export const selectNavbarCollapsed = (state: rootState) =>
    state.app.navbarCollapsed;
export const selectAccountPopoverHidden = (state: rootState) =>
    state.app.accountPopoverHidden;
export const selectAppTheme = (state: rootState) => state.app.theme;
