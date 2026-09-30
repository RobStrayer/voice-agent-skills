---
name: voice-conversation-design
description: Write and evaluate voice agent prompts for spoken turn taking, concise responses, clarification, tool progress, interruptions, and safe handoffs.
license: MIT
---

# Voice conversation design

Design for someone listening in real time. Establish the agent's task, audience,
entry channel, languages, tools, and escalation destination. Read the current
prompt, accepted voice identity, and actual tool contracts before rewriting them.
Inspect a few real or representative dialogs to find where callers hesitate,
correct the agent, repeat themselves, or leave without a resolved task.

## Write the conversation contract

Keep identity, allowed work, authoritative knowledge, tool rules, turn behavior,
and completion criteria explicit. Separate speaking style from business policy.
Use short spoken examples that illustrate an otherwise ambiguous instruction.
Preserve the user's voice choice and accepted persona. Give each required fact one
clear home in the prompt; repeated or contradictory instructions make changes
harder to evaluate. Keep tool parameter details in the actual tool contract.

Prefer one useful question at a time. Give a direct answer before optional detail.
Avoid spoken Markdown, URLs, raw JSON, and long lists unless the caller needs
them. Match response length to the task and the caller's request. Use ordinary
spoken terms for internal systems, and keep implementation details out of the call.
[Source: LiveKit prompting guide](https://docs.livekit.io/agents/start/prompting.md).

Write dates, amounts, phone numbers, and identifiers in a form the selected TTS can
pronounce correctly. Spell or confirm critical details when a mishearing would
change an action. An approved date or amount does not need to be reconfirmed every
turn; a caller's correction does need to update the state used for the action.

## Handle uncertainty and repair

Choose a specific response for each kind of uncertainty:

| Situation | Conversation behavior | State or tool requirement |
| --- | --- | --- |
| Speech is unclear | Ask for the missing word or offer the two plausible alternatives. | Preserve known fields; avoid replacing an uncertain detail with a guess. |
| Knowledge is missing or contradictory | State the relevant limit and offer the supported lookup or escalation. | Use the authoritative source; do not invent policy or availability. |
| Required action details are missing | Ask the next question needed to complete the request. | Validate required arguments before invoking the tool. |
| A consequential action needs confirmation | Restate the affected service, amount, destination, or time and ask for approval once. | Bind approval to those values; changes require the applicable new confirmation. |
| A tool failed | Explain the failure briefly and offer a supported next step. | Preserve the error and distinguish retryable failure from uncertain completion. |
| A result is unknown after a timeout | Say that the outcome is being checked. | Read action status before promising failure, retrying, or claiming success. |

Ask a narrow repair question instead of restarting intake. For multilingual calls,
define whether the agent follows the caller's language, can switch languages, or
needs to transfer. Verify the available recognition and synthesis support before
promising a language or pronunciation. Use the caller's locale for ambiguous dates
and numbers when known; clarify when it changes the requested action.

## Keep speech synchronized with actions

Describe what the current evidence supports. "I'll check" precedes a lookup;
"It's booked" follows authoritative confirmation. Separate the requested action,
in-flight work, committed result, and the response the caller has heard. A model's
tool-call proposal or a plausible spoken promise does not establish completion.

For a necessary wait, use a brief, truthful acknowledgment when it helps the
caller. Avoid repeated fillers and fabricated progress. Decide how the agent can
respond to a new question while work continues, how it communicates a failure,
and when it checks whether the caller still wants the result. Measure first filler
and first substantive answer separately when evaluating responsiveness.

When the caller interrupts, identify whether they are acknowledging, correcting,
canceling, or starting a new request. A backchannel such as "uh-huh" can mean
"continue." The runtime's turn/interruption policy needs to support the intended
behavior. In LiveKit, realtime provider-side detection and framework-side handling
have different control surfaces; verify the active owner before assuming prompt
wording or a framework setting changes the result.
[Source: LiveKit turn handling](https://docs.livekit.io/agents/logic/turns.md).

Track the pending action's status and suppress stale results before acting on a
new intent. Acknowledge the user while a slow operation remains unresolved; do not
claim its outcome or repeat a write until its status is established. Speech stopped,
generation stopped, tool work canceled, and action rolled back are distinct states.
The current LiveKit tool docs describe background work continuing after an
interruption unless cancellation reaches that work. Define which reads may be
canceled, which writes must finish, and how to check a result that arrives late.
Keep critical non-interruptible sections short and authorized; avoid suppressing
the caller throughout a long lookup. [Source: LiveKit function tools](https://docs.livekit.io/agents/logic/tools/definition.md#interruptions).

After interruption, the next reply must use the caller's new intent and the portion
of agent speech actually delivered. Preserve committed action state even if its
confirmation was cut off. Say the relevant outcome once, then address the correction.

Prompt instructions cannot replace runtime cancellation, tool authorization,
idempotency, or transcript/state handling. Identify required implementation changes
separately instead of implying that more wording fixes those mechanisms.

## Define handoffs and ending

Specify when to transfer: an explicit request, work beyond the agent's authority,
repeated failed repair, or the application's escalation rule. Establish a real
destination and a fallback for unavailable recipients. Passing control to another
software agent and connecting a caller to a human have different evidence of
success; test the applicable path.

Carry the task, confirmed details, unresolved issue, pending actions, and relevant
action IDs into the handoff. Send only context the recipient needs and may receive.
Tell the caller what will happen, and claim a connection only after transfer state
confirms it. If it fails, return to a supported next step. A farewell needs a
call-end rule that accounts for queued audio and unresolved actions; inspect and
use the runtime's playback-completion and shutdown mechanisms.
[Source: LiveKit speech control](https://docs.livekit.io/agents/multimodality/audio/).

## Test the spoken result

Use realistic dialogs with hesitation, corrections, interruption, unknown answers,
and failed or late tool results. Include a multi-turn dialog so repeated openers
and unnecessary confirmation become visible. The following are illustrative test
inputs, not claims about an existing application:

- A caller changes the requested day while the lookup is running. The agent uses
  the corrected day and does not announce the stale result.
- A caller says "actually, cancel that" just after a write commits. The agent
  checks status and explains the supported cancellation path without claiming rollback.
- A caller asks for a human while a transfer destination is unavailable. The agent
  explains the failure and offers the configured alternative.
- A caller says "uh-huh" halfway through an answer. The expected continuation or
  interruption is explicit and verified under the active turn policy.

Check task success, question order, truthful progress, repair burden, and intelligible
speech. Read examples aloud. When the actual TTS voice is available and authorized,
check abbreviations, currency, names, pronunciation, pauses, and long answers using
that voice. Do not rely on text formatting to establish audible behavior.

Treat text simulations as prompt checks. Qualify any claim about real interruption
behavior or audio quality until tested on the media path. Use the
[evaluation skill](../voice-agent-evaluation/SKILL.md) to select the evidence layer
and keep live tests within the user's scope.

## Deliver

The revised prompt, the material changes and their purpose, short test dialogs
with outcomes, and any runtime dependencies or unresolved business rules. Separate
expected outcomes from observed results, including any dialogs that were designed
but not run.

## Source review

Documentation reviewed on 2026-09-30 UTC. This date records the review; publication
dates were not established for the linked documentation. The conversation rules
above require the application's actual policy and tool behavior. Verify runtime
APIs and provider-specific interruption semantics against the installed versions.
