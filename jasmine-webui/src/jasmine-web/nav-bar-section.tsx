import { makeStyles } from "@material-ui/core/styles";
import Accordion from "@material-ui/core/Accordion";
import AccordionSummary from "@material-ui/core/AccordionSummary";
import AccordionDetails from "@material-ui/core/AccordionDetails";
import IconButton from "@material-ui/core/IconButton";
import Typography from "@material-ui/core/Typography";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import { ReactNode } from "react";

const useStyles = makeStyles((theme) => ({
    sectionName: {
        marginLeft: theme.spacing(1),
        //marginTop: theme.spacing(0.5),
        [theme.breakpoints.down("xs")]: {
            fontSize: theme.typography.pxToRem(22),
        },
        [theme.breakpoints.only("sm")]: {
            fontSize: theme.typography.pxToRem(20),
        },
        [theme.breakpoints.up("md")]: {
            fontSize: theme.typography.pxToRem(20),
        },
        fontWeight: theme.typography.fontWeightRegular,
        alignItems: "center",
    },
    accordion: {
        "&.MuiPaper-root.MuiAccordion-root.Mui-expanded": {
            marginTop: 1,
            marginBottom: 1,
            minHeight: "40vh",
        },
    },
    accordionSummaryContent: {
        "&.MuiAccordionSummary-content.Mui-expanded": {
            marginTop: theme.spacing(0.5),
            marginBottom: theme.spacing(0.5),
        },
    },
    accordionDetails: {
        paddingTop: theme.spacing(0),
    },
    expandIcon: {
        paddingTop: theme.spacing(1),
        paddingBottom: theme.spacing(1),
    },
}));

export default function NavQuerySectionHeader({
    sectionIcon,
    sectionLabel,
    defaultExpanded,
    actionButtons,
    children,
}: {
    sectionIcon: any;
    sectionLabel: string;
    defaultExpanded: boolean;
    actionButtons?: ReactNode;
    children: ReactNode;
}) {
    const classes = useStyles();

    return (
        <Accordion
            defaultExpanded={defaultExpanded}
            className={classes.accordion}
        >
            <AccordionSummary
                expandIcon={<ExpandMoreIcon />}
                classes={{
                    content: classes.accordionSummaryContent,
                    expandIcon: classes.expandIcon,
                }}
            >
                <IconButton color="inherit" size="small">
                    {" "}
                    {sectionIcon}{" "}
                </IconButton>
                <Typography variant="h6" className={classes.sectionName}>
                    {sectionLabel}
                </Typography>
                {actionButtons || []}
            </AccordionSummary>
            <AccordionDetails className={classes.accordionDetails}>
                {children}
            </AccordionDetails>
        </Accordion>
    );
}
