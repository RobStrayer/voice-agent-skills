---
name: voice-agent-evaluation
description: Design and run proportionate voice agent evaluations covering conversation success, turn taking, tool correctness, audio behavior, failures, and lifecycle cleanup.
license: MIT
---

# Voice agent evaluation

Define the behavior being evaluated and a clear passing outcome. Inspect the
actual engine, transport, turn policy, tool permissions, and state lifecycle.
Read the implementation and existing tests. Use the existing harness before adding
another. Match the test layer to the claim and keep paid or external actions within
the user's authorized scope.

## Choose the evidence layer

| Layer | Useful evidence | Coverage limit |
| --- | --- | --- |
| Scripted text turns | Tool selection, arguments, policy, reply content, state transitions | Bypasses speech recognition, synthesis, and the media path. |
| Conversation simulation | Goal completion, repair across turns, handoffs, unsupported requests | A simulator or model judge can miss faults a human caller would notice. |
| Audio into the runtime | Recognition errors, pause handling, synthesized response, interruption events | An injected clip may bypass capture, echo processing, transport, or device playback. |
| Actual browser or phone path | Connection, codecs, audio queues, audible overlap, reconnect, caller experience | Covers the exercised devices, network conditions, language, and workload. |

Use exact assertions for tool names, arguments, authorization decisions, authoritative
state, and duplicate side effects. Reserve semantic judgments for language properties
that cannot be expressed with those checks. Record a judge's model/version, rubric,
and input; inspect disputed passes and failures. A judge score does not establish
that a booking, transfer, or payment took effect.

LiveKit's test framework can run scripted turns with `session.run`, inspect ordered
messages and function events, check agent handoffs, and replace tools with mocks.
Assert the function result and subsequent response, then check for unexpected
remaining events. A mocked tool verifies how the agent uses that result; a separate
integration check establishes the real tool's behavior. Model-backed test runs and
judges can still require paid inference even when business tools are mocked.
[Source: LiveKit test framework](https://docs.livekit.io/agents/start/testing/test-framework.md).

## Build a focused scenario set

Begin with normal task completion and the demonstrated regression. Add the nearby
failure cases affected by the change. Write the expected result before running it.

| Area | Useful cases | Observable result |
| --- | --- | --- |
| Turn taking | Hesitation inside a sentence, long pause, "uh-huh", overlap, resumed speech | Waits for completion, handles backchannels according to policy, and produces one intended response. |
| Interruption | Caller corrects intent during speech, during a read, or after a write begins | Audible output yields as configured; stale replies stay suppressed; action status remains available. |
| Tools | Success, timeout, malformed result, denial, duplicate callback, retry after uncertain completion | Valid arguments and authorization; truthful result handling; no duplicate effect. |
| Knowledge | Missing answer, stale or contradictory source, quoted instructions inside retrieved content | Grounded answer, clarification, or an explicit limit; external content does not override policy. |
| Recognition | Names, negation, dates, account digits, accents, relevant languages, code switching | Task-critical meaning survives transcription or the agent asks for repair. |
| Output audio | Pronunciation, numbers, silence, noise, codec/rate mismatch, long response | Intelligible speech without clipped starts, drift, or obsolete buffered audio. |
| Handoffs | Agent handoff, human transfer, unavailable destination, caller changes their mind | Confirmed ownership, sufficient context, and a usable failure path. |
| Lifecycle | Disconnect during tool work, reconnect, farewell, provider failure, worker shutdown | Consistent terminal state, bounded retries, and resources released once. |

Measure transcription quality on the task as well as text similarity. A wrong digit
or dropped "not" can break an otherwise plausible transcript. Aggregate WER does
not establish tool-argument correctness. Record the tested languages and conditions;
one clean English call does not cover multilingual or noisy-phone behavior.

## Exercise ownership and cancellation

Identify who owns the input turn, generated response, playback queue, tool work,
and external action. Test each relevant transition independently. After an
interruption, verify both the audible cutoff and the history used on the next turn.
The agent must not assume the caller received the unplayed remainder of its reply.

LiveKit's current tool documentation states that interrupting the agent does not
cancel running tool work by default. Cancellation must reach the actual task or
request, and interrupted handoffs have their own behavior. Inspect the SDK and
execution path instead of treating a speech-stop event as tool rollback.
[Source: LiveKit function tools](https://docs.livekit.io/agents/logic/tools/definition.md#interruptions).

For interrupted or timed-out writes, read the authoritative action status before
replaying. Reuse the original idempotency key for the same action when the API
supports it; do not assume every provider accepts one. Verify exactly one committed
effect, suppressed stale output, and a truthful explanation on the next turn. A
successful cancellation request can arrive after a remote service has committed.
Include a commit followed by a lost response and a temporarily empty lookup. Without
external idempotency or conclusive status, the expected behavior is reconciliation
of an uncertain action, not automatic replay. App-side deduplication alone does not
establish exactly-once effects across that boundary.

Use invented identities and synthetic content. Mock tools that send messages,
charge money, book services, or change account state unless the user has authorized
those actions. Keep authorization and state assertions outside the model's prose.

## Record evidence that can be replayed

Record scenario ID, inputs, expected behavior, run ID, engine and model versions,
relevant settings, prompt revision, tool events, final state, and actual outcome.
Include the test layer, transport, language, codec, and any deterministic mocks or
randomization. Use stable case IDs so a rerun can compare the same behavior.

Retain redacted events and permitted audio. Keep the transcript, generated text,
tool trace, and played-audio evidence distinguishable. Provider timing fields may
leave delivery unmeasured. Use the [latency audit](../voice-latency-audit/SKILL.md)
for clocks, event boundaries, and comparable timing groups. Use human listening for
claims about perceived speech quality, and record the listening setup and rubric.

Report task success, tool correctness, recognition errors, interruption behavior,
and speech quality separately. Show eligible, passed, failed, skipped, interrupted,
and unevaluable counts without counting one run twice in its outcome denominator.
For a metric, state which subset has the required evidence. Preserve failed attempts
when retrying; a later successful run does not erase the original result.

If live calls are necessary, establish the permitted destination, run count,
spend limit, recording policy, and cleanup before dialing. Retry transient failures
only within that bound. Do not reset a call allowance or expand to production.

## Deliver

A scenario/outcome table, denominator and failed/skipped counts, links to redacted
evidence, regressions and causes, and the exact layer that remains unverified.
For a fix, rerun the demonstrated regression and nearby affected scenarios. State
whether the result came from mocks, paid model inference, injected audio, or an
actual call. Completion requires the requested behavior and applicable checks to
pass; mark inaccessible or unauthorized test layers as unverified.

## Source review

Documentation reviewed on 2026-09-30 UTC. This date records the review; publication
dates were not established for the linked documentation. For turn and playback
semantics, see [LiveKit turn handling](https://docs.livekit.io/agents/logic/turns.md)
and [data hooks](https://docs.livekit.io/testing/observability/data.md). Verify API
assertions and event names against the project's installed SDK.
