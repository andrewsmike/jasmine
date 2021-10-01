import { gql, useMutation } from "@apollo/client";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Divider from "@material-ui/core/Divider";
import { DataGrid, GridColumns, GridRowsProp } from "@material-ui/data-grid";
import PlayCircleFilledIcon from "@material-ui/icons/PlayCircleFilled";

import { mapFromArray } from "utils/map-utils";

const useStyles = makeStyles((theme) => ({
    button: {
        margin: theme.spacing(0.5),
        alignSelf: "flex-start",
    },
    dataGrid: {
        margin: theme.spacing(0.5),
    },
}));

const viewResultPreviewMutation = gql`
    mutation viewResultPreview($viewId: ID!) {
        preview_view_result(id: $viewId) {
            success
            error
            result
        }
    }
`;

function columnsFromRows(rows: GridRowsProp): GridColumns {
    /* Unable to infer columns without data. */
    if (rows.length === 0) return [];

    const columnNames: string[] = Object.keys(rows[0]);
    const columnHeaderRow: any = Object.fromEntries(
        mapFromArray(columnNames, (columnName) => [columnName, columnName])
    );

    /* Narrow column names shouldn't be squished by the column controls, add a base width. */
    const baseWidth = 10;
    const columnMaxWidth: Map<string, number> = mapFromArray(
        columnNames,
        (columnName) => [
            columnName,
            baseWidth +
                Math.max(
                    ...rows
                        .concat([columnHeaderRow])
                        .map((row) => ((row[columnName] || "") + "").length)
                ),
        ]
    );

    const fontWidth = 7.5;
    return columnNames.map((colName: string) => ({
        field: colName,
        flex: columnMaxWidth.get(colName),
        minWidth: (columnMaxWidth.get(colName) as number) * fontWidth,
        hide: colName === "id",
    }));
}

export default function ViewResultPreview({
    viewId,
    disabled,
}: {
    viewId: number;
    disabled: boolean;
}) {
    const classes = useStyles();

    const [viewResultsMutation, { data, loading, error }] = useMutation(
        viewResultPreviewMutation,
        {
            variables: { viewId },
        }
    );

    var resultRows: any[] = [];
    var resultColumns: any[] = [];

    const results = data?.preview_view_result?.result;
    if (results !== undefined && results !== null) {
        resultRows = results;

        resultRows = resultRows.map((row: any, rowIndex: number) => {
            row["id"] = rowIndex;
            return row;
        });

        resultColumns = columnsFromRows(resultRows);
    }

    const networkError = error?.message;
    const sqlError = data?.preview_view_result?.error;
    const finalError =
        (networkError
            ? `Network connection error: ${networkError}`
            : undefined) ||
        (sqlError ? `Backend SQL error: ${sqlError}` : undefined);

    return (
        <>
            <Divider />
            <Button
                className={classes.button}
                variant="contained"
                color="secondary"
                disabled={disabled}
                startIcon={<PlayCircleFilledIcon />}
                onClick={() => viewResultsMutation()}
            >
                Run
            </Button>
            <DataGrid
                className={classes.dataGrid}
                rows={resultRows}
                columns={resultColumns}
                pageSize={10}
                loading={loading}
                error={finalError ? { message: finalError } : undefined}
                density="compact"
                rowsPerPageOptions={[1, 5, 10, 20, 50]}
            />
        </>
    );
}
