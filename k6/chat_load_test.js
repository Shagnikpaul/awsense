import http from "k6/http";
import { check } from "k6";
import { Counter } from "k6/metrics";

const requestCounter = new Counter("chat_requests");
export const options = {
  stages: [
    // failed
    // { duration: "30s", target: 10 },
    // { duration: "2m", target: 10 },
    // { duration: "30s", target: 0 },

    { duration: "30s", target: 3 },
    { duration: "2m", target: 3 },
    { duration: "30s", target: 0 },
  ],

  thresholds: {
    http_req_duration: [
      "p(50)<6000",
      "p(95)<12000",
    ],
    http_req_failed: ["rate<0.05"],
  },
};

const BASE_URL = __ENV.API_BASE_URL;
const API_KEY = __ENV.API_KEY;

export default function () {
  const payload = JSON.stringify({
    sessionId: "k6-load-test-session",
    message: "What is Amazon S3 and when should I use it?",
    topicFilter: "Amazon S3",
  });

  const params = {
    headers: {
      "Content-Type": "application/json",
      "x-api-key": API_KEY,
    },
  };

  const response = http.post(
    `${BASE_URL}/chat`,
    payload,
    params
  );
  requestCounter.add(1);
  check(response, {
    "status is 200": (r) => r.status === 200,
  });
}