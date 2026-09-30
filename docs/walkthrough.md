# How a voice call really works

[Home](../README.md) / [Engineering handbook](handbook.md) / Walkthrough

This walkthrough follows one conversation from capture to playback, then through
actions, phone routing and testing. Each part names the skills that help and links
a deeper guide. Read it in order or jump to the problem you're solving. New to
voice agents? Start with [getting started](getting-started.md) first.

[Architecture](#choose-the-system-you-can-explain) · [Turn taking](#give-the-caller-room-to-finish) · [Audio](#keep-the-words-lose-the-interference) · [Recognition and speech](#carry-the-meaning-through-recognition-and-speech) · [Actions](#when-the-caller-changes-their-mind) · [Calls](#make-calls-and-handoffs-recoverable) · [Timings and tests](#measure-the-conversation-the-caller-received)

## Choose the system you can explain

Before comparing models, write down what the agent must accomplish. Answering
questions, collecting an address, and changing a reservation have different
failure costs. Include the channel, languages, expected noise, human escalation,
existing tools, operating team, and budget. Leave unknowns visible.

Then draw the responsibilities: who carries audio, decides whose turn it is,
executes an action, and recovers an interrupted session? A speech model choice
answers only part of that design.

![Three ways to build the voice loop: a cascade of speech-to-text, a language model and text-to-speech; one speech-to-speech model; and a hybrid with a speech model in front of an existing text workflow.](../assets/diagrams/speech-architectures.svg)

### Three speech paths worth comparing

| Starting point | Why you might choose it | What to prove |
| :--- | :--- | :--- |
| **Speech-to-text → text agent → text-to-speech** | You need intermediate text, an existing text workflow, or separate speech components. | Transcript revisions, phrase buffering, and cancellation behave correctly across stages. |
| **Speech-to-speech session** | You want the model to interpret and produce audio within the conversation. | The chosen session provides the controls, languages, tool behavior, and evidence your application needs. |
| **Spoken interface with delegated backend work** | You want to retain an existing workflow behind the voice interaction. | Delegation, progress, returned results, and failure recovery preserve the right state. |

These are conceptual boundaries. The [current OpenAI voice guide](https://developers.openai.com/api/docs/guides/voice-agents)
describes all three paths. No path guarantees the lowest caller-perceived delay;
endpointing, streaming, network placement, and playback still affect the result.

Hosting is another decision. A chain can run in a managed runtime, and an
application you operate can call a hosted speech model. Can your team
keep enough servers ready for calls, start new calls on the right one, and deploy
without dropping live calls? Also check where audio and transcripts are processed
and stored before you promise a customer a region.

### A booking system makes the tradeoffs concrete

Suppose you already have a booking service and need web and inbound phone access.
The business requires validated values before a write, callers need human
escalation, and the team is small. This is a design exercise, not a tested stack
recommendation.

A chain is a useful candidate if you also need a text checkpoint before every
spoken response or want to retain an existing text agent. A native speech session
remains a candidate when validated tool arguments satisfy the business checkpoint.
Checking an action before it runs doesn't mean the whole conversation has to go through a text chain.

Both candidates still need an authorized booking service, a way to establish
unclear outcomes, and a tested transfer route. Compare them using the same
corrections, noisy input, and failed writes. Record caller-audible timing and total
cost with the same boundaries. Choose a default and name the requirement that
would make you reconsider it.

> **Keep generated speech, delivered speech, and committed actions separate.**
> The model may finish an answer that the caller never hears. A booking may finish
> after its confirmation was interrupted. Each needs its own evidence.

The [architecture guide](../skills/foundations/voice-stack-selection/references/architecture-guide.md)
includes transport choices, capacity, billing boundaries, and a worked worksheet.

Skills for this decision:

- [Stack selection](../skills/foundations/voice-stack-selection/SKILL.md): compare complete candidates and write the decision record.
- [Twilio agent architect](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-ai-agent-architect/SKILL.md): choose a Twilio voice implementation path.
- [Build a LiveKit agent](https://github.com/livekit/agent-skills/blob/main/skills/building-livekit-agents/SKILL.md): implement sessions, tools, and workflows.
- [Initialize Pipecat](https://github.com/pipecat-ai/skills/blob/main/skills/init/SKILL.md): turn the chosen pipeline into a project; check the [current CLI notes](usage.md#pipecat-cli-installation).

## Give the caller room to finish

“Send it to Alex… actually, to Alexis.” A quiet stretch between those phrases
doesn't tell you whether the thought is complete. Voice activity detection finds
likely speech. Silence endpointing waits for a gap. End-of-turn prediction estimates
completion. A “final” transcript from the speech service means only that the service won't change those words.
Your application still needs to decide when to respond.

![A call timeline where the agent waits through a pause, replies at the end of the turn, then stops mid-sentence when the caller barges in, with five steps for handling the interruption.](../assets/diagrams/turn-taking.svg)

Let one part of your code decide when the caller has finished and when the agent may answer.
Everything else only gives it hints. Otherwise, two policies can trigger two
answers or add their waiting periods together.

An “uh-huh” can invite the agent to continue. A quiet “no” can reverse the answer
to a confirmation question. Raising duration or word-count thresholds may suppress
both. Test short corrections, spelled names, numbers, code switching, and callers
who need more time to formulate a response.

When an interruption is accepted, follow it through the system:

1. Invalidate the old response and cancel obsolete generation where supported.
2. Stop active playback and clear its queued audio.
3. Reject late chunks belonging to that response.
4. Reconcile conversation history with playback evidence.
5. Keep any external action under its own cancellation or recovery contract.

A stopped generator can leave seconds of audio in another buffer. A stopped
coroutine can't prove that a remote write stopped. Check every boundary
your actual transport exposes.

The [turn-taking guide](../skills/foundations/voice-turn-taking/references/turn-taking-guide.md)
includes detector requirements and a correction-during-booking trace.

- [Turn taking](../skills/foundations/voice-turn-taking/SKILL.md): find early endpoints, false interruptions, and competing response triggers.
- [Conversation design](../skills/foundations/voice-conversation-design/SKILL.md): write questions and repairs that leave room for the caller.
- [Debug LiveKit agents](https://github.com/livekit/agent-skills/blob/main/skills/debugging-livekit-agents/SKILL.md): exercise a multi-turn conversation and inspect behavior.
- [Deepgram conversational STT, JavaScript](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-conversational-stt/SKILL.md): integrate the conversational recognition path using its own event contract.

## Keep the words, lose the interference

Noise cancellation deserves its own design. An agent hearing its speaker,
a fan keeping speech detection active, and a nearby person issuing an apparent
command are different problems.

**Acoustic echo cancellation** reduces playback leaking into capture. Conventional
AEC needs a reference to the rendered audio, with usable timing. **Noise suppression**
attenuates interference. **Speaker isolation** favors a selected or primary speaker.
A **noise gate** changes level below a threshold and can remove quiet syllables.
Gain control cannot recover a word that an earlier processor deleted.

![Four sounds reach the microphone (caller, echo, background noise, other talkers) and pass through echo cancellation, noise suppression, voice activity detection and speech-to-text, with notes on where each runs.](../assets/diagrams/echo-and-noise.svg)

Place processing where its inputs exist. A browser capture path may see both the
microphone and playback; a remote agent server usually receives audio after device
processing. The server does not automatically have the caller endpoint's echo
reference. Telephone capture adds carrier and codec boundaries to inspect.

For a laptop that interrupts itself, compare headphones with speaker playback and
inspect capture processing first. If whispered corrections disappear after adding
enhancement, bypass that added stage using the same input. Check clipping and
format conversion before changing gain or turn thresholds.

Keep double-talk in the test set: the agent speaks while the caller says “wait,
change that.” Removing both voices can look like excellent echo reduction while
making interruption impossible. Compare retained words and intended interruptions,
alongside residual noise and added delay.

The [audio guide](../skills/foundations/voice-audio-frontends/references/audio-frontends-guide.md)
covers AEC references, browser constraints, resampling, deployment choices, and
speech-preservation measures.

- [Audio frontends](../skills/foundations/voice-audio-frontends/SKILL.md): locate the interference and compare processing without losing speech.
- [Media debugging](../skills/foundations/voice-media-debugging/SKILL.md): inspect format conversion, capture, and playback boundaries.
- [ElevenLabs voice isolation](https://github.com/elevenlabs/skills/blob/main/voice-isolator/SKILL.md): use the provider's isolation workflow. Check its input and processing contract before considering a live audio path; an isolation skill doesn't prove streaming AEC support.

## Carry the meaning through recognition and speech

In a cascade, speech-to-text (STT) produces words, the text agent reasons about
them, and text-to-speech (TTS) produces audio. The arrows also carry assumptions:
whether a transcript can still change, when a phrase is ready, and who owns a
cancelled response. This separation lets you inspect intermediate results and
choose components independently. Replacing one component still requires testing
the neighboring event and media contracts.

### Protect the words that change the outcome

Recognition quality is task-specific. A broad word-error score can hide the wrong
booking day, a missing negation, or a nearly correct street name. Build fixtures
from the words that change the outcome, using the microphone or phone channel the
caller will actually use.

### Handle transcript revisions

Treat a streaming transcript as a draft that keeps changing. Replace each draft
with the provider's newer version of the same segment; adding every update to the
end repeats words. Hold finished segments until your turn logic accepts the
caller's utterance. Preparation that's easy to undo can start earlier, in case a
correction makes it obsolete.

For example, an application might receive this synthetic sequence. These are
illustrative records, not a provider's event schema:

```text
Segment 7, revision 1, interim: "Tuesday at two"
Segment 7, revision 2, final:   "Thursday at two"
Turn state: waiting for completion evidence
```

Replace the first guess with the second. A segment being final is not the same
as your application deciding the turn is over.

### Form phrases for playback

Speech generation needs an equally explicit contract. Streaming audio output and
streaming text input are separate capabilities. Decide who forms phrases, flushes
the final short phrase, and bounds output queues. A quick first byte provides
little benefit if the player waits for the entire answer.

Test pronunciation on names, dates, amounts, abbreviations, and identifiers.
Keep the authoritative value separate from its spoken form: changing how a date
is read should not change the date stored by the business service. Listen through
the final transport with the selected voice and language.

The [speech pipeline guide](../skills/foundations/voice-speech-pipeline/references/speech-pipeline-guide.md)
covers transcript finality, pronunciation dictionaries, buffering, and component
replacement tests.

- [Speech pipeline](../skills/foundations/voice-speech-pipeline/SKILL.md): specify the whole recognition-to-playback contract.
- [Deepgram STT, Python](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-speech-to-text/SKILL.md): integrate recognition in a Python application.
- [ElevenLabs text-to-speech](https://github.com/elevenlabs/skills/blob/main/text-to-speech/SKILL.md): work with speech generation, streaming, and voice settings.
- [Cartesia API](https://github.com/cartesia-ai/skills/blob/main/skills/cartesia-api/SKILL.md): integrate speech APIs and their streaming interfaces.

## When the caller changes their mind

Consider this synthetic case. The caller authorizes Friday at two. The booking
service commits the request, but its response is lost. While the agent is speaking,
the caller says, “Actually, make it Monday.”

![When a caller changes their mind while an action is in flight, the agent stops talking, checks what happened to the first action, then branches on committed, not committed or unknown.](../assets/diagrams/action-outcomes.svg)

Stopping the old speech is useful. The application must also discover what happened
to Friday. Keep the original action, its arguments, and its idempotency key if the service
supports one (an ID that lets it spot a repeated request); retain Monday as
corrected intent. A temporarily empty lookup does not prove the
first request failed.

- **Friday committed:** use the service's authorized change or cancellation workflow.
- **Friday did not commit:** validate and submit the corrected request with its own action identity.
- **Friday remains unknown:** preserve both records and use the defined reconciliation or human recovery path.

This gives the agent something honest to say: “I'm checking whether Friday went
through before I change it.” The caller speaking again is not a reason to book twice. And if the
booking system can't tell you whether a request went through, your code can't
guarantee it happened exactly once.

Conversation design includes these recovery sentences, narrow clarification
questions, meaningful progress, and alternatives for people who cannot use the
speech flow comfortably. Keep prompts tied to actual tool state. “Almost done”
requires evidence that the work is nearly complete.

The [transactions guide](../skills/foundations/voice-conversation-design/references/transactions-and-handoffs.md)
develops durable action states and recovery across handoffs.

- [Conversation design](../skills/foundations/voice-conversation-design/SKILL.md): connect prompts, corrections, and progress to actual application state.
- [ElevenLabs agents](https://github.com/elevenlabs/skills/blob/main/agents/SKILL.md): configure agents, tools, and procedures in that platform.
- [Build LiveKit workflows](https://github.com/livekit/agent-skills/blob/main/skills/building-livekit-agents/SKILL.md): implement tools and handoffs while retaining application action ownership.

## Make calls and handoffs recoverable

A phone call has a control path and a media path. An answered call can still have
one-way audio, a bad codec, or an empty playback queue. Inspect both directions
and record the actual format at each boundary. Build inbound and outbound flows
independently; one working direction doesn't prove the other.

For a warm handoff, retain the caller while reaching the destination, verify
acceptance, and connect the parties before retiring the bot when the selected
mechanism permits it. Decide who speaks during each transition. Ringing or an
acknowledged transfer request doesn't prove that a person accepted the caller.

When the destination fails, the caller needs a supported next step: return to the
agent, a bounded wait, contact instructions, or an authorized callback. Confirm
which legs and controls remain available under the chosen carrier's contract.

### Draw a call tree before writing the happy path

![An intent router sends each call down a question, action or person branch, each with a happy-path outcome, a dashed recovery outcome and a named exit.](../assets/diagrams/call-flow-tree.svg)

For an appointment service, begin with what the caller needs: a service question,
a booking, or a person. A question can return to the conversation after an answer.
A booking follows the validation and action checks above. A request for a person
enters a handoff route with an explicit unavailable-destination branch.

Now walk each branch as a caller. What happens when the answer is unclear, the
booking result is unknown, or nobody accepts the transfer? Add a repair or recovery
route beside that decision. Keep the current owner of the caller and any pending
action visible. A final box labeled “done” needs evidence that its promised
outcome happened.

This tree is a design exercise, not a required IVR menu or provider API recipe.
Natural speech can select the route. The tree helps you check that every route
has a useful response and an exit, including a deliberate end to the call.

Production adds another set of caller-visible decisions. Define what happens when
capacity is full, a worker drains during deployment, or a speech service fails.
Track active sessions separately from start rate. Preserve pending action records
through worker loss. Include extra transfer legs and idle capacity when comparing
costs.

The [telephony guide](../skills/foundations/voice-call-reliability/references/telephony-guide.md)
and [operations guide](../skills/foundations/voice-call-reliability/references/production-operations-guide.md)
cover event authentication, duplicate delivery, draining, overload, and incident recovery.

- [Call reliability](../skills/foundations/voice-call-reliability/SKILL.md): trace every leg, transfer, worker, and pending outcome.
- [Twilio TwiML](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-voice-twiml/SKILL.md): define voice and IVR call flows.
- [Twilio conferences](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-conference-calls/SKILL.md): build conferences, holds, and transfer workflows.
- [Telnyx voice, Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-python/SKILL.md): implement inbound, outbound, transfer, and bridge operations.
- [Operate LiveKit agents](https://github.com/livekit/agent-skills/blob/main/skills/operating-livekit-agents/SKILL.md): deploy, configure, and roll back workers.

## Measure the conversation the caller received

![An illustrative timeline of one reply: the caller stops speaking at 0 ms, the turn is committed at 260 ms, the first phrase is ready at 720 ms, the first audio chunk at 900 ms, it reaches the device at 950 ms, playback starts at 1,060 ms and useful words are heard at 1,120 ms.](../assets/diagrams/latency-budget.svg)

**Synthetic trace, not a benchmark or target.** On one assumed shared clock:
speech ends at 0 ms; turn commit is 260 ms; the first speakable phrase is ready at
720 ms; the first synthesis chunk at 900 ms; its arrival at 950 ms; the first
playback sound at 1,060 ms; useful speech at 1,120 ms. The latter two are deliberately
different: hearing something is not necessarily hearing a useful answer.

### Read one turn from left to right

Begin at the end of the caller's speech, using a defined audio boundary. The turn
controller may still be waiting for completion evidence. Its **turn commit** says
that the application accepted the turn and can release a response. The gap between
those points includes the waiting policy; a faster text model cannot remove it.

In a chain, **first text** marks when the agent starts producing output. That text
may be too short to speak naturally, so a phrase buffer waits for a usable unit.
The chart marks that speakable phrase, not the first token.
The **first synthesis chunk** marks generated audio reaching the next boundary.
It can still need decoding, transport, and player buffering before **playback**
begins. Define which of those events the log actually captures.

The **first useful audible response** is the caller-facing endpoint. A filler
such as “one moment” is different from the requested answer. A server log can't prove what reached the caller's ear without the corresponding evidence.
Report runtime playback when that is all you observed, and keep missing coverage
visible.

These stages can overlap. Recognition can run while the caller speaks; later
text and synthesis can continue while an earlier phrase plays. Read the chart
as one causally ordered trace, not a row of independent durations to add. A
speech-to-speech session may not expose the same internal text and synthesis
boundaries, so preserve what its actual API provides.

The illustration is synthetic, with no vendor benchmark or universal timing
target implied. On real calls, correlate session, turn, response, and action IDs,
and align clock domains before subtracting timestamps. Compute the distribution
from comparable end-to-end turn measurements. Adding each component's p95 does
not produce end-to-end p95. Keep interruption-to-stop delay as another measure,
including residual queued speech, rather than folding it into answer latency.

For a timing investigation:

- [Latency audit](../skills/foundations/voice-latency-audit/SKILL.md): reconstruct a turn from raw events and state measurement coverage.
- [Media debugging](../skills/foundations/voice-media-debugging/SKILL.md): locate transport, decoder, and playback queues.
- [LiveKit debugging](https://github.com/livekit/agent-skills/blob/main/skills/debugging-livekit-agents/SKILL.md): reproduce the conversation that exposes the delay.
- [ElevenLabs TTS](https://github.com/elevenlabs/skills/blob/main/text-to-speech/SKILL.md): inspect the synthesis integration and its streaming settings.

### Give each failure a repeatable test

When audio is silent, distorted, or late, follow samples and events from capture
to playback. Inspect codec, sample rate, channels, framing, conversion, and queue
ownership. Relabeling samples changes their interpreted duration; upsampling
telephone audio does not restore missing frequencies.

Build a release set around successful tasks and difficult transitions: pauses,
quiet corrections, interruptions during writes, failed transfers, cold starts,
disconnects, and cleanup. Text simulations help with dialogue and tool logic.
Audio and transport tests show different things. Verify the resulting
business records as well as what the agent said.

- [Agent evaluation](../skills/foundations/voice-agent-evaluation/SKILL.md): build a proportionate test matrix and record what remains unproven.
- [Test LiveKit agents](https://github.com/livekit/agent-skills/blob/main/skills/testing-livekit-agents/SKILL.md): write turn-level behavior regressions.
- [Write LiveKit scenarios](https://github.com/livekit/agent-skills/blob/main/skills/writing-livekit-scenarios/SKILL.md): preserve meaningful caller situations as simulation scenarios.
- [Run LiveKit simulations](https://github.com/livekit/agent-skills/blob/main/skills/running-livekit-simulations/SKILL.md): exercise those scenarios within the authorized test scope and inspect outcomes.

**Next:** [common problems](common-problems.md) for fixes, or the [skill catalog](catalog.md) to install what you need.
