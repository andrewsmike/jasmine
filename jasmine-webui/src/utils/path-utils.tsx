import _ from "lodash";

export function fullPathParts(fullPath: string): [string, string] {
    const fullPathRegex = /^\[([^/\]]+)\]\/(.+)$/;
    const [, projectName, viewPath] = fullPath.match(
        fullPathRegex
    ) as RegExpMatchArray;
    return [projectName, viewPath];
}

export function fullPathValid(fullPath: string): boolean {
    const fullPathRegex = /^\[([^/\]]+)\]\/(.+)$/;
    return fullPath.match(fullPathRegex) !== null;
}

export function fullPath(projectName: string, viewPath: string): string {
    return `[${projectName}]/${viewPath}`;
}

export function pathDirectories(path: string): Set<string> {
    const parts = path.split("/");

    const path_prefixes = _.range(parts.length).map((end_inclusive_index) =>
        _.join(parts.slice(0, end_inclusive_index + 1), "/")
    );
    /* We're not interested in the full path, only the directories. */
    const path_proper_prefixes = path_prefixes.slice(0, -1);

    return new Set(path_proper_prefixes);
}
