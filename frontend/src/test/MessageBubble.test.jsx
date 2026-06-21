import React from "react";
import { render, screen } from "@testing-library/react";
import { MessageBubble } from "../components/MessageBubble";
import { vi } from "vitest";

vi.mock("../components/SourceCitations", () => ({
  SourceCitations: ({ sources }) => (
    <div data-testid="sources">Sources: {sources?.length || 0}</div>
  ),
}));

vi.mock("../components/TokenUsage", () => ({
  TokenUsage: ({ tokenUsage }) => (
    <div data-testid="tokens">Tokens: {tokenUsage?.outputTokens}</div>
  ),
}));

describe("MessageBubble", () => {
  it("renders user message", () => {
    render(<MessageBubble role="user" content="What is Amazon S3?" />);

    expect(screen.getByText("What is Amazon S3?")).toBeInTheDocument();

    expect(screen.queryByTestId("sources")).not.toBeInTheDocument();

    expect(screen.queryByTestId("tokens")).not.toBeInTheDocument();
  });

  it("renders assistant message with sources and token usage", () => {
    render(
      <MessageBubble
        role="assistant"
        content="Amazon S3 is object storage."
        sources={["https://docs.aws.amazon.com/s3"]}
        tokenUsage={{
          inputTokens: 10,
          outputTokens: 20,
        }}
      />,
    );

    expect(
      screen.getByText("Amazon S3 is object storage."),
    ).toBeInTheDocument();

    expect(screen.getByTestId("sources")).toBeInTheDocument();

    expect(screen.getByTestId("tokens")).toBeInTheDocument();
  });
});
