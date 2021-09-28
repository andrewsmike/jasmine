import { all } from "utils/iter-utils";

export function mapFromSet<ValueType, ResultType>(
    values: Set<ValueType>,
    mapperFunc: (value: ValueType) => ResultType
): ResultType[] {
    return Array.from(values).map(mapperFunc);
}

export function isSubset<ValueType>(
    left: Set<ValueType>,
    right: Set<ValueType>
): boolean {
    return all(mapFromSet(left, (leftValue) => right.has(leftValue)));
}

export function setUnion<ValueType>(
    left: Set<ValueType>,
    right: Set<ValueType>
): Set<ValueType> {
    let result = new Set(left);
    for (let elem of right) {
        result.add(elem);
    }
    return result;
}

export function setIntersection<ValueType>(
    left: Set<ValueType>,
    right: Set<ValueType>
): Set<ValueType> {
    let result = new Set<ValueType>();
    for (let elem of right) {
        if (left.has(elem)) {
            result.add(elem);
        }
    }
    return result;
}

export function setDifference<ValueType>(
    left: Set<ValueType>,
    right: Set<ValueType>
) {
    let result = new Set(left);
    for (let elem of right) {
        result.delete(elem);
    }
    return result;
}
