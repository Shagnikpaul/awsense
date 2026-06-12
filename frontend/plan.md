# AWSense — Frontend Build Prompt (Week 2, Days 6–7)

> This prompt is for an AI coding agent. Paste it at the start of a session where you want the agent to build the AWSense frontend UI from scratch.

---

## WHO YOU ARE AND WHAT YOU ARE DOING

You are a frontend engineering assistant helping build the UI for **AWSense** — a full-stack RAG (Retrieval-Augmented Generation) chatbot that answers AWS documentation questions. This is a solo CS undergraduate internship project.

Your job today is **only to build the frontend UI**. You will not touch anything outside the `frontend/` folder. You will not wire to a real backend, set up deployment, or configure CI/CD. Those come in later sessions.

---

## CRITICAL BEHAVIOR RULES

1. **Work only inside the `frontend/` folder.** Do not touch `backend/`, `infra/`, `scripts/`, `k6/`, or any other top-level folder. If you think you need to touch something outside `frontend/`, stop and ask.
2. **Give instructions or code in chunks.** Do not dump everything at once. After each file or logical group of files, stop and ask: *"Done? Any issues before I continue?"*
3. **Wait for confirmation** ("done", "ok", "no doubts") before moving to the next chunk.
4. **Today's hard stop:** Once all frontend UI components are built and the app runs locally with `npm run dev`, tell the user: *"Day 6–7 frontend build is complete. Stop here. Day 7–8 (wiring to backend) is the next session."* Do not begin backend wiring or deployment prep today.
5. **No tests today.** Frontend unit tests (Jest + React Testing Library) are a separate task for a later session. Do not write any test files.

---

## PROJECT CONTEXT (READ FOR UNDERSTANDING — DO NOT BUILD BACKEND)

**AWSense** is a chatbot that:
- Takes AWS-related questions from the user
- Retrieves relevant chunks from a local FAISS vector index built from AWS documentation pages
- Generates an answer using an LLM (Amazon Bedrock / Claude Haiku)
- Returns the answer alongside source citations and token usage stats

The backend is **not yet complete**. The frontend you build today must work standalone with mock/placeholder data wherever real API responses would normally appear. The backend API contract is documented below for reference — use it to shape the frontend's data structures and integration points.

**Backend API contract (reference only — do not implement):**
- `POST /chat` → accepts `{ message, sessionId, topicFilter? }` → returns `{ answer, sources[], tokenUsage }`
- `GET /health` → returns service status + dependency check
- HTTP 429 with `retry-after` header when rate limit exceeded (20 requests/session/hour)
- Errors returned as `{ error, code, requestId }` — never raw stack traces

---

## EXISTING PROJECT SETUP

The `frontend/` folder already has a **Vite + React** project bootstrapped with the default template. It has:
- `package.json` with basic React + Vite deps
- `src/App.jsx` with boilerplate code
- `src/main.jsx`
- `index.html`
- `vite.config.js`

**Nothing extra is installed yet.** You need to install all additional packages yourself as part of the setup.

---

## WHAT TO BUILD

### Target folder structure inside `frontend/src/`

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatWindow.jsx       # scrollable message list area
│   │   ├── MessageBubble.jsx    # single message (user or assistant)
│   │   ├── InputBar.jsx         # text input + send button + topic filter
│   │   ├── TokenUsage.jsx       # token count display per response
│   │   ├── SourceCitations.jsx  # source links shown below each answer
│   │   ├── TopicFilter.jsx      # dropdown for AWS service category filter
│   │   ├── RateLimitBanner.jsx  # warning banner when rate limit is hit
│   │   ├── ThemeToggle.jsx      # dark/light mode toggle button
│   │   └── Sidebar.jsx          # optional: left sidebar with session info / branding
│   ├── api/
│   │   └── chatClient.js        # API call functions (stubbed with mock data for now)
│   ├── hooks/
│   │   └── useChat.js           # custom hook managing chat state and session logic
│   ├── constants/
│   │   └── awsTopics.js         # list of AWS topic filter options
│   ├── __tests__/               # leave empty — tests come in a later session
│   ├── App.jsx                  # root component, sets up layout and theme
│   └── main.jsx                 # entry point (likely no changes needed)
├── public/
├── index.html
├── vite.config.js
├── tailwind.config.js           # to be created
└── package.json
```

Feel free to use judgment on splitting components further if a file is getting too large. The structure above is a guide, not a rigid contract.

---

## PACKAGES TO INSTALL

Install the following before writing any component code:

```bash
# Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# shadcn/ui (component library) — follow their Vite setup
npm install class-variance-authority clsx tailwind-merge lucide-react

