---
name: voice-latency-audit
description: Investigate voice agent response delay using raw turn events, consistent clocks, component timings, and audio playback evidence; use for latency regressions and benchmark audits.
license: MIT
---

# Voice latency audit

Reproduce the reported delay or locate a conversation that demonstrates it. Trace
capture, transport, turn detection, speech recognition, model response, tools,
synthesis, delivery, decoding, and playback. Read the affected code and every caller
of the suspected shared function before changing it. Keep provider inspection and
live tests within the account, destination, and budget already authorized.

## Define what was measured

Record the event boundaries, unit, clock, and evidence source for every duration.

| Metric | Start and end | What it establishes |
| --- | --- | --- |
| End-of-turn delay | User speech ends, then the runtime decides the turn is complete | Endpointing behavior; record how speech end was detected or annotated. |
| LLM time to first token (TTFT) | Model request starts, then its first generated token arrives | Model/request responsiveness, including any setup the emitter includes. |
| TTS time to first byte/chunk (TTFB) | The emitter's synthesis start, then its first audio arrives | Synthesis responsiveness; identify whether start means request, connection, or first text input. |
| Runtime response latency | Runtime speech-end event, then its output-start event | The path between those instrumented events. |
| Audible response latency | End of user speech in captured audio, then first audible agent response | The measured listener path, including buffering and device or phone delivery. |
| Interruption stop latency | Caller starts interrupting, then agent audio stops on the measured path | Whether playback yielded promptly; generation cancellation is a separate event. |

Separate the first acknowledgment or filler from the first useful answer. A fast
"I'm checking" can coexist with a slow result. For a tool task, also measure the
confirmed action outcome and the response that communicates it.

## Map the current instrumentation

Read the installed SDK version, event producers, and raw schema before selecting
fields. In the LiveKit documentation reviewed below, per-turn values live on
`ChatMessage.metrics`; `session_usage_updated` tracks usage. Session-level
`metrics_collected` is deprecated, while per-plugin metrics events remain supported.
An older installed version can expose a different surface.

LiveKit's current per-turn fields include `end_of_turn_delay`,
`transcription_delay`, `llm_node_ttft`, `tts_node_ttfb`, `playback_latency`, and
`e2e_latency`. The LLM/TTS node fields apply to an STT-LLM-TTS pipeline and are empty
for realtime models. Its playback field ends at the output component's playback
report, which can be near zero without remote playback reporting. Validate these
events against the actual media path before calling them listener measurements.
[Source: LiveKit data hooks](https://docs.livekit.io/testing/observability/data.md).

A transcript can arrive after speech ends, and generated audio can arrive before
playback starts. On Twilio Media Streams, correlate `mark` with sent media and any
`clear`: marks also return when audio is discarded. A returned mark alone does not
establish that audio was heard. [Source: Twilio WebSocket messages](https://www.twilio.com/docs/voice/media-streams/websocket-messages).

## Keep clocks and overlapping work separate

Use monotonic differences within one clock domain. Keep wall-clock timestamps for
record lookup and dates. Browser, worker, provider, and audio-capture timestamps
need a documented alignment method and uncertainty before cross-domain subtraction.
Audio sample positions are useful only with the capture rate, channel alignment,
and any resampling accounted for. Do not clip unexplained negative durations to zero.

Reconstruct the timeline for each turn. Streaming and speculative generation can
overlap endpointing, model work, and synthesis. Sum components only when their
boundaries prove they are adjacent, disjoint spans of the same turn. Never add
component medians or percentiles to produce an end-to-end percentile. Label a
component-sum estimate and show which delivery stages it omits.

## Reconcile records and comparison groups

Inventory the retained date range, event schema, nested timing fields, alternate
event names, archives, and gaps. Join session, turn, response, speech, and tool IDs
as the schema permits; preserve each record's source. Count unique sessions and
turns independently of metric fields. Check totals against the raw event inventory.
Deduplicate retries of the same exported record while retaining distinct attempts.

Compare groups with the same metric definition and relevant engine/model versions,
region, transport, codec, language, turn policy, hardware, load, and warmup state.
Keep tool turns, cached output, speculative work, cold starts, and ordinary replies
distinguishable when they explain the delay. A provider's offline throughput or
real-time factor is not a microphone-to-speaker response duration.

Keep failed, cancelled, interrupted, and incomplete turns in outcome counts. Show
the total eligible turns, completed measurements, missing boundaries, and any
excluded cases beside each latency distribution. Incomplete turns have no observed
completion latency; do not record zero or silently discard them. State the
percentile method and avoid a stable-tail claim from a small sample.

If the requested metric is not found, say which sources and fields were searched.
Distinguish missing instrumentation from a confirmed zero or an absent event.

## Find and verify the correction

Identify the dominant avoidable delay from correlated traces. Check alternative
explanations: endpointing policy, late final transcripts, blocking callbacks,
provider connection setup, tool waits, transcoding, playback queues, network loss,
or duplicate response ownership. Distinguish a slow detector from a slow inference
call, and a policy timeout from a missing event.

Record which component owns turn completion and interruption. Verify that a
configuration change affects that owner; realtime provider-side turn detection can
ignore framework interruption settings. Review the active provider/plugin docs
before changing thresholds. [Source: LiveKit turn handling](https://docs.livekit.io/agents/logic/turns.md).

Change one demonstrated cause at a time. Preserve confirmation, authorization,
intelligibility, and the caller's ability to finish. When adjusting endpointing,
compare false cutoffs as well as delay. The end-of-turn benchmark below measures
that tradeoff; its ranking does not establish performance on this application's
language, audio, or tasks. [Source: eot-bench](https://github.com/livekit/eot-bench#evaluation-model).

Leave the smallest reproducible check that fails on the demonstrated regression.
Compare equivalent workloads before and after. If cancellation or speech timing
changes, recheck backchannels, resumed speech, stale queued audio, tool completion,
and call cleanup. Canceling speech does not prove an external action was canceled.

## Deliver

Provide a compact table with metric boundaries, comparable groups, eligible and
measured counts, outcomes, and distributions. Include a trace demonstrating the
cause, the focused change, regression results, and the still-unmeasured path.
Keep observed values, derived estimates, and proposed targets labeled separately.

## Source review

Documentation reviewed on 2026-09-30 UTC. This date records the review; publication
dates were not established for the linked documentation. Check the installed SDK
and current pages before relying on field names or configuration behavior.
