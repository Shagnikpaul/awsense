import http from "k6/http";
import { check, sleep } from "k6";
import { Counter } from "k6/metrics";

const requestCounter = new Counter("chat_requests");

export const options = {
  thresholds: {
    http_req_duration: [
      "p(50)<6000",
      "p(95)<12000",
    ],
    http_req_failed: ["rate<0.05"],
  },

  scenarios: {
    persistent_chat_flow: {
      executor: "constant-arrival-rate",
      rate: 5,
      timeUnit: "1m",
      duration: "3m",
      preAllocatedVUs: 3,
      maxVUs: 3,
    },
  },
};

const BASE_URL = __ENV.API_BASE_URL;
const API_KEY = __ENV.API_KEY;

const headers = {
  "Content-Type": "application/json",
  "x-api-key": API_KEY,
};

export default function () {
  const clientId = `k6-client-${__VU}`;
  const conversationId = `k6-conversation-${__VU}`;

  const questions = [
    "What is Amazon S3?",
    "How is Amazon S3 different from Amazon EBS?",
    "When should I use Amazon S3 Standard?",
  ];

  // -------------------------
  // Send multiple chat messages
  // -------------------------
  for (const question of questions) {
    const payload = JSON.stringify({
      clientId,
      conversationId,
      message: question,
      topicFilter: "Amazon S3",
    });

    const response = http.post(
      `${BASE_URL}/chat`,
      payload,
      { headers },
    );

    requestCounter.add(1);

    check(response, {
      "chat status is 200": (r) => r.status === 200,
      "chat has answer": (r) => {
        const body = r.json();
        return body.answer !== undefined;
      },
      "chat has sources": (r) => {
        const body = r.json();
        return Array.isArray(body.sources);
      },
    });

    if (response.status !== 200) {
      console.log(`POST /chat failed (${response.status})`);
      console.log(response.body);
    }

    sleep(1);
  }

  // -------------------------
  // Get conversation list
  // -------------------------
  const conversations = http.get(
    `${BASE_URL}/conversations`,
    {
      headers: {
        "x-api-key": API_KEY,
        "x-client-id": clientId,
      },
    },
  );

  requestCounter.add(1);

  check(conversations, {
    "conversation list status is 200": (r) => r.status === 200,
    "conversation list is array": (r) => Array.isArray(r.json()),
  });

  if (conversations.status !== 200) {
    console.log(`GET /conversations failed (${conversations.status})`);
    console.log(conversations.body);
  }

  // -------------------------
  // Get conversation history
  // -------------------------
  const history = http.get(
    `${BASE_URL}/conversations/${conversationId}`,
    {
      headers: {
        "x-api-key": API_KEY,
        "x-client-id": clientId,
      },
    },
  );

  requestCounter.add(1);

  check(history, {
    "conversation history status is 200": (r) => r.status === 200,
    "conversation history is array": (r) => Array.isArray(r.json()),
  });

  if (history.status !== 200) {
    console.log(`GET /conversations/{id} failed (${history.status})`);
    console.log(history.body);
  }
}