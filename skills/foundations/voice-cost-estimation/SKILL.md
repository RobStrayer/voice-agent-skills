---
name: voice-cost-estimation
description: Estimate what a voice agent costs per minute, per call and per month, and find what drives the bill. Use when someone asks how much a voice agent will cost, compares a managed platform with a self-built stack, sets pricing for clients, sees a bill higher than expected, or plans for scale.
license: MIT
---

# Voice cost estimation

Build a cost model the user can check line by line. Never quote a price from memory:
voice pricing changes often. Read each price from the provider's current pricing
page and record the URL and the date you read it.

## 1. Get the call profile

Ask only for what you can't infer. Label every assumption.

| Input | Why it matters | Typical way to get it |
| --- | --- | --- |
| Calls per month, average minutes per call | Volume | Existing call logs; otherwise a stated guess |
| Share of the call the agent is talking | Drives text-to-speech | Measure a few real calls; if unknown, use 0.5 and also try 0.3 and 0.7 |
| Turns per minute | Drives language-model calls | Count exchanges in a few transcripts |
| System prompt + tool definitions, in tokens | Re-sent every turn | Tokenize the real prompt |
| Tokens added to history per turn | Makes long calls expensive | Caller words + agent words + tool results |
| Peak concurrent calls | Plan limits and server sizing | Busiest hour × average call length |
| Inbound or outbound, countries | Telephony rates differ a lot | Ask |

## 2. List every component

Write down each thing that bills, with its unit:

- **Telephony:** per minute (often rounded up per call), phone number rental,
  extra legs for transfers and conferences, and outbound attempts that never connect.
- **Speech-to-text:** per minute of audio streamed. Streaming usually bills the
  whole call, including silence.
- **Language model:** input tokens, cached input tokens and output tokens. The
  model re-reads the whole conversation on every turn, so input cost grows with
  the square of the call length. Check whether prompt caching applies.
- **Text-to-speech:** per character or per minute of generated audio. Include
  fillers and repeated confirmations.
- **Speech-to-speech models:** usually billed per audio token or per minute, with
  input and output priced differently. Check how the session's history is billed.
- **Platform fee:** managed platforms charge per minute on top of, or bundled
  with, the components. Check which components are included and which are passed through.
- **Everything else:** servers or workers for your own stack (sized to peak
  concurrency, not average), recording storage, analytics, evaluation runs, and
  support plans or minimum commitments needed for higher concurrency.

## 3. Run the numbers

Copy [`references/example-assumptions.json`](references/example-assumptions.json),
replace every price with a current one, and run:

```bash
python scripts/estimate.py my-assumptions.json
```

The script prints each component's share of the cost per call, then the cost per
call, per minute and per month. Run `python scripts/estimate.py --selftest` to check
the math. Units it understands: `per_call_minute` (set `"round_up": true` for
per-minute telephony billing), `per_caller_audio_minute`, `per_agent_speech_minute`,
`per_tts_character`, `per_llm_input_token`, `per_llm_cached_input_token`,
`per_llm_output_token`, `per_call` and `per_month`.

## 4. Stress the model

Re-run with the cases that break budgets:

- Calls twice as long (language-model input more than doubles).
- Outbound campaigns with low answer rates (you pay for attempts, voicemail and retries).
- Every call transferred to a person (a second telephony leg for the whole transfer).
- A bigger prompt or a knowledge base stuffed into the context.
- Peak concurrency above the plan limit.

## 5. Report

Give the user:

1. A table of components with unit, price, source URL and date read.
2. Cost per call, per minute and per month for the expected profile and the stress cases.
3. The top two cost drivers and one concrete way to reduce each (for example: trim
   the system prompt, enable prompt caching, summarize old turns, use a cheaper
   model for simple turns, shorten agent replies, end silent calls sooner).
4. What you assumed and couldn't verify.

Keep the model honest: a per-minute figure from a marketing page is not your cost
until every component above is accounted for. For the architecture choice itself,
use [voice-stack-selection](../voice-stack-selection/SKILL.md).
