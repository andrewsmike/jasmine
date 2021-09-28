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
