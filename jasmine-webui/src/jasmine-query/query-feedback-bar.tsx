import { makeStyles } from "@material-ui/core/styles";
import useMediaQuery from "@material-ui/core/useMediaQuery";
import Accordion from "@material-ui/core/Accordion";
import AccordionSummary from "@material-ui/core/AccordionSummary";
import AccordionDetails from "@material-ui/core/AccordionDetails";
import Drawer from "@material-ui/core/Drawer";
import Typography from "@material-ui/core/Typography";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import WarningTwoToneIcon from "@material-ui/icons/WarningTwoTone";
import { useDispatch, useSelector } from "react-redux";

import { selectFeedbackCollapsed, toggleFeedback } from "jasmine-query/state";

const useStyles = makeStyles((theme) => ({
    drawer: {
        minWidth: "max(300px, 60vw)",
    },
    drawerPaper: {
        minWidth: "max(300px, 60vw)",
    },
    feedbackCardsDrawer: {
        marginTop: theme.spacing(1),
    },
    feedbackCardsInline: {
        marginTop: theme.spacing(3),
        minWidth: "max(280px, 30vw)",
    },
    feedbackDetails: {
        marginLeft: theme.spacing(1),
    },
    feedbackTitle: {
        marginLeft: theme.spacing(2),
        marginTop: theme.spacing(2),
    },
}));

export default function QueryFeedbackBar({
    queryId,
    queryText,
}: {
    queryId: number;
    queryText: string;
}) {
    const classes = useStyles();
    const dispatch = useDispatch();

    const narrowMode = useMediaQuery((theme: any) =>
        theme.breakpoints.down("md")
    );
    const feedbackCollapsed = useSelector(selectFeedbackCollapsed);

    const content = (
        <div
            className={
                narrowMode
                    ? classes.feedbackCardsDrawer
                    : classes.feedbackCardsInline
            }
        >
            <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <WarningTwoToneIcon color="secondary" />
                    <Typography className={classes.feedbackDetails}>
                        Column 'organization_id' needs an index.
                    </Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Typography className={classes.feedbackDetails}>
                        Column organization_id is used by X.
                    </Typography>
                </AccordionDetails>
            </Accordion>
            <Accordion>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <WarningTwoToneIcon color="secondary" />
                    <Typography className={classes.feedbackDetails}>
                        Key 'project_id, query_path' needs an index.
                    </Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Typography className={classes.feedbackDetails}>
                        Key is used by queries to look up rows.
                    </Typography>
                </AccordionDetails>
            </Accordion>
        </div>
    );

    return (
        <>
            <Drawer
                variant="temporary"
                anchor="right"
                open={narrowMode && !feedbackCollapsed}
                onClose={() => dispatch(toggleFeedback())}
                className={classes.drawer}
                classes={{ paper: classes.drawerPaper }}
            >
                <Typography variant="h5" className={classes.feedbackTitle}>
                    Query Warnings
                </Typography>
                {content}
            </Drawer>
            {!narrowMode && !feedbackCollapsed && content}
        </>
    );
}
