---
name: voice-media-debugging
description: Diagnose silent, distorted, one-way, delayed, or obsolete audio in voice agents by checking codecs, sample rates, transport, queues, and playback. Use when a connection succeeds but the media path fails, or audio continues after an interruption.
license: MIT
---

# Voice media debugging

Reviewed: **2026-09-30 UTC**. Original engineering guidance; provider-specific
contracts are linked below. Confirm the application's installed SDK and current
transport documentation before changing its audio path.

Find the earliest boundary where good audio becomes bad audio. Keep the model,
prompt, and voice fixed while isolating transport or playback faults.

## Capture the actual path

Draw both directions, including conversion and buffering:

```text
microphone / phone -> capture -> transport -> decoder / resampler -> model
speaker / phone   <- playback <- transport <- encoder / resampler <- model
```

For each boundary record the negotiated contract and the observed values:

| Field | Evidence to collect |
| --- | --- |
| Format | Codec, raw stream or container, sample rate, channels; for PCM, bit depth, signedness, and byte order |
| Framing | Payload bytes, duration represented, sequence or timestamp, arrival and consumption times |
| Ownership | Session, track, stream, response, and turn identifiers |
| Flow control | Producer rate, consumer rate, queue depth in milliseconds, overflow policy |
| Output state | Track attached, playback started or rejected, device/phone leg, mute state |

Use a short authorized synthetic or consented fixture with a known format and
duration. Keep credentials and real customer recordings out of diagnostic reports.
Preserve the original bytes; changing an extension or WAV header does not convert
the samples. Record any resampling or transcoding step explicitly.

## Check format before tuning timing

For constant-rate uncompressed PCM:

`bytes = sample_rate * duration_seconds * channels * (bits_per_sample / 8)`

Examples for 20 ms of audio, excluding container and transport headers:

| Encoding | Expected bytes |
| --- | ---: |
| 24 kHz, mono, signed 16-bit PCM | 960 |
| 48 kHz, stereo, signed 16-bit PCM | 3,840 |
| 8 kHz, mono, 8-bit G.711 mu-law | 160 |

The mu-law row counts one encoded byte per sample; it is not linear PCM. These
examples are arithmetic checks, not a recommendation that every API accepts
20 ms chunks. Variable-rate codecs such as Opus need their own framing rules.

Check actual bytes and declared metadata independently. A decoder configured for
48 kHz will consume 24 kHz PCM twice as fast unless something resamples it. A
base64 wrapper changes representation, not codec. Avoid repeated sample-rate
conversions; put a necessary conversion at a documented boundary.

## Work from the symptom

| Symptom | First hypotheses | Evidence that separates them |
| --- | --- | --- |
| Speech too fast, slow, or wrong pitch | Sample-rate mismatch | Known duration versus decoded sample count and playback rate |
| Static or severe distortion | Wrong codec, byte order, sample width, header interpreted as samples | Small payload inspection plus decoding with the negotiated format |
| Connected but silent | No captured audio, unsubscribed/muted track, rejected playback, wrong output device | Capture energy, outgoing/incoming counters, track attachment, playback result |
| Only one direction works | Different format or network failure on one leg | Separate inbound and outbound boundary records |
| Delay grows during the call | Producer outpaces consumer, queued obsolete audio, repeated buffering | Queue duration over time and producer/consumer rates |
| Clicks or gaps | Dropped/duplicated chunks, framing error, underruns, discontinuity at conversions | Sequence/timestamp gaps and queue-empty events |
| Old speech resumes after interruption | Late packets accepted, output queue not cleared, active playback not stopped | Response IDs on every queued chunk and interruption timeline |

Treat these as hypotheses. For example, a zero audio level could reflect actual
silence; a missing counter is not a measured zero. Change one boundary at a time
and rerun the same fixture before drawing a conclusion.

## Browser and WebRTC checks

Separate signaling, network connectivity, received media, decoding, and audible
playback. A successful offer/answer exchange proves only part of that path.
Inspect ICE candidates and the selected transport before changing network rules;
TURN relays help when direct connectivity is unavailable. Follow the deployment's
existing configuration and authorization. [WebRTC peer connections](https://webrtc.org/getting-started/peer-connections)
and [TURN](https://webrtc.org/getting-started/turn-server).

Use `getStats()` reports from the affected peer and time window. Match the report
ID, track, and direction; use the transport's `selectedCandidatePairId` to find its
selected pair. Do not join unrelated streams or subtract counters across a
reconnection. [MDN getStats](https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection/getStats)
and [selectedCandidatePairId](https://developer.mozilla.org/en-US/docs/Web/API/RTCTransportStats/selectedCandidatePairId).

For the same inbound RTP report over a valid interval:

`mean_jitter_buffer_ms = 1000 * delta(jitterBufferDelay) / delta(jitterBufferEmittedCount)`

The numerator is cumulative seconds of jitter-buffer residence; the denominator
counts emitted samples or frames. Require both fields, a positive count delta,
and nondecreasing counters. Keep packet loss, network jitter, and this buffer
delay separate. None measures sound reaching a listener's ear. Field availability
depends on the implementation. [W3C statistics definitions](https://www.w3.org/TR/webrtc-stats/)
(published Candidate Recommendation Draft: 2025-09-25; checked 2026-09-30).

Handle the promise from `HTMLMediaElement.play()`. A `NotAllowedError` can indicate
that browser autoplay policy prevented playback; provide a normal user-initiated
play control and observe its result. Do not report playback success merely
because a media element exists. [MDN play](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/play).

## Phone and streaming boundaries

Inspect the contract for the specific product and direction. SIP call setup,
RTP media, and an application WebSocket are different layers. An answered call
does not prove working audio in both directions. Check negotiated codecs, media
addresses, and the application's payload contract before changing the model.

For **Twilio bidirectional Media Streams**, outbound audio is base64-encoded raw
8 kHz mono mu-law, without file headers. A returned `mark` can follow playback or
a `clear`, so correlate it with the clear timeline. Do not reuse that schema for
ConversationRelay or another carrier. [Twilio message contract](https://www.twilio.com/docs/voice/media-streams/websocket-messages).

## Stop the right work on interruption

Trace generation, network delivery, queued chunks, and active playback separately.
Cancellation semantics differ by provider; some already-generating audio can
still arrive. For example, check [Cartesia context cancellation](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts)
before treating cancellation as proof that its output stream ended.

Use a response or generation identifier to reject obsolete chunks, clear the
application's old output queue, and stop already scheduled playback through its
supported API. Keep the next valid response intact. If a transport clear affects
the whole output buffer, complete the clear transition before releasing the new
response; otherwise the fix can discard its first words. Compare cancellation
and packet times only on a common clock, or establish order from explicit events.
Update conversation history
according to what the transport can establish was played; mark uncertainty when
the available acknowledgement cannot distinguish played from discarded audio.

Audio interruption also does not prove that a booking or payment tool stopped.
Handle action state independently using the project's cancellation, idempotency,
and confirmation rules. This skill diagnoses the media path; use
[voice-agent-evaluation](../voice-agent-evaluation/SKILL.md) for tool correctness.

## Return an evidence-based diagnosis

Provide the failing boundary, observed mismatch, smallest correction, and the
same-fixture result before and after. Include session/turn identifiers only when
safe to share. State which directions, devices, codecs, and network conditions
were actually exercised. Preserve unmeasured stages as unknown.

If the bytes and playback are correct but response onset remains slow, use
[voice-latency-audit](../voice-latency-audit/SKILL.md). Do not turn a successful
synthetic test into a claim of production voice quality.
