import { combineReducers } from "redux";
import { configureStore } from "@reduxjs/toolkit";

import { appAction, appReducer, appState } from "jasmine-web/state-reducers";
import {
    queryAction,
    queryReducer,
    queryState,
} from "jasmine-query/state-reducers";

export type rootState = {
    app: appState;
    query: queryState;
};

export type rootAction = appAction | queryAction;

const rootReducer = combineReducers({
    app: appReducer,
    query: queryReducer,
});

export default configureStore({
    reducer: rootReducer,
});
