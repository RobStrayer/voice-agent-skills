<div align="center">

# 🎙 NL Voice Skills

### Next Level Voice Skills

**Skills for the agents that build voice agents.**

Practical instructions for speech, conversation, telephony, and the engineering between them.

![Bundled skills: 32](https://img.shields.io/badge/bundled_skills-32-6366f1?style=flat-square)
![Original foundations: 5](https://img.shields.io/badge/original_foundations-5-0891b2?style=flat-square)
![Resource projects: 43](https://img.shields.io/badge/resource_projects-43-059669?style=flat-square)
![Original material: MIT](https://img.shields.io/badge/original_material-MIT-475569?style=flat-square)

[Find a skill](#find-a-skill) · [Choose an architecture](#choose-an-architecture) · [Get started](#get-started) · [Resource library](docs/resources.md)

</div>

---

Voice agents have to listen, take turns, act, and recover while someone is waiting
on the other end. This collection helps a coding agent work through those details.
It brings together original engineering guides and skills from the people who
maintain the underlying platforms.

**Reviewed September 30, 2026 (UTC).** Provider links lead to their original
repositories' current default branches. The five NL foundations are maintained
here. The 27 bundled provider copies remain dated reference snapshots with
licenses and file hashes. Additional skills are organized in a separate
[upstream index](docs/more-skills.md), including language variants and optional
workflows. These counts describe files and projects, not independent capabilities.

## Find a skill

| Your task | Start here |
| --- | --- |
| Choose a stack and justify the tradeoffs | [Stack selection](skills/foundations/voice-stack-selection/SKILL.md) · [Architecture guide and decision worksheet](skills/foundations/voice-stack-selection/references/architecture-guide.md) |
| Design a conversation people can follow | [Conversation design](skills/foundations/voice-conversation-design/SKILL.md) |
| Explain slow responses or awkward interruptions | [Latency audit](skills/foundations/voice-latency-audit/SKILL.md) |
| Fix silence, distorted audio, or one-way calls | [Media debugging](skills/foundations/voice-media-debugging/SKILL.md) |
| Test conversation behavior and tool correctness | [Evaluation](skills/foundations/voice-agent-evaluation/SKILL.md) · [Coval workflows](docs/more-skills.md#evaluation-and-local-speech) |
| Build with LiveKit or Pipecat | [LiveKit builder](https://github.com/livekit/agent-skills/blob/main/skills/building-livekit-agents/SKILL.md) · [Pipecat init](https://github.com/pipecat-ai/skills/blob/main/skills/init/SKILL.md) |
| Use a hosted voice agent platform | [ElevenLabs](https://github.com/elevenlabs/skills/blob/main/agents/SKILL.md) · [Cartesia Line](https://github.com/cartesia-ai/skills/blob/main/skills/cartesia-line/SKILL.md) · [More platforms](docs/more-skills.md) |
| Build with Azure Voice Live or Gemini Live | [Cloud voice skills](docs/more-skills.md#cloud-voice-and-speech) |
| Connect phone calls, SIP, or browser audio | [Twilio ConversationRelay](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-voice-conversation-relay/SKILL.md) · [Telnyx and other carriers](docs/more-skills.md) |
| Add recognition, synthesis, or local speech | [Deepgram and AssemblyAI](docs/more-skills.md) · [OpenAI speech](https://github.com/openai/skills/blob/main/skills/.curated/speech/SKILL.md) · [Local models](docs/resources.md#local-speech-synthesis-and-audio-inference) |

### Two catalogs, one source policy

| Catalog | What you will find |
| --- | --- |
| [Core skills](docs/catalog.md) | Five original foundations and 27 provider skills from LiveKit, ElevenLabs, Twilio, Pipecat, Cartesia, and OpenAI. Original links appear beside optional snapshots. |
| [More upstream skills](docs/more-skills.md) | Voice-specific source links for Telnyx, Deepgram, Vapi, AssemblyAI, Microsoft, Google, NVIDIA, Coval, Moonshine, Voximplant, Synthflow, and Shiny. Language variants are grouped by task. |
| [Runtime resources](docs/resources.md) | 43 frameworks, models, evaluation tools, media utilities, and learning projects, with dated stars and license qualifications. |

A skill guides your coding agent. A runtime framework or model becomes part of
your application. Some source repositories contain both; the catalogs say which
one you are looking at.

## Choose an architecture

Start with the conversation and operational constraints, then compare two
plausible designs using the same tasks and audio path. A responsive demo alone
cannot tell you how a system handles tool failures, noisy callers, transfers,
or many simultaneous sessions.

| Decision | What to establish before committing |
| --- | --- |
| Realtime speech model or STT → LLM → TTS pipeline | How much control you need over recognized text, speech output, model choice, and interruption behavior. Measure the actual streaming path. |
| Managed platform or application-owned orchestration | Who owns session state, turn detection, tool execution, retries, observability, and incident response. |
| Browser, mobile, or telephone transport | The required media contract, network traversal, codecs, call routing, and where credentials can safely live. |
| Tool execution and human handoff | What may happen during an interruption, which actions need confirmation, how duplicate work is prevented, and what context a human receives. |
| Hosting, cost, and migration | Regions, data handling, concurrency limits, compute and call costs, failover behavior, and the boundaries you can replace later. |

The [architecture guide](skills/foundations/voice-stack-selection/references/architecture-guide.md)
works through those choices, including hybrid designs, conditional examples,
failure cases, a proof-of-concept plan, and a decision record. It separates
provider-documented behavior from engineering recommendations. Use the
[evaluation skill](skills/foundations/voice-agent-evaluation/SKILL.md) to define
what would make you change your mind.

## Get started

1. Choose the skill for the work in front of you and open its original source.
2. Check its prerequisites and current installation instructions. Install the
   **whole skill folder**, including references and scripts. Some SDK skills also
   depend on files elsewhere in their source repository.
3. Invoke it by its frontmatter name using your coding agent's skill syntax.
4. Start with fixtures or mocked tools, then test the authorized real media path.

```sh
git clone https://github.com/RBStrayer/nl-voice-skills.git
```

For an architecture review:

> Use voice-stack-selection to compare two designs for a multilingual phone assistant. Include interruptions during a booking tool, transfer failure, cost, and evidence needed before choosing.

For a media fault:

> Use voice-media-debugging to explain why this connected call is silent. Inspect the negotiated formats, transport counters, and playback result before changing the model.

[Usage notes](docs/usage.md) cover host compatibility, dependencies, and concrete
source caveats. Installing instructions does not itself authorize dialing,
recording, spending, deploying, or changing a provider account.

## Explore the stack

| Work area | Selected starting points |
| --- | --- |
| Orchestration | [LiveKit Agents](https://github.com/livekit/agents), [Pipecat](https://github.com/pipecat-ai/pipecat), [OpenAI Agents SDK](https://github.com/openai/openai-agents-js), [Bolna](https://github.com/bolna-ai/bolna) |
| Turn taking | [Silero VAD](https://github.com/snakers4/silero-vad), [Smart Turn](https://github.com/pipecat-ai/smart-turn), [eot-bench](https://github.com/livekit/eot-bench) |
| Local recognition | [Whisper](https://github.com/openai/whisper), [faster-whisper](https://github.com/SYSTRAN/faster-whisper), [Moonshine](https://github.com/moonshine-ai/moonshine), [Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR) |
| Local synthesis | [Kokoro](https://github.com/hexgrad/kokoro), [Chatterbox](https://github.com/resemble-ai/chatterbox), [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) |
| Speech models | [Ultravox](https://github.com/fixie-ai/ultravox), [Moshi](https://github.com/kyutai-labs/moshi), [Kyutai STT/TTS](https://github.com/kyutai-labs/delayed-streams-modeling) |
| Media and telephone infrastructure | [Pion](https://github.com/pion/webrtc), [coturn](https://github.com/coturn/coturn), [jambonz](https://github.com/jambonz/jambonz-feature-server), [SIPp](https://github.com/SIPp/sipp) |
| Evaluation and traces | [EVA](https://github.com/ServiceNow/eva), [Coval skills](https://github.com/coval-ai/coval-external-skills), [Langfuse](https://github.com/langfuse/langfuse), [Phoenix](https://github.com/Arize-ai/phoenix) |

The [full library](docs/resources.md) explains each project's role, limitations,
licenses, current documentation, and community discovery sources. Stars are dated
signals of adoption. They are not a quality ranking, and code licenses do not
necessarily cover model weights, voices, datasets, or hosted services.

## Freshness and maintenance

This review used **Context7 plus current primary documentation**, with direct
source checks where the index was missing or stale. Retrieval dates are distinct
from provider publication dates. [Documentation review](docs/documentation-review.md)
records those checks and the contradictions found. Examples include changed
Pipecat installation commands, outdated SDK constants, and model-license summaries
that no longer match the current source.

A daily review is configured in the maintainer's Codex workspace for **9:00 a.m.
America/New_York**. It checks original sources and releases, makes supported
updates, validates them, and pushes to this private repository. That scheduler
and its authentication are external to the repository; cloning it does not
install an automation. [Maintenance procedure](docs/maintenance.md).

```sh
python scripts/verify.py
python scripts/test_verify.py
```

These checks cover recorded source hashes and licenses, skill structure, local
links, metadata consistency, and common credential patterns. They do not execute
provider APIs or establish production voice quality.

## Repository map

| Path | Contents |
| --- | --- |
| [skills/](skills/) | Original foundations and dated provider snapshots |
| [docs/catalog.md](docs/catalog.md) · [docs/more-skills.md](docs/more-skills.md) | Core and expanded skill indexes |
| [docs/resources.md](docs/resources.md) | Runtime components, official learning paths, and community leads |
| [sources.json](sources.json) | Snapshot commits, retained licenses, and copied-file hashes |
| [linked-skills.json](linked-skills.json) · [resources.json](resources.json) | Dated metadata for original source links and resource projects |
| [docs/research.md](docs/research.md) | Search coverage, exclusions, and verification limits |

Contributions should fill a concrete voice-engineering gap and link to the
original maintained source. See [CONTRIBUTING.md](CONTRIBUTING.md).

Original NL material is [MIT licensed](LICENSE). Copied upstream content retains
its own terms in [third-party notices](THIRD_PARTY_NOTICES.md).

Maintained by [Rob Strayer](https://github.com/RBStrayer).
