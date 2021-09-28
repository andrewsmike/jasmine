export function any(values: Iterable<boolean>): boolean {
    for (let elem of values) {
        if (elem) return true;
    }
    return false;
}

export function all(values: Iterable<boolean>): boolean {
    for (let elem of values) {
        if (!elem) return false;
    }
    return true;
}
