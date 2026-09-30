---
name: voice-agent-evaluation
description: Design and run proportionate voice agent evaluations covering conversation success, turn taking, tool correctness, audio behavior, failures, and lifecycle cleanup.
license: MIT
---

# Voice agent evaluation

Define the behavior being evaluated and a clear passing outcome. Inspect the
actual engine, transport, turn policy, tool permissions, and state lifecycle.
Use an existing test harness before adding another. Separate text simulations,
streamed-audio tests, and real media-path tests in the report.

## Build a focused scenario set

Use normal task completion plus the relevant failure and boundary cases:

| Area | Useful cases | Observable result |
| --- | --- | --- |
| Turn taking | Pause, hesitation, backchannel, overlapping speech | Correct turn ownership; no duplicate response |
| Interruption | Barge-in during speech or a tool wait; speech resumes | Playback and generation stop appropriately; state stays coherent |
| Tools | Success, timeout, retry, duplicate request, denied action | Correct arguments and authorization; no duplicate side effect |
| Knowledge | Known answer, missing answer, contradictory source | Grounded answer or honest uncertainty |
| Audio | Noise, silence, accents, relevant languages, codec mismatch | Intelligible response and explicit failure behavior |
| Lifecycle | Disconnect, reconnect, farewell, worker failure | Correct terminal state; resources released once |

After an interrupted or timed-out tool, read the authoritative action status
before replaying it. Reuse the same idempotency key for a retry of the same action.

Choose only cases applicable to the requested change. Use invented identities
and synthetic content. Mock tools that send messages, charge money, book services,
or change account state unless the user has authorized those exact actions.

## Record evidence that can be replayed

Record scenario ID, inputs, expected behavior, run ID, engine and model versions,
relevant settings, tool events, final state, and actual outcome. Store recordings
only when permitted; otherwise retain redacted events and metric summaries.

Judge business correctness separately from fluency. A plausible spoken promise
does not prove that the tool executed. A simulator transcript does not verify
WebRTC/SIP, browser autoplay, physical playback, or acoustic echo behavior.
Use human listening for claims about perceived speech quality.

If live calls are necessary, establish the permitted destination, run count,
spend limit, recording policy, and cleanup before dialing. Retry transient failures
only within that bound. Do not reset a call allowance or expand to production.

## Deliver

A scenario/outcome table, denominator and failed/skipped counts, links to redacted
evidence, regressions and causes, and the exact layer that remains unverified.
For a fix, rerun the demonstrated regression and nearby affected scenarios.

## Primary starting points

- [LiveKit testing](https://docs.livekit.io/agents/start/testing/)
- [Pipecat examples](https://github.com/pipecat-ai/pipecat/tree/main/examples)
- [Twilio voice documentation](https://www.twilio.com/docs/voice)
