![Voice Agent Skills: skills, guides and diagrams for building AI voice agents people enjoy talking to. A sound wave runs from green listening bars through violet thinking dots to orange speaking bars.](assets/diagrams/hero.svg)

<p align="center">
  <a href="https://github.com/RobStrayer/voice-agent-skills/actions/workflows/verify.yml"><img alt="verify" src="https://github.com/RobStrayer/voice-agent-skills/actions/workflows/verify.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <a href="https://github.com/RobStrayer/voice-agent-skills/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/RobStrayer/voice-agent-skills"></a>
  <a href="docs/usage.md"><img alt="Works with Claude Code and Codex" src="https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex-6e56cf"></a>
  <a href="CONTRIBUTING.md"><img alt="Pull requests welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
</p>

A free, open collection for anyone building a voice AI agent: a phone receptionist,
a booking line, a browser assistant, or anything else people talk to. It has plain
guides for beginners, diagrams that show how the parts fit, and **skills** your
coding agent (Claude Code, Codex and others) can load to do the work properly.

**13 original skills · 27 bundled provider skills · 345 linked skills from 59 providers and authors · 43 runtime resources**

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

![A decision flowchart. No code: use a managed platform such as Vapi, Retell, ElevenAgents or Bland. Code and full control: use an open-source framework such as LiveKit Agents or Pipecat. Code for a browser or app: use a speech-to-speech API such as OpenAI GPT-Live or Gemini Live. Code for phone calls: use a phone provider plus your own code, such as Twilio ConversationRelay, Telnyx or Plivo.](assets/diagrams/where-to-start.svg)

The [getting started guide](docs/getting-started.md) links the official quickstart
for each path, and the [stack selection skill](skills/foundations/voice-stack-selection/SKILL.md)
walks your coding agent through the choice with you.

## Install the skills

A skill is a folder with a `SKILL.md` file that tells a coding agent how to do one
job well. Install them in whichever way suits your tools.

**Claude Code plugin marketplace**

```text
/plugin marketplace add RobStrayer/voice-agent-skills
/plugin install voice-foundations@voice-agent-skills
```

Provider plugins are also available: `voice-livekit`, `voice-pipecat`,
`voice-elevenlabs`, `voice-twilio`, `voice-cartesia` and `voice-openai-speech`.

**Any agent that supports the open skills format** (Claude Code, Codex and others)

```bash
npx skills add RobStrayer/voice-agent-skills --skill voice-turn-taking
```

**By hand:** copy a skill folder (the whole folder, not just `SKILL.md`) into
`~/.claude/skills/` for Claude Code or `~/.agents/skills/` for Codex (see the
[install guide](docs/usage.md) for older versions).

Then give the agent a real task and the evidence it needs:

> Use voice-turn-taking and voice-audio-frontends on this project. Callers get cut
> off when they pause, and the agent sometimes hears its own voice. Find where turn
> decisions and echo cancellation happen, then propose tests before changing any
> thresholds.

[Full install guide, including every plugin and host](docs/usage.md)

## Find a skill for the job

These thirteen skills are original to this repo and work with any provider.

| What you're working on | Skill |
| --- | --- |
| Choosing a platform, framework or speech model | [voice-stack-selection](skills/foundations/voice-stack-selection/SKILL.md) |
| Writing prompts for the ear, confirmations, repairs and handoffs | [voice-conversation-design](skills/foundations/voice-conversation-design/SKILL.md) |
| The agent cuts people off, or won't stop when interrupted | [voice-turn-taking](skills/foundations/voice-turn-taking/SKILL.md) |
| Echo, background noise, or quiet words going missing | [voice-audio-frontends](skills/foundations/voice-audio-frontends/SKILL.md) |
| Misheard names and numbers, pronunciation, streaming speech | [voice-speech-pipeline](skills/foundations/voice-speech-pipeline/SKILL.md) |
| Capturing phone numbers, emails, names and addresses correctly | [voice-data-capture](skills/foundations/voice-data-capture/SKILL.md) |
| Replies feel slow and you need to know where the time goes | [voice-latency-audit](skills/foundations/voice-latency-audit/SKILL.md) |
| Silent, one-way or garbled audio, codec and sample-rate errors | [voice-media-debugging](skills/foundations/voice-media-debugging/SKILL.md) |
| Phone numbers, transfers, dropped calls, scaling and deploys | [voice-call-reliability](skills/foundations/voice-call-reliability/SKILL.md) |
| Testing calls, tools and recovery before you ship | [voice-agent-evaluation](skills/foundations/voice-agent-evaluation/SKILL.md) |
| Working out the cost per minute before you commit | [voice-cost-estimation](skills/foundations/voice-cost-estimation/SKILL.md) |
| Consent, AI disclosure, calling hours and recording rules | [voice-phone-compliance](skills/foundations/voice-phone-compliance/SKILL.md) |
| Prompt injection, leaked keys, caller identity and abuse | [voice-agent-security](skills/foundations/voice-agent-security/SKILL.md) |

## Level up

![A four-step staircase. 1, Talk to it: voice-stack-selection. 2, Put it to work: voice-conversation-design, voice-turn-taking, voice-phone-compliance. 3, Own the pipeline: voice-speech-pipeline, voice-latency-audit, voice-audio-frontends, voice-media-debugging. 4, Run it for real: voice-agent-evaluation, voice-call-reliability, voice-agent-security, voice-cost-estimation.](assets/diagrams/learning-path.svg)

## Common problems

