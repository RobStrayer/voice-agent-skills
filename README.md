<div align="center">

# NL Voice Skills

### Next Level Voice Skills

**Build voice agents that listen well, act correctly, and recover gracefully.**

An engineering handbook and a curated collection of skills for the agents that build voice agents.

![Original foundations: 9](https://img.shields.io/badge/original_foundations-9-0f766e?style=flat-square)
![Bundled skills: 36](https://img.shields.io/badge/bundled_skills-36-475569?style=flat-square)
![Original material: MIT](https://img.shields.io/badge/original_material-MIT-475569?style=flat-square)

[Engineering handbook](#engineering-handbook) · [Skills and providers](#skills-and-providers) · [Installation](#get-started) · [Resource library](docs/resources.md)

</div>

---

A voice agent can understand every word and still be difficult to talk to. It may
interrupt a hesitant caller, hear its own speaker, announce an unconfirmed booking,
or lose the conversation during a transfer. Those problems cross model, media,
application, and telephone boundaries. This collection gives each one room.

Use the handbook to understand a design or failure. Use the corresponding skill
to guide a coding agent through the work. Provider skills link to the people who
maintain them, with dated copies available when you need to inspect a snapshot.

**Reviewed September 30, 2026 (UTC).** Dates record source review, not a promise that
every SDK or model has been tested. [Documentation checks](docs/documentation-review.md)
identify current-source conflicts and Context7 limitations.

## Engineering handbook

| Work area | The question it answers | Start with |
| --- | --- | --- |
| [Architecture](#architecture) | Which responsibilities should each component own? | [Decision guide](skills/foundations/voice-stack-selection/references/architecture-guide.md) |
| [Turn taking](#turn-taking-and-interruptions) | Has the caller finished, and should the agent yield? | [Turn control guide](skills/foundations/voice-turn-taking/references/turn-taking-guide.md) |
| [Noise and echo](#noise-echo-and-the-audio-frontend) | Is the input preserving the person we need to hear? | [Audio frontend guide](skills/foundations/voice-audio-frontends/references/audio-frontends-guide.md) |
| [Recognition](#speech-recognition) | Which words and fields are reliable enough to use? | [Speech pipeline guide](skills/foundations/voice-speech-pipeline/references/speech-pipeline-guide.md) |
| [Synthesis](#speech-synthesis-and-playback) | What will the caller actually hear, and when? | [Speech output guide](skills/foundations/voice-speech-pipeline/references/speech-pipeline-guide.md) |
| [Conversation](#conversation-and-accessibility) | Can the caller follow, correct, and complete the task? | [Conversation skill](skills/foundations/voice-conversation-design/SKILL.md) |
| [Tools and handoffs](#tools-transactions-and-handoffs) | What happened after an interrupted or uncertain action? | [Transaction guide](skills/foundations/voice-conversation-design/references/transactions-and-handoffs.md) |
| [Telephony](#telephony-and-call-control) | Who owns the call, its media, and its next destination? | [Telephony guide](skills/foundations/voice-call-reliability/references/telephony-guide.md) |
| [Production](#production-operations) | Can sessions start, continue, and end reliably under load? | [Operations guide](skills/foundations/voice-call-reliability/references/production-operations-guide.md) |
| [Latency](#latency-and-media-debugging) | Where did time go on the caller's actual path? | [Latency audit](skills/foundations/voice-latency-audit/SKILL.md) |
| [Evaluation](#evaluation-and-release-decisions) | What evidence would justify shipping this change? | [Evaluation skill](skills/foundations/voice-agent-evaluation/SKILL.md) |

### Architecture

![Conceptual voice architecture: capture, transport, runtime, and playback form the audio path, while call control and durable business actions keep separate state.](skills/foundations/voice-stack-selection/assets/voice-system-map.svg)

Choose a design by working through a difficult conversation, not just a clean
demo. Include a correction during a write, quiet speech, a failed destination,
and a burst of new sessions. Write down who owns the media stream, turn decision,
tool ledger, playback queue, and recovery for each candidate.

| Design choice | Why it matters | Evidence to collect |
| --- | --- | --- |
| Native realtime speech or STT → LLM → TTS | Changes text checkpoints, model interchangeability, speech control, and observability. An auxiliary transcript may differ from what a speech model used. | Same tasks and audio path, interruption recovery, field accuracy, delivered speech, and tool outcomes. |
| Managed platform or application-owned orchestration | Responsibility for sessions, routing, retries, tracing, and upgrades has to live somewhere. | Failure behavior, available logs, supported control surfaces, and the operating work each option requires. |
| Browser, mobile, or telephone | Device processing, network traversal, media format, and call control differ by channel. | Negotiated formats, restrictive networks, speakerphone behavior, and end-to-end call state. |
| Cloud, local, or mixed inference | Region, concurrency, cold starts, hardware, model terms, and support can outweigh a component's demo quality. | Representative load and cost, regional availability, and failure handling. |

The [architecture guide](skills/foundations/voice-stack-selection/references/architecture-guide.md)
includes hybrid designs, migration boundaries, proof-of-concept scenarios, and a
decision record. Use [voice-stack-selection](skills/foundations/voice-stack-selection/SKILL.md)
to apply it to a project. End with a conditional choice and the evidence that
could overturn it.

### Turn taking and interruptions

![Turn controller showing listening, a candidate end of turn, responding, and yielding, with a separate action ledger.](skills/foundations/voice-turn-taking/assets/turn-controller.svg)

Voice activity detection asks whether speech is present. Endpointing and
end-of-turn prediction ask whether it is time to respond. Interruption handling
asks whether to stop an answer already in progress. Treat these as separate
decisions; a better detector cannot repair a playback queue that keeps speaking.

Design for hesitations, short acknowledgments, overlapping speech, corrections,
and a caller who speaks quietly. A fixed silence threshold trades one set of
mistakes for another. Measure premature and delayed replies separately, then
inspect the examples behind each count.

| Boundary | Required behavior |
| --- | --- |
| Candidate end of turn | Allow continuation under the active policy; do not turn a provisional transcript into a committed action. |
| Accepted interruption | Coordinate generation cancellation, queued-audio removal, delivered-history reconciliation, and ongoing tool work. |
| False interruption | Define whether and how an answer resumes without repeating material already heard. |
| Corrected intent | Suppress stale speech while preserving the actual outcome of a submitted action. |

The [turn control guide](skills/foundations/voice-turn-taking/references/turn-taking-guide.md)
provides a state model, event trace, tuning process, metrics, and test matrix.
It compares the roles of Silero VAD, Smart Turn, LiveKit detection, and native
provider controls. Current LiveKit audio and deprecated text detectors have
different inputs and SDK requirements; the guide records those distinctions.
Invoke [voice-turn-taking](skills/foundations/voice-turn-taking/SKILL.md).

### Noise, echo, and the audio frontend

![Echo-processing map: the endpoint sends a render reference to capture processing; physical speaker echo returns to the microphone, while transported audio reaches optional server enhancement.](skills/foundations/voice-audio-frontends/assets/echo-processing.svg)

Noise suppression reduces unwanted sound. Acoustic echo cancellation uses a
reference of rendered audio to reduce sound returning through the microphone.
A noise gate, automatic gain control, beamforming, and speaker isolation solve
different problems. Stacking them without knowing what the device already does
can remove the quiet speech you wanted to keep.

Begin with ownership: which processing is active in the operating system, browser,
SDK, telephone gateway, and server? Check capture format and the playback
reference before tuning a model. On a speakerphone, test the caller speaking
while the agent speaks. Echo reduction during silence says little about
preserving that overlapping voice.

The [audio frontend guide](skills/foundations/voice-audio-frontends/references/audio-frontends-guide.md)
works through a noisy-laptop fault, processing placement, format contracts, and
paired tests. It covers browser processing, RNNoise, DeepFilterNet, and LiveKit
enhancement options with deployment and license qualifications. Judge the result
by intelligibility, critical-field recognition, false interruptions, clipped
speech, and runtime cost across relevant speakers and devices.
Invoke [voice-audio-frontends](skills/foundations/voice-audio-frontends/SKILL.md).

### Speech recognition

Choose recognition around the work the transcript must support. A low aggregate
word error rate can hide failures on names, dates, amounts, and reference numbers.
Measure those fields separately, with the accents, languages, microphone levels,
and network conditions the application expects.

A streaming transcript is a sequence of revisions. Store segment identity and
finality, replace interim hypotheses correctly, and distinguish a stable segment
from a completed turn. Deepgram Nova's `is_final` and `speech_final` carry different
meanings; Flux has a different event contract. Treating every message as more
finalized text can duplicate words and trigger work too early.

The [speech pipeline guide](skills/foundations/voice-speech-pipeline/references/speech-pipeline-guide.md)
includes a correction trace, task-specific selection worksheet, word error rate
normalization, and comparisons that hold the input path constant.
Use [voice-speech-pipeline](skills/foundations/voice-speech-pipeline/SKILL.md)
when integrating or evaluating recognition and synthesis together.

### Speech synthesis and playback

Streaming audio output and streaming text input are different capabilities. If
the whole reply is available, an HTTP audio stream may suffice. If text arrives
incrementally, synthesis needs enough context to speak naturally without buffering
the entire reply. Verify what the selected model and API support.

Use phrase boundaries deliberately. Test abbreviations, names, currency,
ambiguous dates, and the final short fragment of an answer. Keep canonical tool
values separate from their spoken rendering, and check the voice's actual
pronunciation. Do not assume SSML or pronunciation dictionaries work identically
across models.

Track generated, queued, and played audio separately. An interruption must reach
the decoder and playback buffers as well as generation. Use response or generation
identities to reject late audio from an obsolete answer. The
[speech pipeline guide](skills/foundations/voice-speech-pipeline/references/speech-pipeline-guide.md)
covers buffering, final flushes, pronunciation fixtures, output formats, and
measurements of first audible and first substantive response.

### Conversation and accessibility

Write for someone listening once. Ask the next useful question, preserve details
already given, and offer a narrow repair when only one field is uncertain. Bind
confirmation to the actual destination, amount, or time involved in the action.
A corrected value must reach tool state as well as the next sentence.

Plan for different speaking speeds, pauses, hearing needs, language changes, and
background environments. Offer supported alternatives when speech is difficult.
Transcripts, captions, keypad input, repetition, and human help each need an
implemented path before the agent promises them.

The [conversation skill](skills/foundations/voice-conversation-design/SKILL.md)
turns these decisions into a prompt and testable conversation contract. Keep
business policy, speaking style, and runtime behavior distinct. Prompt wording
can describe an interruption; the runtime still has to perform it.

### Tools, transactions, and handoffs

Stopping speech does not undo a booking. A timeout does not prove it failed.
Keep a durable record of proposed, authorized, submitted, committed, failed, and
unresolved actions, then make spoken claims from the evidence in that record.

The [transaction and handoff guide](skills/foundations/voice-conversation-design/references/transactions-and-handoffs.md)
follows a lost booking response through a caller's correction. It explains
idempotency scope, reconciliation, cancellation boundaries, stale results,
compensation, and tests for duplicate writes. It also distinguishes an in-memory
async tool manager from a durable business-action ledger.

For handoffs, define preparation, destination acceptance, release of the old
owner, and recovery when acceptance never arrives. Transfer the confirmed facts,
unresolved issue, and pending action IDs the recipient needs. A software agent
switch and a connected human phone call require different proof of success.

### Telephony and call control

A call has signaling, media, and application state. A successful API request
does not establish that someone answered, an established call does not establish
two-way audio, and an open WebSocket does not establish that the caller can hear
the agent. Observe each boundary.

The [telephony guide](skills/foundations/voice-call-reliability/references/telephony-guide.md)
covers PSTN and SIP, inbound and outbound flow, codec contracts, DTMF direction,
answering-machine detection, transfer choices, webhook verification, disconnect
recovery, and cleanup. A call-failure matrix makes recovery part of the design.
Caller disconnect, media disconnect, worker exit, and provider call completion
should reconcile to one understandable session outcome.

Invoke [voice-call-reliability](skills/foundations/voice-call-reliability/SKILL.md).
For implementation, start with original
[Twilio](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-voice-conversation-relay/SKILL.md),
[LiveKit](https://github.com/livekit/agent-skills/blob/main/skills/building-livekit-agents/SKILL.md),
or [other telephony skills](docs/more-skills.md),
then check the exact media and call-control API in use.

### Production operations

Capacity means more than how many workers can launch. Account for model and
carrier quotas, regional availability, warm capacity, admission decisions,
session duration, and graceful draining. Test a dependency failing after a
session starts, including the state a replacement would need to continue.

The [operations guide](skills/foundations/voice-call-reliability/references/production-operations-guide.md)
provides a readiness worksheet, failure drills, incident evidence, and cost
accounting boundaries. Correlate call, session, turn, model response, and tool
action IDs without collecting more sensitive content than needed.
Choose service objectives from product needs and measured baselines; this
collection does not prescribe a universal latency or availability target.

Evaluate failover as a concrete path. Another model may accept text yet use
different voice, history, tool, or interruption semantics. Document what can
resume, what must restart, and what the caller will be told.

### Latency and media debugging

Measure from a named event to another named event on compatible clocks. End of
speech, committed transcript, first model token, first synthesized audio, and
first playback are different boundaries. Overlapping streams make a sum of stage
p95 values a misleading end-to-end estimate.

Use [voice-latency-audit](skills/foundations/voice-latency-audit/SKILL.md) to
reconstruct a turn, account for missing events, and compare like with like.
Separate first filler from first useful answer, and report failed or canceled
turns in the coverage denominator instead of silently removing them.

For silence, distortion, one-way audio, or speech from an obsolete response,
use [voice-media-debugging](skills/foundations/voice-media-debugging/SKILL.md).
Follow frames from capture to playback, checking formats, counters, buffering,
autoplay permission, and clear ordering. A connected transport and a successful
model response are only intermediate evidence.

### Evaluation and release decisions

Match the test to the claim. A text simulation can test a tool decision but cannot
establish speakerphone echo behavior. A clean audio fixture cannot establish
telephone routing. One completed end-to-end call cannot establish capacity
under concurrent load.

The [evaluation skill](skills/foundations/voice-agent-evaluation/SKILL.md)
organizes conversation, tool, audio, transport, failure, and lifecycle checks.
Use deterministic assertions for action outcomes and cleanup, alongside human
or model-assisted judgments for conversation quality. Preserve important speaker
and channel groups when summarizing results.

Build the release set from observed failures as well as expected conversations:
hesitation, correction, overlapping speech, noisy input, unknown write outcome,
transfer rejection, provider timeout, and disconnect during cleanup. Define
the regression budget before looking at the new result.

## Skills and providers

| Collection | What it contains |
| --- | --- |
| [Core skills](docs/catalog.md) | Nine original foundations and 27 provider skills from LiveKit, ElevenLabs, Twilio, Pipecat, Cartesia, and OpenAI. Original links appear beside dated copies. |
| [More upstream skills](docs/more-skills.md) | 102 voice-related skill files across 20 original repositories, grouped by task. Includes SDK language variants and marked optional workflows. |
| [Runtime resources](docs/resources.md) | 43 frameworks, models, media utilities, evaluation tools, and learning projects, with source dates and license qualifications. |

A skill guides a coding agent. A runtime framework or model becomes part of the
application. Counts describe files and projects, not independent capabilities
or a quality ranking.

Original provider starting points include
[LiveKit](https://github.com/livekit/agent-skills/blob/main/skills/building-livekit-agents/SKILL.md),
[Pipecat](https://github.com/pipecat-ai/skills/blob/main/skills/init/SKILL.md),
[ElevenLabs](https://github.com/elevenlabs/skills/blob/main/agents/SKILL.md),
[Cartesia Line](https://github.com/cartesia-ai/skills/blob/main/skills/cartesia-line/SKILL.md),
and [OpenAI speech](https://github.com/openai/skills/blob/main/skills/.curated/speech/SKILL.md).
The expanded index includes cloud voice, carriers, recognition, synthesis,
evaluation, and local speech. Stars are dated adoption signals; code licenses
may not cover weights, voices, datasets, or hosted services.

## Get started

1. Pick the engineering question and read its guide or skill.
2. Install the **whole skill folder**, including references and scripts. For
   provider material, use the original source's current installation instructions.
3. Invoke the frontmatter name using your coding agent's skill syntax.
4. Begin with fixtures and mocked tools, then test the authorized real media path.

```sh
git clone https://github.com/RBStrayer/nl-voice-skills.git
```

Example requests:

> Use voice-turn-taking to investigate callers being cut off during pauses. Map the active turn owner, distinguish false interruptions from early endpoints, and propose a test set before tuning.

> Use voice-audio-frontends to investigate an agent hearing itself on laptop speakers. Check processing owners and the playback reference, then compare changes using quiet speech and double-talk.

> Use voice-call-reliability to review transfer failures and shutdown. Trace signaling, media, tool actions, and cleanup through the provider events.

[Usage notes](docs/usage.md) cover host compatibility and source caveats.
Installing instructions does not itself authorize dialing, recording, spending,
deploying, or changing a provider account.

## Freshness and maintenance

This review used **Context7 plus current primary documentation**, with direct
source checks where the index was missing or stale. Review dates are distinct
from publication dates. [Documentation review](docs/documentation-review.md)
records changed installation commands, outdated SDK constants, turn-detector
changes, and model-license qualifications.

A daily review is configured in the maintainer's Codex workspace for **9:00 a.m.
America/New_York**. It checks original sources and releases, makes supported
updates, validates them, and pushes to this private repository. The scheduler
and authentication are external; cloning the repo does not install an automation.
[Maintenance procedure](docs/maintenance.md).

```sh
python scripts/verify.py
python scripts/test_verify.py
```

These checks cover source hashes and licenses, skill structure, local links,
metadata consistency, and common credential patterns. They do not execute
provider APIs or establish production voice quality.

## Repository map

| Path | Contents |
| --- | --- |
| [skills/foundations/](skills/foundations/) | Original skills and their portable engineering guides |
| [skills/](skills/) | Foundations and licensed, dated provider snapshots |
| [docs/catalog.md](docs/catalog.md) · [docs/more-skills.md](docs/more-skills.md) | Core and expanded skill indexes |
| [docs/resources.md](docs/resources.md) | Runtime components, official learning paths, and community leads |
| [sources.json](sources.json) | Snapshot commits, retained licenses, and copied-file hashes |
| [linked-skills.json](linked-skills.json) · [resources.json](resources.json) | Dated original-source metadata |
| [docs/research.md](docs/research.md) | Search coverage, exclusions, and verification limits |
| [docs/diagram-style.md](docs/diagram-style.md) | Diagram sources, neutral palette, and export notes |

Contributions should fill a concrete voice-engineering gap and link to the
original maintained source. See [CONTRIBUTING.md](CONTRIBUTING.md).

Original NL material is [MIT licensed](LICENSE). Copied upstream content retains
its own terms in [third-party notices](THIRD_PARTY_NOTICES.md).

Maintained by [Rob Strayer](https://github.com/RBStrayer).
