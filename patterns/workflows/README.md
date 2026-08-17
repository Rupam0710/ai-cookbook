# LLM Workflow Patterns

A practical guide to building LLM-powered workflows — from a single API call to multi-agent orchestration. All examples use the OpenAI API with Pydantic for structured output.

---

## Folder Structure

```
patterns/workflows/
├── 1-introduction/          # Core LLM capabilities (the building blocks)
│   ├── 1-basic.py           # Plain text completion
│   ├── 2-structurred.py     # Structured / typed output
│   ├── 3-tools.py           # Function / tool calling
│   └── 4-retrieval.py       # Knowledge base retrieval
│
└── 2-workflow-patterns/     # Combining building blocks into patterns
    ├── 1-prompt-chaining.py # Sequential steps with gate checks
    ├── 2-routing.py         # Route input to the right handler
    ├── 3-parallization.py   # Run checks in parallel
    └── 4-orchestrator.py    # Orchestrator + workers pattern
```

---

## Part 1 — Introduction: Core Building Blocks

These four files each demonstrate one fundamental LLM capability. Every workflow pattern builds on top of these.

```mermaid
flowchart LR
    A["1-basic.py — Text completion"] --> E["Workflow Patterns"]
    B["2-structurred.py — Typed output"] --> E
    C["3-tools.py — Function calling"] --> E
    D["4-retrieval.py — Knowledge retrieval"] --> E
```

---

### 1. Basic — `1-basic.py`

The simplest possible LLM call. Send a prompt, get text back.

```mermaid
flowchart LR
    U(["User prompt"]) --> LLM["GPT-4o"] --> R(["Text response"])
```

**What it does:** Calls `client.chat.completions.create()` with a system and user message.
**Use when:** You just need a natural language answer — no structure needed.

---

### 2. Structured Output — `2-structurred.py`

Forces the LLM to return typed, validated data using a Pydantic schema instead of free text.

```mermaid
flowchart LR
    U(["Alice and Bob going to science fair Friday"]) --> LLM["GPT-4o parse mode"]
    LLM --> S["Pydantic Schema CalendarEvent"]
    S --> O(["name / date / participants"])
```

**What it does:** Uses `client.beta.chat.completions.parse()` + a `BaseModel` to guarantee the output shape.
**Use when:** Downstream code needs to read specific fields from the response.

---

### 3. Tools (Function Calling) — `3-tools.py`

Lets the LLM call your Python functions to get real-world data.

```mermaid
flowchart LR
    U(["Whats the weather in London?"]) --> LLM["GPT-4o"]
    LLM -->|"calls get_weather(51.5, -0.12)"| API["Weather API"]
    API -->|"18C, 12 km/h wind"| LLM
    LLM --> R(["Its 18C in London with light winds."])
```

**What it does:** Defines a tool schema → LLM decides to call it → your code executes it → result goes back to LLM.
**Use when:** The LLM needs live or external data it does not have in training.

---

### 4. Retrieval — `4-retrieval.py`

Gives the LLM access to a private knowledge base via a search tool.

```mermaid
flowchart LR
    U(["User question"]) --> LLM["GPT-4o"]
    LLM -->|"calls search_kb(question)"| KB[("kb.json Knowledge Base")]
    KB -->|"relevant docs"| LLM
    LLM --> R(["Answer grounded in your data"])
```

**What it does:** Loads relevant documents from a JSON knowledge base and passes them to the LLM as context.
**Use when:** The LLM needs to answer questions about your own private data (RAG pattern).

---

## Part 2 — Workflow Patterns

These patterns combine the building blocks above into more powerful, reliable systems.

---

### 1. Prompt Chaining — `1-prompt-chaining.py`

Break a complex task into a **fixed sequence of LLM calls**, where each step's output feeds the next. Gate checks validate output before moving forward.

**Use case:** Processing a calendar request — extract → validate → format → confirm.

```mermaid
flowchart TD
    Input(["Team meeting Tuesday 2pm with Alice and Bob"]) --> S1

    S1["Step 1 — Extract
    Is this a calendar event?
    Confidence score?"]

    S1 --> G1{"Gate: confidence > 0.8
    and is_event = true?"}
    G1 -- No --> Reject(["Not a calendar event"])
    G1 -- Yes --> S2

    S2["Step 2 — Parse Details
    name, date, duration, participants"]

    S2 --> G2{"Gate: date in the future?"}
    G2 -- No --> Reject2(["Date already passed"])
    G2 -- Yes --> S3

    S3["Step 3 — Format
    Create confirmation message"]

    S3 --> Output(["Created: Team Meeting — Tuesday 2pm — Alice, Bob"])

    style G1 fill:#fffacd
    style G2 fill:#fffacd
```

**Why use it:**
- Each step does one thing — easier to debug
- Gates stop bad input early, saving compute on later steps
- Focused LLM calls → higher accuracy per step

---

### 2. Routing — `2-routing.py`

**Classify the input first**, then send it to the right specialised handler.

**Use case:** A calendar assistant that handles creating new events and modifying existing ones via different prompts.

