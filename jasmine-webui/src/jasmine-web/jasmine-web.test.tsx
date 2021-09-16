import React from "react";
import { render, screen } from "@testing-library/react";
import JasmineWeb from "jasmine-web/jasmine-web";

test("Renders title", () => {
    render(<JasmineWeb />);

    const headerElement = screen.getByText(/Jasmine ETL/i);
    expect(headerElement).toBeInTheDocument();
});

test("Renders account box", () => {
    render(<JasmineWeb />);

    const headerElement = screen.getByText(/My Company/i);
    expect(headerElement).toBeInTheDocument();
});
