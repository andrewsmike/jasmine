import {
    arrayFromMap,
    groupedItems,
    mapApply,
    mapFromArray,
    unflattenedMap,
    withoutKeyPrefix,
} from "utils/map-utils";

test("mapFromList works correctly", () => {
    const testMap = new Map([
        ["hello", 2],
        ["world", 4],
    ]);

    expect(arrayFromMap(testMap, (key, value) => key)).toEqual([
        "hello",
        "world",
    ]);

    expect(arrayFromMap(testMap, (key, value) => [key, value])).toEqual([
        ["hello", 2],
        ["world", 4],
    ]);

    expect(arrayFromMap([], (key, value) => value)).toEqual([]);
});

test("mapFromArray works correctly", () => {
    const testList = ["hello", "world", "foo"];

    expect(mapFromArray(testList, (value) => [value[0], value])).toEqual(
        new Map([
            ["h", "hello"],
            ["w", "world"],
            ["f", "foo"],
        ])
    );

    expect(mapFromArray([], (value) => [value[0], value])).toEqual(new Map());
});

test("mapApply works correctly", () => {
    const testMap = new Map([
        ["hello", 2],
        ["world", 4],
    ]);

    expect(mapApply(testMap, (key, value) => [key, value * 2])).toEqual(
        new Map([
            ["hello", 4],
            ["world", 8],
        ])
    );

    expect(mapApply(testMap, (key, value) => [key + key, 1])).toEqual(
        new Map([
            ["hellohello", 1],
            ["worldworld", 1],
        ])
    );

    expect(mapApply(new Map(), (key, value) => [key + key, 1])).toEqual(
        new Map()
    );
});

test("groupedItems works correctly", () => {
    const emptyTestMap = new Map();
    const testMap = new Map([
        ["hi", 3],
        ["hello", 2],
        ["world", 4],
    ]);

    expect(groupedItems(emptyTestMap, (key) => key[0])).toEqual(new Map());

    expect(groupedItems(testMap, (key) => key[0])).toEqual(
        new Map([
            [
                "h",
                new Map([
                    ["hi", 3],
                    ["hello", 2],
                ]),
            ],
            ["w", new Map([["world", 4]])],
        ])
    );
});

test("withoutKeyPrefix works correctly", () => {
    const emptyTestMap = new Map();
    const testMap = new Map([
        ["hi", 3],
        ["hello/world", 2],
        ["foo/bar/baz", 8],
    ]);

    expect(withoutKeyPrefix(emptyTestMap)).toEqual(new Map());

    expect(withoutKeyPrefix(testMap)).toEqual(
        new Map([
            ["", 3],
            ["world", 2],
            ["bar/baz", 8],
        ])
    );
});

test("unflattenedMap works correctly", () => {
    const emptyTestMap = new Map();
    const testMap = new Map([
        ["hi", 3],
        ["hello/world", 2],
        ["hello/blah", 4],
        ["foo/bar/baz", 8],
    ]);

    expect(withoutKeyPrefix(emptyTestMap)).toEqual(new Map());

    expect(unflattenedMap(testMap)).toEqual(
        new Map([
            ["hi", 3],
            [
                "hello",
                new Map([
                    ["world", 2],
                    ["blah", 4],
                ]),
            ],
            ["foo", new Map([["bar", new Map([["baz", 8]])]])],
        ])
    );
});
