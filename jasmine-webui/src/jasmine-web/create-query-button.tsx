import { gql, useMutation } from "@apollo/client";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import { makeStyles } from "@material-ui/core/styles";
import IconButton from "@material-ui/core/IconButton";
import AddBoxOutlinedIcon from "@material-ui/icons/AddBoxOutlined";
import { MouseEvent } from "react";
import { useHistory } from "react-router-dom";

const createSqlQuery = gql`
    mutation createSqlQuery {
        create_query {
            success
            error
            result {
                view_id
                project {
                    name
                }
                path
                spec {
                    ... on QuerySpec {
                        query_text
                    }
                }
            }
        }
    }
`;

const useStyles = makeStyles((theme) => ({
    createQueryButton: {
        paddingTop: theme.spacing(1),
        paddingBottom: theme.spacing(1),
    },
}));

export default function CreateQueryButton() {
    const classes = useStyles();
    const history = useHistory();

    const narrowMode = useMediaQuery((theme: any) =>
        theme.breakpoints.down("xs")
    );

    const [createSqlQueryMutation] = useMutation(createSqlQuery, {
        refetchQueries: ["orgViewDirectory"],
        variables: {},
        onCompleted: (data) => {
            const projectName = data.create_query.result.project.name;
            const queryPath = data.create_query.result.path;
            const fullQueryPath = "[" + projectName + "]/" + queryPath;
            history.push("/console/view/" + fullQueryPath);
        },
    });

    const createAndNavToQuery = (event: MouseEvent<HTMLButtonElement>) => {
        // Don't toggle the accordion.
        event.stopPropagation();
        createSqlQueryMutation();
    };

    return (
        <IconButton
            color="inherit"
            size={narrowMode ? "medium" : "small"}
            onClick={createAndNavToQuery}
            className={classes.createQueryButton}
        >
            <AddBoxOutlinedIcon
                color="action"
                fontSize={narrowMode ? "medium" : "small"}
            />
        </IconButton>
    );
}
