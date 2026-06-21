import { describe, it, expect, vi, beforeEach } from "vitest";
import { sendMessage, checkHealth } from "../api/chatClient";

global.fetch = vi.fn();

describe("chatClient", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("sendMessage returns API response", async () => {
    const mockResponse = {
      answer: "Amazon S3 is object storage",
      sources: [],
      tokenUsage: {
        inputTokens: 10,
        outputTokens: 20,
      },
    };

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockResponse,
    });

    const result = await sendMessage({
      message: "What is S3?",
      sessionId: "abc123",
      topicFilter: "S3",
    });

    expect(result).toEqual(mockResponse);

    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("sendMessage throws when API fails", async () => {
    fetch.mockResolvedValue({
      ok: false,
    });

    await expect(
      sendMessage({
        message: "test",
        sessionId: "abc123",
        topicFilter: "All",
      }),
    ).rejects.toThrow("Failed to fetch response");
  });

  it("checkHealth returns health response", async () => {
    const mockHealth = {
      status: "healthy",
      service: "AWSense",
    };

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockHealth,
    });

    const result = await checkHealth();

    expect(result).toEqual(mockHealth);
  });

  it("checkHealth throws on failure", async () => {
    fetch.mockResolvedValue({
      ok: false,
    });

    await expect(checkHealth()).rejects.toThrow("Health check failed");
  });
});
