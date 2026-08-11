# OpenAI Responses API

## What we will cover

1. [Introduction](#1-introduction)
2. [Text Prompting](#2-text-prompting)
3. [Conversation States](#3-conversation-states)
4. [Function Calling](#4-function-calling)
5. [Structured Output](#5-structured-output)
6. [Web Search](#6-web-search)
7. [File Search](#7-file-search)
8. [Reasoning](#8-reasoning)

---

## 1. Introduction

**File:** `01-introduction.py`

Covers the basics of the OpenAI Responses API and how it compares to the Chat Completions API.

- **Chat Completions API** — Standard message-based API using `client.chat.completions.create()` with a `messages` list. Returns a response via `response.choices[0].message.content`.
- **Responses API** — Newer, simplified API using `client.responses.create()` with an `input` field. Returns a response via `response.output_text`.
- **Image input** — Pass image URLs directly using `input_image` type in the `input` list.
- **Streaming** — Use `stream=True` and iterate over events filtering for `text.delta` event types to print output progressively.

---

## 2. Text Prompting

**File:** `02-text-prompting.py`  
**Docs:** https://model-spec.openai.com/2025-02-12.html

Demonstrates the new roles and instruction features in the Responses API.

- **`instructions` field** — A top-level system-level instruction (e.g. `"Talk like a pirate."`) that shapes model behavior without needing a separate message role.
- **New roles** — The Responses API introduces a `developer` role in addition to `system`, `user`, and `assistant`.
- **Chain of command** — Role priority is hierarchical: `system` → `developer` → `user`. A `developer` instruction can override a `system` instruction.
- **Input formats** — `input` can be a plain string or a list of role-based messages.

---

## 3. Conversation States

**File:** `03-conversation-state.py`  
**Docs:** https://platform.openai.com/docs/guides/conversation-state?api-mode=responses

Shows three approaches to managing multi-turn conversations.

- **Manual state** — Pass the full conversation history as a list of messages in `input`. You control what gets included.
- **Dynamic state** — Build history programmatically by appending each response's `output` back into the list before the next request.
- **Server-side state** — Use `previous_response_id=response.id` to let OpenAI automatically chain responses server-side. No need to manage history locally. Enabled by default (`store=True`).

---

## 4. Function Calling

**File:** `04-function-calling.py`

Demonstrates how to give the model access to custom functions/tools.

- Define tools as a list of JSON schema objects with `type: "function"`, including `name`, `description`, and `parameters`.
- Pass tools via the `tools` parameter in `client.responses.create()`.
- The model decides when to call a function and returns structured `output` items — inspect with `.model_dump_json()`.
- Multiple function calls can be returned in a single response (e.g. sending emails to multiple recipients at once).

---

## 5. Structured Output

**File:** `05-structured-output.py`

Forces the model to return responses in a strict, predictable format.

- **JSON Schema** — Pass a `text.format` object with `type: "json_schema"` and define the exact schema. Use `strict: True` to enforce it. Parse the result with `json.loads(response.output_text)`.
- **Pydantic models** — Define a Python class inheriting from `BaseModel` and pass it as the response format. OpenAI's SDK automatically generates the schema and deserializes the response.
- Useful for extracting structured data (e.g. calendar events, entities) reliably from unstructured text.

---

## 6. Web Search

**File:** `06-web-search.py`

Enables the model to fetch live data from the web before generating a response.

- Add `{"type": "web_search_preview"}` to the `tools` list.
- The model decides when to search and incorporates results into its answer.
- **User location** — Optionally provide `user_location` with `country` and `city` to get geographically relevant results.
- **Citations** — Access source URLs via `response.output[1].content[0].annotations[0].url`.

---

## 7. File Search

**File:** `07-file-search.py`  
**Docs:** https://platform.openai.com/storage/files/

Allows the model to search uploaded documents to answer questions with grounded context.

- **Upload a file** — Use `client.files.create()` with `purpose="assistants"`. Supports both local files and URLs (downloaded on the fly).
- **Vector store** — Create a vector store with `client.vector_stores.create()`, then attach files to it. The store indexes the content for semantic search.
- **File search tool** — Pass `{"type": "file_search", "vector_store_ids": [...]}` in `tools` to enable retrieval-augmented generation (RAG) over uploaded files.
- Note: Vector stores have associated storage costs.

---

## 8. Reasoning

**File:** `08-reasoning.py`  
**Docs:** https://platform.openai.com/docs/guides/reasoning?api-mode=responses

Uses OpenAI's reasoning models (`o3-mini`, `o1`) for complex, multi-step problems.

- Use reasoning models (`o3-mini`) instead of `gpt-4o` for tasks requiring logic, math, or code generation.
- Pass a `reasoning` parameter with an `effort` level: `"low"`, `"medium"`, or `"high"`. Higher effort = more thinking time = better accuracy.
- Ideal for complex coding tasks, mathematical proofs, multi-step planning, and analytical problems.
- The model outputs a final answer via `response.output_text` after internal reasoning steps.

---

## Most important things to know

1. **Backward Compatibility**: The Responses API is a superset of Chat Completions - everything you can do with Chat Completions can be done with Responses API, plus additional features.
2. **Migration Timeline**: The Chat Completions API is not being deprecated and will continue to be supported indefinitely as an industry standard for building AI applications, while the Assistants API (not Chat Completions) is the one planned for eventual deprecation in 2026.
3. **Key New Features**:

   - Simplified interface for different interaction types
   - Native support for web search capabilities
   - A new `developer` role you can use
   - Improved support for reasoning models
   - Built-in file/vector search functionality
   - Simplified conversation state management

4. **Available Tools**:

   - **Web search**: Include data from the Internet in model response generation
   - **File search**: Search the contents of uploaded files for context when generating a response
   - **Computer use**: Create agentic workflows that enable a model to control a computer interface
   - **Function calling**: Enable the model to call custom code that you define, giving it access to additional data and capabilities

5. **When to Migrate**:

   - For new applications: Start with Responses API to be future-proof
   - For existing applications: Begin planning migration, but no immediate urgency
   - Test the new API in parallel with existing implementations

6. **Implementation Considerations**:

   - API structure changes but core AI engineering principles remain the same
   - Features that previously required multiple API calls can now be done in single calls
   - The fundamental patterns of retrieval, tools, and memory management still apply

7. **New Agent SDK**: OpenAI has released a new Agent SDK that will replace [Swarm](https://github.com/openai/swarm/tree/main). This provides a standardized way to build AI agents with the Responses API. Learn more at: [https://platform.openai.com/docs/guides/agents](https://platform.openai.com/docs/guides/agents)

8. **Documentation Resources**:

   - Official OpenAI documentation: [https://platform.openai.com/docs/api-reference/responses](https://platform.openai.com/docs/api-reference/responses)


## Most important things to know

1. **Backward Compatibility**: The Responses API is a superset of Chat Completions - everything you can do with Chat Completions can be done with Responses API, plus additional features.
2. **Migration Timeline**: The Chat Completions API is not being deprecated and will continue to be supported indefinitely as an industry standard for building AI applications, while the Assistants API (not Chat Completions) is the one planned for eventual deprecation in 2026.
3. **Key New Features**:

   - Simplified interface for different interaction types
   - Native support for web search capabilities
   - A new `developer` role you can use
   - Improved support for reasoning models
   - Built-in file/vector search functionality
   - Simplified conversation state management

4. **Available Tools**:

   - **Web search**: Include data from the Internet in model response generation
   - **File search**: Search the contents of uploaded files for context when generating a response
   - **Computer use**: Create agentic workflows that enable a model to control a computer interface
   - **Function calling**: Enable the model to call custom code that you define, giving it access to additional data and capabilities

5. **When to Migrate**:

   - For new applications: Start with Responses API to be future-proof
   - For existing applications: Begin planning migration, but no immediate urgency
   - Test the new API in parallel with existing implementations

6. **Implementation Considerations**:

   - API structure changes but core AI engineering principles remain the same
   - Features that previously required multiple API calls can now be done in single calls
   - The fundamental patterns of retrieval, tools, and memory management still apply

7. **New Agent SDK**: OpenAI has released a new Agent SDK that will replace [Swarm](https://github.com/openai/swarm/tree/main). This provides a standardized way to build AI agents with the Responses API. Learn more at: [https://platform.openai.com/docs/guides/agents](https://platform.openai.com/docs/guides/agents)

8. **Documentation Resources**:

   - Official OpenAI documentation: [https://platform.openai.com/docs/api-reference/responses](https://platform.openai.com/docs/api-reference/responses)
