import React from "react";
import { render, screen } from "@testing-library/react";
import { TopicFilter } from "@/components/TopicFilter";

describe("TopicFilter", () => {
  it("renders selected topic", () => {
    render(<TopicFilter topicFilter="All" setTopicFilter={() => {}} />);

    expect(screen.getByText("All")).toBeInTheDocument();
  });
});
