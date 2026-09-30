# Skill catalog

31 skills: 27 pinned upstream snapshots and four original foundations.

Copy the complete selected skill folder. Frontmatter names are preserved. See [usage notes](usage.md) for tools, platform assumptions, and runtime caveats.

## Foundations

Original provider-neutral skills. Use with project context and redacted evidence.

| Skill | What it helps with |
| --- | --- |
| [voice-agent-evaluation](../skills/foundations/voice-agent-evaluation/SKILL.md) | Design and run proportionate voice agent evaluations covering conversation success, turn taking, tool correctness, audio behavior, failures, and lifecycle cleanup. |
| [voice-conversation-design](../skills/foundations/voice-conversation-design/SKILL.md) | Write and evaluate voice agent prompts for spoken turn taking, concise responses, clarification, tool progress, interruptions, and safe handoffs. |
| [voice-latency-audit](../skills/foundations/voice-latency-audit/SKILL.md) | Investigate voice agent response delay using raw turn events, consistent clocks, component timings, and audio playback evidence; use for latency regressions and benchmark audits. |
| [voice-stack-selection](../skills/foundations/voice-stack-selection/SKILL.md) | Choose a practical architecture for a voice AI agent by comparing realtime speech models, STT-LLM-TTS pipelines, transports, and hosting against the user's constraints. |

Source: original NL Voice Skills material. License: [MIT](../LICENSE).

## LiveKit

Official lifecycle skills. Relevant SDK/CLI and documentation MCP may be needed.

| Skill | What it helps with |
| --- | --- |
| [building-livekit-agents](../skills/livekit/building-livekit-agents/SKILL.md) | Build voice agents, tools, handoffs, and agent workflows with LiveKit. |
| [debugging-livekit-agents](../skills/livekit/debugging-livekit-agents/SKILL.md) | Exercise a local agent in a multi-turn conversation to diagnose behavior. |
| [operating-livekit-agents](../skills/livekit/operating-livekit-agents/SKILL.md) | Deploy, roll back, configure, and operate LiveKit workers. |
| [reading-livekit-docs](../skills/livekit/reading-livekit-docs/SKILL.md) | Retrieve current SDK, CLI, integration, and provider documentation. |
| [running-livekit-simulations](../skills/livekit/running-livekit-simulations/SKILL.md) | Run simulation scenarios and investigate their outcomes. |
| [testing-livekit-agents](../skills/livekit/testing-livekit-agents/SKILL.md) | Write turn-level regression tests using the project test suite. |
| [writing-livekit-scenarios](../skills/livekit/writing-livekit-scenarios/SKILL.md) | Author and maintain agent simulation scenarios. |

Source: [livekit/agent-skills](https://github.com/livekit/agent-skills/tree/5d7488b118c279812b89e73a9bee8474d1fe00a1). License: MIT. Source repository stars: 72 (dated snapshot; applies to the source collection).

## ElevenLabs

Official speech and agent workflows. Requires the relevant SDK/API, CLI, or MCP.

| Skill | What it helps with |
| --- | --- |
| [agents](../skills/elevenlabs/agents/SKILL.md) | Build and configure conversational agents, tools, procedures, widgets, and phone integrations. |
| [dubbing](../skills/elevenlabs/dubbing/SKILL.md) | Translate and dub recorded speech. |
| [speech-engine](../skills/elevenlabs/speech-engine/SKILL.md) | Unified ElevenLabs speech engine usage and SDK integration. |
| [speech-to-text](../skills/elevenlabs/speech-to-text/SKILL.md) | File and realtime transcription, events, and commit strategies. |
| [text-to-speech](../skills/elevenlabs/text-to-speech/SKILL.md) | Speech generation, streaming, and voice settings. |
| [voice-changer](../skills/elevenlabs/voice-changer/SKILL.md) | Convert a voice while retaining speech delivery. |
| [voice-isolator](../skills/elevenlabs/voice-isolator/SKILL.md) | Isolate spoken voice from noisy audio. |

Source: [elevenlabs/skills](https://github.com/elevenlabs/skills/tree/279173d974ea5cf0c4c4f91d4e7e65202b406dab). License: MIT. Source repository stars: 460 (dated snapshot; applies to the source collection).

## Twilio

Selected official voice skills. Requires appropriate Twilio API/MCP access; optional sibling skills stay upstream.

| Skill | What it helps with |
| --- | --- |
| [twilio-ai-agent-architect](../skills/twilio/twilio-ai-agent-architect/SKILL.md) | Select a Twilio conversational architecture and implementation path. |
| [twilio-call-recordings](../skills/twilio/twilio-call-recordings/SKILL.md) | Implement call recording, channels, pause/resume, and recording workflows. |
| [twilio-conference-calls](../skills/twilio/twilio-conference-calls/SKILL.md) | Build conferences, transfers, holds, coaching, and supervisor participation. |
| [twilio-voice-conversation-relay](../skills/twilio/twilio-voice-conversation-relay/SKILL.md) | Integrate ConversationRelay with WebSocket messages, models, and tools. |
| [twilio-voice-outbound-calls](../skills/twilio/twilio-voice-outbound-calls/SKILL.md) | Create outbound call flows with status tracking and SIP integration. |
| [twilio-voice-twiml](../skills/twilio/twilio-voice-twiml/SKILL.md) | Define voice call behavior and IVR flows using TwiML. |

Source: [twilio/ai](https://github.com/twilio/ai/tree/8aba46fb65dc8d9a20f4b301a68352064b4159a5). License: MIT. Source repository stars: 34 (dated snapshot; applies to the source collection).

## Pipecat

Official CLI and MCP workflows. Some instructions assume Claude Code tools; verify current CLI installation.

| Skill | What it helps with |
| --- | --- |
| [deploy](../skills/pipecat/deploy/SKILL.md) | Deploy a Pipecat agent using the supported platform workflow. |
| [init](../skills/pipecat/init/SKILL.md) | Initialize a Pipecat project using its CLI. |
| [talk](../skills/pipecat/talk/SKILL.md) | Use the Pipecat MCP to start and converse with an agent. |

Source: [pipecat-ai/skills](https://github.com/pipecat-ai/skills/tree/cca35d3b85665fb417fddb2bc8ec8a5c3805aa57). License: BSD-2-Clause. Source repository stars: 27 (dated snapshot; applies to the source collection).

## Cartesia

Official Cartesia API and Line workflows. Requires Cartesia service access or Line CLI.

| Skill | What it helps with |
| --- | --- |
| [cartesia-api](../skills/cartesia/cartesia-api/SKILL.md) | Integrate Cartesia speech APIs, streaming, voices, and SDKs. |
| [cartesia-line](../skills/cartesia/cartesia-line/SKILL.md) | Build, test, and operate voice agents using Cartesia Line. |

Source: [cartesia-ai/skills](https://github.com/cartesia-ai/skills/tree/0ee3f4a4ad8e9cf9d314962448b721cdc34fae42). License: MIT. Source repository stars: 5 (dated snapshot; applies to the source collection).

## OpenAI

Official file-based speech workflows. Included Python scripts need Python/OpenAI SDK and API access.

| Skill | What it helps with |
| --- | --- |
| [speech](../skills/openai/speech/SKILL.md) | Generate speech from text using the OpenAI audio API and included CLI. |
| [transcribe](../skills/openai/transcribe/SKILL.md) | Transcribe recorded audio, with optional diarization and known-speaker references. |

Source: [openai/skills](https://github.com/openai/skills/tree/49f948faa9258a0c61caceaf225e179651397431). License: Apache-2.0 (per-skill). Source repository stars: 27,814 (dated snapshot; applies to the source collection).
