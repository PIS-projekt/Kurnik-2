import {fireEvent, render, screen} from "@testing-library/react";
import {ClickCounter} from "./ClickCounter";

describe("ClickCounter", () => {
  test("renders click counter", () => {
    render(<ClickCounter/>);
    const linkElement = screen.getByText(/you clicked 0 times/i);
    expect(linkElement).toBeInTheDocument();
  });

  test("clicking increments counter", () => {
    render(<ClickCounter/>);
    const button = screen.getByText(/click me/i);
    fireEvent.click(button);
    const linkElement = screen.getByText(/you clicked 1 times/i);
    expect(linkElement).toBeInTheDocument();
  });
});