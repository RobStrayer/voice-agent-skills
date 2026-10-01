# Build your first voice agent

[Home](../README.md) / Getting started

This page takes you from nothing to a voice agent you can talk to, then onto a
phone number, then to something you'd trust with real callers. No prior voice
experience needed. If a word is new, check the [glossary](glossary.md).

**On this page:** [How it works](#how-a-voice-agent-works) ·
[Pick a starting path](#pick-a-starting-path) · [Your first hour](#your-first-hour) ·
[Put it on a phone number](#put-it-on-a-phone-number) · [Write for the ear](#write-for-the-ear) ·
[Test it like a caller](#test-it-like-a-caller) · [What good feels like](#what-good-feels-like) ·
[What it costs](#what-it-costs) · [Where next](#where-next)

## How a voice agent works

![A caller's audio goes to three stages. Listen: voice activity, turn detection and speech-to-text. Think: language model, tools and conversation state. Speak: text-to-speech, streaming playback and barge-in handling. Reply audio streams back to the caller.](../assets/diagrams/voice-agent-anatomy.svg)

Every voice agent does three jobs, over and over, many times a minute:

1. **Listen.** Notice the caller is speaking, work out when they've finished, and
   turn their words into text.
2. **Think.** A language model decides what to say or do, and may call your tools
   (look up an order, book a slot).
3. **Speak.** Turn the reply into audio and play it, and stop at once if the
   caller talks over it.

The hard part isn't any one stage. It's making them hand off fast enough to feel
like a conversation, and making the whole thing behave when real people pause,
mumble, change their minds and interrupt.

## Pick a starting path

![Three ways to build the voice loop: a cascade of speech-to-text, a language model and text-to-speech; a single speech-to-speech model; and a hybrid with a speech model in front of an existing text workflow.](../assets/diagrams/speech-architectures.svg)

There are three common ways in. None is "the best"; they trade speed of setup
against control.

| Path | Pick it when | Time to first conversation | What you give up |
| --- | --- | --- | --- |
| **Managed platform** (Vapi, Retell, ElevenAgents, Bland and others) | You want a working phone agent fast, or you don't want to run servers | Minutes to an hour, often without code | A per-minute platform fee, and less control over each stage |
| **Open-source framework** (LiveKit Agents, Pipecat) | You're a developer who wants to pick every component, self-host, or tune latency and cost | An hour or two with a quickstart | You run and scale the agent yourself (or pay for their cloud) |
| **Speech-to-speech API** (OpenAI GPT-Live or Realtime, Gemini Live) | You want the most natural-sounding conversation in a browser or app prototype | An hour or so for a browser demo | Less control over each stage, and you build the phone and tool plumbing |

Not sure? Start with a managed platform to learn what a good call feels like.
Move to a framework when you hit a wall on cost, control or latency. Both
frameworks can also use a speech-to-speech model inside them, so this isn't a
one-way door. The [provider landscape](landscape.md) compares the options, and the
[stack selection skill](../plugins/voice-foundations/skills/voice-stack-selection/SKILL.md)
walks a coding agent through the decision with you.

## Your first hour

Follow the official quickstart for the path you picked. They change often, so
this page links to them instead of copying commands.

**Managed platform**

1. Sign up and create an agent from a template:
   [Vapi](https://docs.vapi.ai/quickstart) ·
   [Retell](https://docs.retellai.com/get-started/quick-start) ·
   [ElevenLabs ElevenAgents](https://elevenlabs.io/docs/eleven-agents/quickstart).
2. Write a short system prompt (see [write for the ear](#write-for-the-ear)).
3. Talk to it in the browser. Interrupt it. Pause mid-sentence. See what breaks.

**Open-source framework**

1. Run the quickstart:
   [LiveKit Agents](https://docs.livekit.io/agents/start/voice-ai/) ·
   [Pipecat](https://docs.pipecat.ai/pipecat/get-started/quickstart).
2. You'll need API keys for a speech-to-text, a language model and a
   text-to-speech provider (or one speech-to-speech model). The quickstarts
   suggest defaults.
3. Talk to it from the browser playground, then read the agent file top to bottom:
   it's the whole listen, think, speak loop in one place.

Using a coding agent? Install the vendor skills first so it follows current APIs:
`voice-livekit` or `voice-pipecat` from this repo's [marketplace](usage.md), or
straight from [LiveKit](https://github.com/livekit/agent-skills) and
[Pipecat](https://github.com/pipecat-ai/skills).

**Speech-to-speech API**

1. Read the provider guide:
   [OpenAI GPT-Live](https://developers.openai.com/api/docs/guides/live) ·
   [OpenAI Realtime](https://developers.openai.com/api/docs/guides/realtime) ·
   [OpenAI voice agents](https://developers.openai.com/api/docs/guides/voice-agents) ·
   [Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api).
2. Keep your API key on a server. Browsers connect with a short-lived token that
   your server issues. Never put a real key in front-end code. The
   [security skill](../plugins/voice-foundations/skills/voice-agent-security/SKILL.md) covers this.

## Put it on a phone number

![How a phone call reaches your agent: the phone network, a telephony provider, then one of three routes with more or less control, plus a separate call-control path.](../assets/diagrams/phone-call-path.svg)

- **Managed platforms** sell or import phone numbers directly. Click, pick a
  number, attach your agent.
- **Frameworks** connect through a SIP trunk or a provider's media stream:
  [LiveKit telephony](https://docs.livekit.io/telephony/) ·
  [Pipecat telephony](https://docs.pipecat.ai/pipecat/telephony/overview).
- **Your own server** can use a provider such as Twilio, Telnyx, Vonage or Plivo.
  With [Twilio ConversationRelay](https://www.twilio.com/docs/voice/conversationrelay),
  Twilio handles speech and your code only sees text.

Phone audio is usually narrowband (8 kHz), so recognition that worked in the browser can
get worse on a real call. Test on real phone calls early.

Calling people (outbound) is where most legal rules bite: consent, AI disclosure,
calling hours and spam labelling. Inbound calls have rules too. Recording or AI
transcription can need every caller's consent in some US states, and in the EU
callers must be told they're talking to an AI. Read the
[phone compliance skill](../plugins/voice-foundations/skills/voice-phone-compliance/SKILL.md)
before you dial anyone or record a call. It's orientation, not legal advice.

## Write for the ear

A voice prompt is not a chat prompt. People can't skim, scroll or re-read.

- **Keep replies short.** One or two sentences, then let the caller talk.
- **One question at a time.** "What's your name and date of birth?" gets half an answer.
- **No formatting.** No lists, markdown, emoji or URLs; they get read out literally.
- **Say numbers the way people say them.** "Two thirty p.m.", not "14:30".
- **Confirm what matters.** Read back names, dates, amounts and phone numbers before acting.
- **Say what you're doing.** "Let me check that" before a slow lookup, and only if it's true.
- **Plan the exits.** What happens when the agent doesn't know, or the caller wants a person?
- **Say it's an AI** in the first sentence of every call, and answer truthfully whenever someone asks.

```text
You are the booking assistant for Riverside Dental. You're talking on the phone.
Keep every reply to one or two short sentences. Ask one question at a time.
Never use lists, symbols or links. Say times like "two thirty p.m."
Before booking, read back the day, time and the caller's name and ask them to confirm.
If you can't help, offer to take a message or transfer to the front desk.
```

The [conversation design skill](../plugins/voice-foundations/skills/voice-conversation-design/SKILL.md)
goes much deeper: repairs, tool progress, confirmations and accessibility.

## Test it like a caller

Before you show it to anyone, call it and try these:

- [ ] Pause for two seconds mid-sentence. Does it cut you off?
- [ ] Interrupt it halfway through a long answer. Does it stop right away?
- [ ] Say "mm-hm" while it talks. Does it stop when it shouldn't?
- [ ] Spell your email address, then give a phone number and a street address.
- [ ] Change your mind: "Tuesday... actually Thursday."
- [ ] Call from a noisy room, and on speakerphone.
- [ ] Ask something it can't know. Does it admit that, or make something up?
- [ ] Ask for a person. Ask "are you a robot?"
- [ ] Stay silent for 20 seconds. Hang up in the middle of a booking.

Each failure maps to a skill: early cut-offs and barge-in to
[turn taking](../plugins/voice-foundations/skills/voice-turn-taking/SKILL.md), noise and echo to
[audio frontends](../plugins/voice-foundations/skills/voice-audio-frontends/SKILL.md), names and
numbers to [speech pipeline](../plugins/voice-foundations/skills/voice-speech-pipeline/SKILL.md),
made-up answers and missing exits to
[conversation design](../plugins/voice-foundations/skills/voice-conversation-design/SKILL.md).
When you're ready to automate these checks, use
[agent evaluation](../plugins/voice-foundations/skills/voice-agent-evaluation/SKILL.md). The
[common problems](common-problems.md) page lists the fixes that work.

## What good feels like

![An illustrative timeline of one reply: the caller stops talking at 0 ms, the turn is committed at 260 ms, the first phrase is ready at 720 ms, playback starts at 1,060 ms and useful words are heard at 1,120 ms.](../assets/diagrams/latency-budget.svg)

Speed is the thing people notice first. Some reference points:

- **People answer each other fast.** Across ten languages, the typical gap
  between a question and its answer is about 200 ms
  ([Stivers et al., 2009](https://www.pnas.org/doi/abs/10.1073/pnas.0903616106)).
  Gaps of 600 ms or more start to sound like hesitation or a "no"
  ([Levinson and Torreira, 2015](https://pmc.ncbi.nlm.nih.gov/articles/PMC4464110/)).
- **Phone agents are slower than that.** Twilio's published targets for a
  typical speech-to-text, model, text-to-speech agent are a median of about
  1.1 seconds from the caller going quiet to hearing the reply, with 1.4 seconds
  as the upper limit ([Twilio, November 2025](https://www.twilio.com/en-us/blog/developers/best-practices/guide-core-latency-ai-voice-agents)).
- **Real calls are slower than dashboards.** One independent test that recorded
  real phone calls to five managed platforms measured medians of 1.3 to 1.7
  seconds and 95th percentiles of 1.8 to 2.3 seconds, even with the end-of-turn
  wait cut to 0.1 seconds on three of them. The platforms' own numbers
  read about half a second faster than what the caller heard
  ([OpenBenchmarks, August 2026](https://openbenchmarks.com/voice-agent-latency)).

So a good first target is about a second, measured the way the caller hears it,
and watch the slow calls as well as the average. Often the biggest lever is how
long the agent waits to decide you've finished talking, not the model; Twilio's
guide above makes the same point. The
[latency audit skill](../plugins/voice-foundations/skills/voice-latency-audit/SKILL.md) shows
where your time goes, and the [turn taking skill](../plugins/voice-foundations/skills/voice-turn-taking/SKILL.md)
covers the waiting.

## What it costs

Expect roughly $0.05 to $0.14 a minute on a managed platform, before the phone
line. That is what one independent test measured from five platforms' own billing
on short test calls, with the carrier leg left out
([OpenBenchmarks](https://openbenchmarks.com/voice-agent-latency)). Advertised
prices usually cover one layer, and speech, the model, the voice and the phone
line can be billed separately. Before you promise anyone a price, run your own
numbers with the [cost estimation skill](../plugins/voice-foundations/skills/voice-cost-estimation/SKILL.md).

## Where next

![A four-step staircase. 1, Talk to it: voice-stack-selection. 2, Put it to work: voice-conversation-design, voice-turn-taking, voice-phone-compliance. 3, Own the pipeline: voice-speech-pipeline, voice-latency-audit, voice-audio-frontends, voice-media-debugging. 4, Run it for real: voice-agent-evaluation, voice-call-reliability, voice-agent-security, voice-cost-estimation.](../assets/diagrams/learning-path.svg)

- **Ideas for what to build, and what's hard:** [what to build](what-to-build.md)
- **Every provider, compared:** [provider landscape](landscape.md)
- **The problems everyone hits, and the fixes:** [common problems](common-problems.md)
- **All the skills:** [skill catalog](catalog.md) · [install them](usage.md)
