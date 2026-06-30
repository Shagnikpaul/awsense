After running the following k6 script which
ramps up from 0 to 10 users in 30 seconds, maintains 10 active users for 2 minutes and then finally ramps down to 0 active users in 30 seconds ran and 


SCRIPT : 

```
import http from "k6/http";
import { check } from "k6";
import { Counter } from "k6/metrics";

const requestCounter = new Counter("chat_requests");
export const options = {
  stages: [
    { duration: "30s", target: 10 },
    { duration: "2m", target: 10 },
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
```


almost 62/80 api calls failed 





- all 62 of them failed due to Groq API 429 Rate limit (verified from observing the cloud watch logs)


```
{
   "eventType":"ERROR",
   "errorType":"RateLimitError",
   "errorMessage":"Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.1-8b-instant` in organization `org_01ktm6jm13f4na19njaz7vk1m9` service tier `on_demand` on tokens per minute (TPM): Limit 6000, Used 4684, Requested 1321. Please try again in 50ms. Need more tokens? Upgrade to Dev Tier today at https://console.groq.com/settings/billing', 'type': 'tokens', 'code': 'rate_limit_exceeded'}}",
   "sessionId":"k6-load-test-session",
   "topicFilter":"Amazon S3"
}
```

- so the local vector_store (faiss), then hugging face inference API adn the overall aws infrastructure are working fine but groq API is the bottle neck in this case.