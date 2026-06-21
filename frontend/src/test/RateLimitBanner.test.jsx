import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { RateLimitBanner } from "@/components/RateLimitBanner";

describe("RateLimitBanner", () => {
  it("renders nothing when not rate limited", () => {
    const { container } = render(
      <RateLimitBanner isRateLimited={false} setIsRateLimited={() => {}} />,
    );

    expect(container.firstChild).toBeNull();
  });

  it("renders banner message when rate limited", () => {
    render(
      <RateLimitBanner isRateLimited={true} setIsRateLimited={() => {}} />,
    );

    expect(
      screen.getByText(/You've reached the request limit/i),
    ).toBeInTheDocument();
  });

  it("dismisses banner when close button clicked", () => {
    const setIsRateLimited = vi.fn();

    render(
      <RateLimitBanner
        isRateLimited={true}
        setIsRateLimited={setIsRateLimited}
      />,
    );

    fireEvent.click(
      screen.getByRole("button", {
        name: /dismiss/i,
      }),
    );

    expect(setIsRateLimited).toHaveBeenCalledWith(false);
  });
});
