# Choosing a voice agent architecture

Reviewed against official documentation on **2026-09-30 UTC**. This is a review date,
not a source update date. The reviewed pages did not establish last-modified dates.
Check current documentation and installed versions when using this guide.

Sourced paragraphs describe documented behavior. Recommendations and conditional
examples are engineering guidance to test, not verified compatibility or performance.

[Speech and hosting](#separate-five-decisions) ·
[Media paths](#draw-media-and-control-paths) ·
[Turns and actions](#assign-turn-ownership) ·
[Capacity and cost](#size-capacity-and-cost-together) ·
[Decision worksheet](#compare-two-or-three-complete-options) ·
[Migration tests](#prove-the-decision-before-migration)

## Begin with the task

A question-answering agent and an agent that changes bookings have different needs.
Write the task in one sentence, then collect constraints that can rule out a design.

| Constraint | What to record |
| --- | --- |
| Channel | Browser, mobile, inbound/outbound phone, existing audio stream, current provider |
| Conversation | Languages, noise, overlap, pronunciation, accessibility, human transfer |
| Actions | Reads versus writes, identity checks, tool APIs, durable records |
| Experience | Response-delay definition, interruption behavior, startup, failure recovery |
| Traffic | Arrival pattern, duration, peak concurrency, geography |
| Operations | Service owner, network placement, retention, residency, deployment restrictions |
| Money | Shared monthly ceiling, traffic, idle capacity, authorized test spending |

Label unknowns. Monthly minutes do not establish peak concurrency. If the requirement
is sub-500 ms and the evidence is provider TTFT logs, start with instrumentation:
those logs cannot establish caller-perceived response delay.

## Separate five decisions

| Decision | What it owns | What still needs an owner |
| --- | --- | --- |
| Speech engine | Recognition, reasoning, speech, together or in stages | Transport, authorization, durable state |
| Orchestration | Context, tools, turns, adapters | Production hosting unless included |
| Media transport | Audio, codec, buffering, connection lifecycle | Model behavior, business outcomes |
| Runtime | Startup, compute, capacity, deployment, shutdown | Correctness, provider quotas |
| Business service | Identity, permissions, records, action reconciliation | Voice interaction, playback |

Managed hosting and native speech-to-speech are independent choices. A hosted runtime
can run a chain; a self-hosted application can use a hosted speech model. Pipecat does
not require operating its runtime yourself.

### Choose the speech architecture

OpenAI's current guide distinguishes Realtime, a chain, and GPT-Live. Realtime combines
audio interpretation, reasoning, tools, and speech in one session. A chain exposes
speech recognition, a text agent, and speech generation. GPT-Live handles spoken
interaction while delegating backend work, including client delegation to an existing
workflow. The guide describes a chain as “Control over each speech and text stage.”
[OpenAI voice agents](https://developers.openai.com/api/docs/guides/voice-agents)

Test native speech-to-speech when conversational timing and prosody
matter and no text checkpoint is required before each answer. Test a chain when you
must inspect or transform intermediate text, reuse a mature text agent, or choose
speech components independently. Consider a delegated conversational layer when
retaining the backend decides the choice. Check availability and integration rather
than assuming it replaces Realtime without changes.

Neither architecture guarantees lower latency. Streaming, endpointing, model behavior,
and playback affect the result; native speech-to-speech still needs application controls.

Define any text checkpoint precisely: before each spoken answer, before a tool write,
or during later review. Name the reviewer and whether approval is required. A native
speech frontend can submit a text proposal to a trusted action gate before a write;
that requirement alone does not force the whole conversation through a speech chain.

Pipecat composes pipelines from processors and services. Its documented chain includes
transport input, STT, user context, LLM, TTS, transport output, and assistant context.
“Frame processors are modular and reusable.” Replacement is a design option, not proof
that providers share context, cancellation, and tool behavior.
[Pipecat pipelines](https://docs.pipecat.ai/pipecat/learn/pipeline)

### Choose who operates the agent

A managed agent platform may own conversation configuration and routing. A managed
runtime hosts your bot code. A self-hosted design owns the dispatcher and session
processes too. Compare the actual division of work.

Pipecat separates the bot, session-start service, and media transport. Pipecat Cloud
runs agents in Daily-hosted regions; Enterprise uses a region in your VPC. Placement
must be checked across the full data path, including external speech services.
[Deployment overview](https://docs.pipecat.ai/pipecat/deployment/overview),
[Cloud and Enterprise](https://docs.pipecat.ai/pipecat-cloud/introduction)

Prefer managed hosting if the team cannot support dispatch,
isolation, capacity, and deployment during active calls. Operate the runtime when
network placement, custom audio, isolation, or existing infrastructure justifies that
work. Verify export, debugging, regions, tools, and failure handling.

Pipecat's dedicated production guide calls its development runner “not built for
production.” It lacks production admission and lifecycle controls. A local demo does
not establish a deployment plan.
[Running bots in production](https://docs.pipecat.ai/pipecat/deployment/running-bots-in-production)

## Draw media and control paths

![Conceptual audio, call-control, and durable-action responsibilities.](../assets/voice-system-map.svg)

[Editable diagram](../assets/voice-system-map.html). Arrows show logical
responsibilities; output still traverses the deployment's actual media transport.

For OpenAI Realtime, browser initialization can pass through a backend or use a
short-lived client credential minted by the backend. The standard API key stays there.
OpenAI recommends WebRTC for browser/mobile clients and WebSocket for server-to-server.
[Realtime WebRTC](https://developers.openai.com/api/docs/guides/voice-webrtc?api=realtime),
[Realtime WebSockets](https://developers.openai.com/api/docs/guides/voice-websockets?api=realtime)

```text
Browser microphone/speaker <== WebRTC media ==> Realtime session
Browser ---- authenticated setup ----> Application backend
Application backend <== sideband events ==> same session
Application backend ---- authorized tools ----> Business records
```

Realtime documents incoming SIP: configure the trunk, receive the incoming-call webhook,
accept/reject in the application, and attach a control WebSocket using the call ID.
A server sideband for WebRTC or SIP monitors the same session, updates instructions,
and answers tool calls.
[Realtime SIP](https://developers.openai.com/api/docs/guides/voice-sip?api=realtime),
[Server controls](https://developers.openai.com/api/docs/guides/voice-server-controls?api=realtime)

An audio bridge has two connections:

```text
Phone network <== provider media ==> Application relay <== model stream ==> Speech service
                                         |
                                  tools and durable state
```

Use direct SIP when its documented controls and media path satisfy
the task. Use a relay for audio processing, multiple providers, or existing transport
logic. The relay owns event translation, necessary codec conversion, queue limits,
interruptions, and shutdown on both legs. Verify inbound and outbound support separately.

A text relay differs from raw audio streaming. Twilio ConversationRelay exchanges
speech-related events and application text; bidirectional Media Streams exchanges
audio. A returned media mark can follow a clear, so it alone does not prove that audio
was heard.
[ConversationRelay](https://www.twilio.com/docs/voice/twiml/connect/conversationrelay),
[Media Streams messages](https://www.twilio.com/docs/voice/media-streams/websocket-messages)

Check the exact transport, codec, sample rate, channel count, service, region, SDK,
and tool path. Cite an official example or label adapter work unverified. Test microphone
permissions, reconnects, network changes, and transfers instead of promising them.

## Assign turn ownership

Record who detects turn completion, starts a response, interrupts
speech, cancels generation, stops playback, and reconciles history. Test interacting
automatic policies before adding another detector.

Realtime allows automatic VAD, manual turns, or VAD with automatic response creation
and interruption disabled. With WebRTC/SIP, the server manages output buffering and
automatically truncates unheard audio on interruption. With WebSocket, “the client
manages audio playback, and thus must stop playback and handle truncation.” The documented
flow tracks played duration and sends `conversation.item.truncate`; canceling generation
alone does not clear a local playback queue.
[Realtime conversations](https://developers.openai.com/api/docs/guides/realtime-conversations#interruption-and-truncation)

Keep three states separate:

| State | Evidence |
| --- | --- |
| Generated | Provider output or response events |
| Played | Transport/player evidence, with its limits |
| Committed | Authoritative business result |

Stop stale generation and queued playback using each leg's supported controls. Reconcile
model context under that API's playback rules. Correlate late tool results with their
action. A cut-off spoken answer does not undo a completed booking.

Keep action IDs in durable state. Where the business API supports idempotency keys,
retain the original key for a retry of the same action. Otherwise implement deduplication
in the application; do not assume the provider accepts a key. If cancellation races
with a write or a tool times out, query authoritative status before retrying. A new
turn does not justify a duplicate write. These are application recommendations,
not voice-provider cancellation guarantees.

Application deduplication cannot guarantee exactly-once effects across a non-idempotent
external API. A missing result from a lagging lookup does not prove that the write
failed. Preserve an uncertain action for reconciliation; replay only after evidence
establishes that doing so cannot duplicate a committed effect. Define an operator or
user recovery path when the service cannot establish that outcome.

## Keep business authority in the application

Treat tool arguments, transcripts, and client events as requests.
The application checks identity, permissions, inputs, limits, and prior completion.
Keep provider and tool credentials in a trusted service. An ephemeral browser credential
does not authorize access to another account.

A sideband separates private execution from browser media; it does not replace
authorization. Persist outcomes needed after session shutdown. Correlate call, response,
action, and transport events without retaining unnecessary sensitive audio.

Decide when an action becomes committed. If confirmation is required for the task,
obtain it beforehand. Reuse existing authorization instead of adding repeated prompts.

## Size capacity and cost together

Pipecat Cloud runs “one active session at a time” per instance. Warm instances cost
money while idle; `max-agents` limits concurrent instances, and excess starts receive
HTTP 429. Warm capacity and cold startup are separate tradeoffs.
[Cloud scaling](https://docs.pipecat.ai/pipecat-cloud/fundamentals/scaling)

Pipecat's production guidance covers per-session processes and draining old workers
during deployments. Long calls need a different rollout policy from short HTTP requests.
[Session lifecycle](https://docs.pipecat.ai/pipecat/deployment/running-bots-in-production#session-lifecycle)

Size for peak sessions and arrival bursts. Average arrival rate
times average duration estimates steady-state concurrency, not peak capacity. Test cold
startup, warm admission, rejection, quotas, CPU, memory, local models, and connections.
Decide what the caller hears at capacity.

Use current billing units, not remembered prices:

```text
Total =
  phone/transport units × current rate
+ speech/model units × current rate
+ runtime active compute and reserved idle compute
+ platform fees, recording, storage, egress and observability
```

Check included services to avoid double counting. Keep connected time, active speech,
tokens, compute, and reserved capacity distinct. Include retries and failed starts.
Compare the same traffic assumptions and cost per completed task, not only per call.

## Compare two or three complete options

Fill the worksheet and link evidence beside provider-dependent answers. Reject unmet
requirements before scoring convenience.

| Question | Option A | Option B |
| --- | --- | --- |
| Speech path and orchestration | | |
| Browser/phone media path | | |
| Hosting and admission owner | | |
| Turn and playback owner | | |
| Tool authority and durable state | | |
| Adapter work and installed versions | | |
| Latency evidence and boundary | | |
| Capacity and overload behavior | | |
| Cost units, traffic, total | | |
| Data path, retention, regions | | |
| Unknown or blocking test | | |
| Exit path and rewrites | | |

Recommend one default and name the requirement that would change the decision.

### Conditional examples

**Browser tutor, small operations team.** If the native model supports the language and
controls, start with WebRTC and a trusted backend. Compare a managed framework runtime
when added orchestration solves a need. Test noise, interruptions, permissions, reconnects.

**Booking on web and phones.** If an existing text booking service is reliable and a
text checkpoint is required, test a chain with separate channel adapters and one action
service. Compare direct SIP plus Realtime after proving its tools and transfer path.
Interrupt a booking while the write is in flight.

**Changing speech providers.** A modular framework can preserve business code while
replacing a service. Budget for context, tools, turns, codecs, and cancellation differences.
Pipecat organizes that work; it does not make providers equivalent. A component benchmark
alone does not justify migration.

**Sporadic traffic, strict budget.** Compare startup tolerance against idle capacity cost.
A self-hosted server also costs money and needs an operator. If callers cannot wait,
fund warm capacity or test a path without that fleet. Count web and phone under one ceiling.

### Worked comparison: appointments over web and phone

This is a hypothetical design exercise, not a tested provider recommendation.
Assume an existing booking service, web and inbound phone channels, a required
text checkpoint before writes, human escalation, and a small operating team.
The booking API can report operation status but cannot reliably cancel a request
after dispatch. Language support, regional processing, and peak load remain to
be measured or verified.

| Decision | A: staged speech pipeline | B: native speech session |
| --- | --- | --- |
| Input and response | STT supplies revisions to a text agent; TTS speaks its output. | The speech model handles audio interaction; an auxiliary transcript is evidence only under its documented contract. |
| Business checkpoint | Application validates text-agent arguments and required confirmation before dispatch. | Application validates proposed tool arguments and confirmation before dispatch. If policy requires inspecting the model's exact recognized text, an auxiliary transcript alone does not satisfy that requirement. |
| Web and phone | Distinct channel adapters share the action service. Each owns its codec and playback contract. | Supported WebRTC/SIP or bridge paths connect the session. Verify transfer and playback controls for each path. |
| Uncertain booking | Durable action A remains unresolved while the caller gives corrected intent B. | Same durable action contract; conversational fluency does not remove the reconciliation requirement. |
| Operational cost | More speech-stage boundaries to observe, plus selected runtime and provider quotas. | Fewer explicit speech stages, with model-session constraints and any bridge/runtime costs still present. |
| Replacement cost | Stage adapters can be replaced, but segmentation, timing, and cancellation must be retested. | Replacing the speech session may require remapping events, context, voice, tools, and interruption behavior. |

Start the comparison with A because the stated text checkpoint and existing text
workflow favor that boundary. Keep B as a candidate if the owner confirms that
validated tool arguments satisfy the checkpoint requirement, or the selected
native path supplies the necessary text evidence. Neither option passes until
language, region, transfer, and load requirements have evidence.

Run the same booking, correction, quiet-speech, and transfer-failure fixtures
against both. Compare correct authoritative outcomes before response speed.
Measure speech-end to useful playback and interruption-to-stop on compatible
clocks; report missing coverage. Account for the same connected time, active
speech, tool calls, warm capacity, and transfer legs under each billing model.

The decision record might read: "Choose A for the initial release if it meets the
agreed conversation and cost criteria. Reopen the choice if B satisfies the text
checkpoint, required regions, and failure tests while improving measured caller
experience enough to justify migration." Fill in actual measurements before
treating that sentence as an approved project decision.

## Prove the decision before migration

Hold task, input audio, tools, and outcome rubric constant. Change
one architecture at a time. Start with synthetic callers and mocked writes, then provider
tests within authorized scope. Record versions, configuration, traffic, review date,
and exact timing boundaries.

The smallest useful comparison covers:

1. A successful task with correct business state.
2. Hesitation, noise, overlap.
3. Interruption during speech and tool execution.
4. Tool failure or timeout, including an uncertain write result.
5. Startup, capacity rejection, disconnect, shutdown.
6. Total billed usage for the same workload and outcomes.

Measure audible response delay, stop delay, startup, completion, incorrect actions,
recovery, and total cost using identical definitions. Report sample size and missing
measurements. A few scripts do not establish a winning percentile.

For migration, preserve business contracts and action IDs. Map session events explicitly,
compare recordings or synthetic traces offline, then use a bounded rollout and fallback.
Shadow testing must not duplicate writes. Name the reversible switch and evidence needed
to expand traffic.

## Source discipline

Resolve through Context7, then check the primary page and selected API section. OpenAI's
shared guides contain GPT-Live and Realtime material; select the Realtime view for its
behavior. Do not mix event models.

If snippets disagree, check the canonical page and record the discrepancy. This review
found a Pipecat session-initialization snippet suggesting runner use in production while
the dedicated current production page rejects it. This guide follows dedicated guidance.
Repeat the check when documentation changes.
