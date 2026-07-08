# LocalVault

## Project Overview

**LocalVault** is a privacy-first local AI document organizer that will gradually evolve into a local AI workspace.

The project is built primarily as a serious portfolio project and engineering learning platform. The goal is **not** to build a startup or SaaS.

The goal is to learn and demonstrate:

- Python
- Software Architecture
- Testing
- Local AI
- Ollama
- SQLite
- RAG *(later)*
- Agentic AI *(later)*
- Clean Engineering Practices

> LocalVault should feel like a real open-source product, not a tutorial project.

## Core Principle

**User documents never leave the machine.** LocalVault must run locally.

By default:

- No OpenAI
- No Anthropic
- No Google AI APIs
- No telemetry
- No analytics
- No cloud sync

Ollama is the preferred AI runtime.

## Vision

LocalVault evolves in layers:

```
Reliable document organizer
        ↓
Searchable document library
        ↓
Chat with documents
        ↓
Local agents
        ↓
Private AI workspace
```

No layer should be built before the previous one works reliably.

## Current Scope

Current focus: **v0.1** — a local batch PDF organizer.

It is **not**:

- A watcher
- A web application
- A desktop application
- A SaaS

### v0.1 Goal

The objective is to organize PDFs safely using a local LLM.

The workflow is:

```
extract
   ↓
classify
   ↓
propose
   ↓
human confirmation
   ↓
execute
   ↓
record
```

The first version must:

- Process PDFs
- Extract text
- Classify using Ollama
- Suggest destination
- Suggest filename
- Show preview
- Require confirmation
- Move safely
- Record history

## Architectural Decisions

### Batch First

v0.1 uses:

```
localvault organize ./Organizar
```

Folder watching is postponed to v0.2. Watching is considered a delivery mechanism, not part of the core domain.

### Plan / Apply Pattern

The core architecture follows:

```
analyze(path)
      ↓
OrganizationProposal

  (human confirmation)

execute(proposal)
      ↓
OrganizeResult
```

**Rules:**

- `analyze` never mutates the filesystem
- `execute` performs filesystem changes
- Confirmation lives between them
- Confirmation is not domain logic

### Ports & Adapters

The core domain must not know how it is triggered.

- **Current adapter:** CLI
- **Future adapter:** Watcher

Both must call the same domain logic.

### Audit Trail

No file should move without leaving a record. History is considered a domain invariant. Future undo functionality depends on this.

## Path Safety Principles

LLM output is considered **untrusted**. The `paths` module is the trust boundary.

**Rules:**

- Validate results, not inputs
- Reject path traversal
- Reject absolute paths
- Reject home expansion
- Prevent symlink escape
- Keep destination inside `target_root`
- Use deterministic collision handling

Structural violations raise exceptions. The organizer translates them into **Needs Review**.

### Needs Review Rules

Do **not** use LLM confidence scores. Needs Review is triggered by verifiable conditions:

- Extraction failure
- Invalid structured output
- Unknown category
- Path validation failure

## Technology Choices

Current stack:

- Python
- Ollama
- PyMuPDF
- SQLite
- Pydantic
- Typer
- pytest
- Ruff

Avoid introducing additional infrastructure unless a second real use case exists.

### Anti-Overengineering Rules

Before introducing an abstraction, ask:

> Do we have a second real use case?

If not, prefer the simpler implementation.

Examples of what to avoid:

- No plugin system
- No LLM provider abstraction
- No microservices
- No event bus
- No Kubernetes
- No premature interfaces

## Learning Goals

The project exists to improve engineering skills.

**Priorities:**

- Understanding architecture
- Writing code personally
- Learning testing
- Learning design trade-offs
- Building a strong GitHub portfolio

> Finishing faster is less important than understanding the decisions.

## How Claude Should Help

Claude acts as:

- Software Architect
- Technical Mentor
- Design Reviewer
- Code Reviewer
- Engineering Coach

**Default behaviour:**

- Explain concepts
- Challenge decisions
- Discuss trade-offs
- Suggest tests
- Suggest invariants
- Suggest pseudocode when useful

Claude should not generate production code unless explicitly requested. The objective is to teach engineering thinking, not accelerate implementation.

## Communication Rules

- **Conversation language:** Portuguese (Portugal)
- **Project language:** English

Use European Portuguese when communicating. Use English for:

- Code
- Commit messages
- Architecture documents
- README
- Repository structure