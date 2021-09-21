import DnsOutlinedIcon from "@material-ui/icons/DnsOutlined";
import LibraryBooksOutlinedIcon from "@material-ui/icons/LibraryBooksOutlined";

import CreateQueryButton from "jasmine-web/create-query-button";
import ViewDirectoryTree from "jasmine-web/view-directory-tree";
import NavBarSection from "jasmine-web/nav-bar-section";

export default function NavBarSections() {
    return (
        <>
            <NavBarSection
                sectionLabel="Views"
                defaultExpanded={true}
                sectionIcon={<LibraryBooksOutlinedIcon color="primary" />}
                actionButtons={<CreateQueryButton />}
            >
                <ViewDirectoryTree />
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
