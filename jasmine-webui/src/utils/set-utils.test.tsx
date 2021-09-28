import {
    isSubset,
    mapFromSet,
    setUnion,
    setIntersection,
    setDifference,
} from "utils/set-utils";

test("mapFromSet() works correctly", () => {
    const zeroOne = new Set([0, 1]);
    expect(mapFromSet(zeroOne, (value) => value + 10)).toEqual([10, 11]);
});

test("isSubset() works correctly", () => {
    const empty = new Set([]);
    const zero = new Set([0]);
    const one = new Set([1]);
    const zeroOne = new Set([0, 1]);

    expect(isSubset(empty, zero)).toEqual(true);
    expect(isSubset(zero, empty)).toEqual(false);
    expect(isSubset(empty, empty)).toEqual(true);
    expect(isSubset(zero, zero)).toEqual(true);
    expect(isSubset(one, zero)).toEqual(false);
    expect(isSubset(one, zeroOne)).toEqual(true);
});

test("setUnion() works correctly", () => {
    const empty = new Set([]);
    const zero = new Set([0]);
    const one = new Set([1]);
    const zeroOne = new Set([0, 1]);

    expect(setUnion(empty, zero)).toEqual(zero);
    expect(setUnion(zero, empty)).toEqual(zero);
    expect(setUnion(empty, empty)).toEqual(empty);
    expect(setUnion(zero, zero)).toEqual(zero);
    expect(setUnion(one, zero)).toEqual(zeroOne);
    expect(setUnion(one, zeroOne)).toEqual(zeroOne);
});

test("setIntersection() works correctly", () => {
    const empty = new Set([]);
    const zero = new Set([0]);
    const one = new Set([1]);
    const zeroOne = new Set([0, 1]);

    expect(setIntersection(empty, zero)).toEqual(empty);
    expect(setIntersection(zero, empty)).toEqual(empty);
    expect(setIntersection(empty, empty)).toEqual(empty);
    expect(setIntersection(zero, zero)).toEqual(zero);
    expect(setIntersection(one, zero)).toEqual(empty);
    expect(setIntersection(one, zeroOne)).toEqual(one);
});

test("setDifference() works correctly", () => {
    const empty = new Set([]);
    const zero = new Set([0]);
    const one = new Set([1]);
    const zeroOne = new Set([0, 1]);

    expect(setDifference(empty, zero)).toEqual(empty);
    expect(setDifference(zero, empty)).toEqual(zero);
    expect(setDifference(empty, empty)).toEqual(empty);
    expect(setDifference(zero, zero)).toEqual(empty);
    expect(setDifference(one, zero)).toEqual(one);
    expect(setDifference(zeroOne, one)).toEqual(zero);
});
