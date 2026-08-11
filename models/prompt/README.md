# Prompt Engineering: Unlock Your LLM's Full Potential

> "Most people are leaving 80% of an LLM's capability on the table."

---

## Table of Contents

1. [Why Prompt Engineering Matters](#1-why-prompt-engineering-matters)
2. [How LLMs "Think"](#2-how-llms-think)
3. [Core Techniques](#3-core-techniques)
   - [3a. Be Specific & Set the Scene](#3a-be-specific--set-the-scene)
   - [3b. Few-Shot Prompting](#3b-few-shot-prompting)
   - [3c. Chain-of-Thought (CoT)](#3c-chain-of-thought-cot)
   - [3d. Structured Output](#3d-structured-output)
   - [3e. Constraints & Negative Instructions](#3e-constraints--negative-instructions)
   - [3f. Iterative Refinement](#3f-iterative-refinement)
   - [3g. Interview-Style Prompting](#3g-interview-style-prompting)
4. [Advanced Strategies](#4-advanced-strategies)
   - [System vs. User Prompts](#system-vs-user-prompts)
   - [Prompt Chaining](#prompt-chaining)
   - [Self-Evaluation](#self-evaluation)
   - [Temperature & Parameters](#temperature--other-parameters)
5. [Common Mistakes & Fixes](#5-common-mistakes--fixes)
6. [Real-World Use Cases](#6-real-world-use-cases)
7. [Wispr Flow: Speak Your Prompts](#7-wispr-flow-speak-your-prompts)
8. [Toolkit & Resources](#8-prompt-engineering-toolkit--resources)

---

## 1. Why Prompt Engineering Matters

Prompt engineering is **programming in natural language** — you give the model a role, task, format, and constraints instead of writing code.

The same model can seem brilliant or useless depending on how you ask.

| | Bad Prompt | Great Prompt |
|---|---|---|
| Input | `Write something about our product.` | `You are a senior B2B copywriter. Write a 2-sentence LinkedIn ad for our project-management SaaS (Asana alternative). Audience: ops managers at mid-size companies. Tone: confident but not salesy. End with a clear CTA to start a free trial. No emojis.` |
| Output | Generic marketing fluff, wrong tone, no CTA | On-brand, scoped, actionable, ready to drop into an ad |

**Who benefits:**
- **Developers** — code generation, debugging, docs, refactors
- **Marketers** — copy, ads, emails, social, A/B ideas
- **Researchers** — summarization, literature review, brainstorming
- **Everyday users** — writing, planning, learning, decision-making

> Better prompts = better results, for everyone. It's a skill that compounds.

---

## 2. How LLMs "Think"

### Next-Token Prediction
The model predicts the next token (word or sub-word) based on everything in the current context. It has **no memory of past chats** unless you include that information explicitly.

- More relevant context + clearer instructions → more relevant and consistent outputs.

### Steering vs. Commanding

| Approach | Example |
|---|---|
| **Commanding** | `"Summarize this."` — model chooses length, style, and focus |
| **Steering** | `"You are an executive assistant. Summarize this meeting transcript in 4 bullet points. Focus on decisions and action items. No filler."` |

Steering via **role, audience, format, and constraints** gives far more consistent and usable results.

---

## 3. Core Techniques

### 3a. Be Specific & Set the Scene

Define **role, audience, tone, and format** so the model doesn't have to guess.

- **Role:** `"You are a senior technical writer."`
- **Audience:** `"Writing for developers who know Python but not cloud APIs."`
- **Tone:** `"Professional but friendly; avoid jargon or explain it once."`
- **Format:** `"Start with a 2-sentence overview, then numbered steps, then a short 'Common pitfalls' section."`

**Example — support reply:**

```
# Weak
Reply to this customer complaint.

# Strong
You are a customer support lead. Reply to this complaint from a paying user whose
export failed twice. Acknowledge the frustration, apologize briefly, confirm we're
investigating, and offer a concrete next step (e.g. we'll email within 24h).
Keep it under 150 words. Sign off as "Support Team."
```

---

### 3b. Few-Shot Prompting

Give **2–4 examples** of input → output pairs. The model infers the pattern and replicates it.

Especially helpful for: format, style, edge cases, and classification.

**Example — turning feedback into ticket titles:**

```
# Zero-shot (inconsistent results)
Turn this user feedback into a short ticket title.
Feedback: "The app crashes when I upload a PDF over 10MB on iPhone."

# Few-shot (consistent, structured results)
Turn user feedback into a short ticket title (under 60 chars). Use format: [Area] Brief description.

Feedback: "Login is broken with Google on Safari."
Title: [Auth] Google login fails on Safari

Feedback: "Export to CSV only exports first 100 rows."
Title: [Export] CSV export limited to 100 rows

Feedback: "The app crashes when I upload a PDF over 10MB on iPhone."
Title:
```

Result: `[Upload] Crash on large PDF (iPhone)` — consistent and structured every time.

---

### 3c. Chain-of-Thought (CoT)

Ask the model to **reason step by step** before giving a final answer. Reduces errors on logic, math, multi-step planning, and comparisons.

**Example:**

```
# Without CoT (prone to arithmetic errors)
A store sells pens for $2 and notebooks for $5. Sarah buys 3 pens and 2 notebooks.
She has a 10% off coupon. How much does she pay?

# With CoT
A store sells pens for $2 and notebooks for $5. Sarah buys 3 pens and 2 notebooks.
She has a 10% off coupon. How much does she pay?
Think step by step: find subtotal, then apply discount, then state final amount.
```

**Useful phrases:**
- `"Think step by step."`
- `"Show your reasoning."`
- `"Explain each step before concluding."`

---

### 3d. Structured Output

Ask explicitly for **JSON, tables, XML, or Markdown** so you can parse and use the output in code or docs.

**Example — product comparison:**

```
# Free-form (hard to parse)
Compare our product to Competitor X and Competitor Y on price, features, and support.

# Structured (machine-readable)
Compare our product (OurApp) to Competitor X and Competitor Y.
Respond with valid JSON only, no other text, in this shape:

{
  "products": [
    { "name": "...", "price": "...", "keyFeatures": ["...", "..."], "support": "..." }
  ]
}
```

---

### 3e. Constraints & Negative Instructions

Say explicitly what you **don't want**: length, tone, format, or topic.

| Type | Example |
|---|---|
| **Length** | `"Summarize in exactly 3 bullet points."` / `"Keep the reply under 100 words."` |
| **Tone** | `"No slang or humor."` / `"Do not apologize."` |
| **Format** | `"Do not use bullet points; use one short paragraph."` |
| **Scope** | `"Do not suggest paid tools."` / `"Do not include code; describe the approach only."` |

**Example:**
```
# Without constraint (might start with "Welcome!" fluff)
Write a short intro for our onboarding doc.

# With constraint
Write a short intro for our onboarding doc. Start directly with what the user will
do in this section. Do not start with 'Welcome' or generic greetings.
```

---

### 3f. Iterative Refinement

Treat prompting as a **conversation**, not a one-shot. First reply not perfect? Refine:
- `"Shorter."`
- `"More formal."`
- `"Add one example."`
- `"Focus only on X."`

**Example flow:**
1. You: `"Draft a 2-sentence blurb for our new feature: smart scheduling."`
2. Model: Returns 4 sentences, a bit salesy.
3. You: `"Cut it to 2 sentences and make it more factual, less salesy."`
4. Model: Tighter, more factual.
5. You: `"Add that it works with Google Calendar."`
6. Model: Final version. ✓

Iteration is normal and often **faster** than writing the perfect prompt on the first try.

---

### 3g. Interview-Style Prompting

Instead of guessing what context to provide, **let the model ask you questions** before it writes.

**How to do it:**
1. Describe what you want in a sentence or two.
2. Ask the model to interview you: `"Before you do this, interview me: ask me any questions you need answered to do this well. Ask one at a time."`
3. Answer each question concisely.
4. Once it has enough, it delivers the output.

**Example — blog post:**
```
I need a short blog post (about 400 words) for our company blog.
Topic: why small teams should try async standups.
Before you write it, interview me: ask me any questions you need to do this well—
audience, tone, product mentions, format, etc. Ask one question at a time.
When you have enough information, say "I have enough—here's the post" and then write it.
```

**When to use it:** Complex or high-stakes tasks (strategy docs, customer emails, pitches), when you're unsure what context matters, or when you want to avoid multiple wrong-draft cycles.

---

## 4. Advanced Strategies

### System vs. User Prompts

| Prompt Type | Purpose |
|---|---|
| **System prompt** | Sets identity, rules, and style (always-on behavior, not shown to end users) |
| **User prompt** | The actual request for this turn — keep it focused |

**Example:**
```
System: "You are a helpful coding assistant. You answer in concise, correct snippets.
         You never make up API names; if unsure, say so."
User:    "How do I read the first line of a file in Python?"
```

---

### Prompt Chaining

Break complex tasks into **sequential steps**. Use the output of step N as input to step N+1. Improves reliability and makes individual steps easy to debug.

**Example — blog post pipeline:**
1. `"Given topic [X], output a 5-heading outline. JSON: { "headings": [...] }"`
2. `"Expand this outline into a 400-word section. Outline: [paste Step 1]. Tone: [Y]."`
3. `"Turn this draft into meta title and description for SEO. Max 60 chars title, 155 chars description."`

Each step has **one clear job** and **one clear output format**.

---

### Self-Evaluation

Ask the model to **critique or score its own output** before you accept it.

**Example:**
```
Here's a short summary I generated: [text].
Rate it 1–5 for clarity and completeness.
In one sentence, suggest the single most important improvement.
```

Use the critique to refine in the next turn.

---

### Temperature & Other Parameters

| Setting | Use For |
|---|---|
| **Low temperature** (e.g. 0.2) | Facts, code, structured output, consistency |
| **High temperature** (e.g. 0.8) | Brainstorming, varied phrasing, multiple ideas |

- Outputs too random or off-task? → Lower temperature.
- Outputs too repetitive? → Raise it slightly.

---

## 5. Common Mistakes & Fixes

| Mistake | What Goes Wrong | Fix |
|---|---|---|
| **Too vague** | Generic or irrelevant output | Add role, audience, tone, format, and length |
| **Too many tasks in one prompt** | Model drops or mixes tasks | Split into steps or separate prompts (chaining) |
| **Not enough context or examples** | Wrong format or style | Add 1–3 few-shot examples; include relevant background |
| **Ignoring format** | Hard to parse or reuse | Explicitly request structure (e.g. `"JSON with keys X, Y, Z"`) |
| **Assuming memory** | Model "forgets" earlier context | Repeat or summarize key facts in the current turn |

**Example of "too many tasks":**
```
# Overloaded — model will drop or mix tasks
"Summarize this article, list the main criticisms, suggest 3 discussion questions, and write a tweet about it."

# Better — one step at a time
1. "Summarize this article in 3 bullets."
2. "List the main criticisms mentioned."
3. "Suggest 3 discussion questions."
4. "Write a tweet for this article."
```

---

## 6. Real-World Use Cases

### Writing & Content

```
# Email follow-up
You are writing a follow-up email to a prospect who didn't reply to your first message.
Product: project management tool for small teams.
Goal: one short paragraph that adds value (e.g. one tip or resource), then one soft CTA to reply.
Tone: helpful, not pushy. No guilt-tripping. Under 80 words.
```

### Code & Debugging

Provide code + language + framework. Ask **one focused thing** per turn: explain, find bug, add error handling, refactor, or add tests.

```
This Python function sometimes raises KeyError. [paste code].
Find the cause and suggest a minimal fix with a one-line comment explaining why.
```

### Data Analysis & Summarization

```
Here are last month's support tickets by category. [data].
In a markdown table, show: category, count, % of total.
Add one sentence on the biggest driver.
```

### Research & Brainstorming

```
We're naming a new feature: it suggests the best time to send emails.
Give 5 name options. Short, memorable, no jargon.
Then pick your top one and say why in one sentence.
```

---

## 7. Wispr Flow: Speak Your Prompts

**[Wispr Flow](https://wisprflow.ai)** is a voice dictation tool built specifically for developers and knowledge workers. Instead of typing long, detailed prompts, you simply **speak them out loud** — Wispr Flow transcribes and formats them in real time, directly into any text field on your screen (VS Code, browser, Slack, etc.).

### Why It Matters for Prompt Engineering

Writing great prompts requires rich context: role, audience, tone, format, constraints, examples. Typing all of that is slow and breaks your flow. Wispr Flow removes that friction.

| Without Wispr Flow | With Wispr Flow |
|---|---|
| You type out a long, detailed prompt character by character | You speak the context naturally — Wispr Flow transcribes it instantly |
| You simplify or shorten prompts to avoid typing effort | You give the model all the context it needs without hesitation |
| Prompt quality suffers because writing is slow | Prompt quality improves because speaking is fast and natural |
| Context-switching to type breaks your coding flow | Stay in flow — speak while thinking, keep coding |

### How a Developer Uses It

1. **Generating boilerplate or logic** — You're in VS Code. Instead of typing, you say: *"Write a Python function that reads a CSV, groups by the 'category' column, and returns a dict of category to average value. Add type hints and a docstring."* Wispr Flow types it into the Copilot chat for you.

2. **Debugging** — You paste the error and say: *"This is a KeyError in a FastAPI route. The error happens when the user ID is not in the session. Find the cause and suggest a minimal fix."*

3. **Writing commit messages or PR descriptions** — You say: *"Write a commit message. I refactored the auth middleware to use a decorator pattern, removed duplicate token validation logic, and added a unit test."*

4. **Filling in context for interview-style prompts** — When the model asks you clarifying questions, you just speak your answers instead of typing them. Fast and natural.

### Key Benefits

- **No typing fatigue** for long, well-structured prompts
- **Better prompts by default** — you naturally include more context when speaking
- **Works everywhere** — VS Code, browser, Notion, Slack, any text input
- **Stays in your flow** — no copy-paste, no context switching
- **Speeds up iterative refinement** — saying *"make it shorter and more formal"* takes 1 second

> Wispr Flow effectively lowers the cost of writing a good prompt to nearly zero — so there's no reason to write a bad one.

---

## 8. Prompt Engineering Toolkit & Resources

### Prompt Libraries & Templates
- [PromptBase](https://promptbase.com) — marketplace of ready-made prompts
- [FlowGPT](https://flowgpt.com) — community prompt library
- [OpenAI Examples](https://platform.openai.com/examples) — official use-case examples
- [Anthropic Prompt Library](https://docs.anthropic.com/en/prompt-library/library) — Claude-optimized prompts

### Official Guides
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Design Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)

### Build Your Own Prompt Journal
- Save prompts that work well (and note which model/settings you used)
- Note what you changed when something didn't work
- Build a personal library by task type: `"support reply"`, `"blog outline"`, `"code review"`, `"summarize"`, etc.
- Refine over time — good prompts compound in value
