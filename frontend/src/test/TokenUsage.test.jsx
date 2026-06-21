import React from "react";
import { render, screen } from "@testing-library/react";
import { TokenUsage } from "../components/TokenUsage";
import { vi } from "vitest";

vi.mock("../components/ui/tooltip", () => ({
  Tooltip: ({ children }) => <div>{children}</div>,
  TooltipTrigger: ({ children }) => <div>{children}</div>,
  TooltipContent: ({ children }) => <div>{children}</div>,
}));

describe("TokenUsage", () => {
  it("renders nothing when tokenUsage is missing", () => {
    const { container } = render(<TokenUsage tokenUsage={null} />);

    expect(container.firstChild).toBeNull();
  });

  it("renders input and output token counts", () => {
    render(
      <TokenUsage
        tokenUsage={{
          inputTokens: 123,
          outputTokens: 456,
        }}
      />,
    );

    expect(screen.getByText("123")).toBeInTheDocument();
    expect(screen.getByText("456")).toBeInTheDocument();
  });
});
