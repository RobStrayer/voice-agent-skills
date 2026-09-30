---
name: voice-stack-selection
description: Choose a practical architecture for a voice AI agent by comparing realtime speech models, STT-LLM-TTS pipelines, transports, and hosting against the user's constraints.
license: MIT
---

# Voice stack selection

Produce the smallest architecture that meets the actual voice use case. Identify
the entry channel, languages, expected concurrency, deployment environment,
tool actions, data retention needs, budget, and acceptable user-perceived delay.
Proceed with labeled assumptions when they do not block a useful comparison.

## Keep the choices separate

- **Media:** browser/mobile WebRTC, telephony/SIP, or server audio streams.
- **Orchestration:** framework, managed agent platform, or a small custom service.
- **Speech engine:** a realtime speech model or a streaming STT, LLM, and TTS chain.
- **Turn policy:** who decides end of turn, interruptions, cancellation, and resume.
- **Business state:** authorization, tools, durable memory, records, and finalization.

A framework name does not answer all five. A realtime model does not automatically
provide telephony, persistent memory, tool authorization, or production operations.

## Compare against evidence

Read the current official integration documentation and installed SDK versions.
Verify that the desired transport, codec, language, provider, and turn-control
combination works together. Mark an untested combination as an integration risk.

Compare at most three credible options using the same criteria: a complete call
path, required glue, interruption behavior, observability, operational ownership,
pricing units, and restrictions. Stars are a discovery signal, not a performance
measurement. Do not compare a component's first-byte latency with acoustic
end-to-end delay or price per token with price per connected minute.

Estimate total cost at the stated traffic level, including telephony, hosting,
orchestration, and model usage. Label assumed durations and utilization.

Prefer an existing supported integration over a custom adapter. Recommend one
default, explain the deciding tradeoff, and identify the requirement that would
justify switching. Give a bounded proof-of-concept plan using synthetic audio
and mocked business tools before any live calls or paid-provider testing.

## Deliver

A compact decision table, one recommended stack, a media-and-data-flow sketch,
verified compatibility links, explicit unknowns, and the smallest useful next test.

## Primary starting points

- [LiveKit Agents](https://github.com/livekit/agents)
- [Pipecat](https://github.com/pipecat-ai/pipecat)
- [OpenAI voice agents](https://developers.openai.com/api/docs/guides/voice-agents)
