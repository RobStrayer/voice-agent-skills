# Speech recognition and spoken output

[Handbook](../../../../docs/handbook.md) / [Speech pipeline skill](../SKILL.md)

Reviewed **2026-09-30 UTC** using Context7 and current primary documentation.
This is the review date; publication dates were not established for the living
pages cited below. Procedures and examples are engineering guidance.

## Pick the boundary to inspect

| Problem or job | Start here | Evidence to retain |
| --- | --- | --- |
| Wrong names, dates, or corrections | [Recognition selection](#choose-recognition-for-the-task) | Entity accuracy and input fixtures |
| Duplicated words or premature actions | [Transcript events](#treat-transcripts-as-an-event-stream) | Revisions, finals, and committed-turn IDs |
| Slow, distorted, or stale speech | [Spoken output](#design-the-spoken-output-path) | Phrase, format, and playback contract |
| Correct text sounds ambiguous | [Pronunciation](#test-the-words-that-change-the-task) | Intended spoken forms and final-transport audio |
| Replace a speech component | [Pipeline worksheet](#compare-complete-pipelines) | Comparable task outcomes and remaining unknowns |

The speech path connects an acoustic signal to an action and back to a listener.
Each boundary can introduce a different error. A correctly recognized date may
be parsed in the wrong locale; a correct answer may be synthesized with an
ambiguous pronunciation; generated audio may wait in a player queue.

## Choose recognition for the task

Collect representative input before selecting a model. Include the actual
microphone or telephone channel, noise conditions, accents and speaking styles,
code switching, long pauses, short corrections, and the names people will say.
Use consented or synthetic test material within the project's data policy.

| Requirement | Evidence to collect | Why a broad model score is insufficient |
| --- | --- | --- |
| Names, addresses, identifiers | Exact entity/value accuracy and repair dialogs | A small word error can change a destination or record. |
| Multilingual conversation | Results per language and code-switch condition | A model may support file transcription in a language but differ in live mode. |
| Low-volume or distant speech | Captured and processed audio, transcription, VAD events | Input processing may remove the syllable before STT receives it. |
| Fast corrections | Interim revisions, final segments, selected turn boundary | The first plausible transcript can be wrong. |
| Telephone audio | Actual negotiated format and channel-separated fixtures | Upsampling cannot recover information absent from the original signal. |
| Local inference | Warm/cold timing, real-time load, memory, sustained concurrency | Faster-than-real-time file throughput does not establish interactive behavior. |

For a native speech model, determine whether the transcript is its reasoning input,
an auxiliary transcription, or a later record. Do not assume that editing an
auxiliary transcript changes what the model already heard or acted on. Check the
specific session API before designing text review around it.

A basic word error rate is `(substitutions + deletions + insertions) / reference words`.

| Score | Qualification |
| --- | --- |
| Word error rate | Publish normalization and reference policy. Spelled-out amounts versus digits can create format-only errors. |
| Critical-entity accuracy | Check booking day, negation, quantity, account selector, and address. |
| Task outcome | Verify what the application actually did; neither transcript score alone establishes success. |

## Treat transcripts as an event stream

Transcript handling checklist:

- [ ] Separate provisional display text from committed segments.
- [ ] Replace revised hypotheses using API segment IDs or timing ranges; do not append every update.
- [ ] Preserve original events for diagnosis.
- [ ] Define reconnect, replay, and stream-offset handling.

Deepgram's current Nova streaming guide distinguishes `is_final`, which finalizes
a segment, from `speech_final`, which marks a detected speech endpoint. Accumulate
the final segments belonging to the utterance; keeping only the last endpoint
response can discard earlier words. An interim hypothesis can change. These flags
describe that API, not a universal event vocabulary.
[Endpointing and interim results](https://developers.deepgram.com/docs/understand-endpointing-interim-results).

Flux has a different conversational event model. Its migration guide separates
Nova's transcript stream from Flux's structured turn events. Verify the endpoint,
SDK adapter, and event handling together during a migration; changing a model name
alone is not a complete conversion.
[Nova-to-Flux migration](https://developers.deepgram.com/docs/flux/nova-3-migration).

| Boundary | Safe use | Failure to watch for |
| --- | --- | --- |
| Interim hypothesis | Live captions or reversible preparation | A provisional entity becomes a committed action. |
| Final segment | Stable contribution to the current transcript | Segment finalization is mistaken for completed intent. |
| Turn decision | Decide when to respond under the active policy | A mid-thought pause causes an answer or write too early. |
| Parsed action | Validate values against task state and policy | A correctly transcribed correction is ignored. |

For speculative work, separate preparation from commitment. A reversible lookup
can sometimes start before the turn settles; an external write needs validated
intent and whatever authorization the task requires. Tag work with the input
version that produced it so a corrected day or address invalidates stale results.

### Synthetic trace: a corrected day

This is a reasoning example, not a provider event recording:

| Event | Application interpretation |
| --- | --- |
| Interim text: "book it Thursday" | Display provisionally; no committed booking. |
| Final segment: "book it Thursday" | Retain stable text, continue collecting the turn. |
| Caller continues: "actually Friday" | Preserve the correction; invalidate Thursday preparation. |
| Turn accepted | Resolve the requested day to Friday, validate against task state. |
| Booking succeeds | Record the authoritative result, then speak confirmation. |

If a write already committed before the correction, use the business service's
change/cancellation workflow. Replacing transcript text does not change a booking.

## Design the spoken output path

| Text arrival | Interface to consider | Check |
| --- | --- | --- |
| Complete response already available | Streaming HTTP output may suffice | Decoder and playback buffering |
| Text arrives incrementally | Input interface that accepts text during synthesis | Streaming text input is separate from streaming audio output |

Record who forms phrases. Token-by-token input can wait for context
or sound awkward; whole-answer buffering can delay useful speech.

1. Start with the provider's documented behavior.
2. Compare phrase policies with identical answers and playback paths.
3. Flush or otherwise handle the final short phrase so it cannot wait indefinitely.

ElevenLabs' TTS WebSocket guide documents text buffering, chunk schedules, and
`flush` for pending text. Its API reference recommends `auto_mode` for full
sentences and warns about quality with partial sentences. Treat that parameter
as a mode choice with an input contract, not a universal latency switch. The
guide places pronunciation dictionaries in connection initialization.
[WebSocket guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/websockets/realtime-tts),
[API reference](https://elevenlabs.io/docs/api-reference/text-to-speech/v-1-text-to-speech-voice-id-stream-input).

Record where text, generated audio, and playable audio wait. A small first chunk
does little for the listener if the application buffers the response, the decoder
needs more bytes, or the browser rejects playback. Bind each chunk to its response
generation. On interruption, reject obsolete chunks and apply the player or
carrier's queue-clearing contract before new speech is admitted.

| Output contract | Record |
| --- | --- |
| Format | Actual codec, rate, channels, sample representation, and framing |
| Conversion | Owner of decoding/conversion and location of resampling |
| Queues | Phrase buffering, flush, backpressure, and limits |
| Interruption | Generation cancellation, produced audio, and player queue behavior |
| Completion | Playback evidence and history reconciliation |

Keep compressed bytes out of a raw PCM player. Do not add a WAV header to a raw
audio message unless the receiving interface explicitly expects that container.
Inspect actual data and the negotiated contract when the sound is distorted.

## Test the words that change the task

### Check model and text-transform changes before migrating

Reviewed September 30, 2026. These changes have different ownership boundaries:

| Source and publication | Integration consequence | Regression case |
| --- | --- | --- |
| [AssemblyAI Universal-3.6 Pro Realtime](https://www.assemblyai.com/blog/universal-3-6-pro-realtime), September 29 | Select `universal-3-6-pro` on the streaming connection. 3.5 Pro Realtime remains available. | Compare short yes/no answers, identifiers, and turn boundaries on the same audio. Provider benchmarks do not establish your task's accuracy. |
| [ElevenLabs v4 announcement](https://elevenlabs.io/docs/changelog), September 28 | `eleven_v4_turbo` uses the Text to Dialogue WebSocket. Adopt its message and voice-registration contract. | Test a short phrase, final flush, interruption, and reconnect with the chosen output format. |
| [Pipecat 1.12.0](https://github.com/pipecat-ai/pipecat/releases/tag/v1.12.0), September 26 | `TTSService.pronunciation_transform_ipa()` produces service-specific markup. Put it last in `text_transforms`. Unsupported hints fall back to the original spelling. | Place a normalizer before the pronunciation transform; confirm the resulting hint survives and is supported by the selected service/model. |

The [ElevenLabs dialogue protocol](https://elevenlabs.io/docs/eleven-api/guides/how-to/websockets/realtime-tdd)
registers exactly one voice for v4 Turbo and accepts `inputs` frames. It uses a
different buffering contract from the ordinary TTS WebSocket; use `flush` for a
short pending phrase. The [v4 model guide](https://elevenlabs.io/docs/overview/capabilities/text-to-speech/eleven-v4)
also documents changed cross-language accent behavior and no SSML support.
An old pronunciation or TTS connection example needs review before changing its
model identifier. Pipecat's transform behavior was confirmed in
[the 1.12.0 source](https://github.com/pipecat-ai/pipecat/blob/v1.12.0/src/pipecat/services/tts_service.py).

### Build a pronunciation fixture set

Create a small pronunciation fixture set from the domain: product names, people,
street names, abbreviations, dates, amounts, and identifiers. Include words whose
meaning changes with stress or a nearby negation. Record the intended spoken form
and listen with the chosen voice, model, language, and final transport.

Keep a canonical value and a spoken rendering separately. For example, a business
service can retain an ISO date while the agent says an unambiguous localized date.
Do not mutate authoritative values merely to make TTS read them naturally.

Check normalization on and off before adopting a manual substitution that might break
another language or a different occurrence of the same string.

Before diagnosing a dictionary failure, verify:

- Model support for the dictionary or phoneme markup.
- Dictionary version and initialization timing.
- Whether the integration forwards the option in the request.

A dictionary merely present in the provider account cannot explain output if it
was never included in the request.

For multilingual work, compare intelligibility, entity pronunciation, and repair
burden per language. Language labels, accent labels, and voice availability are
different claims. Include callers who pause, speak quietly, stutter, or need more
time to formulate a response. A faster endpoint policy that repeatedly cuts those
callers off has not improved the conversation.

## Compare complete pipelines

Hold input material, task, accepted voice identity, and scoring rules constant.
Compare the old and new processing paths before changing several components at
once. Keep synthetic fixtures separate from observed customer behavior.

| Record | Candidate A | Candidate B |
| --- | --- | --- |
| STT model/version, language and mode | | |
| Input processing and media format | | |
| Transcript/turn event contract | | |
| Critical-entity errors and repair turns | | |
| TTS model/voice, normalization, dictionaries | | |
| Input buffering and output player settings | | |
| First useful audible response and measurement boundary | | |
| False cutoffs, stale speech, missing playback evidence | | |
| Completed tasks and incorrect actions | | |
| Cost units, authorized test volume, remaining unknowns | | |

When a sample fails, retain enough authorized evidence to identify the first bad
boundary. Repeat that fixture after the correction. Measure long answers and
interrupted answers as well as a short greeting; a greeting alone exercises few
of the streaming and state-handling risks.

## Current source limitations

Context7 used `/websites/developers_deepgram` and
`/elevenlabs/elevenlabs-python`. The primary pages above were retrieved directly.
Generated SDK summaries are useful discovery aids, but their transport claims
were not treated as proof of automatic HTTP/WebSocket selection. Check the exact
installed SDK implementation for that behavior.

No provider requests, acoustic tests, model downloads, or comparative performance
measurements were run to write this guide.
