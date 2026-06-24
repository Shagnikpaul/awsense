After reducing the VUs to 3 the token usage per minute limit of 6k for groq was still being reached (while remaining
under the limit of 30 requests per minute)

so because of that almost 77% of the chat_requests were denied with 429 response due to exceeding token usage of 6k per minute

so for now alternative to test will be using constant-arrival-rate