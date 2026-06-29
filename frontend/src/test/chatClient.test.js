import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  sendMessage,
  checkHealth,
  getConversation,
  getConversations,
} from "../api/chatClient";

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
      clientId: "client-123",
      conversationId: "conv-123",
      topicFilter: "S3",
    });

    expect(result).toEqual(mockResponse);

    expect(fetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({
          message: "What is S3?",
          clientId: "client-123",
          conversationId: "conv-123",
          topicFilter: "S3",
        }),
      }),
    );
  });

  it("sendMessage throws when API fails", async () => {
    fetch.mockResolvedValue({
      ok: false,
      status: 500,
      json: async () => ({
        error: "Failed to fetch response",
      }),
    });

    await expect(
      sendMessage({
        message: "test",
        clientId: "client-123",
        conversationId: "conv-123",
        topicFilter: "All",
      }),
    ).rejects.toMatchObject({
      status: 500,
      error: "Failed to fetch response",
    });
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

  it("getConversations returns conversations", async () => {
    const mockData = [
      {
        conversationId: "conv-1",
        title: "What is S3?",
      },
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockData,
    });

    const result = await getConversations("client-123");

    expect(result).toEqual(mockData);

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/conversations"),
      expect.objectContaining({
        method: "GET",
        headers: expect.objectContaining({
          "x-client-id": "client-123",
        }),
      }),
    );
  });

  it("getConversation returns messages", async () => {
    const mockMessages = [
      {
        role: "user",
        content: "What is S3?",
      },
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockMessages,
    });

    const result = await getConversation("conv-123", "client-123");

    expect(result).toEqual(mockMessages);

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/conversations/conv-123"),
      expect.objectContaining({
        method: "GET",
        headers: expect.objectContaining({
          "x-client-id": "client-123",
        }),
      }),
    );
  });
});