![The twenty problems builders hit most, in four groups with a one-line fix each. The conversation: knowing when the caller is done, caller trust, names and numbers, interruptions, echo and noise, languages. Actions and the phone: phone plumbing, tool calls, guardrails, handoffs, voicemail and spam labels, consent. Choosing: platform, cost, one model or a pipeline. Running it: latency, reliability, observability, testing, changing APIs.](assets/diagrams/common-problems.svg)

The [common problems guide](docs/common-problems.md) gives the cause of each one, the fixes builders report, sources, and the skill that helps.

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

The [linked skills index](docs/more-skills.md) points to 345 more skills from
59 providers and other authors. Most come from the provider itself; community and
third-party ones are marked. Every entry is pinned to a commit or file hash and
was checked against it. The [resource library](docs/resources.md) lists
frameworks, turn detectors, speech models and evaluation tools.

Here is where the major providers stand. Each number counts skills, with language
variants counted separately, and links to that provider in the index. Bundled
skills are copied here with their licenses. Linked skills stay with their
maintainer. None yet means no official voice-agent skill was found on September 30, 2026; the
index then names the core skills here that cover the same job. Smaller providers
are in the index's [A to Z list](docs/more-skills.md#find-your-provider).

| Job | Provider | Skills |
| --- | --- | --- |
| Phone and calling | Twilio | [6 bundled](docs/catalog.md#twilio) and [16 linked](docs/more-skills.md#twilio) |
| Phone and calling | Telnyx | [39](docs/more-skills.md#telnyx) |
| Phone and calling | Plivo | [6](docs/more-skills.md#plivo) |
| Phone and calling | Sinch | [6](docs/more-skills.md#sinch) |
| Phone and calling | SignalWire | [1](docs/more-skills.md#signalwire) |
| Phone and calling | Voximplant | [2](docs/more-skills.md#voximplant) |
| Browser and app audio | Agora and Daily | [1](docs/more-skills.md#agora) and [1](docs/more-skills.md#daily) |
| Phone and calling | Vonage, Bandwidth, LiveKit SIP | [none yet](docs/more-skills.md#major-providers-without-an-official-skill-yet-checked-sep-30-2026) |
| Agent platform | Vapi | [10](docs/more-skills.md#vapi) |
| Agent platform | Retell | [2](docs/more-skills.md#retell-ai) |
| Agent platform | Bland | [22](docs/more-skills.md#bland-ai) |
| Agent platform | ElevenAgents | [7 bundled](docs/catalog.md#elevenlabs) and [22 linked](docs/more-skills.md#elevenlabs) |
| Agent platform | Synthflow | [7](docs/more-skills.md#synthflow) |
| Agent platform | PolyAI | [6](docs/more-skills.md#polyai) |
| Agent platform | Ultravox | [1](docs/more-skills.md#ultravox) |
| Agent platform | Hume EVI, Microsoft Copilot Studio, Dialogflow CX | [none yet](docs/more-skills.md#major-providers-without-an-official-skill-yet-checked-sep-30-2026) |
| Speech-to-text | Deepgram | [39](docs/more-skills.md#deepgram) |
| Speech-to-text | AssemblyAI | [3](docs/more-skills.md#assemblyai) |
| Speech-to-text | Gladia | [6](docs/more-skills.md#gladia) |
| Speech-to-text | Speechmatics, Soniox, Google Cloud Speech-to-Text | [none yet](docs/more-skills.md#major-providers-without-an-official-skill-yet-checked-sep-30-2026) |
| Text-to-speech | Cartesia | [2 bundled](docs/catalog.md#cartesia) |
| Text-to-speech | Rime | [1](docs/more-skills.md#rime) |
| Text-to-speech | Inworld | [3](docs/more-skills.md#inworld) |
| Text-to-speech | Murf, Hume Octave, Google Cloud Text-to-Speech | [none yet](docs/more-skills.md#major-providers-without-an-official-skill-yet-checked-sep-30-2026) |
| Speech-to-speech | OpenAI GPT-Live and Realtime, xAI Grok voice | [none yet](docs/more-skills.md#major-providers-without-an-official-skill-yet-checked-sep-30-2026) (Gemini Live, Nova Sonic and Azure Voice Live are in the cloud rows) |
| Framework | LiveKit Agents | [7 bundled](docs/catalog.md#livekit) |
| Framework | Pipecat | [3 bundled](docs/catalog.md#pipecat) and [1 linked](docs/more-skills.md#pipecat) |
| Framework | jambonz | [3](docs/more-skills.md#jambonz) |
| Framework | Vision Agents and Zero Runtime | [1](docs/more-skills.md#vision-agents) and [3](docs/more-skills.md#zero-runtime) |
| Framework | TEN, OpenAI Agents SDK | [none yet](docs/more-skills.md#major-providers-without-an-official-skill-yet-checked-sep-30-2026) |
| Testing | Coval | [13](docs/more-skills.md#coval) |
| Testing | Cekura | [9](docs/more-skills.md#cekura) |
| Testing | Roark and Bluejay | [7](docs/more-skills.md#roark) and [7](docs/more-skills.md#bluejay) |
| Testing | Hamming | [none yet](docs/more-skills.md#major-providers-without-an-official-skill-yet-checked-sep-30-2026) |
| Cloud | AWS (Connect, Chime, Lex, Polly, Transcribe, Nova Sonic) | [15](docs/more-skills.md#aws) |
| Cloud | Azure (Voice Live, Speech, Communication Services) | [10](docs/more-skills.md#azure) |
| Cloud | Google (Gemini Live, CX Agent Studio, ADK) | [11](docs/more-skills.md#google) |

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

Maintained by [Rob Strayer](https://github.com/RobStrayer).
