# AWSense

A full-stack RAG chatbot that answers questions about AWS services and architecture, grounded in official AWS documentation.

**[Live Demo →](https://d3nw1hzdw4124c.cloudfront.net/)**

![Status](https://img.shields.io/badge/status-in%20progress-orange) ![Stack](https://img.shields.io/badge/stack-React%20%7C%20Python%20%7C%20AWS-232F3E?logo=amazonaws) ![License](https://img.shields.io/badge/license-MIT-green)

---

## Overview

AWSense takes a natural language question about AWS, retrieves the most relevant chunks from a local knowledge base built from official AWS documentation, and generates a cited answer using an LLM. Built as a 1-month solo internship project alongside AWS Solutions Architect Associate (SAA-C03) study.

**Ask it things like:**
- *"How does S3 versioning work?"*
- *"What's the difference between a Security Group and a NACL?"*
- *"How do I configure a Lambda function with a VPC?"*

---

## Architecture

```
User Browser
    │
    ▼
React Frontend  ──── S3 + CloudFront
    │
    ▼
API Gateway (HTTP API)
    │
    ▼
Lambda (Python 3.12)
    ├── Hugging Face Inference API   →  query embedding (all-MiniLM-L6-v2)
    ├── FAISS vector index           →  retrieval over 30+ AWS doc pages
    └── Groq API (llama-3.1-8b)     →  answer generation
```

The retrieval layer (`retriever.py`) is fully decoupled from the Lambda entry point. Swapping to Amazon Bedrock when quota is available requires changing one file.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, shadcn/ui |
| Hosting | AWS S3 + CloudFront |
| API | AWS API Gateway + Lambda (Python 3.12) |
| LLM Inference | Groq API — `llama-3.1-8b-instant` |
| Query Embedding | Hugging Face Inference API — `all-MiniLM-L6-v2` |
| Vector Store | FAISS (`faiss-cpu`) — index built offline, bundled in Lambda |
| IaC | AWS CDK (Python) |
| CI/CD | GitHub Actions |
| Monitoring | Amazon CloudWatch |
| Secrets | AWS SSM Parameter Store |

---

## Features

- **Semantic retrieval** over 30+ AWS documentation pages covering EC2, S3, VPC, IAM, Lambda, RDS, CloudFront, Route 53, ELB, and CloudWatch
- **Source citations** — every answer links back to the AWS doc pages it was grounded in
- **Topic filter** — narrow retrieval to a specific AWS service category
- **Session history** — last 5 turns kept in context per session
- **Token usage** shown per response
- **Rate limiting** — 20 requests per session per hour; banner shown on threshold hit

---

## Project Structure

```
awsense/
├── frontend/               # React + Vite application
│   └── src/
│       ├── components/     # ChatWindow, MessageBubble, InputBar, Sidebar, etc.
│       ├── api/            # chatClient.js — sole backend integration layer
│       └── hooks/          # useChat.js — session state management
├── backend/
│   ├── src/
│   │   ├── handler.py          # Lambda entry point
│   │   ├── retriever.py        # FAISS lookup + HF embedding API
│   │   ├── prompt_builder.py
│   │   ├── validator.py
│   │   └── response_formatter.py
│   └── tests/
│       ├── unit/
│       └── integration/
├── infra/                  # AWS CDK stacks
├── scripts/
│   ├── build_vector_store.py   # builds FAISS index from .txt docs
│   └── ingest_docs.py          # downloads AWS docs → S3
├── k6/                     # performance test scripts
└── reports/                # coverage + SLA reports
```

---

## Local Setup

### Prerequisites
- Node.js 18+
- Python 3.12+
- AWS CLI configured
- AWS CDK CLI: `npm install -g aws-cdk`

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Build the FAISS index (run once after cloning):

```bash
cd scripts
python build_vector_store.py
# Outputs: vector_store/awsense.index + vector_store/documents.pkl
```

Run tests:

```bash
pytest --cov=src --cov-report=html
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# http://localhost:5173
```

### Infrastructure

```bash
cd infra
pip install -r requirements.txt
cdk synth
cdk deploy
```

---

## Environment Variables

No secrets are committed to this repo. All keys are stored in AWS SSM Parameter Store or Lambda environment variables.

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key for LLM inference |
| `HF_API_TOKEN` | Hugging Face token for embedding API |
| `VECTOR_STORE_PATH` | Path to FAISS index inside Lambda (`/tmp/awsense.index`) |
| `LOG_LEVEL` | `INFO` or `DEBUG` |
| `MAX_OUTPUT_TOKENS` | Capped at `512` |
| `AWS_REGION` | Deployment region |

Copy `.env.example` to `.env` in `backend/` for local development.

---

## API Reference

### `POST /chat`

```json
// Request
{ "message": "How does S3 versioning work?", "sessionId": "uuid", "topicFilter": "S3" }

// Response
{
  "answer": "S3 versioning lets you preserve, retrieve, and restore...",
  "sources": [{ "title": "Using versioning in S3 buckets", "url": "https://docs.aws.amazon.com/..." }],
  "tokenUsage": { "inputTokens": 312, "outputTokens": 128 }
}
```

### `GET /health`

```json
{ "status": "ok", "retriever": "local-faiss", "inference": "groq-llama3" }
```

Requests exceeding 20/session/hour return `HTTP 429` with a `retry-after` header. Errors always return `{ "error", "code", "requestId" }` — never raw stack traces.

---

## Architecture Decisions

**Why not Amazon Bedrock?**
The original design used Bedrock Knowledge Base (OpenSearch Serverless + Titan Embeddings) for retrieval and Claude Haiku for inference. Persistent `429` throttling errors across all Bedrock models and regions in Week 1 made this path unreliable. An AWS support case is open. The current stack (Groq + HF Inference API + FAISS) runs at effectively zero variable cost and unblocked development. The retrieval layer is isolated so Bedrock can be reintegrated by changing one file.

**Why FAISS inside Lambda?**
Keeps the entire retrieval pipeline within one compute unit — no external vector DB to manage or pay for. The index is built offline and loaded into `/tmp` on Lambda cold start. Tradeoff: slightly higher cold-start latency (~2s). Provisioned concurrency will be evaluated in Week 3 if needed.

---

## Known Limitations

- Bedrock inference not yet active — pending quota resolution from AWS support
- No persistent session history — conversation resets on page refresh
- Topic filter currently scopes the prompt context but does not yet filter the FAISS search query
- Frontend unit tests (Jest) not yet set up — planned for Week 3

---

## Build Progress

| Week | Goal | Status |
|---|---|---|
| 1 — Foundation | Backend, RAG pipeline, unit tests | ✅ Complete |
| 2 — Frontend + CI/CD | UI deployed, GitHub Actions | 🔄 In progress |
| 3 — Throttling + Observability | DynamoDB throttle, CloudWatch dashboard, integration tests | ⏳ Planned |
| 4 — Testing + Docs | k6 performance tests, SLA report, architecture diagram | ⏳ Planned |

---

## License

MIT
