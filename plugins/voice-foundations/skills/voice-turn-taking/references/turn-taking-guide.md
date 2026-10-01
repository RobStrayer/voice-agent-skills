# Turn taking: deciding when to listen, speak, and yield

[Handbook](https://github.com/RobStrayer/voice-agent-skills/blob/main/docs/handbook.md) / [Turn-taking skill](../SKILL.md)

Reviewed against current primary sources on **2026-09-30 UTC**. Provider facts below describe the cited integration; design rules and the worked timeline are engineering recommendations. Synthetic times illustrate ordering and are not benchmarks.

## Contents

- Find the decision you need
- Separate the detectors
- Keep a turn controller
- Decide which overlap should interrupt
  - Stop each kind of work explicitly
- Worked example: a correction during booking
- Tune for the cost of the error
- Recover from an interruption with no transcript
- Instrument and exercise the boundaries
- Choose an integration you can observe

## Find the decision you need

| Problem | Start here | Required result |
| --- | --- | --- |
| Caller is cut off during a pause | [Detector boundaries](#separate-the-detectors) | Distinguish silence from completed intent |
| Duplicate replies or stacked waits | [One turn controller](#keep-a-turn-controller) | One owner commits turns and releases responses |
| Echo, backchannels, or corrections interrupt speech | [Interruption eligibility](#decide-which-overlap-should-interrupt) | A policy that preserves short genuine corrections |
| Old audio or pending tools survive interruption | [Cancellation boundaries](#stop-each-kind-of-work-explicitly) and [booking example](#worked-example-a-correction-during-booking) | Stop output while retaining action truth |
| Choose or tune a detector | [Error costs](#tune-for-the-cost-of-the-error) and [integration choices](#choose-an-integration-you-can-observe) | Cohort-specific evidence, not a universal threshold |

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

Keep streaming transcript uses separate:

| Use | Handling |
| --- | --- |
| Interim display | Preserve segment IDs, revision order, timestamps, and finality under the STT contract |
| Speculative retrieval | Start early only if stale work can be discarded safely |
| Irreversible tool | Require validated intent and the workflow's confirmation |

A mutable partial such as "Tuesday" must not authorize a booking that becomes "Thursday" in the final turn.

Preserve pauses after unfinished phrases, spelled identifiers, numbers, self-corrections, and "let me think." Test the actual languages, accents, code switching, and speaking styles. An EOT model's language list is not evidence for every mixed-language conversation. Missing transcription can reflect a recognizer failure, not a caller who said nothing.

## Keep a turn controller

Give one component authority to commit user turns and release assistant responses. Other detectors supply evidence. Two independent committers can produce duplicate replies or stack their waits.

![State diagram of one turn controller: Listening, CandidateEnd, Responding and Yielding, with the transitions between them. A separate action ledger keeps tool actions independent of these states.](../assets/turn-controller.svg)

[Editable diagram](../assets/turn-controller.svg). One controller owns turn commitment; tool actions keep an independent lifetime.

| State | Responsibility |
| --- | --- |
| Listening | Capture input, including while work is pending |
| CandidateEnd | Hold a possible boundary while EOT and required transcript evidence arrive |
| Responding | Generate and play output; these can overlap |
| Yielding | Invalidate the old response and stop its output |

Business actions remain in a separate ledger and can be pending in any state.

Use stable session, user-turn, response, and tool-operation IDs. A new speech segment that arrives before commitment returns the controller to Listening. If it arrives after speculative generation began, invalidate that generation before exposing its audio. The policy should state how a detector timeout or lost STT stream changes the decision, including when to request clarification.

## Decide which overlap should interrupt

"Uh-huh" during an explanation may mean "continue." "No" after a confirmation question may be the entire answer. Duration or word-count filters alone cannot resolve that distinction.

Before changing interruption filters:

- Check current assistant speech, caller timing, acoustic evidence, available text, and task.
- Keep short corrections and stop requests eligible.
- Test quiet speakers and a one-word "no" when raising duration or word-count minima.
- Keep listening during acknowledgements; filler must not mask the caller's next words.

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

1. Start with the integration's supported defaults.
2. Change one family: VAD sensitivity, onset duration, endpoint wait, EOT threshold, or interruption policy.
3. Assign error costs with the owner and compare errors against delay.
4. Validate the selected configuration on held-out conversations, including failures and quiet speakers.

Model scores need their own calibration; thresholds do not transfer between detectors.

| Measure | Keep explicit |
| --- | --- |
| Early commits | Errors per user turn |
| False accepted interruptions | Errors per overlap candidate |
| Missed intentional interruptions | Desired interruption labels and recall |
| Endpoint-to-first-played audio; overlap after stop | Distribution and clock boundaries |
| Extra clarification turns; duplicate external actions | Task consequences |
| Every measure | Language/device cohorts, sample size, and denominator |

An address correction cut off early may cost more than waiting through a pause. A long wait after "stop" may cost more than a brief false interruption. Use those task costs when choosing a configuration.

## Recover from an interruption with no transcript

Pipecat 1.12.0 (published September 26, reviewed September 30, 2026) enables
`LLMUserAggregatorParams.empty_user_turn` by default. When an empty user turn cuts
the bot off, the aggregator adds a developer message and runs the LLM to recover.
An empty turn while the bot is idle stays unanswered unless `idle_prompt` is set.
`max_consecutive_recoveries` defaults to one. Set `interrupted_prompt=None` to
disable interrupted recovery, or `empty_user_turn=None` to disable both cases.
This configuration is ignored for realtime LLM services that hear audio directly.
[Release](https://github.com/pipecat-ai/pipecat/releases/tag/v1.12.0),
[aggregator contract](https://github.com/pipecat-ai/pipecat/blob/v1.12.0/src/pipecat/processors/aggregators/llm_response_universal.py),
[recovery configuration](https://github.com/pipecat-ai/pipecat/blob/v1.12.0/src/pipecat/turns/empty_user_turn.py).

Test a cough during speech, a cough while idle, and quiet speech that STT misses.
Assert whether recovery is expected, that its repetition is bounded, and that an
empty transcript cannot authorize a write. Record this default during an upgrade:
an added recovery reply can change behavior even when application code is unchanged.

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

| Option | Input and version requirements |
| --- | --- |
| LiveKit audio turn detector | Python Agents 1.6.1+ or Node 1.4.7+, VAD, and minimum VAD silence duration of at least 250 ms; no transcript required |
| LiveKit text turn detector | Transcript-driven, open weights; deprecated for future SDK removal |
| Pipecat Smart Turn | Current v3.2: 16 kHz mono, up to eight seconds of context, evaluation after VAD silence |
| Silero VAD | 8/16 kHz probabilities; current direct ONNX wrapper uses 256/512-sample chunks respectively |
| Provider-native detection | Selected session/model's controls and event contract |

| Option | Deployment and policy work |
| --- | --- |
| LiveKit audio | Full v1 on LiveKit Inference; v1-mini local. Observe fallback and language thresholds. |
| LiveKit text | Preserve legacy STT timing/language coverage; audio and text configurations are different integrations. |
| Smart Turn | Re-evaluate after resumed speech; check the installed analyzer's model artifact. Pipeline commitment may also wait for STT. |
| Silero | Buffer/resample correctly, isolate state per stream, and supply completion/interruption policy. |
| Provider-native | Fewer application detectors; confirm client/server ownership, transcription, cancellation, and buffering. Avoid a second response trigger. |

Sources: [LiveKit audio and text models](https://docs.livekit.io/agents/logic/turns/turn-detector/), [Smart Turn model](https://github.com/pipecat-ai/smart-turn), [Pipecat turn strategies](https://docs.pipecat.ai/api-reference/server/utilities/turn-management/user-turn-strategies), [Silero source and input checks](https://github.com/snakers4/silero-vad/blob/master/src/silero_vad/utils_vad.py).

LiveKit adaptive interruption is a separate Cloud feature with its own SDK and transcript-alignment requirements, or a supported realtime model under client turn control. EOT accuracy does not establish interruption accuracy. [Adaptive interruption requirements](https://docs.livekit.io/agents/logic/turns/adaptive-interruption-handling/).

Choose using the installed SDK, observed language/audio path, deployment capacity, and the labeled failure costs. Recheck current sources through Context7 and their originals before copying settings. The review did not execute these SDKs or reproduce vendor accuracy and latency claims.
