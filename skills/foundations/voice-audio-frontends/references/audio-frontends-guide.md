# Audio frontends: preserve speech while removing interference

Reviewed: **2026-09-30 UTC**. Processing choices and test procedures here are original engineering guidance. Linked provider contracts were checked on that date; living pages usually do not establish a publication date. No model, audio benchmark, or provider call was run for this review.

An audio frontend decides which samples reach recognition and turn detection. Choose it against a specific failure: agent speech returning through a speaker, a fan keeping VAD active, background conversation becoming a command, or quiet words disappearing. Record the existing processing before adding another stage.

## Choose the operation that matches the interference

| Operation | What it changes | What to check |
| --- | --- | --- |
| Acoustic echo cancellation (AEC) | Estimates and removes playback leaking into microphone capture; conventional AEC uses a render reference. | Reference routing, timing, output device, room changes, and preservation of simultaneous user speech. |
| Noise suppression | Attenuates interference such as fan or traffic noise. | Speech distortion, transient noise, and whether competing voices are preserved. |
| Noise gate | Attenuates audio below an opening threshold, often with attack, release, and hysteresis. | Quiet syllables, onset clipping, and repeated opening/closing. It does not separate overlapping speech from noise. |
| Automatic gain control (AGC) | Adjusts signal level over time. | Clipping, gain changes during pauses, and raised background noise. It cannot reconstruct a word already removed. |
| Beamforming | Combines microphone-array channels to favor a direction. | Geometry, channel synchronization, speaker position, and reflections. Preserve array channels until this operation finishes. |
| Dereverberation | Reduces room reflections and lingering speech energy. | Lost consonants, altered tails, and added processing delay. |
| Speaker isolation | Emphasizes a selected or primary speaker while suppressing other voices. | Intended multi-speaker conversations and diarization. Isolation is not identity verification. |

The [Microsoft Audio Stack DSP reference](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/audio-processing-speech-sdk) documents beamforming, dereverberation, AEC, AGC, and suppression as separate enhancements. Its supported pipeline needs microphone geometry and a loopback/reference channel for AEC. These requirements are specific to that stack.

## Put processing where its inputs exist

A browser or native capture SDK can see device input and playback. An agent server typically receives encoded or decoded capture after device processing. A phone endpoint may already apply undocumented processing before the carrier delivers media. Treat those upstream effects as unknown until measured or documented.

```mermaid
flowchart LR
    M[Microphone] --> C[Capture processing]
    C --> T[Encode and transport]
    T --> F[Decode and optional enhancement]
    F --> V[VAD and speech model]
    R[Device render PCM] --> S[Speaker]
    R -. AEC reference .-> C
    S -. Acoustic echo .-> M
```

Capture processing can include AEC, suppression, and AGC, depending on the device. The server enhancement is optional, and its input is already capture-processed when those features are enabled. The AEC reference belongs to the rendering endpoint; the arrow does not imply that a remote server automatically receives it.

```mermaid
flowchart LR
    P[Phone capture and endpoint processing] --> N[Carrier codec and media transport]
    N --> D[Server decode]
    D --> E[Optional speech enhancement]
    E --> V[VAD and speech model]
```

For a phone call, investigate echo at the caller's endpoint and the actual carrier/media path. The agent's generated TTS file alone lacks the caller's playback timing, speaker behavior, and capture clock. A noise filter on received media cannot substitute for a working endpoint echo-reference path.

In browsers, request appropriate `echoCancellation`, `noiseSuppression`, and `autoGainControl` constraints, then inspect support and the track's actual `getSettings()`. A simple boolean is a preference; an `exact` constraint can reject the request if it cannot be satisfied. Returned settings describe configuration, not measured cancellation quality. Device changes require another inspection. See [MDN capture constraints](https://developer.mozilla.org/en-US/docs/Web/API/Media_Capture_and_Streams_API/Constraints) and [echo cancellation](https://developer.mozilla.org/en-US/docs/Web/API/MediaTrackConstraints/echoCancellation).

## Keep the echo reference aligned during double-talk

