import { combineReducers } from "redux";
import { configureStore } from "@reduxjs/toolkit";

import { appAction, appReducer, appState } from "jasmine-web/state-reducers";
import {
    viewAction,
    viewReducer,
    viewState,
} from "jasmine-view/state-reducers";

export type rootState = {
    app: appState;
    view: viewState;
};

export type rootAction = appAction | viewAction;

const rootReducer = combineReducers({
    app: appReducer,
    view: viewReducer,
});

export default configureStore({
    reducer: rootReducer,
});
