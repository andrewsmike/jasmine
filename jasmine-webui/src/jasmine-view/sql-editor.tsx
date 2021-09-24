import CodeEditor from "@uiw/react-textarea-code-editor";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
    editor: {
        flex: "auto",
        fontSize: 14,
        backgroundColor: "#f5f5f5",
        fontFamily:
            "ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace",
        minWidth: "470px",
    },
    scrollDiv: {
        overflowX: "auto",
        overflowY: "auto",
    },
}));

export default function SqlEditor({
    code,
    setCode,
}: {
    code: string;
    setCode: any;
}) {
    const classes = useStyles();

    return (
        <div className={classes.scrollDiv}>
            <CodeEditor
                value={code}
                language="sql"
                placeholder="Enter your SQL query here."
                onChange={(evn) => setCode(evn.target.value)}
                className={classes.editor}
                padding={15}
            />
        </div>
    );
}
