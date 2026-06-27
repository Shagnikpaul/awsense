import { useState, useEffect, useCallback } from "react";
import { v4 as uuidv4 } from "uuid";
import { sendMessage as apiSendMessage } from "../api/chatClient";

// ---------------------------------------------------------------------------
// Persistent, tamper-resistant client ID helpers
// The UUID is stored in localStorage together with an HMAC-SHA256 signature.
// If someone manually edits either value the signature check will fail and a
// fresh UUID is generated transparently.
// ---------------------------------------------------------------------------
const LS_ID_KEY = "_awsense_client_id";
const LS_SIG_KEY = "_awsense_client_sig";

// A static per-build secret mixed with the origin so the key is not easily
// portable across different deployments.
const HMAC_SECRET = `awsense-v1::${window.location.origin}`;

async function signId(id) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(HMAC_SECRET),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );

  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(id));

  return Array.from(new Uint8Array(sig))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

async function verifyId(id, storedSig) {
  try {
    const expected = await signId(id);
    return expected === storedSig;
  } catch {
    return false;
  }
}

/** Load (or create) a tamper-proof client UUID from localStorage. */
async function loadOrCreateClientId() {
  const storedId = localStorage.getItem(LS_ID_KEY);
  const storedSig = localStorage.getItem(LS_SIG_KEY);

  if (storedId && storedSig && (await verifyId(storedId, storedSig))) {
    return storedId;
  }

  // Missing, corrupted, or tampered — mint a fresh one.
  return persistNewClientId();
}

/** Create a new UUID, sign it, and write both values to localStorage. */
async function persistNewClientId() {
  const id = uuidv4();
  const sig = await signId(id);

  localStorage.setItem(LS_ID_KEY, id);
  localStorage.setItem(LS_SIG_KEY, sig);

  return id;
}

export function useChat() {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isRateLimited, setIsRateLimited] = useState(false);

  // Start with a temporary placeholder; replaced once the async load resolves.
  const [clientId, setClientId] = useState("");
  const [conversationId, setConversationId] = useState(null);
  const [topicFilter, setTopicFilter] = useState("All");

  // Load (or create) the persistent, verified client ID once on mount.
  useEffect(() => {
    loadOrCreateClientId().then(setClientId);
  }, []);

  const sendMessage = useCallback(
    async (text) => {
      if (!text.trim()) return;
      // if a new chat was created and first message was sent then create a conversation Id for that particular chat
      let activeConversationId = conversationId;

      if (!activeConversationId) {
        activeConversationId = uuidv4();
        setConversationId(activeConversationId);
      }
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
        // Expected request body: { message, clientId, topicFilter }
        // Expected response: { answer, sources[], tokenUsage }
        const response = await apiSendMessage({
          message: text,
          clientId,
          conversationId: activeConversationId,
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
    [clientId, conversationId, topicFilter],
  );

  const newChat = useCallback(() => {
    setMessages([]);
    setIsRateLimited(false);

    // No active conversation until the first message is sent.
    setConversationId(null);

    // Client ID is intentionally kept — it only resets when localStorage is cleared.
  }, []);

  return {
    messages,
    isLoading,
    isRateLimited,
    setIsRateLimited,
    clientId,
    conversationId,
    setConversationId,
    topicFilter,
    setTopicFilter,
    sendMessage,
    newChat,
  };
}