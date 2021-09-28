import { fullPath, fullPathValid, fullPathParts } from "utils/path-utils";

test("fullPath works correctly", () => {
    expect(fullPath("dev", "my/lovely/view/tree")).toEqual(
        "[dev]/my/lovely/view/tree"
    );
});

test("fullPathParts works correctly", () => {
    expect(fullPathParts("[dev]/my/lovely/view/tree")).toEqual([
        "dev",
        "my/lovely/view/tree",
    ]);
});

test("fullPathValid works correctly", () => {
    expect(
        fullPathValid("[dev_htuenao_u HTUp32343]/my_project/is_great")
    ).toEqual(true);
    expect(fullPathValid("[dev]/my/lovely_view")).toEqual(true);
    expect(fullPathValid("[dev/my/lovely_view")).toEqual(false);
    expect(fullPathValid("dev/my/lovely_view")).toEqual(false);
    expect(fullPathValid("[dev/blah]/my/lovely_view")).toEqual(false);
});