In reference-based AEC, feed the playback/render stream through the supported reference API while processing microphone capture. Check delay, clock drift, dropped reference frames, and changes in output routing. Clipping and nonlinear speaker behavior complicate the relationship between digital playback and captured echo. The current [WebRTC APM interface](https://webrtc.googlesource.com/src/+/refs/heads/main/api/audio/audio_processing.h) distinguishes capture `ProcessStream()` from render `ProcessReverseStream()`.

Exercise far-end-only playback, near-end-only speech, and double-talk: the user says “wait, change that” while the agent is speaking. A quiet output during double-talk can mean the user's interruption was suppressed. Test moving the device, changing volume, switching to Bluetooth, and reconnecting. A headset comparison helps isolate the acoustic path; it does not prove every remaining fault is AEC.

Avoid muting microphone input for the entire agent utterance when interruption is a product requirement. That prevents the system from observing genuine barge-in. Route an identified echo problem to its processing owner before raising VAD thresholds.

## Preserve the format contract

Record codec, container/raw format, rate, channel order, sample width, byte order, numeric scale, frame size, and timestamps at each boundary. Decode compressed audio before passing samples to a PCM processor. Downmix only after an array-dependent operation. Convert a reference channel separately; do not average it into user speech.

RNNoise's example consumes raw mono 16-bit PCM at 48 kHz. Its C API accepts float buffers, and the demo converts integer-valued PCM directly to floats. Confirm numeric scale when adapting normalized browser samples. Obtain frame size through `rnnoise_get_frame_size()` instead of assuming an arbitrary WebSocket chunk is one processing frame. [RNNoise README](https://gitlab.xiph.org/xiph/rnnoise/-/blob/main/README), [API](https://gitlab.xiph.org/xiph/rnnoise/-/blob/main/include/rnnoise.h), and [demo](https://gitlab.xiph.org/xiph/rnnoise/-/blob/main/examples/rnnoise_demo.c).

Use a stateful resampler and preserve continuous timestamps across chunks. Relabeling 24 kHz samples as 48 kHz changes their interpreted duration. Upsampling narrowband phone audio does not recover missing frequencies. Count processing lookahead, frame accumulation, resampling, and queue delay separately; offline trimming of output cannot remove live algorithmic delay.

## Compare deployment choices

| Choice | Suitable ownership boundary | Deployment and license limits |
| --- | --- | --- |
| Browser/WebRTC APM | Device capture and render, including echo | Browser behavior varies. Standalone upstream WebRTC code has [BSD-3-Clause terms](https://webrtc.googlesource.com/src/+/refs/heads/main/LICENSE); dependency and packaged-browser terms are separate. |
| RNNoise | Local microphone or decoded server input noise suppression | Portable C integration; 48 kHz example contract. Root [COPYING](https://gitlab.xiph.org/xiph/rnnoise/-/blob/main/COPYING) is BSD-3-Clause; retain file-level notices. Separately sourced models/training data need their own review. |
| DeepFilterNet | Local or server speech enhancement | [README](https://github.com/Rikorose/DeepFilterNet) describes 48 kHz full-band processing and a 48 kHz WAV CLI; a file helper is not a complete streaming adapter. Code is MIT OR Apache-2.0 under its [LICENSE](https://github.com/Rikorose/DeepFilterNet/blob/main/LICENSE). Pin the chosen model artifact and retain its applicable terms. |
| LiveKit enhanced processing | Frontend, agent input, or SIP trunk, as supported | Cloud provides the Krisp/ai-coustics route. The agent-side ai-coustics plugin also supports a self-hosted SFU with a separately supplied license key and direct ai-coustics billing. Commercial model terms remain separate from the framework license. |
| Provider speech processing | Provider input buffer or supported native SDK | Check exact API, language, platform, and service/SDK terms. The provider may expose no processed samples or internal quality metric. |

LiveKit's [current cancellation guide](https://docs.livekit.io/transport/media/noise-cancellation) names agent-side Krisp VIVA and VIVA telephony, exposed in Python as `krisp.voice_isolation()` and `krisp.voice_isolation_telephony()`. BVC remains a frontend model; SIP-trunk processing uses NC. Avoid stacked enhanced frontend/agent filters; standard capture suppression and separate AEC can remain enabled. Check client support by SDK. The [ai-coustics self-hosted section](https://docs.livekit.io/transport/media/noise-cancellation#self-hosted-auth) specifies direct authentication through `auth`; agent hosting location alone does not establish that configuration.

OpenAI's [Realtime reference](https://developers.openai.com/api/reference/resources/realtime) places input noise reduction before VAD and model processing. Its `near_field` and `far_field` profiles describe microphone use. Select against the current Realtime schema, not an older beta field layout. Azure MAS DSP is documented for C++, C#, and Java on Windows/Linux, with minimum 16 kHz input and integral multiples of 16 kHz for downsampling. Neither interface establishes a universal configuration for every platform.

## Diagnose a noisy call without hiding the user

Suppose a laptop agent interrupts itself when its speaker plays, a desk fan prolongs turns, and whispered corrections vanish after adding suppression. Preserve the same authorized capture and render fixture. Keep model, transcript prompts, output volume, and turn settings fixed.

First compare headphones with speaker playback. Inspect capture AEC configuration and render-reference availability. Next bypass only the added enhancement while retaining the known capture configuration. Compare whisper onsets and trailing consonants. Then test environmental suppression alone against the fan, without speaker isolation unless nearby speech is genuinely unwanted. Check clipping before adjusting gain.

Only after selecting the frontend, recalibrate VAD/EOT on its output. Changed signal energy can move speech-start and speech-end decisions. Threshold tuning cannot restore deleted words. For languages, accents, distant speakers, and quiet speech, measure subgroup results rather than asserting a universal benefit.

## Run a paired test that catches information loss

Replay the same authorized source through bypass and candidate processing, preserving unprocessed capture, render reference, processed output, configuration, timestamps, and ground-truth words. Store recordings privately with a retention policy. A browser/device AEC cannot be fully assessed by replaying microphone audio into a server filter; use synchronized endpoint capture/render or a controlled acoustic replay. “Unprocessed” is only accurate if earlier device effects are absent or recorded as a limitation.

Use fixtures for silence/noise, normal and quiet speech, fan/transients, competing talkers, reverberation, far-end-only echo, and double-talk. Include supported devices, codecs, languages, and distances. Do not normalize each output separately before checking gain or clipping, since that can conceal a processing failure.

| Evidence | Calculation or observation | Qualification |
| --- | --- | --- |
| Residual echo | Playback-correlated residual and energy in controlled far-end-only windows | Align signals and report the selected windows. Noise and nonlinear echo confound simple correlation. |
| Echo attenuation | `10 * log10(sum(input_echo^2) / sum(residual_echo^2))` in isolated echo windows | ERLE-style estimate, not a valid aggregate over double-talk or mixed speech/noise. Muting everything can score well while destroying speech. |
| Information loss | WER/CER and deletion errors, plus exact names, numbers, and correction words | Keep recognizer/version fixed; state normalization and language. Count hallucinations separately on no-speech windows. |
| Turn behavior | Missed/false starts, onset clipping, premature ends, false barge-ins, and end-detection delay | Compare the same labeled turns. Preserve genuine interruption recall alongside lower false-trigger counts. |
| Runtime | Added algorithmic delay, processing duration distribution, queue growth, and dropped frames | A mean real-time factor below one can still conceal stalls; measure on the deployment hardware. |

With aligned clean reference speech, signal distortion and intelligibility measures can supplement listening. Treat reference-free quality predictors as model estimates. The [AEC Challenge](https://www.microsoft.com/en-us/research/academic-program/acoustic-echo-cancellation-challenge-icassp-2023/) separates single-talk/double-talk and recognition outcomes; [AECMOS research](https://www.microsoft.com/en-us/research/?p=837829) evaluates echo and other degradation separately. Neither supplies a quality guarantee for a new deployment.

Choose the smallest processing configuration that improves the target failures while preserving required words and interruptions. Report cohort counts, regressions, unknown upstream processing, and measured delay. If speaker isolation removes another authorized participant, change the mode or conversation design before calling the test successful.
