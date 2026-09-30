![Next Level Voice Skills: skills, guides and diagrams for building AI voice agents people enjoy talking to. A sound wave runs from green listening bars through violet thinking dots to orange speaking bars.](assets/diagrams/hero.svg)

[![verify](https://github.com/RBStrayer/nl-voice-skills/actions/workflows/verify.yml/badge.svg)](https://github.com/RBStrayer/nl-voice-skills/actions/workflows/verify.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A free, open collection for anyone building a voice AI agent: a phone receptionist,
a booking line, a browser assistant, or anything else people talk to. It has plain
guides for beginners, diagrams that show how the parts fit, and **skills** your
coding agent (Claude Code, Codex and others) can load to do the work properly.

**12 original skills · 27 bundled provider skills · LINKED_TOTAL linked official skills from LINKED_PROVIDERS providers · 43 runtime resources**

## Start here

| If you are… | Go to |
| --- | --- |
| New to voice agents | [Build your first voice agent](docs/getting-started.md): how it works, a first hour, a phone number, a test checklist |
| Deciding what to build | [What to build](docs/what-to-build.md): use cases ranked by difficulty and value |
| Choosing providers | [Provider landscape](docs/landscape.md): platforms, frameworks, speech APIs and phone carriers compared |
| Stuck on a problem | [Common problems](docs/common-problems.md): symptom, cause, fix and the skill that helps |
| Ready to hand work to a coding agent | [Install the skills](#install-the-skills) |

## How a voice agent works

![A caller's audio goes to three stages. Listen: voice activity, turn detection and speech-to-text. Think: language model, tools and conversation state. Speak: text-to-speech, streaming playback and barge-in handling. Reply audio streams back to the caller.](assets/diagrams/voice-agent-anatomy.svg)

Every voice agent listens, thinks and speaks, many times a minute. The hard part
is making those stages hand off fast enough to feel like a conversation, and
making the whole thing behave when real people pause, mumble, change their minds
and interrupt. That is what this repo is about.

## Where should you start?

![A decision flowchart. No code: use a managed platform such as Vapi, Retell, ElevenLabs Agents or Synthflow. Code and full control: use an open-source framework such as LiveKit Agents or Pipecat. Code for a browser or app: use a speech-to-speech API such as OpenAI Realtime or Gemini Live. Code for phone calls: use a phone provider plus your own code, such as Twilio ConversationRelay, Telnyx or Plivo.](assets/diagrams/where-to-start.svg)

The [getting started guide](docs/getting-started.md) links the official quickstart
for each path, and the [stack selection skill](skills/foundations/voice-stack-selection/SKILL.md)
walks your coding agent through the choice with you.

## Install the skills

A skill is a folder with a `SKILL.md` file that tells a coding agent how to do one
job well. Install them in whichever way suits your tools.

**Claude Code plugin marketplace**

```text
/plugin marketplace add RBStrayer/nl-voice-skills
/plugin install voice-foundations@nl-voice-skills
```

Provider plugins are also available: `voice-livekit`, `voice-pipecat`,
`voice-elevenlabs`, `voice-twilio`, `voice-cartesia` and `voice-openai-speech`.

**Any agent that supports the open skills format** (Claude Code, Codex and others)

```bash
npx skills add RBStrayer/nl-voice-skills --skill voice-turn-taking
```

**By hand:** copy a skill folder (the whole folder, not just `SKILL.md`) into
`~/.claude/skills/` for Claude Code or `~/.codex/skills/` for Codex.

Then give the agent a real task and the evidence it needs:

> Use voice-turn-taking and voice-audio-frontends on this project. Callers get cut
> off when they pause, and the agent sometimes hears its own voice. Find where turn
> decisions and echo cancellation happen, then propose tests before changing any
> thresholds.

[Full install guide, including every plugin and host](docs/usage.md)

## Find a skill for the job

These twelve skills are original to this repo and work with any provider.

| What you're working on | Skill |
| --- | --- |
| Choosing a platform, framework or speech model | [voice-stack-selection](skills/foundations/voice-stack-selection/SKILL.md) |
| Writing prompts for the ear, confirmations, repairs and handoffs | [voice-conversation-design](skills/foundations/voice-conversation-design/SKILL.md) |
| The agent cuts people off, or won't stop when interrupted | [voice-turn-taking](skills/foundations/voice-turn-taking/SKILL.md) |
| Echo, background noise, or quiet words going missing | [voice-audio-frontends](skills/foundations/voice-audio-frontends/SKILL.md) |
| Misheard names and numbers, pronunciation, streaming speech | [voice-speech-pipeline](skills/foundations/voice-speech-pipeline/SKILL.md) |
| Replies feel slow and you need to know where the time goes | [voice-latency-audit](skills/foundations/voice-latency-audit/SKILL.md) |
| Silent, one-way or garbled audio, codec and sample-rate errors | [voice-media-debugging](skills/foundations/voice-media-debugging/SKILL.md) |
| Phone numbers, transfers, dropped calls, scaling and deploys | [voice-call-reliability](skills/foundations/voice-call-reliability/SKILL.md) |
| Testing calls, tools and recovery before you ship | [voice-agent-evaluation](skills/foundations/voice-agent-evaluation/SKILL.md) |
| Working out the cost per minute before you commit | [voice-cost-estimation](skills/foundations/voice-cost-estimation/SKILL.md) |
| Consent, AI disclosure, calling hours and recording rules | [voice-phone-compliance](skills/foundations/voice-phone-compliance/SKILL.md) |
| Prompt injection, leaked keys, caller identity and abuse | [voice-agent-security](skills/foundations/voice-agent-security/SKILL.md) |

## Level up

![A four-step staircase from Talk to it through Put it to work and Own the pipeline to Run it for real, each step listing the repo skills that help.](assets/diagrams/learning-path.svg)

## Common problems

| What you notice | Usually because | Start with |
| --- | --- | --- |
| It talks over people or cuts them off mid-thought | The end-of-turn decision fires on a pause | [voice-turn-taking](skills/foundations/voice-turn-taking/SKILL.md) |
| It keeps talking when the caller interrupts | Playback isn't stopped and flushed on barge-in | [voice-turn-taking](skills/foundations/voice-turn-taking/SKILL.md) |
| It interrupts itself on speakerphone | Its own voice leaks back in without echo cancellation | [voice-audio-frontends](skills/foundations/voice-audio-frontends/SKILL.md) |
| Replies take too long | Waiting, model time and audio buffering add up | [voice-latency-audit](skills/foundations/voice-latency-audit/SKILL.md) |
| Emails, names and numbers come out wrong | Phone audio is narrowband and the prompt never confirms | [voice-speech-pipeline](skills/foundations/voice-speech-pipeline/SKILL.md) |
| Silence or robot noise on real phone calls | Wrong codec, sample rate or framing at a boundary | [voice-media-debugging](skills/foundations/voice-media-debugging/SKILL.md) |

[All common problems and fixes](docs/common-problems.md)

## Provider skills

Six provider collections are bundled here as dated copies, each linked to its
maintained original:

| Collection | What's in it |
| --- | --- |
| [LiveKit](https://github.com/livekit/agent-skills) | Build, debug, test, simulate and operate LiveKit agents |
| [Pipecat](https://github.com/pipecat-ai/skills) | Start and deploy Pipecat projects, talk to agents through MCP |
| [ElevenLabs](https://github.com/elevenlabs/skills) | Conversational agents, speech-to-text, text-to-speech, dubbing, voice changing and isolation |
| [Twilio](https://github.com/twilio/ai) | Voice architecture, ConversationRelay, TwiML, outbound calls, conferences, recordings |
| [Cartesia](https://github.com/cartesia-ai/skills) | Speech API integration and Line agent workflows |
| [OpenAI](https://github.com/openai/skills) | Speech generation and transcription from files (not a realtime agent runtime) |

The [linked skills index](docs/more-skills.md) points to LINKED_TOTAL more official
skills from LINKED_PROVIDERS providers, including Telnyx, Vapi, Retell, Deepgram,
AssemblyAI, Plivo, Sinch, SignalWire, AWS, Azure and testing platforms. Every entry
is pinned to a commit or file hash and was checked against it. The [resource library](docs/resources.md)
lists frameworks, turn detectors, speech models and evaluation tools.

## Go deeper

| Guide | What it covers |
| --- | --- |
| [How a voice call really works](docs/walkthrough.md) | One conversation followed from capture to playback, actions, phone routing and tests |
| [Engineering handbook](docs/handbook.md) | Every work area with its deep guide and skill |
| [Glossary](docs/glossary.md) | Barge-in, endpointing, SIP, μ-law and every other term, in plain English |
| [Skill catalog](docs/catalog.md) | All bundled skills with their sources |
| [Diagram style](docs/diagram-style.md) | How the figures are made, so you can edit or add one |

## Contributing

Corrections, new skills and better diagrams are welcome. Read the
[contributing guide](CONTRIBUTING.md), then run `python scripts/verify.py` before
opening a pull request; it checks sources, licenses, links and figures.

Original material is [MIT licensed](LICENSE). Bundled provider copies keep their
own licenses; see [third-party notices](THIRD_PARTY_NOTICES.md).

Maintained by [Rob Strayer](https://github.com/RBStrayer).
