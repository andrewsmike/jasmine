import DnsOutlinedIcon from "@material-ui/icons/DnsOutlined";
import LibraryBooksOutlinedIcon from "@material-ui/icons/LibraryBooksOutlined";

import CreateQueryButton from "jasmine-web/create-query-button";
import QueryDirectoryTree from "jasmine-web/query-directory-tree";
import NavBarSection from "jasmine-web/nav-bar-section";

export default function NavBarSections() {
    return (
        <>
            <NavBarSection
                sectionLabel="Queries"
                defaultExpanded={true}
                sectionIcon={<LibraryBooksOutlinedIcon color="primary" />}
                actionButtons={<CreateQueryButton />}
            >
                <QueryDirectoryTree />
            </NavBarSection>
            <NavBarSection
                sectionLabel="Backends"
                defaultExpanded={false}
                sectionIcon={<DnsOutlinedIcon color="primary" />}
            >
                TBD
            </NavBarSection>
        </>
    );
}
