---
name: voice-call-reliability
description: Diagnose and recover voice call failures across signaling, media, transfers, and business actions. Use for silent calls, failed handoffs, duplicate effects, stranded sessions, capacity incidents, or production readiness reviews.
license: MIT
---

# Voice call reliability

Treat call control, media delivery, conversation, and committed business actions as separate states. A connected call, a completed callback, or a finished worker is not proof that the caller achieved their task.

For call-path faults and handoffs, read [the telephony guide](references/telephony-guide.md), covering legs, codecs, DTMF, transfers, event handling, and cleanup. For service readiness or fleet incidents, read [production operations](references/production-operations-guide.md), covering admission, capacity, draining, observability, cost, and recovery. Read both when the incident crosses those boundaries. Keep these references with the skill when installing it.

## Establish the evidence and authority

Record channel, inbound or outbound direction, carrier/trunk, media transport, provider and installed SDK versions, languages, deployment regions, and the affected time window. Map the application session to every call leg, SIP dialog, room/participant, stream, turn, response, and action ID actually available. Do not invent missing provider events or fields.

Separate inspection and synthetic fixtures from live calls, account changes, recordings, deployments, and paid tests. Reuse the user's existing authorization for the exact account, destinations, and budget; do not expand it because credentials are available. Keep secrets out of transcripts, traces, screenshots, and reports.

## Trace one complete attempt

1. Draw the call-control and media paths, including browser relays or carrier bridges. Identify who accepts the call, starts the agent, owns playback, requests transfers, and ends each leg.
2. Reconstruct the timeline from raw events and authoritative status queries. Distinguish ringing, answered, machine/unknown detection, usable two-way audio, human handoff, final call status, and business outcome. Keep unknown states explicit.
3. For silence or distortion, verify directionality, codecs, sample rates, channels, payload framing, sequence/timestamps, playback queues, and received audio. Use the media-debugging and latency skills when their deeper workflows apply.
4. For a handoff, retain or safely recover the caller leg until the chosen method's success condition is proven. Check busy, no answer, voicemail, queue closure, lost callbacks, and caller abandonment. Verify the fallback after the actual transfer mechanism; do not assume the bot retains control.
5. Verify webhook authentication before accepting effects. Then handle retries, replay, ordering, stale sessions, and duplicate action requests through a durable, versioned application state machine. Signature validity does not establish freshness or business authorization.
6. Reconcile disconnects and uncertain writes before retrying. Ending speech or replacing a worker does not undo a booking. An empty lookup after a timed-out non-idempotent write can remain uncertain; do not automatically submit again.

## Prove and operate the correction

Build a fixture that reproduces the observed failure, with duplicate or reordered events and a late result where relevant. Change the demonstrated cause, then test the affected call leg and business state. Do not replace evidence with a provider demo or a successful SIP handshake.

Use the operations worksheet to establish session admission, arrival bursts, downstream concurrency, cold starts, overload behavior, deployment drain, regional fallback limits, and the incident owner. Define SLIs with boundaries and denominators before choosing SLOs. Keep failed starts, missing playback evidence, transfers, and interrupted actions in the inventory.

For an incident, stop new unsafe work first, preserve active-call outcomes, recover through the approved route, and reconcile orphaned calls, participants, streams, and actions. A traffic switch affects new sessions unless a tested migration procedure establishes otherwise.

## Deliver

Provide the control/media diagram, correlated failure timeline, call-leg and action states, focused correction or proposed intervention, fixture results, capacity/overload worksheet, and recovery path. State source review dates, installed versions, observed versus inferred outcomes, missing evidence, and any live validation still requiring authorization. Claim a successful handoff or business action only from the evidence that establishes it.
