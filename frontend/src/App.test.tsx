import React from "react";
import {render, screen} from "@testing-library/react";
import App from "./App";

describe("App", () => {
  test("renders learn react link", () => {
    render(<App/>);
    const linkElement = screen.getByText(/projekt pis 2024z/i);
    expect(linkElement).toBeInTheDocument();
  });

  test("math problem", () => {
    expect(1 + 1).toBe(2);
  });
});