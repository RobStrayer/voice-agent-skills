<div align="center">

# 🎙 NL Voice Skills

### Next Level Voice Skills

**Skills for the agents that build voice agents.**

A curated workbench for realtime conversation, speech, telephony, and voice agent engineering.

![Skills: 31](https://img.shields.io/badge/skills-31-6366f1?style=flat-square)
![Upstream providers: 6](https://img.shields.io/badge/upstream_providers-6-0891b2?style=flat-square)
![Resources: 28](https://img.shields.io/badge/resources-28-059669?style=flat-square)
![Original material: MIT](https://img.shields.io/badge/original_material-MIT-475569?style=flat-square)

[Choose a skill](#choose-a-skill) · [Get started](#get-started) · [Explore the stack](#explore-the-stack) · [Full catalog](docs/catalog.md) · [Contribute](CONTRIBUTING.md)

</div>

---

Building a voice agent means getting a lot of details right: streaming audio, turn
taking, tool calls, phone connections, spoken responses, and the moments when things
fail. NL Voice Skills brings practical instructions for that work into one place.

**31 ready-to-browse skills:** 27 official upstream skills from six providers,
with their supporting files and licenses, plus four original skills for engineering
across providers. A separate library covers 28 frameworks, models, and tools,
along with official documentation and community discoveries.

These skills guide a coding or operations agent. The frameworks and models in the
resource library are the components that run your voice application.

## Choose a skill

| I want to… | Start with |
| --- | --- |
| Choose the right voice architecture | [Voice stack selection](skills/foundations/voice-stack-selection/SKILL.md) |
| Build a LiveKit agent | [Building LiveKit agents](skills/livekit/building-livekit-agents/SKILL.md) |
| Create a Pipecat project | [Pipecat init](skills/pipecat/init/SKILL.md) |
| Build an ElevenLabs conversational agent | [ElevenLabs agents](skills/elevenlabs/agents/SKILL.md) |
| Build with Cartesia speech or Line | [Cartesia API](skills/cartesia/cartesia-api/SKILL.md) · [Cartesia Line](skills/cartesia/cartesia-line/SKILL.md) |
| Connect a phone conversation to an AI agent | [Twilio ConversationRelay](skills/twilio/twilio-voice-conversation-relay/SKILL.md) |
| Generate speech or transcribe audio | [OpenAI speech](skills/openai/speech/SKILL.md) · [OpenAI transcribe](skills/openai/transcribe/SKILL.md) |
| Make spoken conversations feel natural | [Voice conversation design](skills/foundations/voice-conversation-design/SKILL.md) |
| Diagnose slow responses and interruptions | [Voice latency audit](skills/foundations/voice-latency-audit/SKILL.md) · [LiveKit debugging](skills/livekit/debugging-livekit-agents/SKILL.md) |
| Test real conversation behavior | [Voice agent evaluation](skills/foundations/voice-agent-evaluation/SKILL.md) · [LiveKit testing](skills/livekit/testing-livekit-agents/SKILL.md) |

## The collection

| Collection | Skills | What it covers | Source license |
| --- | ---: | --- | --- |
| [Foundations](docs/catalog.md#foundations) | 4 | Stack decisions, conversation design, latency, evaluation | MIT |
| [LiveKit](docs/catalog.md#livekit) | 7 | Docs, building, debugging, tests, scenarios, simulations, operations | MIT |
| [ElevenLabs](docs/catalog.md#elevenlabs) | 7 | Agents, speech engine, STT, TTS, voice isolation, voice conversion, dubbing | MIT |
| [Twilio](docs/catalog.md#twilio) | 6 | Agent architecture, ConversationRelay, TwiML, outbound calls, recordings, conferences | MIT |
| [Pipecat](docs/catalog.md#pipecat) | 3 | Initialize, deploy, and talk to a Pipecat agent | BSD-2-Clause |
| [Cartesia](docs/catalog.md#cartesia) | 2 | Speech API and Line agents | MIT |
| [OpenAI](docs/catalog.md#openai) | 2 | Speech generation and transcription with diarization | Apache-2.0 |

Browse [all 31 skills and their prerequisites](docs/catalog.md). Upstream snapshots
are pinned to immutable commits; [sources.json](sources.json) records origins,
licenses, and file checksums.

The [existing skill discovery index](docs/local-skills.md) also covers all 80
distinct voice-related skill names found during the local inventory, including
specialist packs and useful operational helpers.

### More skill packs worth exploring

- [Deepgram skills](https://github.com/deepgram/skills): speech recognition, speech
  synthesis, voice agents, and debugging workflows.
- [Vapi skills](https://github.com/VapiAI/skills): agents, tools, phone numbers,
  integrations, and platform workflows.
- [Twilio's full AI collection](https://github.com/twilio/ai): additional integration
  skills that can complement the voice subset here.
- [ElevenLabs Agents documentation](https://elevenlabs.io/docs/agents-platform/overview):
  specialist topics such as evaluation, procedures, tools, and production operations.

Deepgram and Vapi are indexed as external collections while complete redistribution
terms are unresolved. The [research notes](docs/research.md) explain the selection,
local inventory, exclusions, and source coverage.

## Get started

1. Pick the skill that matches your task. Read its description and prerequisites.
2. Clone this repo, or download the selected folder using authenticated GitHub access.
3. Copy the **whole skill folder** into your agent's supported skill directory.
   Keep references, scripts, metadata, and assets beside `SKILL.md`.
4. Invoke the skill by its frontmatter name, using your agent's skill syntax.

```sh
git clone https://github.com/RBStrayer/nl-voice-skills.git
```

For example, select `skills/livekit/building-livekit-agents/` and ask your agent:

> Use building-livekit-agents to add a browser voice assistant with a mocked booking tool.

For a provider-neutral review:

> Use voice-latency-audit to explain response delay from these traces. Separate measured stages from missing playback evidence.

Install only the skills you need. Provider skills may require a CLI, documentation
MCP, SDK, or credentials. [Usage notes](docs/usage.md) explain those dependencies
and snapshot caveats. Installing a skill grants no permission to dial, spend,
record, deploy, or change a live account.

## Explore the stack

### Frameworks and realtime agents

| Project | Useful for | Stars* |
| --- | --- | ---: |
| [Pipecat](https://github.com/pipecat-ai/pipecat) | Composable streaming speech pipelines and transports | 16,017 |
| [LiveKit Agents](https://github.com/livekit/agents) | Voice agents over WebRTC and SIP, with provider integrations | 14,427 |
| [OpenAI Agents SDK, TypeScript](https://github.com/openai/openai-agents-js) | Realtime agents, tools, and browser/server connections | 3,880 |
| [Hugging Face speech-to-speech](https://github.com/huggingface/speech-to-speech) | Exploring a local speech pipeline | See resource library |

### Go deeper

- **Conversation timing:** [Silero VAD](https://github.com/snakers4/silero-vad),
  [Smart Turn](https://github.com/pipecat-ai/smart-turn),
  [eot-bench](https://github.com/livekit/eot-bench).
- **Speech recognition:** [Whisper](https://github.com/openai/whisper),
  [faster-whisper](https://github.com/SYSTRAN/faster-whisper),
  [whisper.cpp](https://github.com/ggml-org/whisper.cpp).
- **Speech synthesis:** [Kokoro](https://github.com/hexgrad/kokoro),
  [F5-TTS](https://github.com/SWivid/F5-TTS),
  [Piper](https://github.com/OHF-Voice/piper1-gpl).
- **Telephony:** [Twilio Media Streams](https://github.com/twilio/media-streams),
  [jambonz](https://github.com/jambonz/jambonz-feature-server),
  [drachtio-srf](https://github.com/drachtio/drachtio-srf).
- **Tracing and evaluation:** [Langfuse](https://github.com/langfuse/langfuse),
  [Phoenix](https://github.com/Arize-ai/phoenix), plus the voice-specific timing
  and test guidance in this collection.

**[Open the full resource library →](docs/resources.md)** for all 28 projects,
licenses, official learning paths, benchmarks, and Reddit/community discovery links.

*Stars are a dated discovery signal, not a quality ranking. Snapshot: September 29,
2026 (America/New_York). Exact observation times and sources are in
[resources.json](resources.json). Framework, model-weight, and hosted-service terms
can differ; qualifications are recorded in the resource library.*

## Repository layout

```text
skills/
  foundations/    Cross-provider engineering skills
  livekit/        Agent lifecycle and realtime conversation
  elevenlabs/     Voice agents and speech workflows
  twilio/         Phone calls and voice infrastructure
  pipecat/        Pipeline project workflows
  cartesia/       Speech API and Line agents
  openai/         Speech and transcription
docs/
  catalog.md      Every skill and its prerequisites
  local-skills.md Existing skill names and public counterparts
  resources.md    Frameworks, models, tools, and learning paths
  usage.md        Portability and runtime notes
  research.md     Curation method and coverage
licenses/         Preserved upstream licenses
sources.json      Pinned skill origins and file checksums
resources.json    Resource metadata and dated evidence
scripts/verify.py Local collection checks
```

## Curation and contribution

Selection favors practical voice-specific work, credible maintainers, usable
instructions, supporting material, and clear provenance. Community discussion and
stars help find candidates; direct source inspection decides what belongs here.

Run `python scripts/verify.py` to check the collection locally. See
[CONTRIBUTING.md](CONTRIBUTING.md) to propose a skill or resource.

Original NL Voice Skills material is [MIT licensed](LICENSE). Upstream material
retains its own terms; see [third-party notices](THIRD_PARTY_NOTICES.md).

Maintained by [Rob Strayer](https://github.com/RBStrayer).