```mermaid
flowchart TD
    Input(["User request"]) --> Router["Router LLM
    Classifies: new_event / modify_event / other
    Confidence score: 0.0 to 1.0"]

    Router --> G{"Confidence >= 0.7?"}
    G -- No --> Fallback(["Low confidence — return None"])
    G -- Yes --> D{"Request type?"}

    D --> |"new_event"| H1["handle_new_event
    Extract: name, date, duration, participants"]
    D --> |"modify_event"| H2["handle_modify_event
    Extract: event ID, changes, add/remove people"]
    D --> |"other"| H3["Not supported — return None"]

    H1 --> Out(["CalendarResponse — message + calendar_link"])
    H2 --> Out

    style G fill:#fffacd
    style D fill:#e8f4fd
```

**Why use it:**
- Each handler has a focused prompt — no single prompt handling everything
- Cheap router model (GPT-4o-mini) → expensive model only for actual work
- Confidence threshold filters out ambiguous or off-topic input

---

### 3. Parallelization — `3-parallization.py`

Run **multiple LLM checks simultaneously** and combine the results. Same latency as running one check.

**Use case:** Validate a calendar request for content validity AND security at the same time.

```mermaid
flowchart TD
    Input(["User input"]) --> Dispatch["Dispatch to parallel checks"]

    Dispatch --> C1["Validation Check
    Is this a valid calendar request?
    Confidence score?"]

    Dispatch --> C2["Security Check
    Is it safe?
    Any prompt injection risk?"]

    C1 --> Combine["Combine Results"]
    C2 --> Combine

    Combine --> G{"Both pass?
    confidence > 0.7
    and is_safe = true?"}

    G -- Yes --> OK(["Safe to process"])
    G -- No --> Reject(["Rejected — show reason"])

    style G fill:#fffacd
```

**Why use it:**
- Both checks run at the same time — half the latency vs sequential
- Each LLM focuses on one concern → better accuracy than one big prompt
- Easy to add more parallel checks without increasing total latency

---

### 4. Orchestrator-Workers — `4-orchestrator.py`

A **central orchestrator LLM** plans the work, **worker LLMs** each write one section with context from previous sections, and a **reviewer LLM** polishes the final result.

**Use case:** Writing a full blog post — orchestrator decides structure, workers write each section, reviewer improves cohesion.

```mermaid
flowchart TD
    Input(["Topic: AI impact on software development
    Target: 1200 words, technical style"]) --> Orch

    Orch["Orchestrator
    Analyses topic and audience
    Defines sections with style guides"]

    Orch --> W1["Worker 1 — Write Introduction
    (gets context: this is first section)"]
    Orch --> W2["Worker 2 — Write Main Body
    (gets context: introduction already written)"]
    Orch --> W3["Worker 3 — Write Conclusion
    (gets context: intro + body already written)"]

    W1 --> Rev
    W2 --> Rev
    W3 --> Rev

    Rev["Reviewer
    Cohesion score 0 to 1
    Suggested edits per section
    Final polished version"]

    Rev --> Output(["Final Blog Post
    + cohesion score
    + edit suggestions"])
```

**Data models used:**

| Model | Purpose |
|-------|---------|
| `SubTask` | One section: type, description, style guide, target word count |
| `OrchestratorPlan` | Topic analysis + audience + list of SubTasks |
| `SectionContent` | Written content + key points for one section |
| `ReviewFeedback` | Cohesion score + suggested edits + final polished post |

**Why use it:**
- Orchestrator dynamically decides the sections — no hardcoded structure
- Each worker receives context from previously written sections for coherence
- Reviewer ensures the whole post flows better than its individual parts

---

## Pattern Comparison

| Pattern | When to use | Latency | Complexity |
|---------|-------------|---------|------------|
| Basic | Simple Q&A, no structure needed | Lowest | Low |
| Structured Output | Need typed fields for code to use | Low | Low |
| Tools | Need live or external data | Medium | Medium |
| Retrieval | Answer from your own private data | Medium | Medium |
| Prompt Chaining | Fixed multi-step task with quality gates | Medium | Medium |
| Routing | Different input types need different handlers | Low | Medium |
| Parallelization | Independent checks that can run together | Low | Medium |
| Orchestrator-Workers | Dynamic tasks, number of steps not known upfront | High | High |

---

## How patterns build on each other

```mermaid
flowchart LR
    B["Basic"] --> S["Structured Output"]
    S --> T["Tools and Retrieval"]
    T --> PC["Prompt Chaining"]
    T --> RT["Routing"]
    T --> PA["Parallelization"]
    PC & RT & PA --> OW["Orchestrator-Workers"]
```

> **Rule of thumb:** Start with the simplest pattern. Only add complexity when you can measure that it improves results.

---

## Setup

```bash
# Set your OpenAI API key
export OPENAI_API_KEY=sk-...

# Run any example from the repo root
python patterns/workflows/1-introduction/1-basic.py
python patterns/workflows/2-workflow-patterns/4-orchestrator.py
```

**Dependencies:** `openai`, `pydantic`, `requests`, `nest_asyncio`
