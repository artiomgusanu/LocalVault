# Architecture — LocalVault v0.1

## Scope

v0.1 is a one-shot, batch PDF organizer with a CLI. No folder watching, no web
UI, no OCR, no search. Its only job is to prove the core loop end to end and be
trustworthy while doing it.

## The core loop (the domain)

```
extract text -> classify -> resolve destination -> propose
                                                      |
                                            (human confirms)
                                                      |
                                              execute -> record
```

Everything else in the system is scaffolding around this loop.

## Ports & adapters

The trigger is an **adapter** over a trigger-agnostic core. In v0.1 the only
adapter is the `organize` CLI command, which lists existing PDFs and drives the
loop. In v0.2 a `watch` command becomes a *second* adapter that debounces
filesystem events and calls the exact same core functions. Adding watching must
never require touching the domain — if it does, the boundary was drawn wrong.

## The plan/apply seam

```
analyze(path)      -> OrganizationProposal   # never mutates the file tree
execute(proposal)  -> OrganizeResult         # re-validates, moves, records
```

Confirmation lives **between** these two calls, in the interface layer — never
inside the domain. This is the plan/apply pattern (as in Terraform): produce a
concrete proposed action, let something outside approve it, then apply it.

**Key invariant.** `analyze` is not pure — it reads a file and calls the LLM, so
it does I/O and is non-deterministic. The invariant that matters is narrower and
more useful: **`analyze` must never mutate the target tree.** No moves, no writes
to the destination. That single guarantee is what makes the core reusable across
every future interface.

## Data model

- **`OrganizationDecision`** — the raw LLM output: `document_type`, `category`,
  `title`, `suggested_filename`, `reasoning_summary`. Kept conceptually distinct
  from the proposal, but in v0.1 it is folded directly into building the proposal
  rather than exposed as its own persisted type. (Promote to a first-class type
  when a second consumer of the raw decision appears.)
- **`OrganizationProposal`** — the reviewed, concrete action:
  - `source_path`
  - `source_fingerprint` (size + mtime, or a content hash) — used to detect
    staleness at execute time
  - `destination_path` — the **fully resolved** final path string
  - decision metadata (type, category, title, reasoning)
  - `collision_strategy` (e.g. numeric suffix)
- **`OrganizeResult`** — per-file outcome: `moved | skipped | failed`, final path,
  error detail.
- **`HistoryRecord`** — the persisted result.

**Decision: the proposal carries the fully-resolved destination path.**
Rationale: a proposal must represent a concrete, unambiguous, auditable action;
the user confirms exactly what will happen, not a higher-level intent that could
resolve differently later. Accepted cost: the proposal is a snapshot, so
`execute` must re-validate against `source_fingerprint` and re-check for
collisions before moving.

## Modules (v0.1)

Changes from the nine-module sketch in the project brief:

- **Cut:** `watcher.py` -> deferred to v0.2 (second adapter over the same core).
- **Re-drawn:** path safety pulled *out* of `organizer.py` into its own module.
  It is the correctness/security centre of the system and deserves isolation.
- **Resisted:** no LLM-provider interface yet (a concrete `OllamaClient` is
  already replaceable enough); no extractor plugin system (one function). These
  abstractions arrive when a *second* case exists, not before.

```
localvault/
├── models.py          # value objects: Proposal, Result, HistoryRecord
├── extractor.py       # PDF -> text via PyMuPDF. One function, no plugin registry.
├── ollama_client.py   # transport to Ollama. Concrete class, narrow surface.
├── classifier.py      # text -> OrganizationDecision. Structured output + validate + one retry.
├── paths.py           # resolve, sanitize, collision, traversal guard. Most-tested module.
├── organizer.py       # the service: analyze() and execute(). Orchestration only.
├── history.py         # SQLite persistence via stdlib sqlite3.
├── config.py          # Ollama host/model, watched & target roots. Deliberately minimal.
└── cli.py             # the adapter. No business logic.
```

`sqlite3` stays in v0.1 despite being tempting to defer: it is stdlib (zero
dependencies), it is an explicit learning goal, history is an acceptance
criterion, and undo (v0.4) will query it. Keeping it is not premature.

## Safety (the actual hard part)

The LLM generates filesystem paths. Treat every suggested path as hostile input:

- Reject absolute paths, `~`, and any component that would escape the target
  root via `..`.
- Sanitize filenames: strip illegal characters, cap length, trim trailing dots
  and spaces, avoid reserved names.
- Resolve the final path and assert (via realpath containment) that it lives
  inside `target_root`.
- Collisions: a deterministic strategy (numeric suffix), resolved at `execute`
  time and surfaced to the user if the final name differs from what was
  confirmed.
- Move atomically where possible (`os.rename` within one filesystem); across
  filesystems fall back to copy + fsync + atomic replace. Never leave a
  half-moved file.

The Ollama call is the easy part. This module is where correctness is won or lost.

## Needs Review — gate on facts, not vibes

Do **not** route files based on the LLM's self-reported confidence score; it is
uncalibrated. Route a file to `Needs Review/` when:

- text extraction produced too little content to classify, or
- structured output failed validation after one retry, or
- the suggested category maps to no known folder and cannot be safely created.

These are verifiable conditions. A float emitted by the model is not.

## What v0.1 deliberately excludes

`watch`, TXT/DOCX, OCR, embeddings and semantic search, undo, YAML rules, an
LLM-provider abstraction, and proposal persistence/versioning. Each returns only
when a working layer beneath it makes it necessary.

## On recording decisions

For now this file is the single source of architectural truth. Adopt lightweight
ADRs (`docs/adr/NNNN-title.md`) later — specifically when a decision *reverses* an
earlier one and "why did we change our mind?" becomes a real question. For a
solo greenfield repo on day one, a directory of ADRs would be ceremony without
payoff.
