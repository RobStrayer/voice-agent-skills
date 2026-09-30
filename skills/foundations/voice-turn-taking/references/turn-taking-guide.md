# Turn taking: deciding when to listen, speak, and yield

Reviewed against current primary sources on **2026-09-30 UTC**. Provider facts below describe the cited integration; design rules and the worked timeline are engineering recommendations. Synthetic times illustrate ordering and are not benchmarks.

[Detection](#separate-the-detectors) · [Turn state](#keep-a-turn-controller) · [Interruptions](#decide-which-overlap-should-interrupt) · [Worked example](#worked-example-a-correction-during-booking) · [Tuning](#tune-for-the-cost-of-the-error) · [Integration](#choose-an-integration-you-can-observe)

## Separate the detectors

A caller says, "Send it to Alex... actually, to Alexis." The system must preserve the correction through a pause, assemble the right words, and decide when a reply is welcome.

| Signal | What it establishes | What still needs a decision |
| --- | --- | --- |
| Voice activity detection (VAD) | Likely speech versus non-speech in an audio window | Whether the caller finished, or intends to interrupt |
| Silence endpointing | A configured period without detected speech | Whether that pause is hesitation, a breath, or the end |
| Semantic or acoustic end-of-turn (EOT) | A model's estimate of conversational completion | Its language coverage, errors, timeout, and fallback |
| STT final segment | The recognizer finalized that segment under its contract | Whether more segments belong to the same user turn |
| Accepted interruption | Application policy yields the floor to incoming speech | How generation, playback, history, and actions stop |

OpenAI distinguishes silence-based server VAD from semantic VAD, whose timeout adapts to estimated completion. Its create_response and interrupt_response controls apply to speech-to-speech conversations; transcription sessions use turn detection for audio chunking. Some transcription models require explicit commits instead. Check the selected session and model. [Realtime VAD](https://developers.openai.com/api/docs/guides/realtime-vad).

Treat streaming hypotheses as revisions. Record segment IDs, revision order, timestamps, and finality according to the STT's contract. A UI can show interim text, and speculative retrieval can start early if discarded safely. A mutable partial such as "Tuesday" must not authorize a booking that becomes "Thursday" in the final turn. An irreversible tool needs validated intent and the workflow's required confirmation.

Preserve pauses after unfinished phrases, spelled identifiers, numbers, self-corrections, and "let me think." Test the actual languages, accents, code switching, and speaking styles. An EOT model's language list is not evidence for every mixed-language conversation. Missing transcription can reflect a recognizer failure, not a caller who said nothing.

## Keep a turn controller

Give one component authority to commit user turns and release assistant responses. Other detectors supply evidence. Two independent committers can produce duplicate replies or stack their waits.

![One controller owns turn commitment; tool actions keep an independent lifetime.](../assets/turn-controller.svg)

[Editable diagram](../assets/turn-controller.html). One controller owns turn commitment; tool actions keep an independent lifetime.

Listening includes capture while work is pending. CandidateEnd holds a possible boundary while EOT and required transcript evidence arrive. Responding includes generation and output, which can overlap. Yielding invalidates the old response and stops its output. Business actions live in a separate ledger and can remain pending in any of these states.

Use stable session, user-turn, response, and tool-operation IDs. A new speech segment that arrives before commitment returns the controller to Listening. If it arrives after speculative generation began, invalidate that generation before exposing its audio. The policy should state how a detector timeout or lost STT stream changes the decision, including when to request clarification.

## Decide which overlap should interrupt

"Uh-huh" during an explanation may mean "continue." "No" after a confirmation question may be the entire answer. Duration or word-count filters alone cannot resolve that distinction.

Consider the assistant's current speech, caller timing, acoustic evidence, available text, and task. Keep short corrections and stop requests eligible. Test quiet speakers and a one-word "no" when raising a minimum duration or word count. Agent acknowledgements can also seize the floor accidentally: keep listening and prevent a filler response from masking the caller's next words.

Separate permission to interrupt output from permission to change an action. A caller can be heard during a transaction even when its external API cannot cancel. If a bounded announcement must finish, specify whether overlapping input is buffered, transcribed, or dropped. Do not disable input silently to make a metric look better.

False interruption recovery requires evidence that the original response is still appropriate. A cough may justify resuming; an empty STT result after a real correction needs investigation. Avoid replaying an introduction, repeating a completed action, or resuming speech whose output queue was already cleared. LiveKit exposes false-interruption recovery controls; its timeout units differ between Python and Node.js. [Interruption handling](https://docs.livekit.io/agents/logic/turns/).

### Stop each kind of work explicitly

| Boundary | Required behavior |
| --- | --- |
| Generation | Cancel obsolete LLM/TTS work where supported; reject late output by response ID |
| Playback | Clear queued old speech and stop active/scheduled audio; record the transport result |
| Conversation history | Retain the spoken portion supported by playback evidence; qualify unknown alignment |
| Tool execution | Track whether work was dispatched, cancelled, committed, failed, or remains unknown |

Cancellation of a coroutine cannot roll back an external booking. Reconcile the operation using an API-supported idempotency key or an application operation ledger before retrying. Keep an eventual tool result even when its original spoken response was interrupted.

Pipecat documents interruption propagation, cancellation of interruptible work, and transport queue flushing. Tool cancellation is separately configurable. A custom processor or remote playback buffer still needs verification at its boundary. [Pipecat interruptions](https://docs.pipecat.ai/pipecat/fundamentals/interruptions), [function calling](https://docs.pipecat.ai/pipecat/learn/function-calling).

OpenAI's WebSocket client owns playback tracking and truncation of unplayed assistant content. WebRTC/SIP manages that output buffer on the server. Generation completion is not playback completion, and a server acknowledgement does not prove sound reached the caller's ear. [Interruption and truncation](https://developers.openai.com/api/docs/guides/realtime-conversations#interruption-and-truncation).

## Worked example: a correction during booking

Assume the caller already authorized a Tuesday booking. The booking API provides an operation-status lookup but cannot reliably cancel after dispatch. These times share a synthetic controller clock; deployed systems need clock mapping or causal event order.

| Time | Event | Controller consequence |
| --- | --- | --- |
| 0 ms | Tuesday turn committed; operation B7 dispatched | Mark B7 pending, not booked |
| 250 ms | Response R4 begins: "Working on Tuesday..." | Track actual playback separately from generated text |
| 800 ms | Caller says "Thursday instead" | Preserve audio; evaluate interruption eligibility |
| 900 ms | Correction accepted | Invalidate R4; request generation cancellation and playback stop |
| 1,100 ms | Output reports stop at its played offset | Repair R4 history using that evidence |
| 1,200 ms | Late R4 audio arrives | Drop it; do not place it in the new response's queue |
| 1,450 ms | Corrected turn finalized | Record Thursday intent; B7 remains unresolved |
| 1,900 ms | B7 reports Tuesday committed | Explain the actual result and follow the authorized change/cancel workflow |

~~~mermaid
sequenceDiagram
    participant C as Caller
    participant S as Turn controller
    participant P as Playback
    participant T as Booking API
    S->>T: Dispatch authorized B7
    S->>P: Play R4
    C->>S: Thursday instead
    S->>S: Accept correction, invalidate R4
    S->>P: Stop and clear R4
    P-->>S: Played offset and stop result
    S->>S: Repair history, retain B7 pending
    T-->>S: B7 committed Tuesday
    S-->>C: Report result, follow change workflow
~~~

The caller gets the floor while action reconciliation continues. No Thursday booking is dispatched merely because Tuesday's speech stopped. A new response may acknowledge the correction before B7 settles, provided it does not imply cancellation succeeded.

## Tune for the cost of the error

Label a replay corpus with completed turns, hesitation, desired interruptions, backchannels, and unacceptable speech overlap. Include disagreements between annotators instead of forcing ambiguous examples into certain labels.

Start with the integration's supported defaults. Change one control family at a time: VAD sensitivity, onset duration, endpoint wait, EOT threshold, or interruption policy. Model scores need their own calibration; a threshold from another detector has no transferable meaning.

Track early turn commits per user turn, false accepted interruptions per overlap candidate, missed intentional interruptions, and endpoint-to-first-played-audio distributions. Also measure overlap after a requested stop, extra clarification turns, and duplicate external actions. Keep denominators, language/device cohorts, sample sizes, and clock boundaries explicit.

Assign error costs with the product owner. Cutting off an address correction may be more costly than waiting through a pause. A long wait after "stop" may be more costly than a brief false interruption. Choose a configuration from the tradeoff between errors and delay, then validate it on held-out conversations. Do not optimize average latency by excluding failures or quiet speakers.

## Instrument and exercise the boundaries

Log capture speech boundaries, STT revisions/finals, EOT decisions/timeouts, user-turn commits, interruption candidates/decisions, generation cancellation, output queue depth, played offsets, history edits, and tool state transitions. Record model/SDK versions and active fallback. Missing events remain unknown.

| Test condition | Assertion |
| --- | --- |
| Hesitation, long number, self-correction | No premature action; resumed speech remains in the same intended turn |
| "Uh-huh," then a genuine correction | Backchannel does not hide the later correction |
| Quiet "no," multiple languages, code switching | Short answers survive filters; unsupported cases have a defined fallback |
| Cough, background voice, speaker echo | Measure false yields and recovery; distinguish echo from intended speech |
| Slow/failing STT or EOT inference | Timeout behavior is bounded and visible; no duplicate committed turn |
| Late audio, remote output buffering | Old response cannot resume after a stop or overwrite new playback |
| Tool commit during barge-in | One operation, honest result, reconciliation before retry |

Replay tests diagnose detector behavior. Also test the authorized browser or telephone path with realistic buffering: a correct EOT label cannot demonstrate prompt playback stopping.

## Choose an integration you can observe

| Option | Concrete requirements and tradeoff |
| --- | --- |
| LiveKit audio turn detector | Current docs require Python Agents 1.6.1+ or Node 1.4.7+, VAD, and a VAD minimum silence duration of at least 250 ms. Full v1 runs on LiveKit Inference; v1-mini runs locally. It does not require a transcript. Observe model fallback and language thresholds. |
| LiveKit text turn detector | Transcript-driven, open weights, and deprecated for future SDK removal. Keep legacy STT timing and language coverage explicit. New audio and old text configurations are different integrations. |
| Pipecat Smart Turn | Current v3.2 source consumes 16 kHz mono audio with up to eight seconds of context, evaluated after VAD detects silence. Re-evaluate when speech resumes. Check the model artifact bundled by the installed analyzer. Pipeline strategies may additionally wait for STT; audio inference and turn commitment are separate boundaries. |
| Silero VAD plus endpoint policy | Speech probabilities at 8/16 kHz; direct current ONNX wrapper uses 256/512-sample chunks respectively. Buffer/resample correctly and isolate state per stream. You supply conversational completion and interruption policy. |
| Provider-native turn detection | Fewer application detectors, but provider-specific controls and events. Confirm client versus server ownership, transcription constraints, cancellation, and output buffering. Avoid a second automatic response trigger. |

Sources: [LiveKit audio and text models](https://docs.livekit.io/agents/logic/turns/turn-detector/), [Smart Turn model](https://github.com/pipecat-ai/smart-turn), [Pipecat turn strategies](https://docs.pipecat.ai/api-reference/server/utilities/turn-management/user-turn-strategies), [Silero source and input checks](https://github.com/snakers4/silero-vad/blob/master/src/silero_vad/utils_vad.py).

LiveKit adaptive interruption is a separate Cloud feature with its own SDK and transcript-alignment requirements, or a supported realtime model under client turn control. EOT accuracy does not establish interruption accuracy. [Adaptive interruption requirements](https://docs.livekit.io/agents/logic/turns/adaptive-interruption-handling/).

Choose using the installed SDK, observed language/audio path, deployment capacity, and the labeled failure costs. Recheck current sources through Context7 and their originals before copying settings. The review did not execute these SDKs or reproduce vendor accuracy and latency claims.
