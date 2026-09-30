---
name: voice-latency-audit
description: Investigate voice agent response delay using raw turn events, consistent clocks, component timings, and audio playback evidence; use for latency regressions and benchmark audits.
license: MIT
---

# Voice latency audit

Start with the reported experience and trace one affected conversation through
capture, transport, turn detection, speech recognition, model response, synthesis,
delivery, decoding, and playback. Inspect every caller of the suspected shared
function before changing it. Locate evidence before proposing a fix.

## Define what was measured

Write the start and end event for each metric. Separate these examples:

- End of caller speech to first audible agent audio.
- End-of-turn decision to first model token.
- TTS request to first returned audio chunk.
- Interruption onset to stopped playback.

Use a monotonic clock for differences within one process. Do not subtract
timestamps from different machines without documented synchronization and its
uncertainty. Identify whether events represent real audio, server activity,
transcripts, estimates, or synthetic instrumentation. An audio chunk is not proof
that a listener heard it. Transcript arrival is not necessarily end of speech.

## Reconcile the raw records

Inventory the retained date range, event schema, nested timing fields, alternate
event names, and source gaps. Count unique sessions and turns independently of
the number of metric fields. Deduplicate on stable event/session/turn identifiers.

Group by engine, model/version, region, transport, language, turn policy, and
measurement definition. Keep failed, cancelled, interrupted, and incomplete turns
visible with separate outcome counts. Report sample counts beside percentiles.
State the percentile method. Never add component medians to claim an end-to-end
median, or filter out failures to make a system appear faster.

If the requested metric is not found, say which sources and fields were searched.
Distinguish missing instrumentation from a confirmed zero or an absent event.

## Find and verify the correction

Identify the dominant avoidable delay from correlated traces. Check alternative
explanations such as silence thresholds, buffering, network loss, provider startup,
tool waits, duplicate turn ownership, or playback queues. Change one cause at a
time. Do not cut confirmation, authorization, or intelligibility to improve a graph.

Leave the smallest reproducible check that fails on the demonstrated regression.
Compare equivalent workloads before and after. Recheck interruption, resumed
speech, and completion behavior if timing or cancellation changed.

## Deliver

Metric definitions, source coverage, outcome/sample counts, comparable distributions,
the root cause and evidence, the focused change, and any still-unmeasured stages.

## Primary starting points

- [LiveKit observability](https://docs.livekit.io/agents/ops/)
- [Pipecat documentation](https://docs.pipecat.ai/)
- [OpenAI Realtime conversations](https://developers.openai.com/api/docs/guides/realtime-conversations)
