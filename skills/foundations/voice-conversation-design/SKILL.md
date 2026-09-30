---
name: voice-conversation-design
description: Write and evaluate voice agent prompts for spoken turn taking, concise responses, clarification, tool progress, interruptions, and safe handoffs.
license: MIT
---

# Voice conversation design

Design for someone listening in real time. Establish the agent's task, audience,
entry channel, languages, tools, and escalation destination. Read the current
prompt and actual tool contracts before rewriting them.

## Write the conversation contract

Keep identity, allowed work, authoritative knowledge, tool rules, turn behavior,
and completion criteria explicit. Separate speaking style from business policy.
Use short spoken examples that illustrate an otherwise ambiguous instruction.
Do not impose a persona or catchphrase the user did not request.

Prefer one useful question at a time. Give a direct answer before optional detail.
Avoid spoken Markdown, URLs, raw JSON, and long lists unless the caller needs
them. Spell or confirm critical names, numbers, dates, and identifiers when a
mishearing could change an action; do not repeatedly confirm low-impact facts.

## Keep speech synchronized with actions

- Do not say an action succeeded until its tool result establishes success.
- For a necessary wait, use a brief truthful acknowledgment; avoid repeated fillers.
- If a caller interrupts, respond to the new intent and reconcile any pending tool.
- Define when to clarify, decline unsupported work, or transfer to a human.
- Define an actual completion or call-end condition, including pending actions.

Prompt instructions cannot replace runtime cancellation, tool authorization,
idempotency, or transcript/state handling. Identify required implementation changes
separately instead of implying that more wording fixes those mechanisms.

## Test the spoken result

Use realistic dialogs with hesitation, corrections, interruption, unknown answers,
and a failed tool. Check task success, natural question order, truthful progress,
and intelligibility when read aloud. Use the actual TTS voice when available and
authorized; punctuation and abbreviations can sound different than they look.

Treat text simulations as prompt checks. Qualify any claim about real interruption
behavior or audio quality until tested on the media path. Preserve the user's
scope and previously accepted voice identity.

## Deliver

The revised prompt, the material changes and their purpose, short test dialogs
with outcomes, and any runtime dependencies or unresolved business rules.

## Primary starting points

- [OpenAI Realtime prompting](https://developers.openai.com/api/docs/guides/realtime-prompting)
- [ElevenLabs agents](https://elevenlabs.io/docs/agents-platform/overview)
