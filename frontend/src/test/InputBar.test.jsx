import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import { InputBar } from "../components/InputBar";
import React from "react";

// Mock TopicFilter
vi.mock("../components/TopicFilter", () => ({
  TopicFilter: () => <div>TopicFilter</div>,
}));

describe("InputBar", () => {
  it("renders input and send button", () => {
    render(
      <InputBar
        onSendMessage={vi.fn()}
        isLoading={false}
        topicFilter="All"
        setTopicFilter={vi.fn()}
      />,
    );

    expect(
      screen.getByPlaceholderText(/ask anything about aws/i),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", {
        name: /send/i,
      }),
    ).toBeInTheDocument();
  });

  it("calls onSendMessage when send clicked", async () => {
    const user = userEvent.setup();

    const onSendMessage = vi.fn();

    render(
      <InputBar
        onSendMessage={onSendMessage}
        isLoading={false}
        topicFilter="All"
        setTopicFilter={vi.fn()}
      />,
    );

    const textarea = screen.getByRole("textbox");

    await user.type(textarea, "What is S3?");

    await user.click(
      screen.getByRole("button", {
        name: /send/i,
      }),
    );

    expect(onSendMessage).toHaveBeenCalledWith("What is S3?");
  });

  it("does not send empty messages", async () => {
    const user = userEvent.setup();

    const onSendMessage = vi.fn();

    render(
      <InputBar
        onSendMessage={onSendMessage}
        isLoading={false}
        topicFilter="All"
        setTopicFilter={vi.fn()}
      />,
    );

    const button = screen.getByRole("button", {
      name: /send/i,
    });

    expect(button).toBeDisabled();

    await user.click(button);

    expect(onSendMessage).not.toHaveBeenCalled();
  });
});
