const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Mock chat response (matches real API contract for future wiring)
// const mockResponse = {
//   answer: "Amazon S3 (Simple Storage Service) is an object storage service that offers industry-leading scalability, data availability, security, and performance...",
//   sources: [
//     {
//       title: "Amazon S3 Documentation — Getting Started",
//       url: "https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html"
//     },
//     {
//       title: "Amazon S3 FAQs",
//       url: "https://aws.amazon.com/s3/faqs/"
//     }
//   ],
//   tokenUsage: {
//     inputTokens: 312,
//     outputTokens: 128
//   }
// };

// // Mock health response
// const mockHealth = {
//   status: "ok",
//   retriever: "local-faiss",
//   inference: "pending-bedrock-access"
// };

// Expected request body:
// { message, clientId, conversationId, topicFilter }

// Expected response:
// { answer, sources[], tokenUsage }
// See: chatClient.js → sendMessage()

export const sendMessage = async ({
  message,
  clientId,
  conversationId,
  topicFilter,
}) => {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": import.meta.env.VITE_API_KEY,
    },
    body: JSON.stringify({
      message,
      clientId,
      conversationId,
      topicFilter,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));

    throw {
      status: response.status,
      ...error,
    };
  }

  return response.json();
};

export const getConversations = async (clientId) => {
  const response = await fetch(`${API_BASE_URL}/conversations`, {
    method: "GET",
    headers: {
      "x-api-key": import.meta.env.VITE_API_KEY,
      "x-client-id": clientId,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));

    throw {
      status: response.status,
      ...error,
    };
  }

  return response.json();
};

export const getConversation = async (conversationId, clientId) => {
  const response = await fetch(
    `${API_BASE_URL}/conversations/${conversationId}`,
    {
      method: "GET",
      headers: {
        "x-api-key": import.meta.env.VITE_API_KEY,
        "x-client-id": clientId,
      },
    },
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));

    throw {
      status: response.status,
      ...error,
    };
  }

  return response.json();
};

export const checkHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Health check failed");
  }

  return response.json();
};
