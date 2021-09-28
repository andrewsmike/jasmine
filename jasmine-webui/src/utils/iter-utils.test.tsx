import { all, any } from "utils/iter-utils";

test("All() works correctly", () => {
    expect(all([])).toEqual(true);
    expect(all([false])).toEqual(false);
    expect(all([true])).toEqual(true);
    expect(all([true, true])).toEqual(true);
    expect(all([true, false])).toEqual(false);
    expect(all([true, false, true])).toEqual(false);
    expect(all([true, true, true])).toEqual(true);
});

test("Any() works correctly", () => {
    expect(any([])).toEqual(false);
    expect(any([false])).toEqual(false);
    expect(any([true])).toEqual(true);
    expect(any([true, false])).toEqual(true);
    expect(any([false, false])).toEqual(false);
    expect(any([false, true, false])).toEqual(true);
    expect(any([false, false, false])).toEqual(false);
});
