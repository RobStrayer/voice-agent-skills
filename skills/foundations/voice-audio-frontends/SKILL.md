---
name: voice-audio-frontends
description: Select, configure, and evaluate microphone and incoming-call audio processing for voice agents. Use when echo, background noise, competing speakers, gain changes, or speech suppression affect transcription, VAD, turn detection, and interruptions.
license: MIT
---

# Voice audio frontends

Reviewed: **2026-09-30 UTC**. Use the [audio frontend engineering guide](references/audio-frontends-guide.md) for processing mechanisms, placement diagrams, deployment limits, source contracts, and paired-test metrics. Read the relevant sections before recommending settings.

Preserve speech information while addressing a specific interference source. Confirm the application's SDK/API version and target device; configuration examples from a different browser, native SDK, or phone transport are not interchangeable.

## 1. Locate processing and its owner

Draw capture through VAD/model input, plus agent output through device rendering. Inventory device/OS enhancement, browser constraints, native SDK processing, frontend model filters, carrier/trunk effects, agent-side enhancement, and provider input reduction. For every stage record enabled mode, observed support, input/output format, and bypass control. Mark inaccessible stages unknown.

Distinguish these operations in the diagnosis:

- AEC removes playback echo and commonly requires a synchronized render reference.
- Suppression attenuates noise; a gate closes on a level threshold and can clip quiet speech.
- AGC adjusts level; check clipping and gain pumping.
- Beamforming needs array channels and geometry; dereverberation addresses reflections.
- Speaker isolation removes competing voices; confirm who must remain audible, including interpreters and other authorized callers.

Do not treat a denoiser as proof that an echo path is controlled. Confirm which component has capture and actual render timing. An agent's TTS bytes do not automatically form the caller device's echo reference.

## 2. Establish a reversible baseline

Use a short authorized synthetic or consented fixture. Preserve capture, available render reference, transcript labels, configured effects, and timestamps privately. Record upstream processing that cannot be disabled. Never publish customer recordings, credentials, or device identifiers in the report.

Keep model, prompt, turn settings, volume, and fixture fixed while changing one processing stage. Compare headphone and loudspeaker paths when echo is suspected. Inspect browser `getSupportedConstraints()` and track `getSettings()` after configuration and device changes; settings report configuration, not cancellation effectiveness.

For native AEC, verify reference routing, common timing, dropped frames, output-device switches, and clock drift through its supported API. Include near-end speech while agent output is playing. Avoid muting all microphone input when the product must support barge-in.

## 3. Enforce the audio contract

Record codec, container/raw format, rate, channel order, sample representation, byte order, numeric scale, frame size, and timestamps. Decode before PCM processing, retain array channels until beamforming, and keep any reference channel out of the speech downmix.

Validate the selected library's sample scale as well as its float/integer type. RNNoise's C demo uses integer-valued PCM converted to floats; normalized browser floats need explicit adaptation. Query its frame size. Use stateful resampling with continuous timestamps, and measure frame accumulation and lookahead. An offline delay-compensation option does not remove live latency.

If formats or playback are already wrong, apply [voice-media-debugging](../voice-media-debugging/SKILL.md) before tuning suppression.

## 4. Choose the mode and deployment deliberately

Use the guide's [comparison](references/audio-frontends-guide.md#compare-deployment-choices). Check code, selected weights, dependencies, and service terms separately. Open-source orchestration does not grant rights to a commercial enhancement model.

For LiveKit, use the guide's current placement/model distinction: agent VIVA/VIVA telephony, frontend BVC, and SIP-trunk NC. Verify the Cloud route or ai-coustics self-hosted authentication and direct-billing exception explicitly. Avoid stacked enhanced frontend/agent filters while retaining required capture AEC. Confirm the installed plugin contract instead of importing an older model alias.

For a provider input filter, confirm whether it precedes VAD and whether processed samples are observable. Use current microphone profiles and API schemas. Platform and language support must come from the actual SDK documentation. Preserve unavailable processed audio as a measurement limit.

## 5. Measure preservation and turn behavior

Run bypass and candidate processing on the same source with paired labels. Include quiet/distant speech, language and accent cohorts, transient noise, competing talkers, reverberation, echo-only playback, and double-talk on supported devices/codecs.

Report transcription WER/CER and deletions, exact critical words, no-speech hallucinations, missed/false speech starts, clipped onsets, premature ends, interruption recall, residual echo, clipping, added delay, processing stalls, and queue growth. Calculate echo attenuation only in controlled far-end-only windows with aligned signals. Suppressing all samples is a failed preservation result even if echo energy falls.

Record cohort size and failures, not only the average. Listen to paired clips without separately normalizing away gain differences. Reference-free quality scores are estimates; a cleaner-sounding clip can still delete a needed word. Recalibrate VAD/EOT after choosing the frontend, then rerun the same labeled cases.

Use [voice-agent-evaluation](../voice-agent-evaluation/SKILL.md) for the wider audio/transcript/tool evaluation and [voice-latency-audit](../voice-latency-audit/SKILL.md) to account for added delay across the conversation.

## Return a reviewable decision

Provide the observed failing stage, retained processing inventory, one proposed change, exact format/mode/version, license/deployment boundary, paired evidence, regressions, and rollback to the previous configuration. Name unavailable reference signals, opaque upstream effects, and untested platforms. If no authorized audio or runtime is available, return a concrete test plan and clearly label results unmeasured.
