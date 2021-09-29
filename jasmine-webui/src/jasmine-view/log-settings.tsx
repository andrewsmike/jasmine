import { gql, useQuery } from "@apollo/client";
import { DataGrid } from "@material-ui/data-grid";

interface ViewLogsArgs {
    viewId: number;
}

interface ViewLogsData {
    view: {
        backend_events: {
            backend_event_id: number;
            title: string;
            description: string;
            created_time: string;
            backend: { name: string };
            project?: { name: string };
            view?: { path: string };
        }[];
    };
}

const viewBackendEvents = gql`
    query viewBackendEvents($viewId: ID!) {
        view(id: $viewId) {
            backend_events {
                backend_event_id
                title
                description
                created_time
                backend {
                    name
                }
                project {
                    name
                }
                view {
                    path
                }
            }
        }
    }
`;

export default function LogSettings({ viewId }: { viewId: number }) {
    const { loading, error, data } = useQuery<ViewLogsData, ViewLogsArgs>(
        viewBackendEvents,
        { variables: { viewId } }
    );

    /*
    if (loading)
        return <div> Loading... </div>;
    else if (error)
        return <div> Failed to load logs. </div>;
    */

    const columns = [
        { field: "backendName", headerName: "Backend", minWidth: 140 },
        { field: "projectName", headerName: "Project", minWidth: 140 },
        { field: "viewPath", headerName: "View", minWidth: 200 },
        { field: "eventTitle", headerName: "Event", minWidth: 250, flex: 1 },
        {
            field: "eventDescription",
            headerName: "Details",
            minWidth: 450,
            flex: 2,
        },
        {
            field: "eventCreatedTime",
            headerName: "Time",
            type: "dateTime",
            minWidth: 160,
        },
    ];

    var logEntries: any[] = [];
    if (data !== undefined) {
        logEntries = (data as ViewLogsData).view.backend_events.map(
            (entry) => ({
                id: entry.backend_event_id,
                backendName: entry.backend.name,
                projectName: entry.project?.name,
                viewPath: entry.view?.path,
                eventTitle: entry.title,
                eventDescription: entry.description,
                eventCreatedTime: entry.created_time,
            })
        );
    }

    return (
        <DataGrid
            rows={logEntries}
            columns={columns}
            pageSize={10}
            loading={loading}
            error={error}
            rowsPerPageOptions={[1, 10, 20, 50]}
        />
    );
}