# shadcn/ui init
npx shadcn@latest init

# Additional utility
npm install uuid
```

Use **shadcn/ui** components as much as possible for things like: Button, Input, Badge, Dropdown/Select, Separator, Tooltip, ScrollArea. Pull them in with `npx shadcn@latest add <component>` as needed.

Use **lucide-react** for icons (Send, Trash2, Sun, Moon, ChevronDown, etc.).

---

## VISUAL DESIGN REQUIREMENTS

- **Theme:** Dark by default, with a light mode toggle. Use CSS variables or Tailwind's `dark:` classes.
- **Style reference:** Think Claude.ai or ChatGPT dark — clean, minimal, professional. Not flashy or loud.
- **Font:** Use `Inter` from Google Fonts (or system font stack as fallback). Apply via `index.html` or Tailwind config.
- **Layout:** Two-column on desktop (optional narrow sidebar left + main chat area right). Single column on tablet/mobile.
- **Color palette suggestion (dark mode):**
  - Background: `#0f0f0f` or `#111111`
  - Surface/card: `#1a1a1a` or `#1e1e1e`
  - Border: `#2a2a2a`
  - Primary accent: `#FF9900` (AWS orange) — use sparingly for buttons, highlights
  - Text primary: `#f5f5f5`
  - Text muted: `#888888`
  - User message bubble: slightly lighter surface
  - Assistant message bubble: transparent / same as background
- **Light mode:** Clean white background, dark text, same orange accent.

---

## FUNCTIONAL REQUIREMENTS TO IMPLEMENT

| ID | Requirement | Implementation Notes |
|---|---|---|
| F01 | User can type a question and receive an answer | Use mock/placeholder response for now; mark integration point with a comment |
| F02 | Each answer includes source citations (doc title + URL) | Use `SourceCitations.jsx` with placeholder sources array |
| F03 | Conversation history shown in session (last 5 turns) | `useChat.js` hook manages messages array; cap display at last 5 turns |
| F04 | Topic filter dropdown for AWS service category | Dropdown with options: All, EC2, S3, VPC, IAM, Lambda, RDS, CloudFront, Route 53, ELB, CloudWatch |
| F05 | Token usage indicator per response | Show `inputTokens / outputTokens` below each assistant message using `TokenUsage.jsx` |
| F06 | Rate-limit warning banner when throttle exceeded | `RateLimitBanner.jsx` — show conditionally when `isRateLimited` state is true |
| F07 | Responsive layout — desktop and tablet | Tailwind responsive classes; sidebar hidden on mobile |
| F08 | "Clear conversation" button resets session | Clears messages array in `useChat.js`; generates a new sessionId |

---

## MOCK DATA SPEC

Since the backend is not connected yet, use this shape for mock/placeholder data everywhere:

```js
// Mock chat response (matches real API contract for future wiring)
const mockResponse = {
  answer: "Amazon S3 (Simple Storage Service) is an object storage service that offers industry-leading scalability, data availability, security, and performance...",
  sources: [
    {
      title: "Amazon S3 Documentation — Getting Started",
      url: "https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html"
    },
    {
      title: "Amazon S3 FAQs",
      url: "https://aws.amazon.com/s3/faqs/"
    }
  ],
  tokenUsage: {
    inputTokens: 312,
    outputTokens: 128
  }
};

// Mock health response
const mockHealth = {
  status: "ok",
  retriever: "local-faiss",
  inference: "pending-bedrock-access"
};
```

Use a simulated delay (e.g., `setTimeout` of 800–1200ms) when returning mock responses so the loading state is visible and testable.

---

## INLINE COMMENT REQUIREMENTS

This is important. In every file where a real backend integration point exists, add a clearly visible inline comment like this:

```js
// TODO [BACKEND INTEGRATION]: Replace this mock response with a real call to POST /chat
// Expected request body: { message, sessionId, topicFilter }
// Expected response: { answer, sources[], tokenUsage }
// See: chatClient.js → sendMessage()
```

