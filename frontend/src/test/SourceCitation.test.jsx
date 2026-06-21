import React from "react";
import { render, screen } from "@testing-library/react";
import { SourceCitations } from "@/components/SourceCitations";

describe("SourceCitations", () => {
  it("renders nothing when sources are empty", () => {
    const { container } = render(<SourceCitations sources={[]} />);

    expect(container.firstChild).toBeNull();
  });

  it("renders all source links", () => {
    const sources = [
      "https://docs.aws.amazon.com/s3",
      "https://docs.aws.amazon.com/lambda",
    ];

    render(<SourceCitations sources={sources} />);

    expect(screen.getByText("Sources")).toBeInTheDocument();

    expect(
      screen.getByText("https://docs.aws.amazon.com/s3"),
    ).toBeInTheDocument();

    expect(
      screen.getByText("https://docs.aws.amazon.com/lambda"),
    ).toBeInTheDocument();

    const links = screen.getAllByRole("link");

    expect(links).toHaveLength(2);
    expect(links[0]).toHaveAttribute("href", "https://docs.aws.amazon.com/s3");
    expect(links[1]).toHaveAttribute(
      "href",
      "https://docs.aws.amazon.com/lambda",
    );
  });
});
