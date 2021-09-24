import { ApolloClient, ApolloProvider, InMemoryCache } from "@apollo/client";
import { Provider } from "react-redux";
import React from "react";
import ReactDOM from "react-dom";

import "css/index.css";
import store from "store";
import JasmineWeb from "./jasmine-web/jasmine-web";
import reportWebVitals from "report-web-vitals";

const graphqlClient = new ApolloClient({
    uri: "/api/graphql",
    cache: new InMemoryCache(),
});

ReactDOM.render(
    <React.StrictMode>
        <ApolloProvider client={graphqlClient}>
            <Provider store={store}>
                <JasmineWeb />
            </Provider>
        </ApolloProvider>
    </React.StrictMode>,
    document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