Specifically, mark integration points in:
- `chatClient.js` — every stubbed function
- `useChat.js` — where mock response is used
- `RateLimitBanner.jsx` — where `isRateLimited` is currently hardcoded/simulated
- `TokenUsage.jsx` — where token data comes from mock
- `SourceCitations.jsx` — where sources come from mock

The goal is that a developer picking this up later can `Ctrl+F "TODO [BACKEND INTEGRATION]"` and find every integration point immediately.

---

## COMPONENT-LEVEL NOTES

### `App.jsx`
- Root layout component
- Manages `darkMode` state and provides a `ThemeToggle`
- Apply `dark` class to `<html>` or root `div` based on state
- Renders `Sidebar` (optional/collapsible) + `ChatWindow` side by side

### `useChat.js` (custom hook)
- Manages: `messages[]`, `isLoading`, `isRateLimited`, `sessionId`, `topicFilter`
- `sessionId` generated with `uuid` on mount and on "Clear conversation"
- `sendMessage(text)` function: appends user message, calls `chatClient.sendMessage()`, appends mock assistant response
- Keeps only last 5 turns in the displayed conversation (can store full history internally if needed)

### `chatClient.js`
- Export `sendMessage({ message, sessionId, topicFilter })` — returns mock response after a delay
- Export `checkHealth()` — returns mock health object
- All functions clearly stubbed with integration comments
- This is the **only** file that will need to change when the real backend is ready

### `ChatWindow.jsx`
- Renders the scrollable list of `MessageBubble` components
- Auto-scrolls to the bottom on new messages
- Shows a loading indicator (spinner or pulsing dots) while `isLoading` is true

### `MessageBubble.jsx`
- Accepts `role` (`"user"` | `"assistant"`) and `content`
- User messages: right-aligned or left-aligned with different background
- Assistant messages: show `SourceCitations` and `TokenUsage` below the answer text

### `InputBar.jsx`
- Text `<textarea>` or `<input>` (shadcn Input)
- Send button (shadcn Button) — disabled when input is empty or `isLoading` is true
- `TopicFilter` dropdown embedded inside or beside the input area
- Submit on Enter key (Shift+Enter for newline)
- Character counter visible when approaching 500 char limit

### `TopicFilter.jsx`
- shadcn Select component
- Options defined in `constants/awsTopics.js`
- Passes selected value up to `useChat` via prop or context

### `TokenUsage.jsx`
- Small muted text below each assistant message
- Format: `Tokens: 312 in / 128 out`

### `SourceCitations.jsx`
- Rendered below each assistant answer
- List of clickable links: `[doc title] → external URL`
- Open in new tab

### `RateLimitBanner.jsx`
- Fixed banner at top of chat area
- Only visible when `isRateLimited === true`
- Show: *"You've reached the request limit. Please wait before sending more messages."*
- Dismissible with an X button

### `ThemeToggle.jsx`
- Single icon button: Sun (light) / Moon (dark)
- Toggles `darkMode` state in `App.jsx`

---

## WHAT SUCCESS LOOKS LIKE TODAY

When done, running `npm run dev` should show:
- A polished dark-mode chat UI in the browser
- User can type a message, hit send, and see a mock assistant reply appear after ~1 second
- Reply includes placeholder source citations and token usage
- Topic filter dropdown works (selection stored in state, passed with mock request)
- Clear conversation button resets the chat
- Light/dark toggle switches the theme
- Layout is clean and responsive on desktop and tablet widths
- No console errors

---

## WHAT NOT TO DO TODAY

- Do NOT touch anything outside `frontend/`
- Do NOT make real HTTP calls to any backend
- Do NOT set up Vite proxy, CORS config, or environment variables for API URLs
- Do NOT write any test files
- Do NOT start Day 7–8 work (wiring to real backend)
- Do NOT configure anything for deployment (S3, CloudFront, etc.)

---

## START INSTRUCTION

Begin by confirming the current state of `frontend/` — ask the user to share or describe what's currently in `src/App.jsx` and `package.json` so you know exactly what the baseline is. Then start with package installation, and proceed chunk by chunk from there.

---

*Session: Week 2, Days 6–7 | AWSense Frontend Build | Dark theme, shadcn/ui, Tailwind, React + Vite*