import { combineReducers } from "redux";
import { configureStore } from "@reduxjs/toolkit";

import { appAction, appReducer, appState } from "jasmine-web/state-reducers";

export type rootState = {
    app: appState;
};

export type rootAction = appAction;

const rootReducer = combineReducers({
    app: appReducer,
});

export default configureStore({
    reducer: rootReducer,
});
