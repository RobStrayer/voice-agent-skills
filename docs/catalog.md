# Skill catalog

[Home](../README.md) / [Engineering handbook](handbook.md) / Core skills

**36 bundled skills** · **9 original foundations** · **27 provider skills**

Choose a foundation for the engineering problem, then a provider skill for the implementation. All provider names below open the original maintained source; **Snapshot** opens the dated copy kept here.

Reviewed: **2026-09-30 UTC**. [More upstream skills](more-skills.md) cover additional providers and language-specific SDKs. [Usage notes](usage.md) explain host compatibility, tools, and runtime caveats. Install from the original source for its latest instructions; frontmatter names are preserved.

## Choose your starting point

| You want to… | Start with |
| --- | --- |
| Choose the stack and ownership boundaries | [voice-stack-selection](../skills/foundations/voice-stack-selection/SKILL.md) |
| Improve listening, noise handling, or turn taking | [voice-audio-frontends](../skills/foundations/voice-audio-frontends/SKILL.md) · [voice-turn-taking](../skills/foundations/voice-turn-taking/SKILL.md) |
| Integrate recognition and spoken output | [voice-speech-pipeline](../skills/foundations/voice-speech-pipeline/SKILL.md) |
| Fix conversation, tool progress, or handoffs | [voice-conversation-design](../skills/foundations/voice-conversation-design/SKILL.md) · [voice-call-reliability](../skills/foundations/voice-call-reliability/SKILL.md) |
| Investigate delay, silence, or stale playback | [voice-latency-audit](../skills/foundations/voice-latency-audit/SKILL.md) · [voice-media-debugging](../skills/foundations/voice-media-debugging/SKILL.md) |
| Test a change before release | [voice-agent-evaluation](../skills/foundations/voice-agent-evaluation/SKILL.md) |

