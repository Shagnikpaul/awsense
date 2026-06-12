import { useState, useCallback } from "react";
import { v4 as uuidv4 } from "uuid";
import { sendMessage as apiSendMessage } from "../api/chatClient";

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isRateLimited, setIsRateLimited] = useState(false);
  const [sessionId, setSessionId] = useState(() => uuidv4());
  const [topicFilter, setTopicFilter] = useState("All");

  const sendMessage = useCallback(
    async (text) => {
      if (!text.trim()) return;

      const userMessage = {
        id: uuidv4(),
        role: "user",
        content: text,
      };

      setMessages((prev) => {
        const newMessages = [...prev, userMessage];
        // Keep only last 5 turns (10 messages: 5 user, 5 assistant)
        if (newMessages.length > 10) {
          return newMessages.slice(newMessages.length - 10);
        }
        return newMessages;
      });

      setIsLoading(true);
      setIsRateLimited(false);

      try {
        // TODO [BACKEND INTEGRATION]: Replace this mock response with a real call to POST /chat
        // Expected request body: { message, sessionId, topicFilter }
        // Expected response: { answer, sources[], tokenUsage }
        const response = await apiSendMessage({
          message: text,
          sessionId,
          topicFilter: topicFilter === "All" ? undefined : topicFilter,
        });

        const assistantMessage = {
          id: uuidv4(),
          role: "assistant",
          content: response.answer,
          sources: response.sources,
          tokenUsage: response.token_usage || response.tokenUsage,
        };

        setMessages((prev) => {
          const newMessages = [...prev, assistantMessage];
          if (newMessages.length > 10) {
            return newMessages.slice(newMessages.length - 10);
          }
          return newMessages;
        });
      } catch (error) {
        if (error?.status === 429 || error?.code === "RATE_LIMIT") {
          setIsRateLimited(true);
        } else {
          console.error("Failed to send message:", error);
        }
      } finally {
        setIsLoading(false);
      }
    },
    [sessionId, topicFilter],
  );

  const clearConversation = useCallback(() => {
    setMessages([]);
    setSessionId(uuidv4());
    setIsRateLimited(false);
  }, []);

  return {
    messages,
    isLoading,
    isRateLimited,
    setIsRateLimited,
    sessionId,
    topicFilter,
    setTopicFilter,
    sendMessage,
    clearConversation,
  };
}
