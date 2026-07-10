# Validated Assumption

**Date:** YYYY-MM-DD

## Hypothesis
A local LLM can classify real-world PDFs with useful accuracy.

## Method
10 representative PDFs from different categories were tested.

## Result
The model correctly identified:
- Document type
- Category
- Title
- Reasonable filenames

## Decision
Proceed with the Ollama-based architecture for v0.1.

## File extension comes from the source, never from the LLM

**Context:** The model suggested filenames ending in `.json` for PDF inputs
(contamination from being asked to reply in JSON). Trusting the model's
extension would corrupt files at execute time.

**Decision:** The LLM suggests only the descriptive name stem. The real
extension is taken from the source file and enforced by `paths.py`, which
strips any extension the model may have added.

**Why:** LLM output is untrusted input. The source file's type is a known
fact; the model's guess is not.

## Drop the reasoning_summary field

**Context:** The Classification model had an optional `reasoning_summary`
field holding the model's explanation. In practice it came back `None` on
some documents and verbose on others — the reasoning model (qwen3) leaking
its thinking into the JSON.

**Decision:** Remove the field entirely. Stop asking the model to justify.

**Why:** The field had no consumer — no part of the system reads it. It was
non-deterministic, slowed responses (tokens spent reasoning), and risked
being mistaken for a signal. This aligns with the Needs Review principle:
gate on verifiable facts, never on the model's self-reported reasoning.