**Provider shortcuts:** [LiveKit](#livekit) · [ElevenLabs](#elevenlabs) · [Twilio](#twilio) · [Pipecat](#pipecat) · [Cartesia](#cartesia) · [OpenAI](#openai)

## Foundations

Original provider-neutral skills. Use with project context and redacted evidence.

| Skill and original source | What it helps with | Bundled copy |
| --- | --- | --- |
| [voice-agent-evaluation](../skills/foundations/voice-agent-evaluation/SKILL.md) | Design and run proportionate voice agent evaluations covering conversation success, turn taking, tool correctness, audio behavior, failures, and lifecycle cleanup. | Original NL Voice Skills material |
| [voice-audio-frontends](../skills/foundations/voice-audio-frontends/SKILL.md) | Diagnose echo and noise, choose processing placement, preserve quiet speech, and compare enhancement with paired tests. | Original NL Voice Skills material |
| [voice-call-reliability](../skills/foundations/voice-call-reliability/SKILL.md) | Design and debug telephony, transfers, capacity, shutdown, observability, and incident recovery. | Original NL Voice Skills material |
| [voice-conversation-design](../skills/foundations/voice-conversation-design/SKILL.md) | Write and evaluate voice agent prompts for spoken turn taking, concise responses, clarification, tool progress, interruptions, and safe handoffs. | Original NL Voice Skills material |
| [voice-latency-audit](../skills/foundations/voice-latency-audit/SKILL.md) | Investigate voice agent response delay using raw turn events, consistent clocks, component timings, and audio playback evidence; use for latency regressions and benchmark audits. | Original NL Voice Skills material |
| [voice-media-debugging](../skills/foundations/voice-media-debugging/SKILL.md) | Isolate bad codecs, sample rates, buffering, one-way audio, and stale playback after interruption. | Original NL Voice Skills material |
| [voice-stack-selection](../skills/foundations/voice-stack-selection/SKILL.md) | Choose a practical architecture for a voice AI agent by comparing realtime speech models, STT-LLM-TTS pipelines, transports, and hosting against the user's constraints. | Original NL Voice Skills material |
| [voice-speech-pipeline](../skills/foundations/voice-speech-pipeline/SKILL.md) | Select and integrate streaming recognition and synthesis, handle transcript revisions and playback, and test task-specific accuracy. | Original NL Voice Skills material |
| [voice-turn-taking](../skills/foundations/voice-turn-taking/SKILL.md) | Design turn ownership, diagnose early endpoints and false interruptions, and coordinate output cancellation with action state. | Original NL Voice Skills material |

Source: original NL Voice Skills material. License: [MIT](../LICENSE).


## LiveKit

Official lifecycle skills. Relevant SDK/CLI and documentation MCP may be needed.

| Skill and original source | What it helps with | Bundled copy |
| --- | --- | --- |
| [building-livekit-agents](https://github.com/livekit/agent-skills/blob/main/skills/building-livekit-agents/SKILL.md) | Build voice agents, tools, handoffs, and agent workflows with LiveKit. | [Snapshot](../skills/livekit/building-livekit-agents/SKILL.md) |
| [debugging-livekit-agents](https://github.com/livekit/agent-skills/blob/main/skills/debugging-livekit-agents/SKILL.md) | Exercise a local agent in a multi-turn conversation to diagnose behavior. | [Snapshot](../skills/livekit/debugging-livekit-agents/SKILL.md) |
| [operating-livekit-agents](https://github.com/livekit/agent-skills/blob/main/skills/operating-livekit-agents/SKILL.md) | Deploy, roll back, configure, and operate LiveKit workers. | [Snapshot](../skills/livekit/operating-livekit-agents/SKILL.md) |
| [reading-livekit-docs](https://github.com/livekit/agent-skills/blob/main/skills/reading-livekit-docs/SKILL.md) | Retrieve current SDK, CLI, integration, and provider documentation. | [Snapshot](../skills/livekit/reading-livekit-docs/SKILL.md) |
| [running-livekit-simulations](https://github.com/livekit/agent-skills/blob/main/skills/running-livekit-simulations/SKILL.md) | Run simulation scenarios and investigate their outcomes. | [Snapshot](../skills/livekit/running-livekit-simulations/SKILL.md) |
| [testing-livekit-agents](https://github.com/livekit/agent-skills/blob/main/skills/testing-livekit-agents/SKILL.md) | Write turn-level regression tests using the project test suite. | [Snapshot](../skills/livekit/testing-livekit-agents/SKILL.md) |
| [writing-livekit-scenarios](https://github.com/livekit/agent-skills/blob/main/skills/writing-livekit-scenarios/SKILL.md) | Author and maintain agent simulation scenarios. | [Snapshot](../skills/livekit/writing-livekit-scenarios/SKILL.md) |

<details>
<summary>Source, snapshot, license and dated stars</summary>

Current source: [livekit/agent-skills](https://github.com/livekit/agent-skills/tree/main). [Recorded snapshot](https://github.com/livekit/agent-skills/tree/5d7488b118c279812b89e73a9bee8474d1fe00a1). License: MIT. Source repository stars: 72 (dated snapshot; applies to the source collection).

</details>



## ElevenLabs

Official speech and agent workflows. Requires the relevant SDK/API, CLI, or MCP.

| Skill and original source | What it helps with | Bundled copy |
| --- | --- | --- |
| [agents](https://github.com/elevenlabs/skills/blob/main/agents/SKILL.md) | Build and configure conversational agents, tools, procedures, widgets, and phone integrations. | [Snapshot](../skills/elevenlabs/agents/SKILL.md) |
| [dubbing](https://github.com/elevenlabs/skills/blob/main/dubbing/SKILL.md) | Translate and dub recorded speech. | [Snapshot](../skills/elevenlabs/dubbing/SKILL.md) |
| [speech-engine](https://github.com/elevenlabs/skills/blob/main/speech-engine/SKILL.md) | Unified ElevenLabs speech engine usage and SDK integration. | [Snapshot](../skills/elevenlabs/speech-engine/SKILL.md) |
| [speech-to-text](https://github.com/elevenlabs/skills/blob/main/speech-to-text/SKILL.md) | File and realtime transcription, events, and commit strategies. | [Snapshot](../skills/elevenlabs/speech-to-text/SKILL.md) |
| [text-to-speech](https://github.com/elevenlabs/skills/blob/main/text-to-speech/SKILL.md) | Speech generation, streaming, and voice settings. | [Snapshot](../skills/elevenlabs/text-to-speech/SKILL.md) |
| [voice-changer](https://github.com/elevenlabs/skills/blob/main/voice-changer/SKILL.md) | Convert a voice while retaining speech delivery. | [Snapshot](../skills/elevenlabs/voice-changer/SKILL.md) |
| [voice-isolator](https://github.com/elevenlabs/skills/blob/main/voice-isolator/SKILL.md) | Isolate spoken voice from noisy audio. | [Snapshot](../skills/elevenlabs/voice-isolator/SKILL.md) |

<details>
<summary>Source, snapshot, license and dated stars</summary>

Current source: [elevenlabs/skills](https://github.com/elevenlabs/skills/tree/main). [Recorded snapshot](https://github.com/elevenlabs/skills/tree/279173d974ea5cf0c4c4f91d4e7e65202b406dab). License: MIT. Source repository stars: 460 (dated snapshot; applies to the source collection).

</details>



## Twilio

Selected official voice skills. Requires appropriate Twilio API/MCP access; optional sibling skills stay upstream.

| Skill and original source | What it helps with | Bundled copy |
| --- | --- | --- |
| [twilio-ai-agent-architect](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-ai-agent-architect/SKILL.md) | Select a Twilio conversational architecture and implementation path. | [Snapshot](../skills/twilio/twilio-ai-agent-architect/SKILL.md) |
| [twilio-call-recordings](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-call-recordings/SKILL.md) | Implement call recording, channels, pause/resume, and recording workflows. | [Snapshot](../skills/twilio/twilio-call-recordings/SKILL.md) |
| [twilio-conference-calls](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-conference-calls/SKILL.md) | Build conferences, transfers, holds, coaching, and supervisor participation. | [Snapshot](../skills/twilio/twilio-conference-calls/SKILL.md) |
| [twilio-voice-conversation-relay](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-voice-conversation-relay/SKILL.md) | Integrate ConversationRelay with WebSocket messages, models, and tools. | [Snapshot](../skills/twilio/twilio-voice-conversation-relay/SKILL.md) |
| [twilio-voice-outbound-calls](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-voice-outbound-calls/SKILL.md) | Create outbound call flows with status tracking and SIP integration. | [Snapshot](../skills/twilio/twilio-voice-outbound-calls/SKILL.md) |
| [twilio-voice-twiml](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-voice-twiml/SKILL.md) | Define voice call behavior and IVR flows using TwiML. | [Snapshot](../skills/twilio/twilio-voice-twiml/SKILL.md) |

<details>
<summary>Source, snapshot, license and dated stars</summary>

Current source: [twilio/ai](https://github.com/twilio/ai/tree/main). [Recorded snapshot](https://github.com/twilio/ai/tree/8aba46fb65dc8d9a20f4b301a68352064b4159a5). License: MIT. Source repository stars: 34 (dated snapshot; applies to the source collection).

</details>



## Pipecat

Official CLI and MCP workflows. Some instructions assume Claude Code tools; verify current CLI installation.

| Skill and original source | What it helps with | Bundled copy |
| --- | --- | --- |
| [deploy](https://github.com/pipecat-ai/skills/blob/main/skills/deploy/SKILL.md) | Deploy a Pipecat agent using the supported platform workflow. | [Snapshot](../skills/pipecat/deploy/SKILL.md) |
| [init](https://github.com/pipecat-ai/skills/blob/main/skills/init/SKILL.md) | Initialize a Pipecat project using its CLI. | [Snapshot](../skills/pipecat/init/SKILL.md) |
| [talk](https://github.com/pipecat-ai/skills/blob/main/skills/talk/SKILL.md) | Use the Pipecat MCP to start and converse with an agent. | [Snapshot](../skills/pipecat/talk/SKILL.md) |

<details>
<summary>Source, snapshot, license and dated stars</summary>

Current source: [pipecat-ai/skills](https://github.com/pipecat-ai/skills/tree/main). [Recorded snapshot](https://github.com/pipecat-ai/skills/tree/cca35d3b85665fb417fddb2bc8ec8a5c3805aa57). License: BSD-2-Clause. Source repository stars: 27 (dated snapshot; applies to the source collection).

</details>



## Cartesia

Official Cartesia API and Line workflows. Requires Cartesia service access or Line CLI.

| Skill and original source | What it helps with | Bundled copy |
| --- | --- | --- |
| [cartesia-api](https://github.com/cartesia-ai/skills/blob/main/skills/cartesia-api/SKILL.md) | Integrate Cartesia speech APIs, streaming, voices, and SDKs. | [Snapshot](../skills/cartesia/cartesia-api/SKILL.md) |
| [cartesia-line](https://github.com/cartesia-ai/skills/blob/main/skills/cartesia-line/SKILL.md) | Build, test, and operate voice agents using Cartesia Line. | [Snapshot](../skills/cartesia/cartesia-line/SKILL.md) |

<details>
<summary>Source, snapshot, license and dated stars</summary>

Current source: [cartesia-ai/skills](https://github.com/cartesia-ai/skills/tree/main). [Recorded snapshot](https://github.com/cartesia-ai/skills/tree/0ee3f4a4ad8e9cf9d314962448b721cdc34fae42). License: MIT. Source repository stars: 5 (dated snapshot; applies to the source collection).

</details>



## OpenAI

Official file-based speech workflows. Included Python scripts need Python/OpenAI SDK and API access.

| Skill and original source | What it helps with | Bundled copy |
| --- | --- | --- |
| [speech](https://github.com/openai/skills/blob/main/skills/.curated/speech/SKILL.md) | Generate speech from text using the OpenAI audio API and included CLI. | [Snapshot](../skills/openai/speech/SKILL.md) |
| [transcribe](https://github.com/openai/skills/blob/main/skills/.curated/transcribe/SKILL.md) | Transcribe recorded audio, with optional diarization and known-speaker references. | [Snapshot](../skills/openai/transcribe/SKILL.md) |

<details>
<summary>Source, snapshot, license and dated stars</summary>

Current source: [openai/skills](https://github.com/openai/skills/tree/main). [Recorded snapshot](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431). License: Apache-2.0 (per-skill). Source repository stars: 27,814 (dated snapshot; applies to the source collection).

</details>
