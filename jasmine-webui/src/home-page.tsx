import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
    content: {
        padding: theme.spacing(2),
    },
}));

export default function HomePage() {
    const classes = useStyles();

    return <div className={classes.content}> Hello, world! </div>;
}
