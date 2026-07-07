---
title: "Context window is not max output — and you cannot infer one from the other"
date: 2026-07-07
slug: context-window-is-not-max-output
summary: "Two Groq models share the same 131,072-token context window, yet one lets you generate all 131,072 tokens of output and the other caps at 65,536. Context window and max output are independent facts — code that derives one from the other silently truncates responses or throws."
---

# Context window is not max output — and you cannot infer one from the other

Here are two models on the same provider, with the same context window, and different
maximum output. Both figures are from Groq's own models API (`GET
https://api.groq.com/openai/v1/models`, accessed 2026-07-07):

- **llama-3.1-8b-instant** — context window **131,072**, max output **131,072** (equal)
- **openai/gpt-oss-120b** — context window **131,072**, max output **65,536** (half)

Same host. Same context window. One model will return up to 131,072 generated tokens; the
other refuses past 65,536. There is no ratio, no rule of thumb, no "max output is a quarter
of context" that survives contact with real model metadata. You have to look up each one.

## Two different facts that people treat as one

- **Context window** is the total token budget for a single request: input **plus** output
  share it.
- **Max output** (a.k.a. max completion tokens) is a separate cap on how many tokens the
  model will *generate* in one response, regardless of how much context is free.

A model can cap output well below its context window (gpt-oss-120b: 65,536 of 131,072), or
let output consume the entire window (llama-3.1-8b-instant: 131,072 of 131,072). Neither is
derivable from the other; they are two independently published numbers.

## How the confusion shows up

When code assumes the two are the same, the failure is quiet: either the SDK sends a
`max_tokens` larger than the model allows and the request is rejected, or the response is
truncated at a cap the caller did not know existed. It reaches production because it looks
correct in every small test. The confusion is common enough to have produced bug reports in
widely used tooling — e.g. a model configured with a **1,000,000** max output that was
really the model's *context* window
([BerriAI/litellm#14876](https://github.com/BerriAI/litellm/issues/14876)), and threads on
`max_tokens` changing meaning across models
([BerriAI/litellm#18779](https://github.com/BerriAI/litellm/issues/18779)). The pattern is
older than any one library: it is what happens when a schema stores one number where the
world has two.

## The rule

Store the context window and the max output as separate facts, each with its own source.
Never compute one from the other, and never carry a default that happens to equal the
context window — that is the exact shape of the bug above.

Our machine-readable records keep both fields distinct for all 135 models, each field
carrying the verbatim primary-source quote it came from:

- https://factquire.com/feed.json
- https://factquire.com/models/groq/llama-3_1-8b-instant.json
- https://factquire.com/models/groq/openai_gpt-oss-120b.json
