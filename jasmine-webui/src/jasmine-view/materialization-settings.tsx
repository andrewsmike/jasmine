import { gql, useLazyQuery } from "@apollo/client";
import { makeStyles } from "@material-ui/core/styles";

import { fullPath } from "utils/path-utils";

const useStyles = makeStyles((theme) => ({
    materializationBar: {},
}));

export default function MaterializationSettings({
    viewId,
}: {
    viewId: number;
}) {
    const classes = useStyles();

    return <div />;
}
