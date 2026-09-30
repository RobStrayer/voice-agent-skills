# More voice skills

[Home](../README.md) / [Engineering handbook](handbook.md) / [Core skills](catalog.md) / More upstream skills

**297 linked skills** · **279 in 62 source repositories** · **18 on vendor documentation sites** · **50 providers** · **Checked September 30, 2026 UTC**

These are skills from voice providers and other authors, linked to where they are published. Nothing here is copied into this repository. Open the original source for current instructions. [Usage notes](usage.md) cover installation and host assumptions. [linked-skills.json](../linked-skills.json) keeps exact source metadata for each skill: commit, hash, license, dependencies and concerns.

## How to read this page

- Each provider keeps its skills together in one section. Use [Find your provider](#find-your-provider) or [Choose a task](#choose-a-task) to jump to it.
- Counts are skill files, not independent capabilities. Language variants and optional workflows count separately. Stars describe the whole repository, not one skill.
- Optional migration and preview skills sit in collapsed blocks inside their provider section. Migration skills move an existing agent between providers. Preview skills target alpha or beta APIs that can change.
- **Published on** marks a docs-hosted skill: a vendor serves the file from its documentation site. It has no commit to pin, so the index records a SHA-256 hash of the file instead.
- **No license file: linked only** means the repository has no license file at the checked commit. This index links to the skill and does not copy it.
- Some skills send telemetry or ask the agent to call the vendor. Read [Use with care](#use-with-care) first.

## Find your provider

| Provider | Section | Skills |
| --- | --- | ---: |
| [Agora](#agora) | [Phone and calling platforms](#phone-and-calling-platforms) | 1 |
| [AssemblyAI](#assemblyai) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 2 |
| [AWS](#aws) | [Cloud providers](#cloud-providers) | 15 |
| [Azure](#azure) | [Cloud providers](#cloud-providers) | 10 |
| [Bland AI](#bland-ai) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 1 |
| [Bluejay](#bluejay) | [Testing, evaluation and monitoring](#testing-evaluation-and-monitoring) | 7 |
| [Bolna](#bolna) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 9 |
| [Cekura](#cekura) | [Testing, evaluation and monitoring](#testing-evaluation-and-monitoring) | 9 |
| [Coval](#coval) | [Testing, evaluation and monitoring](#testing-evaluation-and-monitoring) | 13 |
| [Daily](#daily) | [Frameworks and real-time infrastructure](#frameworks-and-real-time-infrastructure) | 1 |
| [Deepgram](#deepgram) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 39 |
| [ElevenLabs](#elevenlabs) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 22 |
| [Fish Audio](#fish-audio) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 2 |
| [Gladia](#gladia) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 6 |
| [Google](#google) | [Cloud providers](#cloud-providers) | 7 |
| [Hookdeck](#hookdeck) | [Webhooks and security](#webhooks-and-security) | 7 |
| [iFlytek](#iflytek) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 2 |
| [jambonz](#jambonz) | [Phone and calling platforms](#phone-and-calling-platforms) | 3 |
| [Jellypod](#jellypod) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 1 |
| [Mahimai Labs](#mahimai-labs) | [Community references](#community-references) | 1 |
| [Moonshine](#moonshine) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 1 |
| [NVIDIA](#nvidia) | [Frameworks and real-time infrastructure](#frameworks-and-real-time-infrastructure) | 3 |
| [OpenRouter](#openrouter) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 2 |
| [Patter](#patter) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 4 |
| [Pipecat](#pipecat) | [Frameworks and real-time infrastructure](#frameworks-and-real-time-infrastructure) | 1 |
| [Plivo](#plivo) | [Phone and calling platforms](#phone-and-calling-platforms) | 6 |
| [pyannoteAI](#pyannoteai) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 1 |
| [Resemble AI](#resemble-ai) | [Webhooks and security](#webhooks-and-security) | 1 |
| [Retell AI](#retell-ai) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 2 |
| [Rime](#rime) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 1 |
| [Roark](#roark) | [Testing, evaluation and monitoring](#testing-evaluation-and-monitoring) | 7 |
| [Sarvam AI](#sarvam-ai) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 5 |
| [Shiny](#shiny) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 1 |
| [SignalWire](#signalwire) | [Phone and calling platforms](#phone-and-calling-platforms) | 1 |
| [Sinch](#sinch) | [Phone and calling platforms](#phone-and-calling-platforms) | 6 |
| [SLNG](#slng) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 8 |
| [Smallest AI](#smallest-ai) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 4 |
| [StepFun](#stepfun) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 3 |
| [Superlog](#superlog) | [Testing, evaluation and monitoring](#testing-evaluation-and-monitoring) | 1 |
| [Synthflow](#synthflow) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 7 |
| [Telnyx](#telnyx) | [Phone and calling platforms](#phone-and-calling-platforms) | 39 |
| [Together AI](#together-ai) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 1 |
| [Twilio](#twilio) | [Phone and calling platforms](#phone-and-calling-platforms) | 16 |
| [Ultravox](#ultravox) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 1 |
| [Vapi](#vapi) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 10 |
| [Venice AI](#venice-ai) | [Speech-to-text and text-to-speech APIs](#speech-to-text-and-text-to-speech-apis) | 2 |
| [Voiceflow](#voiceflow) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 1 |
| [voicetest](#voicetest) | [Testing, evaluation and monitoring](#testing-evaluation-and-monitoring) | 1 |
| [Voximplant](#voximplant) | [Managed voice-agent platforms](#managed-voice-agent-platforms) | 2 |
| [Zavu](#zavu) | [Phone and calling platforms](#phone-and-calling-platforms) | 1 |

## Choose a task

| Your next step | Providers | Linked skills |
| --- | --- | ---: |
| Build and run an agent on a hosted platform | [Bland AI](#bland-ai) · [Bolna](#bolna) · [ElevenLabs](#elevenlabs) · [Patter](#patter) · [Retell AI](#retell-ai) · [SLNG](#slng) · [Smallest AI](#smallest-ai) · [Synthflow](#synthflow) · [Ultravox](#ultravox) · [Vapi](#vapi) · [Voiceflow](#voiceflow) · [Voximplant](#voximplant) | 71 |
| Connect phone numbers, SIP trunks, or call control | [Agora](#agora) · [jambonz](#jambonz) · [Plivo](#plivo) · [SignalWire](#signalwire) · [Sinch](#sinch) · [Telnyx](#telnyx) · [Twilio](#twilio) · [Zavu](#zavu) | 73 |
| Add speech recognition or speech synthesis | [AssemblyAI](#assemblyai) · [Deepgram](#deepgram) · [Fish Audio](#fish-audio) · [Gladia](#gladia) · [iFlytek](#iflytek) · [Jellypod](#jellypod) · [Moonshine](#moonshine) · [OpenRouter](#openrouter) · [pyannoteAI](#pyannoteai) · [Rime](#rime) · [Sarvam AI](#sarvam-ai) · [Shiny](#shiny) · [StepFun](#stepfun) · [Together AI](#together-ai) · [Venice AI](#venice-ai) | 69 |
| Build on an open framework or real-time media stack | [Daily](#daily) · [NVIDIA](#nvidia) · [Pipecat](#pipecat) | 5 |
| Use a cloud provider's voice and speech services | [AWS](#aws) · [Azure](#azure) · [Google](#google) | 32 |
| Test, simulate, or monitor an agent | [Bluejay](#bluejay) · [Cekura](#cekura) · [Coval](#coval) · [Roark](#roark) · [Superlog](#superlog) · [voicetest](#voicetest) | 38 |
| Verify webhooks or detect synthetic voices | [Hookdeck](#hookdeck) · [Resemble AI](#resemble-ai) | 8 |
| Draft a spoken prompt with worked examples | [Mahimai Labs](#mahimai-labs) | 1 |

Some skills sit under their provider instead of a task group. Test skills: [ElevenLabs](#elevenlabs), [Vapi](#vapi), [Synthflow](#synthflow), [AWS](#aws) and [Google](#google). Security and webhook skills: [Twilio](#twilio) and [ElevenLabs](#elevenlabs). Migration skills (9) are under [Telnyx](#telnyx), [ElevenLabs](#elevenlabs), [SLNG](#slng) and [AWS](#aws). Spoken-prompt skills are also under [Vapi](#vapi), [Bolna](#bolna), [SLNG](#slng) and [Synthflow](#synthflow).

## Managed voice-agent platforms

These platforms host the agent for you. You set up the agent, its tools and its phone numbers in a dashboard or through an API, and the skills teach a coding agent that API. Most of them can place real calls, buy numbers or change a live agent, so check what an instruction will do before you run it.

### Bland AI

[Skill index on docs.bland.ai](https://docs.bland.ai/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

Bland publishes its skill on its documentation site, not on GitHub.

| Task | Skill |
| --- | --- |
| Build, publish and promote Bland AI phone agents, attach tools and knowledge, and place calls through the API. *Published on docs.bland.ai.* | [blandai](https://docs.bland.ai/.well-known/agent-skills/blandai/skill.md) |

### Bolna

- [bolna-ai/skills](https://github.com/bolna-ai/skills) · **3 stars** · [MIT](https://github.com/bolna-ai/skills/blob/main/LICENSE)
- [Skill index on www.bolna.ai](https://www.bolna.ai/docs/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

Bolna also publishes a skill on its documentation site.

| Task | Skill |
| --- | --- |
| Build a Bolna voice agent with the v2 API: LLM, TTS, STT, telephony, RAG, routes and multilingual settings. | [create-agent](https://github.com/bolna-ai/skills/blob/main/create-agent/SKILL.md) |
| Add function tools (HTTP calls, call transfer, Cal.com booking, DTMF) to a Bolna voice agent's configuration. | [setup-tools](https://github.com/bolna-ai/skills/blob/main/setup-tools/SKILL.md) |
| Map a Bolna phone number to an agent for inbound calls, with optional IVR menus, caller lookup and spam limits. | [setup-inbound](https://github.com/bolna-ai/skills/blob/main/setup-inbound/SKILL.md) |
| Connect your own SIP trunk to Bolna: create trunks, add DIDs, map numbers to agents, and troubleshoot audio. | [setup-sip-trunk](https://github.com/bolna-ai/skills/blob/main/setup-sip-trunk/SKILL.md) |
| Place, schedule, retry and cancel outbound Bolna calls with per-call variables, using curl or bundled scripts. | [make-call](https://github.com/bolna-ai/skills/blob/main/make-call/SKILL.md) |
| Diagnose Bolna call problems by mapping symptoms to agent settings using execution latency data and raw logs. | [debug-bolna-calls](https://github.com/bolna-ai/skills/blob/main/debug-bolna-calls/SKILL.md) |
| Write and repair Bolna voice-agent prompts in a fixed section format for Hindi, English and Hinglish calls. | [bolna-voice-prompt](https://github.com/bolna-ai/skills/blob/main/prompt-writing/SKILL.md) |
| Build, configure and operate Bolna phone voice agents, including calls, batch campaigns and post-call data. *Published on www.bolna.ai.* | [bolna](https://www.bolna.ai/docs/.well-known/agent-skills/bolna/skill.md) |

<details>
<summary>Preview and beta APIs (1 optional skill)</summary>

These target alpha or beta features or APIs that can change. Check the current documentation before you use them.

| Task | Skill |
| --- | --- |
| Design node-based Bolna voice flows with routing edges, static nodes, silence handling and live event injection. | [bolna-graph-agents](https://github.com/bolna-ai/skills/blob/main/bolna-graph-agents/SKILL.md) |

</details>

### ElevenLabs

- [elevenlabs/plugin](https://github.com/elevenlabs/plugin) · **1 star** · **No license file: linked only**
- [elevenlabs/packages](https://github.com/elevenlabs/packages) · **114 stars** · [MIT](https://github.com/elevenlabs/packages/blob/main/LICENSE)

ElevenLabs' official skills for agents, speech and transcription are in the [core catalogue](catalog.md#elevenlabs). The skills below come from its plugin repository, plus one SDK migration skill from its packages repository. They configure, test and review ElevenLabs agents over the REST API. Webhook signature checks for ElevenLabs are in [Hookdeck](#hookdeck).

**Build and configure agents**

| Task | Skill |
| --- | --- |
| Create an ElevenLabs agent from a user's requirements via the REST create endpoint, then refine it with PATCH. | [architect-generate-agent](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-generate-agent/SKILL.md) |
| Change ElevenLabs agent settings via the ConvAI API: read current state, patch one field, check language/TTS pairing. | [architect-update-config-safely](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-update-config-safely/SKILL.md) |
| Read and edit an ElevenLabs agent's workflow (nodes and edges) over REST without validation failures. | [architect-edit-workflows](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-edit-workflows/SKILL.md) |
| Manage ElevenLabs agent procedures through the REST API, including the draft-then-publish sequence and error recovery. | [architect-manage-procedures](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-manage-procedures/SKILL.md) |
| Create an ElevenLabs client tool that runs in the caller's browser or app, and attach it to an agent. | [architect-create-client-tool](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-create-client-tool/SKILL.md) |
| Create an ElevenLabs webhook (server) tool with a valid schema and attach it to an agent or workflow node. | [architect-create-webhook-tool](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-create-webhook-tool/SKILL.md) |
| Write JS/TS code tools that run on ElevenLabs, with secrets, allowed domains, test plans and an optional local runner. | [code-tools](https://github.com/elevenlabs/plugin/blob/main/architect/skills/code-tools/SKILL.md) |
| Choose an LLM for an ElevenLabs agent by filtering on region and compliance first, then latency, capability and cost. | [architect-llm-selection](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-llm-selection/SKILL.md) |
| Explain and change an ElevenLabs agent's turn-taking settings (speculative turn, eagerness, timeout) via PATCH. | [architect-turn-taking-latency](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-turn-taking-latency/SKILL.md) |
| Diagnose ElevenLabs agent tool problems: invalid schemas, tools never called, missing results, backend errors. | [architect-troubleshoot-tool-errors](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-troubleshoot-tool-errors/SKILL.md) |
| Rebuild a large ElevenLabs workflow agent as a simpler one, using native tests to show behavior is preserved. | [agent-simplification](https://github.com/elevenlabs/plugin/blob/main/architect/skills/agent-simplification/SKILL.md) |

**Test agents**

| Task | Skill |
| --- | --- |
| Create, attach and run single-turn LLM response tests for an ElevenLabs agent, avoiding schema errors. | [architect-create-llm-test](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-create-llm-test/SKILL.md) |
| Create, attach and run multi-turn simulation tests for an ElevenLabs agent, including tool mocking. | [architect-create-simulation-test](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-create-simulation-test/SKILL.md) |
| Create, attach and run tool-call tests that assert an ElevenLabs agent calls, or avoids, a tool. | [architect-create-tool-test](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-create-tool-test/SKILL.md) |
| Mock every tool in an ElevenLabs simulation test by tool ID and verify the mocks actually applied. | [architect-mock-all-tools](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-mock-all-tools/SKILL.md) |
| Explain why ElevenLabs agent test runs passed, failed or differed, using invocation rationales and transcripts. | [architect-explain-test-runs](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-explain-test-runs/SKILL.md) |
| Run an ElevenLabs agent's test suite, classify failures by cause, and repair test bugs to reach green. | [architect-get-agent-ci-green](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-get-agent-ci-green/SKILL.md) |

**Review calls and harden for production**

| Task | Skill |
| --- | --- |
| Review recent finished ElevenLabs agent conversations, cluster issues by root cause, and route each to a fix. | [architect-review-live-calls](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-review-live-calls/SKILL.md) |
| Set up post-call data-collection fields and evaluation criteria for an ElevenLabs agent using real call samples. | [architect-post-call-data](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-post-call-data/SKILL.md) |
| Guide production hardening of an ElevenLabs agent: access control, guardrails, testing, rollout, monitoring, privacy. | [architect-secure-for-production](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-secure-for-production/SKILL.md) |

<details>
<summary>Migration (1 optional skill)</summary>

Use these to move an existing agent or integration. They can change application code, create resources, and transfer configuration. Review the requested scope before you authorize them.

| Task | Skill |
| --- | --- |
| Convert a Retell, Vapi or Bland agent export to an ElevenLabs agent and check it runs with mocked tool calls. | [architect-migrate-from-competitor](https://github.com/elevenlabs/plugin/blob/main/architect/skills/architect-migrate-from-competitor/SKILL.md) |

</details>

<details>
<summary>Preview and beta APIs (1 optional skill)</summary>

These target alpha or beta features or APIs that can change. Check the current documentation before you use them.

| Task | Skill |
| --- | --- |
| Migrate code using @elevenlabs/client, react and react-native to the next major version's changed APIs. | [elevenlabs:sdk-migration](https://github.com/elevenlabs/packages/blob/main/.agents/skills/elevenlabs:sdk-migration/SKILL.md) |

</details>

### Patter

[PatterAI/skills](https://github.com/PatterAI/skills) · **6 stars** · [MIT](https://github.com/PatterAI/skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Build a Patter voice agent that answers or places real phone calls through Twilio or Telnyx, in Python or TypeScript. | [build-voice-agent](https://github.com/PatterAI/skills/blob/main/build-voice-agent/SKILL.md) |
| Set up Twilio or Telnyx for a Patter agent: webhook URL or tunnel, outbound AMD and voicemail, recording, signatures. | [configure-telephony](https://github.com/PatterAI/skills/blob/main/configure-telephony/SKILL.md) |
| Add custom function tools, call transfer and hang-up, and output guardrails to a Patter voice agent. | [add-tools-and-handoffs](https://github.com/PatterAI/skills/blob/main/add-tools-and-handoffs/SKILL.md) |
| Inspect Patter calls: live dashboard, per-call metrics and cost, transcripts, REST/SSE access and CSV or JSON export. | [inspect-calls-and-metrics](https://github.com/PatterAI/skills/blob/main/inspect-calls-and-metrics/SKILL.md) |

### Retell AI

- [Skill index on docs.retellai.com](https://docs.retellai.com/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**
- [Target-Dial/voice-agent-skills](https://github.com/Target-Dial/voice-agent-skills) · **1 star** · [MIT](https://github.com/Target-Dial/voice-agent-skills/blob/main/LICENSE)

Retell publishes its skill on its documentation site. The second skill comes from a community repository, not from Retell. Webhook signature checks for Retell are in [Hookdeck](#hookdeck).

| Task | Skill |
| --- | --- |
| Build, test, publish and monitor Retell AI phone and chat agents using the dashboard and REST API. *Published on docs.retellai.com.* | [retellai](https://docs.retellai.com/.well-known/agent-skills/retellai/skill.md) |
| Create, inspect, update and publish Retell agents, LLMs and conversation flows via curl, using per-client API keys. | [retell](https://github.com/Target-Dial/voice-agent-skills/blob/main/retell/SKILL.md) |

### SLNG

- [slng-ai/skills](https://github.com/slng-ai/skills) · **0 stars** · [MIT](https://github.com/slng-ai/skills/blob/main/LICENSE)
- [Skill index on docs.slng.ai](https://docs.slng.ai/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

SLNG fronts several speech providers behind one API and also runs an agent builder.

**Agents**

| Task | Skill |
| --- | --- |
| Manage slng.ai voice agents, dispatch outbound calls and start web sessions via its Agents API. | [agents](https://github.com/slng-ai/skills/blob/main/agents/SKILL.md) |
| Generate a greeting, system prompt, template variables and two webhook tools for the SLNG Agent Builder. | [agent-prompt](https://github.com/slng-ai/skills/blob/main/agent-prompt/SKILL.md) |
| Create, configure, test and operate SLNG voice agents: models, tools, SIP dispatch and call review. *Published on docs.slng.ai.* | [slng](https://docs.slng.ai/.well-known/agent-skills/slng/skill.md) |

**Speech APIs**

| Task | Skill |
| --- | --- |
| Transcribe files or live audio through slng's speech-to-text API, which fronts several providers. | [speech-to-text](https://github.com/slng-ai/skills/blob/main/speech-to-text/SKILL.md) |
| Synthesize speech through slng's text-to-speech API, which fronts several providers. | [text-to-speech](https://github.com/slng-ai/skills/blob/main/text-to-speech/SKILL.md) |

<details>
<summary>Migration (3 optional skills)</summary>

Use these to move an existing agent or integration. They can change application code, create resources, and transfer configuration. Review the requested scope before you authorize them.

| Task | Skill |
| --- | --- |
| Migrate an existing Python/JS/TS voice project's STT, TTS or LLM call sites to SLNG with small, auditable edits. | [custom-migration](https://github.com/slng-ai/skills/blob/main/custom-migration/SKILL.md) |
| Move a LiveKit Agents Python project's STT/TTS to SLNG via livekit-plugins-slng, with optional LLM router. | [livekit-migration](https://github.com/slng-ai/skills/blob/main/livekit-migration/SKILL.md) |
| Move a Pipecat Python bot's STT/TTS to SLNG via pipecat-slng, with optional LLM router. | [pipecat-migration](https://github.com/slng-ai/skills/blob/main/pipecat-migration/SKILL.md) |

</details>

### Smallest AI

[smallest-inc/skills](https://github.com/smallest-inc/skills) · **0 stars** · **No license file: linked only**

The manifests declare MIT, but the repository has no license file, so this index links to the skills only.

| Task | Skill |
| --- | --- |
| Create and operate Smallest AI Atoms voice agents: outbound calls, campaigns, knowledge bases, logs. | [voice-agents](https://github.com/smallest-inc/skills/blob/main/voice-agents/SKILL.md) |
| Build full-duplex speech-to-speech voice sessions over one WebSocket with Smallest AI's Hydra model. | [speech-to-speech](https://github.com/smallest-inc/skills/blob/main/speech-to-speech/SKILL.md) |
| Transcribe audio files and live streams with Smallest AI Pulse models over HTTP and WebSocket. | [speech-to-text](https://github.com/smallest-inc/skills/blob/main/speech-to-text/SKILL.md) |
| Synthesize, stream and clone speech with Smallest AI Lightning models over HTTP, SSE and WebSocket. | [text-to-speech](https://github.com/smallest-inc/skills/blob/main/text-to-speech/SKILL.md) |

### Synthflow

- [SynthFlowAI/synthflow-skills](https://github.com/SynthFlowAI/synthflow-skills) · **0 stars** · **No license file: linked only**
- [SynthFlowAI/AnthropicPlugin](https://github.com/SynthFlowAI/AnthropicPlugin) · **0 stars** · [MIT](https://github.com/SynthFlowAI/AnthropicPlugin/blob/main/LICENSE)

Five skills come from the skills repository, which has no license file. Two come from the plugin repository. Three of the five (create-assistant, create-call and manage-actions) tell the agent to send a usage event to a PostHog endpoint. It is on by default and stops when `DO_NOT_TRACK` or `DISABLE_TELEMETRY` is set. create-eval and create-simulation also contain telemetry commands with the same opt-outs. See [Use with care](#use-with-care).

**Build and run assistants**

| Task | Skill |
| --- | --- |
| Create and configure Synthflow voice assistants through the API: model, voice, language, greeting and settings. | [create-assistant](https://github.com/SynthFlowAI/synthflow-skills/blob/main/create-assistant/SKILL.md) |
| Start outbound Synthflow calls through the API or CLI and list or inspect call records. | [create-call](https://github.com/SynthFlowAI/synthflow-skills/blob/main/create-call/SKILL.md) |
| Configure Synthflow assistant actions: live transfer, SMS, custom API calls, data extraction, booking and evals. | [manage-actions](https://github.com/SynthFlowAI/synthflow-skills/blob/main/manage-actions/SKILL.md) |

**Evaluate and review**

| Task | Skill |
| --- | --- |
| Define post-call custom evaluations and business outcomes. | [create-eval](https://github.com/SynthFlowAI/synthflow-skills/blob/main/create-eval/SKILL.md) |
| Build caller scenarios and simulation tests for Synthflow agents. | [create-simulation](https://github.com/SynthFlowAI/synthflow-skills/blob/main/create-simulation/SKILL.md) |
| Audit recent calls for a Synthflow agent via MCP tools and report flagged problems with transcript evidence. | [call-review](https://github.com/SynthFlowAI/AnthropicPlugin/blob/main/plugins/synthflow/skills/call-review/SKILL.md) |
| Review voice-agent prompts, mainly Synthflow Single-Prompt, for contradictions, tool gaps, and regression risk. | [prompt-review](https://github.com/SynthFlowAI/AnthropicPlugin/blob/main/plugins/synthflow/skills/prompt-review/SKILL.md) |

Inspect Synthflow's telemetry section before running its instructions. No telemetry, provider changes, or calls were performed for this index. Use its current [custom evaluations](https://docs.synthflow.ai/create-a-custom-evaluation) and [simulation documentation](https://docs.synthflow.ai/simulations) for API details.

### Ultravox

[Skill index on docs.ultravox.ai](https://docs.ultravox.ai/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

Ultravox publishes its skill on its documentation site. The skill is named fixie, and it covers Ultravox.

| Task | Skill |
| --- | --- |
| Create Ultravox voice agents, start calls, attach tools and webhooks, and connect phone or web clients via REST. *Published on docs.ultravox.ai.* | [fixie](https://docs.ultravox.ai/.well-known/agent-skills/fixie/skill.md) |

### Vapi

[Official collection](https://github.com/VapiAI/skills/tree/main) · **66 stars** · **No license file: linked only**

The manifests declare MIT, but the repository has no LICENSE or NOTICE file in the checked archive. This index links to ten voice-specific workflows. Generic credential setup and the opt-in Bun bootstrap scaffold are excluded.

| Task | Skill |
| --- | --- |
| Configure a Vapi voice assistant, model, voice, and conversation behavior. | [create-assistant](https://github.com/VapiAI/skills/blob/main/create-assistant/SKILL.md) |
| Build grounded voice prompts with intake, capability, and trust-boundary reviews. | [vapi-prompt-builder](https://github.com/VapiAI/skills/blob/main/vapi-prompt-builder/SKILL.md) |
| Configure callable tools for a voice assistant. | [create-tool](https://github.com/VapiAI/skills/blob/main/create-tool/SKILL.md) |
| Coordinate assistants and voice handoffs using Squads. | [create-squad](https://github.com/VapiAI/skills/blob/main/create-squad/SKILL.md) |
| Create inbound or outbound voice call workflows. | [create-call](https://github.com/VapiAI/skills/blob/main/create-call/SKILL.md) |
| Configure outbound calling campaigns. | [create-campaign](https://github.com/VapiAI/skills/blob/main/create-campaign/SKILL.md) |
| Attach or configure a phone number for voice calls. | [create-phone-number](https://github.com/VapiAI/skills/blob/main/create-phone-number/SKILL.md) |
| Define structured extraction of call outcomes. | [create-structured-output](https://github.com/VapiAI/skills/blob/main/create-structured-output/SKILL.md) |
| Configure server events and call-related webhooks. | [setup-webhook](https://github.com/VapiAI/skills/blob/main/setup-webhook/SKILL.md) |
| Plan and run voice simulations and focused evaluations. | [simulations](https://github.com/VapiAI/skills/blob/main/simulations/SKILL.md) |

Live operations require `VAPI_API_KEY` and current schema checks. Calls, campaigns, number provisioning, and simulation runs can change external resources or consume usage. Text simulations help test logic; voice tests are needed to assess speech recognition, audio delivery, and interruptions. Webhook signature checks for Vapi are in [Hookdeck](#hookdeck).

### Voiceflow

[Skill index on voiceflow.com](https://voiceflow.com/docs/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

This skill covers the Voiceflow HTTP APIs in general. Voice is a small part of it: the only voice-specific content is the speak trace in one table row.

| Task | Skill |
| --- | --- |
| Run conversations and manage knowledge base, analytics and environments through Voiceflow's HTTP APIs. *Published on voiceflow.com.* | [voiceflow](https://voiceflow.com/docs/.well-known/agent-skills/voiceflow/skill.md) |

### Voximplant

[voximplant/ai-agent-skills](https://github.com/voximplant/ai-agent-skills) · **7 stars** · [Apache-2.0](https://github.com/voximplant/ai-agent-skills/blob/main/LICENSE)

Use the current docs.voximplant.ai references and narrowly scoped account roles.

| Task | Skill |
| --- | --- |
| Build VoxEngine call flows and media bridges with current API references. | [voximplant-voxengine-dev](https://github.com/voximplant/ai-agent-skills/blob/main/plugins/voximplant-ai-agent-skills/skills/voximplant-voxengine-dev/SKILL.md) |
| Manage voice application configuration, scenarios, rules, and call logs. | [voximplant-management-api](https://github.com/voximplant/ai-agent-skills/blob/main/plugins/voximplant-ai-agent-skills/skills/voximplant-management-api/SKILL.md) |

Voximplant's current [voice orchestration examples](https://docs.voximplant.ai/voice-ai-orchestration/openai/inbound.md) are preferable to copying an older indexed snippet without checking the API.

## Phone and calling platforms

Telephony and real-time calling providers give you numbers, SIP trunks, call control and media streams. An agent you run yourself needs them to reach callers. These skills can place calls, send messages and spend money on your account, so check what a step will do before you run it.

### Agora

[AgoraIO/skills](https://github.com/AgoraIO/skills) · **83 stars** · [MIT](https://github.com/AgoraIO/skills/blob/main/LICENSE)

The skill tells the agent to run the official ConvoAI quickstart before writing custom code. Its CLI writes an App Certificate to env files. Treat that certificate as a long-lived secret.

| Task | Skill |
| --- | --- |
| Route Agora work (RTC, RTM, ConvoAI voice agents, CLI, recording, tokens); gate ConvoAI on the official quickstart. | [agora](https://github.com/AgoraIO/skills/blob/main/skills/agora/SKILL.md) |

### jambonz

[jambonz/skills](https://github.com/jambonz/skills) · **4 stars** · [MIT](https://github.com/jambonz/skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Pick jambonz verbs, WebSocket vs webhook transport and avoid pitfalls in voice AI, IVR and call-control apps. | [jambonz](https://github.com/jambonz/skills/blob/main/skills/jambonz/SKILL.md) |
| Implementation patterns for jambonz voice AI agents, IVR, call control and env_vars using @jambonz/sdk or raw JSON. | [jambonz-recipes](https://github.com/jambonz/skills/blob/main/skills/jambonz-recipes/SKILL.md) |
| Catalog of ready-to-clone jambonz starter apps (voice agents, IVR, dialing, recording) with a degit clone command. | [jambonz-starters](https://github.com/jambonz/skills/blob/main/skills/jambonz-starters/SKILL.md) |

### Plivo

- [plivo/plivo-cli](https://github.com/plivo/plivo-cli) · **2 stars** · [Apache-2.0](https://github.com/plivo/plivo-cli/blob/main/LICENSE)
- [Skill index on plivo.com](https://plivo.com/docs/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

Most of the skills live in the repository of the Plivo command-line tool. The documentation-site skill is a router that points to companion skills, so it does little on its own. The plivo-audio-streaming and plivo-sip-trunking descriptions contain an unquoted colon, so a strict YAML loader rejects them. Quote the description after you install them.

| Task | Skill |
| --- | --- |
| Set up, verify and debug Plivo phone calls that stream audio to a WebSocket voice bot, through to production. | [plivo-audio-streaming](https://github.com/plivo/plivo-cli/blob/main/audio-streaming-skill/SKILL.md) |
| Set up and debug Plivo SIP trunks linking AI voice platforms to phone numbers, using the Plivo CLI. | [plivo-sip-trunking](https://github.com/plivo/plivo-cli/blob/main/sip-trunking-skill/SKILL.md) |
| Build, validate and publish Plivo CX agent flow graphs through the Agents API, with a pre-POST check script. | [plivo-cx-agents](https://github.com/plivo/plivo-cli/blob/main/agents-skill/SKILL.md) |
| Write and debug Plivo Voice XML for answer and action URLs: IVR, dial, record, conference, callbacks, error codes. | [plivo-voice-xml](https://github.com/plivo/plivo-cli/blob/main/voice-xml-skill/SKILL.md) |
| Drive Plivo messaging, calls, numbers, verify and WebSocket stream testing through the plivo CLI. | [plivo-cli](https://github.com/plivo/plivo-cli/blob/main/cli-skill/SKILL.md) |
| Route Plivo tasks to the right companion skill and state platform facts that every integration relies on. *Published on plivo.com.* | [plivo](https://plivo.com/docs/.well-known/agent-skills/plivo/skill.md) |

### SignalWire

[signalwire/signalwire-claude](https://github.com/signalwire/signalwire-claude) · **9 stars** · [MIT](https://github.com/signalwire/signalwire-claude/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Build SignalWire phone, SMS and AI voice-agent apps with SWML, REST, Relay and the Python AI Agents SDK. | [signalwire](https://github.com/signalwire/signalwire-claude/blob/main/skills/signalwire/SKILL.md) |

### Sinch

[sinch/skills](https://github.com/sinch/skills) · **10 stars** · [Apache-2.0](https://github.com/sinch/skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Build and control Sinch Voice API v1 calls: callouts, SVAML call flows, IVR, conferences, recording and callbacks. | [sinch-voice-api](https://github.com/sinch/skills/blob/main/skills/sinch-voice-api/SKILL.md) |
| Provision Sinch Elastic SIP Trunking trunks, ACLs, credential lists, endpoints and phone numbers over REST. | [sinch-elastic-sip-trunking](https://github.com/sinch/skills/blob/main/skills/sinch-elastic-sip-trunking/SKILL.md) |
| Integrate the Sinch In-App Calling SDKs for voice and video in Android, iOS and web apps, with backend JWT auth. | [sinch-in-app-calling](https://github.com/sinch/skills/blob/main/skills/sinch-in-app-calling/SKILL.md) |

<details>
<summary>Preview and beta APIs (3 optional skills)</summary>

These target alpha or beta features or APIs that can change. Check the current documentation before you use them.

| Task | Skill |
| --- | --- |
| Build and deploy voice and SMS handlers on the beta Sinch Functions platform (Node.js or C#). | [sinch-functions](https://github.com/sinch/skills/blob/main/skills/sinch-functions/SKILL.md) |
| Write Sinch Functions in Node.js/TypeScript for call handling, IVR, AI-agent handoff and messaging webhooks. | [sinch-functions-node](https://github.com/sinch/skills/blob/main/skills/sinch-functions-node/SKILL.md) |
| Use the Sinch Voice API v2 preview for calls, SVAML v2 flows, webhooks and AI agent audio (Relay or Stream). | [sinch-voice-api-v2](https://github.com/sinch/skills/blob/main/skills/sinch-voice-api-v2/SKILL.md) |

</details>

### Telnyx

[Official collection](https://github.com/team-telnyx/ai/tree/main/skills) · **219 stars** · [MIT](https://github.com/team-telnyx/ai/blob/main/LICENSE)

Choose the guide for your server language. Backend WebRTC guides create credentials and tokens; the client guides below handle browser or mobile calling. Live operations require `TELNYX_API_KEY` and the matching SDK. Keep account keys on the server.

| Task | Python | JavaScript |
| --- | --- | --- |
| Configure AI voice assistants and tools | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-ai-assistants-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-ai-assistants-javascript/SKILL.md) |
| Make, receive, transfer, and bridge calls | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-javascript/SKILL.md) |
| Stream live call audio | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-streaming-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-streaming-javascript/SKILL.md) |
| Collect speech and DTMF | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-gather-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-gather-javascript/SKILL.md) |
| Synthesize, play, and record call audio | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-media-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-media-javascript/SKILL.md) |
| Manage conferences and call queues | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-conferencing-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-conferencing-javascript/SKILL.md) |
| Use SIPREC, supervision, and advanced controls | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-advanced-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-voice-advanced-javascript/SKILL.md) |
| Configure SIP and outbound voice routing | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-sip-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-sip-javascript/SKILL.md) |
| Use TeXML and TwiML-compatible voice flows | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-texml-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-texml-javascript/SKILL.md) |
| Provision backend WebRTC credentials and tokens | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-webrtc-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-webrtc-javascript/SKILL.md) |
| Search, reserve, and order phone numbers | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-numbers-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-numbers-javascript/SKILL.md) |
| Find per-endpoint examples for recordings, media, SIPREC, Dialogflow, and Zoom or Teams connections | [Python](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-sip-integrations-python/SKILL.md) | [JavaScript](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-sip-integrations-javascript/SKILL.md) |

#### Speech, client calling and other skills

| Task | Original skill |
| --- | --- |
| Build an outbound AI calling flow | [Python outbound voice](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-ai-outbound-voice-python/SKILL.md) |
| Transcribe speech | [Python STT](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-stt-python/SKILL.md) |
| Generate speech | [Python TTS](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-tts-python/SKILL.md) |
| Browser calling | [JavaScript client](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-webrtc-client-js/SKILL.md) |
| React Native calling | [React Native client](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-webrtc-client-react-native/SKILL.md) |
| Flutter calling | [Flutter client](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-webrtc-client-flutter/SKILL.md) |
| Native iOS calling | [iOS client](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-webrtc-client-ios/SKILL.md) |
| Native Android calling | [Android client](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-webrtc-client-android/SKILL.md) |
| Send test VoIP pushes through APNs or FCM to check that a mobile calling app receives them | [push-notification-tester](https://github.com/team-telnyx/ai/blob/main/skills/push-notification-tester/SKILL.md) |
| Operate a Telnyx Meeting Bot: join meetings, poll transcripts, raise alerts, and write a report | [telnyx-meeting-bot](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-meeting-bot/SKILL.md) |
| Use the Telnyx REST API, CLI and webhooks for SMS, voice calls and phone number management. *Published on developers.telnyx.com.* | [telnyx](https://developers.telnyx.com/.well-known/agent-skills/telnyx/skill.md) |

<details>
<summary>Migration from Twilio, Vapi, Retell or ElevenLabs (4 optional skills)</summary>

Use these when migrating an existing provider integration. They can change application code, provision resources, transfer configuration, and store integration secrets. The Twilio migration includes non-voice products and bundled scripts, and requires bash 4+, jq, curl, and Python. Review the requested scope and current prices before authorizing its paid test workflow.

| Starting point | Original skill |
| --- | --- |
| Twilio | [Migration guide](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-twilio-migration/SKILL.md) |
| Vapi | [Migration guide](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-import-vapi/SKILL.md) |
| Retell | [Migration guide](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-import-retell/SKILL.md) |
| ElevenLabs | [Migration guide](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-import-elevenlabs/SKILL.md) |

</details>

### Twilio

[twilio/ai](https://github.com/twilio/ai) · **34 stars** · [MIT](https://github.com/twilio/ai/blob/main/LICENSE)

Twilio's core voice skills, including ConversationRelay, are in the [core catalogue](catalog.md#twilio). The sixteen below come from the same repository and cover compliance, observability, agent assist, routing and security. Webhook signature checks for Twilio are also in [Hookdeck](#hookdeck).

**Run voice and messaging traffic safely**

| Task | Skill |
| --- | --- |
| Follow consent, recording, payment, health-data and caller-ID rules for live Twilio voice and messaging traffic. | [twilio-compliance-traffic](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-compliance-traffic/SKILL.md) |
| Diagnose Twilio failures with callbacks, Debugger, Monitor APIs and Event Streams and set production alerts. | [twilio-debugging-observability](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-debugging-observability/SKILL.md) |
| Apply backoff, throughput, callback-queue and fallback patterns to Twilio messaging and voice at volume. | [twilio-reliability-patterns](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-reliability-patterns/SKILL.md) |
| Map Twilio sender types to required registrations: A2P 10DLC, toll-free, WhatsApp, RCS and voice trust programs. | [twilio-compliance-onboarding](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-compliance-onboarding/SKILL.md) |
| Compare Twilio number and sender types and the registration and caller-ID trust programs each one needs. | [twilio-numbers-senders](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-numbers-senders/SKILL.md) |
| Create, evaluate and submit Twilio regulatory bundles so international phone numbers can be provisioned. | [twilio-regulatory-compliance-bundles](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-regulatory-compliance-bundles/SKILL.md) |

**Agent assist, memory and knowledge**

| Task | Skill |
| --- | --- |
| Scope an AI agent-assist architecture for call centers using Twilio transcription, intelligence, memory and routing. | [twilio-agent-augmentation-architect](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-agent-augmentation-architect/SKILL.md) |
| Set up Twilio Conversation Intelligence operators and rules and query conversation results and aggregate insights. | [twilio-conversation-intelligence](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-conversation-intelligence/SKILL.md) |
| Store and recall per-customer profiles, traits, observations and summaries with Twilio Conversation Memory. | [twilio-conversation-memory](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-conversation-memory/SKILL.md) |
| Set up Twilio Conversation Orchestrator configs to capture voice and messaging traffic into memory-linked conversations. | [twilio-conversation-orchestrator](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-conversation-orchestrator/SKILL.md) |
| Provision Twilio Enterprise Knowledge bases, ingest web/PDF/text sources, and search chunks to ground agent answers. | [twilio-enterprise-knowledge](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-enterprise-knowledge/SKILL.md) |

**Routing and flows**

| Task | Skill |
| --- | --- |
| Author, validate, publish and update Twilio Studio flow definitions (IVR, SMS) through the Studio REST API. | [twilio-studio-flows](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-studio-flows/SKILL.md) |
| Set up Twilio TaskRouter workers, queues and workflows to route calls and AI-agent escalations to human agents. | [twilio-taskrouter-routing](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-taskrouter-routing/SKILL.md) |

**Webhooks and account security**

| Task | Skill |
| --- | --- |
| Receive and verify Twilio webhooks: signature checks, status callbacks, retry overrides, tunnels, Event Streams. | [twilio-webhook-architecture](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-webhook-architecture/SKILL.md) |
| Choose and implement Twilio authentication: API keys, OAuth2 client credentials, Access Tokens, test credentials. | [twilio-security-api-auth](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-security-api-auth/SKILL.md) |
| Harden a Twilio account: credential choice and rotation, webhook validation, PCI and HIPAA notes, fraud controls. | [twilio-security-hardening](https://github.com/twilio/ai/blob/main/skills/twilio/twilio-security-hardening/SKILL.md) |

### Zavu

[zavudev/zavu-skills](https://github.com/zavudev/zavu-skills) · **1 star** · [Apache-2.0](https://github.com/zavudev/zavu-skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Declare, deploy and test phone voice agents on Zavu Cloud, with tool handlers, transcripts and human handoff. | [voice-agent](https://github.com/zavudev/zavu-skills/blob/main/skills/voice-agent/SKILL.md) |

## Speech-to-text and text-to-speech APIs

Each skill here covers one speech API: recognition, synthesis or both. Use them when you pick your own recognizer or voice and wire it into an agent you build. Audio and transcripts go to the provider, so check its data terms before you send real caller audio.

### AssemblyAI

- [AssemblyAI/assemblyai-skill](https://github.com/AssemblyAI/assemblyai-skill) · **15 stars** · **No license file: linked only**
- [Skill index on assemblyai.com](https://assemblyai.com/docs/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

Keep the repository skill's reference guides beside its manifest, and use a supported SDK or REST client.

| Task | Skill |
| --- | --- |
| Prerecorded and streaming transcription, dictation, speech analytics, and voice-agent integrations. | [assemblyai](https://github.com/AssemblyAI/assemblyai-skill/blob/main/skills/assemblyai/SKILL.md) |
| Use AssemblyAI speech-to-text, streaming, Voice Agent API and LLM Gateway for voice applications. *Published on assemblyai.com.* | [assemblyai](https://assemblyai.com/docs/.well-known/agent-skills/assemblyai/skill.md) |

The documentation-site copy has frontmatter that is not valid YAML, because its description contains an unquoted colon. Quote the description before you install it.

The September 30 upstream revision updates its SDK examples to Python 1.6.1 and JavaScript 4.41.5 and covers [Universal-3.6 Pro Realtime](https://www.assemblyai.com/blog/universal-3-6-pro-realtime), published September 29. The new model identifier is `universal-3-6-pro`; 3.5 Pro Realtime remains available for comparisons. Match the streaming API and installed SDK to the example. A realtime model announcement does not establish support in the prerecorded or dictation APIs. Context7 still returned older 3.5 Pro examples during this review.

### Deepgram

#### SDK skills by language

Each SDK repository carries product-specific instructions for its own code and examples. Choose the language you use, and keep that repository's reference context available. Live requests require `DEEPGRAM_API_KEY` or an appropriate temporary token. These six SDK repositories have MIT licenses.

| Product | JavaScript | Python | Java | Go | Rust | .NET |
| --- | --- | --- | --- | --- | --- | --- |
| Standard STT | [Skill](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-speech-to-text/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-speech-to-text/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-java-sdk/blob/main/.agents/skills/deepgram-java-speech-to-text/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-go-sdk/blob/main/.agents/skills/deepgram-go-speech-to-text/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-rust-sdk/blob/main/.agents/skills/deepgram-rust-speech-to-text/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/.agents/skills/deepgram-dotnet-speech-to-text/SKILL.md) |
| Conversational STT / Flux | [Skill](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-conversational-stt/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-conversational-stt/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-java-sdk/blob/main/.agents/skills/deepgram-java-conversational-stt/SKILL.md) | [Current examples](https://github.com/deepgram/deepgram-go-sdk/blob/main/examples/speech-to-text/websocket/flux_channel/README.md)¹ | [Skill](https://github.com/deepgram/deepgram-rust-sdk/blob/main/.agents/skills/deepgram-rust-conversational-stt/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/.agents/skills/deepgram-dotnet-conversational-stt/SKILL.md) |
| TTS | [Skill](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-text-to-speech/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-text-to-speech/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-java-sdk/blob/main/.agents/skills/deepgram-java-text-to-speech/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-go-sdk/blob/main/.agents/skills/deepgram-go-text-to-speech/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-rust-sdk/blob/main/.agents/skills/deepgram-rust-text-to-speech/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/.agents/skills/deepgram-dotnet-text-to-speech/SKILL.md) |
| Voice agents | [Skill](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-voice-agent/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-voice-agent/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-java-sdk/blob/main/.agents/skills/deepgram-java-voice-agent/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-go-sdk/blob/main/.agents/skills/deepgram-go-voice-agent/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-rust-sdk/blob/main/.agents/skills/deepgram-rust-voice-agent/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/.agents/skills/deepgram-dotnet-voice-agent/SKILL.md) |
| Audio intelligence | [Skill](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-audio-intelligence/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-audio-intelligence/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-java-sdk/blob/main/.agents/skills/deepgram-java-audio-intelligence/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-go-sdk/blob/main/.agents/skills/deepgram-go-audio-intelligence/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-rust-sdk/blob/main/.agents/skills/deepgram-rust-audio-intelligence/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/.agents/skills/deepgram-dotnet-audio-intelligence/SKILL.md) |

¹ The Go conversational-STT manifest says that a v2 client and Flux examples do not exist. Its current repository already contains both, including a [typed v2 client example](https://github.com/deepgram/deepgram-go-sdk/blob/main/examples/speech-to-text/websocket/flux_channel/main.go). The stale manifest is excluded from the skill count.

The Java skills reference a root `reference.md` file that is absent from the checked repository. Use its [README](https://github.com/deepgram/deepgram-java-sdk/blob/main/README.md) and current source examples. Rust's voice-agent guide uses a raw WebSocket fallback with extra crates. Python's force-end-turn support requires the documented Flux provider or deployment enablement; it is not interchangeable with standard v1 STT.

<details>
<summary>Six SDK repositories: dated stars and license links</summary>

| SDK source | Stars observed | License |
| --- | ---: | --- |
| [deepgram/deepgram-js-sdk](https://github.com/deepgram/deepgram-js-sdk) | 274 | [MIT](https://github.com/deepgram/deepgram-js-sdk/blob/main/LICENSE) |
| [deepgram/deepgram-python-sdk](https://github.com/deepgram/deepgram-python-sdk) | 468 | [MIT](https://github.com/deepgram/deepgram-python-sdk/blob/main/LICENSE) |
| [deepgram/deepgram-java-sdk](https://github.com/deepgram/deepgram-java-sdk) | 11 | [MIT](https://github.com/deepgram/deepgram-java-sdk/blob/main/LICENSE) |
| [deepgram/deepgram-go-sdk](https://github.com/deepgram/deepgram-go-sdk) | 90 | [MIT](https://github.com/deepgram/deepgram-go-sdk/blob/main/LICENSE) |
| [deepgram/deepgram-rust-sdk](https://github.com/deepgram/deepgram-rust-sdk) | 66 | [MIT](https://github.com/deepgram/deepgram-rust-sdk/blob/main/LICENSE) |
| [deepgram/deepgram-dotnet-sdk](https://github.com/deepgram/deepgram-dotnet-sdk) | 55 | [MIT](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/LICENSE) |

</details>

#### Product guides

[Official collection](https://github.com/deepgram/skills/tree/main/skills) · **23 stars** · **No license file: linked only**

Use these for cross-language API guidance and deployment choices. The browser guide covers core, React, UI, and widget packages; browser authentication requires a server-issued temporary token. Self-hosting requires the appropriate entitlement and infrastructure.

| Task | Original skill |
| --- | --- |
| Speech recognition | [speech-to-text](https://github.com/deepgram/skills/blob/main/skills/speech-to-text/SKILL.md) |
| Speech synthesis | [text-to-speech](https://github.com/deepgram/skills/blob/main/skills/text-to-speech/SKILL.md) |
| Interactive voice agents | [voice-agent](https://github.com/deepgram/skills/blob/main/skills/voice-agent/SKILL.md) |
| Speech analytics | [audio-intelligence](https://github.com/deepgram/skills/blob/main/skills/audio-intelligence/SKILL.md) |
| Browser agents and voice widgets | [browser-agent](https://github.com/deepgram/skills/blob/main/skills/browser-agent/SKILL.md) |
| Self-hosting, optional deployment | [self-hosted](https://github.com/deepgram/skills/blob/main/skills/self-hosted/SKILL.md) |
| Reference for the speech-to-text, text-to-speech, and voice agent APIs: hosts, parameters, and known pitfalls | [api](https://github.com/deepgram/skills/blob/main/skills/api/SKILL.md) |
| Pick, clone, and run a starter app by feature and framework | [starters](https://github.com/deepgram/skills/blob/main/skills/starters/SKILL.md) |
| Find Deepgram's external repository of third-party integration examples for telephony, voice frameworks, and web | [examples](https://github.com/deepgram/skills/blob/main/skills/examples/SKILL.md) |
| Find Deepgram's external recipe repository of single-feature snippets in each language | [recipes](https://github.com/deepgram/skills/blob/main/skills/recipes/SKILL.md) |

The central README advertises Swift, Kotlin, and browser SDK repository URLs that returned HTTP 404 in this check. Those repositories are not indexed here. The browser packages documented by the browser-agent skill are available on npm; a broken repository link does not establish that a package is unavailable.

Deepgram's [September 18 correction](https://developers.deepgram.com/changelog/2026/9/18) withdraws earlier browser documentation about client-side Silero VAD. The microphone streams while unmuted; server speech events drive playback interruption. Token minting uses `ttl_seconds`, and an unknown `ttl` field can be ignored despite HTTP
200. The current browser skill reflects these corrections. Check older integrations
against the [shipped browser contract](https://developers.deepgram.com/docs/browser-agent-javascript).

### Fish Audio

[fishaudio/docs](https://github.com/fishaudio/docs) · **11 stars** · [CC-BY-4.0](https://github.com/fishaudio/docs/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Call Fish Audio TTS, ASR, voice design, voice models and WebSocket streaming directly over REST. | [fish-audio-api](https://github.com/fishaudio/docs/blob/main/.mintlify/skills/fish-audio-api/SKILL.md) |
| Use the official Fish Audio Python and TypeScript SDKs for TTS, STT, voice cloning and realtime TTS. | [fish-audio-sdk](https://github.com/fishaudio/docs/blob/main/.mintlify/skills/fish-audio-sdk/SKILL.md) |

### Gladia

- [gladiaio/skills](https://github.com/gladiaio/skills) · **1 star** · [MIT](https://github.com/gladiaio/skills/blob/main/LICENSE)
- [Skill index on docs.gladia.io](https://docs.gladia.io/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

| Task | Skill |
| --- | --- |
| Stream live audio to Gladia's real-time speech-to-text API over WebSocket with the JS/TS or Python SDK. | [gladia-live-transcription](https://github.com/gladiaio/skills/blob/main/plugins/gladia/skills/gladia-live-transcription/SKILL.md) |
| Transcribe audio files or URLs with Gladia's async pre-recorded API using the JS/TS or Python SDK. | [gladia-pre-recorded-transcription](https://github.com/gladiaio/skills/blob/main/plugins/gladia/skills/gladia-pre-recorded-transcription/SKILL.md) |
| Choose and configure Gladia audio intelligence features and check which work in live versus pre-recorded mode. | [gladia-audio-intelligence](https://github.com/gladiaio/skills/blob/main/plugins/gladia/skills/gladia-audio-intelligence/SKILL.md) |
| Install and configure the Gladia JS/TS and Python SDKs, and decide when raw REST is justified. | [gladia-sdk-integration](https://github.com/gladiaio/skills/blob/main/plugins/gladia/skills/gladia-sdk-integration/SKILL.md) |
| Diagnose Gladia API errors, limits, audio-format and transcription-quality problems with a verification checklist. | [gladia-troubleshooting](https://github.com/gladiaio/skills/blob/main/plugins/gladia/skills/gladia-troubleshooting/SKILL.md) |
| Transcribe audio with Gladia pre-recorded and live speech-to-text through its SDKs, CLI or REST API. *Published on docs.gladia.io.* | [gladia](https://docs.gladia.io/.well-known/agent-skills/gladia/skill.md) |

### iFlytek

[iflytek/iFly-Skills](https://github.com/iflytek/iFly-Skills) · **218 stars** · [Apache-2.0](https://github.com/iflytek/iFly-Skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Synthesize text to an MP3 file with iFlytek Hyper TTS through a Python CLI with selectable voices and prosody. | [iflytek-hyper-tts](https://github.com/iflytek/iFly-Skills/blob/main/skills/iflytek-hyper-tts/SKILL.md) |
| Transcribe MP3 recordings with iFlytek Speed Transcription through a Python CLI with domain and speaker options. | [iflytek-speed-transcription](https://github.com/iflytek/iFly-Skills/blob/main/skills/iflytek-speed-transcription/SKILL.md) |

The repository also has a voice-clone skill that is not linked. Its script turns off TLS certificate checks and sends voice samples and auth tokens over plain http. See [Use with care](#use-with-care).

### Jellypod

[Jellypod-Inc/speech-sdk](https://github.com/Jellypod-Inc/speech-sdk) · **52 stars** · [Apache-2.0](https://github.com/Jellypod-Inc/speech-sdk/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Generate, stream and stitch multi-speaker text-to-speech across many providers with the @speech-sdk/core library. | [speech-sdk](https://github.com/Jellypod-Inc/speech-sdk/blob/main/skills/speech-sdk/SKILL.md) |

### Moonshine

[moonshine-ai/moonshine](https://github.com/moonshine-ai/moonshine) · **11,162 stars** · [MIT code](https://github.com/moonshine-ai/moonshine/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Integrate local speech recognition and supported speech workflows with Moonshine. | [moonshine-voice](https://github.com/moonshine-ai/moonshine/blob/main/.agents/skills/moonshine-voice/SKILL.md) |

Its current LICENSE assigns MIT to streaming STT and English STT models, while listed legacy nonstreaming non-English models have noncommercial terms. TTS/G2P assets carry separate source terms. See the [resource qualifications](resources.md#current-source-caveats) and the exact source licenses in [linked-skills.json](../linked-skills.json).

### OpenRouter

[OpenRouterTeam/skills](https://github.com/OpenRouterTeam/skills) · **275 stars** · **No license file: linked only**

| Task | Skill |
| --- | --- |
| Send audio to OpenRouter's JSON/base64 transcription endpoint and read back text (curl, TypeScript, Python). | [openrouter-stt](https://github.com/OpenRouterTeam/skills/blob/main/skills/openrouter-stt/SKILL.md) |
| Synthesize speech to mp3 or pcm files via OpenRouter, including voice discovery and chunking of long text. | [openrouter-tts](https://github.com/OpenRouterTeam/skills/blob/main/skills/openrouter-tts/SKILL.md) |

### pyannoteAI

[Skill index on docs.pyannote.ai](https://docs.pyannote.ai/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

The skill creates voiceprints, which identify people by voice. It gives no consent guidance.

| Task | Skill |
| --- | --- |
| Diarize audio, create voiceprints, identify speakers and stream live diarization via the pyannoteAI API. *Published on docs.pyannote.ai.* | [pyannote](https://docs.pyannote.ai/.well-known/agent-skills/pyannote/skill.md) |

### Rime

[Skill index on docs.rime.ai](https://docs.rime.ai/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

| Task | Skill |
| --- | --- |
| Synthesize speech with Rime TTS over HTTP or WebSocket, choose models and voices, and wire it into voice agents. *Published on docs.rime.ai.* | [rimelabs](https://docs.rime.ai/.well-known/agent-skills/rimelabs/skill.md) |

### Sarvam AI

[sarvamai/skills](https://github.com/sarvamai/skills) · **73 stars** · [Apache-2.0](https://github.com/sarvamai/skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Write Sarvam Saaras speech-to-text code for REST, Batch with diarization, and WebSocket streaming. | [speech-to-text](https://github.com/sarvamai/skills/blob/main/speech-to-text/SKILL.md) |
| Write Sarvam Bulbul text-to-speech code over REST, HTTP stream and WebSocket, including pronunciation dictionaries. | [text-to-speech](https://github.com/sarvamai/skills/blob/main/text-to-speech/SKILL.md) |
| Build real-time Indic voice agents with Sarvam STT, TTS and LLM on LiveKit or Pipecat in Python. | [voice-agents](https://github.com/sarvamai/skills/blob/main/voice-agents/SKILL.md) |
| Use the Sarvam MCP server from an agent for live Indic translate, STT, TTS, dubbing and API-code help. | [sarvam-mcp](https://github.com/sarvamai/skills/blob/main/sarvam-mcp/SKILL.md) |
| Build a Sarvam dubbing job pipeline that localizes video or audio into Indian languages with voice cloning. | [dubbing](https://github.com/sarvamai/skills/blob/main/dubbing/SKILL.md) |

### Shiny

[shinyorg/skills](https://github.com/shinyorg/skills) · **4 stars** · [MIT](https://github.com/shinyorg/skills/blob/main/LICENSE)

The Shiny Speech skill gives microphone capture, playback, recognition, synthesis, and platform audio processing guidance for native .NET apps. **Optional prerelease workflow:** the inspected core APIs are in `3.0.0-beta-0030` packages targeting .NET 10; stable Shiny.Speech `2.1.0` and the SDK's default branch do not expose the same surface. Follow the versioned package and [current documentation](https://shinylib.net/speech/), preserving `reference/api-reference.md` with the skill.

<details>
<summary>Preview and beta APIs (1 optional skill)</summary>

These target alpha or beta features or APIs that can change. Check the current documentation before you use them.

| Task | Skill |
| --- | --- |
| Capture audio, play it back, recognize and synthesize speech, and use platform audio processing in a .NET app. | [shiny-speech](https://github.com/shinyorg/skills/blob/main/plugins/shiny/skills/shiny-speech/SKILL.md) |

</details>

The upstream overview and later sections disagree about monitor/device support on Linux. Verify each target platform before using those features. Processing flags do not guarantee echo cancellation or suppression on every device, driver, or recognition backend. The reviewed package XML confirms selected API members; no integration was compiled or run. This skill supplies a frontend, not an entire voice-agent runtime.

### StepFun

[stepfun-ai/StepAudio-Skills](https://github.com/stepfun-ai/StepAudio-Skills) · **29 stars** · [Apache-2.0](https://github.com/stepfun-ai/StepAudio-Skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Transcribe audio files to text with the StepFun ASR streaming (SSE) API through a Python CLI. | [step-asr](https://github.com/stepfun-ai/StepAudio-Skills/blob/main/skills/step-asr/SKILL.md) |
| Synthesize speech and create cloned voices with StepFun TTS through a bash CLI. | [step-tts](https://github.com/stepfun-ai/StepAudio-Skills/blob/main/skills/step-tts/SKILL.md) |
| Call StepFun step-audio-r1.1 chat completions with text or audio input; save the reply audio, transcript and raw JSON. | [stepfun-step-audio-r1-1](https://github.com/stepfun-ai/StepAudio-Skills/blob/main/skills/stepfun-step-audio-r1-1/SKILL.md) |

### Together AI

[togethercomputer/skills](https://github.com/togethercomputer/skills) · **36 stars** · [MIT](https://github.com/togethercomputer/skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Use Together AI audio APIs: TTS (REST, streaming, WebSocket) plus transcription, diarization and realtime STT. | [together-audio](https://github.com/togethercomputer/skills/blob/main/skills/together-audio/SKILL.md) |

### Venice AI

[veniceai/skills](https://github.com/veniceai/skills) · **145 stars** · [MIT](https://github.com/veniceai/skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Venice text-to-speech and voice-cloning reference: endpoint parameters, model and voice families, formats and limits. | [venice-audio-speech](https://github.com/veniceai/skills/blob/main/skills/venice-audio-speech/SKILL.md) |
| Venice speech-to-text reference: multipart upload, model choices, response options, size limit and error codes. | [venice-audio-transcription](https://github.com/veniceai/skills/blob/main/skills/venice-audio-transcription/SKILL.md) |

## Frameworks and real-time infrastructure

Open-source frameworks and real-time media infrastructure for agents you run yourself. LiveKit Agents and Pipecat also have bundled skills in the [core catalogue](catalog.md).

### Daily

[Skill index on docs.daily.co](https://docs.daily.co/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

The skill covers the Daily video-calling APIs in general and does not mention voice agents. Its meeting-token curl example builds invalid JSON, so do not copy it as written.

| Task | Skill |
| --- | --- |
| Create Daily rooms and meeting tokens, embed call UIs, and configure recording, streaming, transcription and webhooks. *Published on docs.daily.co.* | [daily](https://docs.daily.co/.well-known/agent-skills/daily/skill.md) |

### NVIDIA

- [NVIDIA/skills](https://github.com/NVIDIA/skills) · **3,490 stars** · [CC-BY-4.0 documentation; Apache-2.0 code](https://github.com/NVIDIA/skills/blob/main/LICENSE-APACHE)
- [nvidia-riva/Nemotron-speech-skills](https://github.com/nvidia-riva/Nemotron-speech-skills) · **3 stars** · [CC-BY-4.0 documentation; Apache-2.0 code](https://github.com/nvidia-riva/Nemotron-speech-skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Guide building and iterating NVIDIA voice agents (ASR-LLM-TTS or audio-in LLM) on Pipecat or LiveKit. | [nemotron-voice-agent-builder](https://github.com/NVIDIA/skills/blob/main/skills/nemotron-voice-agent-builder/SKILL.md) |
| Choose ASR, TTS, and NMT NIMs and follow streaming, pronunciation, hosted, and self-hosted deployment workflows. | [nemotron-speech](https://github.com/nvidia-riva/Nemotron-speech-skills/blob/main/skills/nemotron-speech/SKILL.md) |
| Scope ASR domain or language adaptation for NVIDIA Nemotron Speech/Riva and pick boosting, n-gram LM or fine-tuning. | [nemotron-asr-finetune](https://github.com/NVIDIA/skills/blob/main/skills/nemotron-asr-finetune/SKILL.md) |

NVIDIA's manifests mention Apache-2.0, but the repository license distinguishes documentation (CC-BY-4.0) from source code (Apache-2.0). Model, hosted-service, and container terms need their own review.

### Pipecat

[Skill index on docs.pipecat.ai](https://docs.pipecat.ai/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

Pipecat's own skills are in the [core catalogue](catalog.md#pipecat). The documentation-site skill below adds Pipecat Cloud and Flows. Its deploy steps upload your local `.env` file, which holds provider API keys, to Pipecat Cloud.

| Task | Skill |
| --- | --- |
| Build Pipecat voice agents (STT, LLM, TTS pipelines), structure them with Flows, and deploy to Pipecat Cloud. *Published on docs.pipecat.ai.* | [Pipecat](https://docs.pipecat.ai/.well-known/agent-skills/pipecat/skill.md) |

## Cloud providers

These skills cover different account and deployment models. Resolve the current service and SDK reference before you adopt a sample endpoint or model name.

### AWS

<details>
<summary>Seven source repositories: stars and licenses</summary>

| Source | Stars | License |
| --- | ---: | --- |
| [aws-samples/amazon-nova-samples](https://github.com/aws-samples/amazon-nova-samples) | 453 | [MIT-0](https://github.com/aws-samples/amazon-nova-samples/blob/main/LICENSE) |
| [aws-samples/sample-ai-agent-skills](https://github.com/aws-samples/sample-ai-agent-skills) | 5 | [MIT-0](https://github.com/aws-samples/sample-ai-agent-skills/blob/main/LICENSE) |
| [aws-samples/sample-aicc-builder-for-amazon-connect-ai-agent](https://github.com/aws-samples/sample-aicc-builder-for-amazon-connect-ai-agent) | 17 | [MIT-0](https://github.com/aws-samples/sample-aicc-builder-for-amazon-connect-ai-agent/blob/main/LICENSE) |
| [aws-samples/sample-amazon-connect-speed-dial](https://github.com/aws-samples/sample-amazon-connect-speed-dial) | 2 | [MIT-0](https://github.com/aws-samples/sample-amazon-connect-speed-dial/blob/main/LICENSE) |
| [aws-samples/sample-amazon-nova-sonic-eval-harness](https://github.com/aws-samples/sample-amazon-nova-sonic-eval-harness) | 8 | [MIT-0](https://github.com/aws-samples/sample-amazon-nova-sonic-eval-harness/blob/main/LICENSE) |
| [aws-samples/sample-ramp-aidlc-mod-starter-packs](https://github.com/aws-samples/sample-ramp-aidlc-mod-starter-packs) | 10 | [MIT-0](https://github.com/aws-samples/sample-ramp-aidlc-mod-starter-packs/blob/main/LICENSE) |
| [aws-samples/sample-voice-agent-on-aws](https://github.com/aws-samples/sample-voice-agent-on-aws) | 12 | [MIT-0](https://github.com/aws-samples/sample-voice-agent-on-aws/blob/main/LICENSE) |

</details>

These come from AWS sample repositories, not from AWS service documentation. The nova-sonic-voice-agent skill builds on the Strands BidiAgent API, which is marked experimental. Its example server is demo grade: no authentication, open CORS, and it binds to all interfaces by default.

**Build Nova Sonic voice agents**

| Task | Skill |
| --- | --- |
| Build a Nova Sonic voice agent from scratch with a FastAPI WebSocket server, Strands BidiAgent, tools and sub-agents. | [nova-sonic-voice-agent](https://github.com/aws-samples/sample-voice-agent-on-aws/blob/main/skills/nova-sonic-voice-agent/SKILL.md) |
| Design guidance for Nova Sonic voice agents: model choice, spoken prompts, tool results, barge-in, and confirmations. The upstream file is cut off near the end. | [nova-sonic-best-practices](https://github.com/aws-samples/sample-ramp-aidlc-mod-starter-packs/blob/main/skills-library/nova-sonic-best-practices/SKILL.md) |
| Checklist for cutting Nova Sonic voice-agent latency and cost and adding multi-Region reliability on AWS. | [nova-sonic-optimization](https://github.com/aws-samples/sample-ramp-aidlc-mod-starter-packs/blob/main/skills-library/nova-sonic-optimization/SKILL.md) |

**Deploy on Amazon Connect**

| Task | Skill |
| --- | --- |
| Scaffold and deploy an Amazon Connect instance with a Nova Sonic 2 agent via CDK, claim a UK number, and smoke test. | [connect-bootstrap](https://github.com/aws-samples/sample-amazon-connect-speed-dial/blob/main/SKILL.md) |
| Interview-driven generator of Amazon Connect AI agent PoC assets, with validation gates and a deploy hand-off. | [aicc-builder](https://github.com/aws-samples/sample-aicc-builder-for-amazon-connect-ai-agent/blob/main/skills/aicc-builder-skill/claude/SKILL.md) |

**Test Nova Sonic agents**

These three work only inside the layout of the Nova Sonic eval-harness repository.

| Task | Skill |
| --- | --- |
| Turn a scenario description into a Nova Sonic eval-harness test config JSON with prompts, tools, and criteria. | [config-generator](https://github.com/aws-samples/sample-amazon-nova-sonic-eval-harness/blob/main/.kiro/skills/config-generator/SKILL.md) |
| Read Nova Sonic eval-harness batch and session results, find failure patterns, and suggest prompt and config fixes. | [eval-analyzer](https://github.com/aws-samples/sample-amazon-nova-sonic-eval-harness/blob/main/.kiro/skills/eval-analyzer/SKILL.md) |
| Generate mock tool handler modules and matching toolSpec JSON for Nova Sonic eval-harness test scenarios. | [tool-builder](https://github.com/aws-samples/sample-amazon-nova-sonic-eval-harness/blob/main/.kiro/skills/tool-builder/SKILL.md) |

**Diagnose AWS voice and contact services with the AWS CLI**

| Task | Skill |
| --- | --- |
| Diagnose Amazon Connect routing, agent, telephony and integration problems using AWS CLI checks and runbooks. | [connect-diagnostics](https://github.com/aws-samples/sample-ai-agent-skills/blob/main/connect-troubleshooting/SKILL.md) |
| Troubleshoot Amazon Connect Contact Lens analytics and Wisdom knowledge base problems with AWS CLI checks. | [connect-analytics-diagnostics](https://github.com/aws-samples/sample-ai-agent-skills/blob/main/connect-analytics-troubleshooting/SKILL.md) |
| Troubleshoot Amazon Lex bot builds, intent and slot recognition, fulfillment Lambdas and V1-to-V2 migration via AWS CLI. | [lex-diagnostics](https://github.com/aws-samples/sample-ai-agent-skills/blob/main/lex-troubleshooting/SKILL.md) |
| Troubleshoot Amazon Polly synthesis, SSML, lexicon, neural voice and async task problems with AWS CLI checks. | [polly-diagnostics](https://github.com/aws-samples/sample-ai-agent-skills/blob/main/polly-troubleshooting/SKILL.md) |
| Troubleshoot Amazon Transcribe batch, streaming, vocabulary, call analytics and medical jobs with AWS CLI checks. | [transcribe-diagnostics](https://github.com/aws-samples/sample-ai-agent-skills/blob/main/transcribe-troubleshooting/SKILL.md) |
| Troubleshoot Amazon Chime SDK meetings, messaging, SIP media applications and PSTN audio with AWS CLI checks. | [chimesdk-diagnostics](https://github.com/aws-samples/sample-ai-agent-skills/blob/main/chimesdk-troubleshooting/SKILL.md) |

<details>
<summary>Migration (1 optional skill)</summary>

Use these to move an existing agent or integration. They can change application code, create resources, and transfer configuration. Review the requested scope before you authorize them.

| Task | Skill |
| --- | --- |
| Convert an existing text agent into a Nova Sonic speech-to-speech agent with a WebSocket server and browser client. | [text-agent-to-nova-sonic-voice](https://github.com/aws-samples/amazon-nova-samples/blob/main/skills/text-agent-to-strands-voice-agent/SKILL.md) |

</details>

### Azure

- [microsoft/skills](https://github.com/microsoft/skills) · **3,066 stars** · [MIT](https://github.com/microsoft/skills/blob/main/LICENSE)
- [MicrosoftDocs/Agent-Skills](https://github.com/MicrosoftDocs/Agent-Skills) · **767 stars** · [CC-BY-4.0 documentation; MIT code](https://github.com/MicrosoftDocs/Agent-Skills/blob/main/LICENSE)
- [Azure-Samples/Cognitive-Speech-TTS](https://github.com/Azure-Samples/Cognitive-Speech-TTS) · **1,014 stars** · [MIT, stated for SDK code only](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/LICENSE.md)

Azure samples may use preview versions. Resolve the current service and SDK reference before adopting a sample endpoint or model name. The Azure-Samples license file says MIT applies to SDK code. It does not say whether that covers the skill text, so do not copy those two skills without checking.

**Voice Live and Speech**

| Task | Skill |
| --- | --- |
| Build bidirectional voice applications with Azure.AI.VoiceLive: VAD, session events, tools, and audio lifecycle. | [azure-ai-voicelive-dotnet](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-dotnet/skills/azure-ai-voicelive-dotnet/SKILL.md) |
| Build reactive Java voice sessions over WebSocket with Azure AI VoiceLive. | [azure-ai-voicelive-java](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-java/skills/azure-ai-voicelive-java/SKILL.md) |
| Run Python bidirectional voice sessions with events, VAD, function calling, transcription, and Azure voices. | [azure-ai-voicelive-py](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-python/skills/azure-ai-voicelive-py/SKILL.md) |
| Use Node and browser Voice Live SDK patterns for streaming, function calling, and lifecycle. | [azure-ai-voicelive-ts](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-typescript/skills/azure-ai-voicelive-ts/SKILL.md) |
| Transcribe short files with a REST utility. It explicitly excludes real-time streaming and long audio. **Optional.** | [azure-speech-to-text-rest-py](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-python/skills/azure-speech-to-text-rest-py/SKILL.md) |
| Use a live index of official documentation for STT and TTS, Voice Live, containers, streaming, security, and quotas. | [azure-speech](https://github.com/MicrosoftDocs/Agent-Skills/blob/main/skills/azure-speech/SKILL.md) |

**Azure Communication Services**

| Task | Skill |
| --- | --- |
| Drive calls with the Azure Communication Services Call Automation Java SDK: IVR prompts, DTMF, recording, transfer. | [azure-communication-callautomation-java](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-java/skills/azure-communication-callautomation-java/SKILL.md) |
| Topic-to-URL index of Azure Communication Services docs, fetched on demand from Microsoft Learn. | [azure-communication-services](https://github.com/MicrosoftDocs/Agent-Skills/blob/main/skills/azure-communication-services/SKILL.md) |

**Foundry voice agent samples**

| Task | Skill |
| --- | --- |
| Diagnose failures in the Foundry Voice Agent sample stack from session recordings, logs and Project settings. | [debug-local-session](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/VoiceAgent/skills/debug-local-session/SKILL.md) |

<details>
<summary>Preview and beta APIs (1 optional skill)</summary>

These target alpha or beta features or APIs that can change. Check the current documentation before you use them.

| Task | Skill |
| --- | --- |
| Create and test Azure AI Foundry preview voice agents in Python, with MCP, knowledge-base and local function tools. | [voice-agent-preview](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/VoiceAgent/skills/voice-agent-preview/SKILL.md) |

</details>

The Azure AI Transcription Python manifest was excluded: its streaming and batch method examples are absent from the released SDK checked in this review. Use the [current SDK README](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/transcription/azure-ai-transcription/README.md) for supported file-transcription methods.

MicrosoftDocs' Azure Speech entry is a generated documentation index, dated 2026-09-27 in its metadata. Use its live documentation links; its illustrative `security.md` reference is not a file in that skill folder.

#### Azure SDK version notes

Checked against released package contents on **2026-09-30 UTC**. These are focused source checks; none of the provider workflows was executed.

| Skill | Qualification for current use | Primary API reference |
| --- | --- | --- |
| Voice Live Java | Its `1.0.0-beta.2` pin accepts `startSession(String)`. Release `1.1.0` uses a model-plus-options overload; preserve the pin or migrate deliberately. | [Java client source](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/voicelive/azure-ai-voicelive/src/main/java/com/azure/ai/voicelive/VoiceLiveAsyncClient.java) |
| Voice Live TypeScript | The quick-start handler should be `onConversationItemInputAudioTranscriptionCompleted`. The shorter name is absent from both the pinned beta and released `1.1.0`. | [Public API declarations](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/voicelive/ai-voicelive/review/ai-voicelive-node.api.md) |
| Voice Live .NET | The hierarchy's `SendAudioAsync` name should be `SendInputAudioAsync`. Checked in `1.0.0` and released `1.2.0`; other sampled lifecycle methods exist. | [.NET public API](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/voicelive/Azure.AI.VoiceLive/api/Azure.AI.VoiceLive.netstandard2.0.cs) |
| Voice Live Python | Central session, audio-buffer, and response methods exist in released `1.3.0`. This check does not cover every model, endpoint, or authentication branch. | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/voicelive/azure-ai-voicelive/README.md) |

### Google

- [google-gemini/gemini-skills](https://github.com/google-gemini/gemini-skills) · **4,234 stars** · [Apache-2.0](https://github.com/google-gemini/gemini-skills/blob/main/LICENSE)
- [google/skills](https://github.com/google/skills) · **20,529 stars** · [Apache-2.0](https://github.com/google/skills/blob/main/LICENSE)
- [GoogleCloudPlatform/cxas-scrapi](https://github.com/GoogleCloudPlatform/cxas-scrapi) · **104 stars** · [Apache-2.0](https://github.com/GoogleCloudPlatform/cxas-scrapi/blob/main/LICENSE.txt)

Gemini Developer API credentials and Google Cloud authentication are not interchangeable.

| Task | Skill |
| --- | --- |
| Build Developer API audio, video, and text sessions with VAD, nonblocking tools, ephemeral tokens, transcription, and migration. | [gemini-live-api-dev](https://github.com/google-gemini/gemini-skills/blob/main/skills/gemini-live-api-dev/SKILL.md) |
| Scaffold a cloud-authenticated Live API client with session resumption, token refresh, protobuf messages, and a demo. | [gemini-live-api](https://github.com/google/skills/blob/main/skills/cloud/gemini-live-api/SKILL.md) |
| Plan a multimodal cloud solution, including voice. It is broader than voice agents. **Optional.** | [google-cloud-solution-agentic-ai-bidirectional-streaming](https://github.com/google/skills/blob/main/skills/cloud/google-cloud-solution-agentic-ai-bidirectional-streaming/SKILL.md) |
| Lifecycle workflow for Google CES/CXAS agents: build from a PRD, run evals, triage failures, push with the cxas CLI. | [cxas-agent-foundry](https://github.com/GoogleCloudPlatform/cxas-scrapi/blob/main/.agents/skills/cxas-agent-foundry/SKILL.md) |
| Audit and remediate CXAS agent configs for Gemini Composite V1 voice: Director's Notes, accents, prompts, tool pacing. | [cxas-composite-voice-agent-optimizer](https://github.com/GoogleCloudPlatform/cxas-scrapi/blob/main/.agents/skills/cxas-composite-voice-agent-optimizer/SKILL.md) |
| Fetch non-contained CCAI Insights conversations for a CXAS app and cluster failure patterns into a Markdown report. | [cxas-loss-analysis](https://github.com/GoogleCloudPlatform/cxas-scrapi/blob/main/.agents/skills/cxas-loss-analysis/SKILL.md) |
| Export a CES app's golden evals, convert them to SCRAPI simulation cases with Gemini, and run them with an HTML report. | [cxas-sim-eval](https://github.com/GoogleCloudPlatform/cxas-scrapi/blob/main/.agents/skills/cxas-sim-eval/SKILL.md) |

## Testing, evaluation and monitoring

Skills for simulated callers, test suites, scoring and call review. Runs can place calls and use metered credits, and several skills read production transcripts. Set a run size first, and use a non-production agent where you can. Some platforms include their own test skills: ElevenLabs, Vapi (simulations), Synthflow, AWS Nova Sonic and Google CX Agent Studio. They are listed under those providers.

### Bluejay

- [bluejay-ai-dev/bluejay-skills](https://github.com/bluejay-ai-dev/bluejay-skills) · **0 stars** · **No license file: linked only**
- [Skill index on docs.getbluejay.ai](https://docs.getbluejay.ai/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

| Task | Skill |
| --- | --- |
| Queue a Bluejay simulation run for a voice agent and summarize pass rate and per-metric results. | [run-simulation](https://github.com/bluejay-ai-dev/bluejay-skills/blob/main/bluejay/skills/run-simulation/SKILL.md) |
| Generate a varied set of Bluejay digital-human test callers and attach them to a simulation. | [persona-suite](https://github.com/bluejay-ai-dev/bluejay-skills/blob/main/bluejay/skills/persona-suite/SKILL.md) |
| Load-test a voice agent with a high-concurrency Bluejay simulation and report degradation under load. | [load-test](https://github.com/bluejay-ai-dev/bluejay-skills/blob/main/bluejay/skills/load-test/SKILL.md) |
| Run adversarial simulated callers against a Bluejay agent and report guardrail failures with fixes. | [red-team-sweep](https://github.com/bluejay-ai-dev/bluejay-skills/blob/main/bluejay/skills/red-team-sweep/SKILL.md) |
| Cluster failed Bluejay production calls from transcripts into ranked failure modes with prioritized fixes. | [failed-call-triage](https://github.com/bluejay-ai-dev/bluejay-skills/blob/main/bluejay/skills/failed-call-triage/SKILL.md) |
| Find where a Bluejay agent's response latency comes from using call logs, traces and spans. | [latency-triage](https://github.com/bluejay-ai-dev/bluejay-skills/blob/main/bluejay/skills/latency-triage/SKILL.md) |
| Test voice and chat agents with simulated customers, score production calls with custom metrics, and version agents. *Published on docs.getbluejay.ai.* | [bluejay](https://docs.getbluejay.ai/.well-known/agent-skills/bluejay/skill.md) |

### Cekura

- [cekura-ai/cekura-skills](https://github.com/cekura-ai/cekura-skills) · **7 stars** · [MIT](https://github.com/cekura-ai/cekura-skills/blob/main/LICENSE)
- [Skill index on docs.cekura.ai](https://docs.cekura.ai/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

Six of the eight repository skills tell the agent to call the vendor tool `mcp__cekura__cekura_skill_started` before anything else. See [Use with care](#use-with-care).

| Task | Skill |
| --- | --- |
| Walk through registering an existing voice agent on Cekura, from provider setup to a verification run. | [cekura-create-agent](https://github.com/cekura-ai/cekura-skills/blob/main/cekura/skills/cekura-create-agent/SKILL.md) |
| Design, generate and revise Cekura evaluators (test scenarios) for voice and chat agents, including scripted call flows. | [cekura-eval-design](https://github.com/cekura-ai/cekura-skills/blob/main/cekura/skills/cekura-eval-design/SKILL.md) |
| Design, test and troubleshoot Cekura LLM-judge and custom-code metrics for scoring voice agent calls. | [cekura-metric-design](https://github.com/cekura-ai/cekura-skills/blob/main/cekura/skills/cekura-metric-design/SKILL.md) |
| Turn flagged production call failures into Cekura evaluator scenarios, test profiles and metric choices. | [cekura-generate-scenarios](https://github.com/cekura-ai/cekura-skills/blob/main/cekura/skills/cekura-generate-scenarios/SKILL.md) |
| Triage recent Cekura production call logs into failure flags and an outcome breakdown with percentages. | [cekura-flag-call-log-failures](https://github.com/cekura-ai/cekura-skills/blob/main/cekura/skills/cekura-flag-call-log-failures/SKILL.md) |
| Keep a repo's committed Cekura test suite in step with a pull request diff, usually by making no change. | [cekura-bot-test-writer](https://github.com/cekura-ai/cekura-skills/blob/main/cekura/skills/cekura-bot-test-writer/SKILL.md) |
| Write a Cekura JSON regression suite and CI workflow for a voice-agent repo, linted and dry-run validated. | [cekura-infra-test-suite](https://github.com/cekura-ai/cekura-skills/blob/main/cekura/skills/cekura-infra-test-suite/SKILL.md) |
| Reproduce a voice-agent failure in Cekura simulation, apply and verify a config fix, then promote it. | [cekura-self-improving-agent](https://github.com/cekura-ai/cekura-skills/blob/main/cekura/skills/cekura-self-improving-agent/SKILL.md) |
| Create evaluators and metrics, run simulated calls against voice agents, and monitor production calls in Cekura. *Published on docs.cekura.ai.* | [Cekura](https://docs.cekura.ai/.well-known/agent-skills/cekura/skill.md) |

### Coval

- [coval-ai/coval-external-skills](https://github.com/coval-ai/coval-external-skills) · **2 stars** · [MIT](https://github.com/coval-ai/coval-external-skills/blob/main/LICENSE)
- [Skill index on docs.coval.ai](https://docs.coval.ai/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

Coval's selected workflows cover evidence review, test suites, evaluator calibration, and matched comparisons. They can evaluate voice or chat agents; choose actual audio tests when the claim concerns speech. Hosted runs require an authorized workspace and budget. Keep helper scripts and references with the skill, and set a bounded run size before execution.

| Task | Skill |
| --- | --- |
| Choose an evaluation workflow and define the evidence needed next. | [coval-eval-start](https://github.com/coval-ai/coval-external-skills/blob/main/skills/evaluation/coval-eval-start/SKILL.md) |
| Find recurring failure patterns in existing evaluation evidence. | [coval-discover-failures](https://github.com/coval-ai/coval-external-skills/blob/main/skills/evaluation/coval-discover-failures/SKILL.md) |
| Compare a scoring metric with labeled examples and inspect disagreements. | [coval-calibrate-metric](https://github.com/coval-ai/coval-external-skills/blob/main/skills/evaluation/coval-calibrate-metric/SKILL.md) |
| Compare matched runs without hiding retries, missing cases, or changed conditions. | [coval-compare-runs](https://github.com/coval-ai/coval-external-skills/blob/main/skills/evaluation/coval-compare-runs/SKILL.md) |
| Audit evaluation coverage, evidence quality, and unsupported conclusions. | [coval-eval-audit](https://github.com/coval-ai/coval-external-skills/blob/main/skills/evaluation/coval-eval-audit/SKILL.md) |
| Run a bounded evaluation against an authorized agent and test set. | [quick-eval](https://github.com/coval-ai/coval-external-skills/blob/main/skills/runs/quick-eval/SKILL.md) |
| Turn a task and its known failure modes into a focused test suite. | [build-test-suite](https://github.com/coval-ai/coval-external-skills/blob/main/skills/test-cases/build-test-suite/SKILL.md) |
| Define task-specific evaluation metrics and scoring criteria. | [configure-metrics](https://github.com/coval-ai/coval-external-skills/blob/main/skills/metrics/configure-metrics/SKILL.md) |
| Interactively design and create a Coval simulation persona for testing a voice or chat agent. | [design-persona](https://github.com/coval-ai/coval-external-skills/blob/main/skills/personas/design-persona/SKILL.md) |
| Create accent personas and run a per-accent Coval simulation sweep with a comparison table and saved report. | [run-accent-testing](https://github.com/coval-ai/coval-external-skills/blob/main/skills/runs/run-accent-testing/SKILL.md) |
| Build an adversarial test set, persona and metric in Coval, run red-team simulations, and score each scenario. | [run-adversarial-testing](https://github.com/coval-ai/coval-external-skills/blob/main/skills/runs/run-adversarial-testing/SKILL.md) |
| Launch one Coval simulation run per audio-condition persona and build the multi-run report link. | [run-audio-quality-testing](https://github.com/coval-ai/coval-external-skills/blob/main/skills/runs/run-audio-quality-testing/SKILL.md) |
| Simulate conversations against voice and chat agents, score them with metrics, and track regressions in Coval. *Published on docs.coval.ai.* | [coval](https://docs.coval.ai/.well-known/agent-skills/coval/skill.md) |

Coval's source files are MIT licensed. Older specialist launch recipes have whole-set defaults and less bounded retry/watch behavior; this selection favors the newer evaluation workflows. Three skills added later (the accent, adversarial and audio-quality runs) launch several simulation runs each and use metered usage. Their optional report sharing can make runs public or publish a link that needs no login.

### Roark

- [roarkhq/mcp-roark-analytics](https://github.com/roarkhq/mcp-roark-analytics) · **0 stars** · [Apache-2.0](https://github.com/roarkhq/mcp-roark-analytics/blob/main/LICENSE)
- [Skill index on docs.roark.ai](https://docs.roark.ai/.well-known/agent-skills/index.json) · **Vendor documentation site, not a repository** · **No license confirmed: linked only**

Several of the repository skills rely on shared guides outside their own folders (roark-concepts). Install them together.

| Task | Skill |
| --- | --- |
| Create Roark simulated-caller personas and improv customer flows, and pick test environments, through the SDK. | [author-personas-flows](https://github.com/roarkhq/mcp-roark-analytics/blob/main/plugins/roark/skills/author-personas-flows/SKILL.md) |
| Author Roark scripted customer flows as step graphs covering IVR menus, DTMF keypad entry, silence and voicemail. | [author-scripted-flows](https://github.com/roarkhq/mcp-roark-analytics/blob/main/plugins/roark/skills/author-scripted-flows/SKILL.md) |
| Choose built-in Roark metrics, add pass/fail checks, and author custom LLM-judge, formula or pattern metrics. | [configure-metrics](https://github.com/roarkhq/mcp-roark-analytics/blob/main/plugins/roark/skills/configure-metrics/SKILL.md) |
| Configure a Roark simulation run plan, preview its call count, and start the run against a voice or chat agent. | [build-run-plan](https://github.com/roarkhq/mcp-roark-analytics/blob/main/plugins/roark/skills/build-run-plan/SKILL.md) |
| Gate a deploy or CI pipeline on a Roark simulation: start a run, wait, then assert pass/fail check metrics. | [gate-ci](https://github.com/roarkhq/mcp-roark-analytics/blob/main/plugins/roark/skills/gate-ci/SKILL.md) |
| Grade real production calls and chats with Roark metrics using standing policies or one-off backfill jobs. | [monitor-live-calls](https://github.com/roarkhq/mcp-roark-analytics/blob/main/plugins/roark/skills/monitor-live-calls/SKILL.md) |
| Run simulated-caller tests on voice agents, score live calls with metrics, and manage Roark config via its CLI. *Published on docs.roark.ai.* | [roark](https://docs.roark.ai/.well-known/agent-skills/roark/skill.md) |

### Superlog

[superloglabs/skills](https://github.com/superloglabs/skills) · **13 stars** · [Apache-2.0](https://github.com/superloglabs/skills/blob/main/LICENSE)

This is a third-party repository, not from LiveKit.

| Task | Skill |
| --- | --- |
| Conventions for OpenTelemetry session spans, metrics and LLM token counters in a LiveKit Agents worker. | [otel-livekit-style](https://github.com/superloglabs/skills/blob/main/otel-livekit-style/SKILL.md) |

### voicetest

[voicetestdev/voicetest](https://github.com/voicetestdev/voicetest) · **35 stars** · [Apache-2.0](https://github.com/voicetestdev/voicetest/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Drive the voicetest CLI to import, test, evaluate and export voice agent definitions across platforms. | [voicetest](https://github.com/voicetestdev/voicetest/blob/main/claude-plugin/skills/voicetest/SKILL.md) |

## Webhooks and security

Checking that a webhook really comes from the provider, and detecting synthetic voices. Twilio and ElevenLabs also publish security skills. They are listed under [Twilio](#twilio) and [ElevenLabs](#elevenlabs).

### Hookdeck

[hookdeck/webhook-skills](https://github.com/hookdeck/webhook-skills) · **89 stars** · [MIT](https://github.com/hookdeck/webhook-skills/blob/main/LICENSE)

Hookdeck is a webhook service. These are third-party skills that describe other providers' webhooks, so check them against the provider's own documentation. The local-testing steps in every skill run `npx hookdeck-cli listen`, which runs a remote npm package and opens a public tunnel.

| Task | Skill |
| --- | --- |
| Verify X-Twilio-Signature and handle SMS, voice call, message/call status and recording callbacks with TwiML replies. | [twilio-webhooks](https://github.com/hookdeck/webhook-skills/blob/main/skills/twilio-webhooks/SKILL.md) |
| Verify Telnyx Ed25519 webhook signatures (timestamp plus raw body) and handle message received, sent, and finalized events. It covers messaging events, not call control. | [telnyx-webhooks](https://github.com/hookdeck/webhook-skills/blob/main/skills/telnyx-webhooks/SKILL.md) |
| Authenticate Vapi Server URL messages and answer the four message types that need a JSON reply during live calls. | [vapi-webhooks](https://github.com/hookdeck/webhook-skills/blob/main/skills/vapi-webhooks/SKILL.md) |
| Verify Retell X-Retell-Signature and handle call, transcript, transfer and chat webhook events. | [retell-webhooks](https://github.com/hookdeck/webhook-skills/blob/main/skills/retell-webhooks/SKILL.md) |
| Verify ElevenLabs webhook signatures and handle post-call transcription and voice-removal events. | [elevenlabs-webhooks](https://github.com/hookdeck/webhook-skills/blob/main/skills/elevenlabs-webhooks/SKILL.md) |
| Receive Deepgram asynchronous transcription callbacks and check the dg-token header. The check is a plain header comparison, not a signature. | [deepgram-webhooks](https://github.com/hookdeck/webhook-skills/blob/main/skills/deepgram-webhooks/SKILL.md) |
| Verify OpenAI Standard Webhooks signatures and route fine-tuning, batch and realtime.call.incoming events. | [openai-webhooks](https://github.com/hookdeck/webhook-skills/blob/main/skills/openai-webhooks/SKILL.md) |

### Resemble AI

[resemble-ai/detect-skill](https://github.com/resemble-ai/detect-skill) · **84 stars** · [Apache-2.0](https://github.com/resemble-ai/detect-skill/blob/master/LICENSE)

| Task | Skill |
| --- | --- |
| Run Resemble AI deepfake detection on audio, image, video and text, plus site visitor agent detection, via REST calls. | [resemble-detect](https://github.com/resemble-ai/detect-skill/blob/master/SKILL.md) |

## Community references

Reference material from independent authors, not from a provider.

### Mahimai Labs

[Maintainer's collection](https://github.com/mahimailabs/voice-ai-skills) · **2 stars** · [MIT](https://github.com/mahimailabs/voice-ai-skills/blob/main/LICENSE)

| Task | Skill |
| --- | --- |
| Separate spoken output, persona, task flow, and confirmation; draft read-backs for dates and codes. Optional reference, with prompt blocks and provider adapters. | [voice-prompting](https://github.com/mahimailabs/voice-ai-skills/blob/main/skills/voice-prompting/SKILL.md) |

Use the worked prompts as drafts for audio tests. Its twenty-word sentence cap, digit spellings, and fixed confirmation wording are the author's conventions, not provider requirements. Adapt them to the caller's language and the actual TTS normalizer. The adapter notes were checked upstream on September 11 and describe LiveKit 1.8.x, Pipecat 1.0, and unversioned Vapi documentation. Recheck current APIs before copying an integration. Its claim that prompting is the only normalization control is too broad: [Pipecat text transforms](https://docs.pipecat.ai/api-reference/server/utilities/text/voice-formatter) also prepare text for synthesis. Prompt instructions need application enforcement for authorization, idempotency, and uncertain writes.

The collection contains ten skills; this index selects one. Its broader latency ceilings, readiness scores, and full-duplex restrictions need more evidence before they can be used as general engineering guidance.

## Use with care

- **Call-home instructions.** Six Cekura skills open by telling the agent to call the vendor tool `mcp__cekura__cekura_skill_started`. The call reports the skill name, a fixed tag and the plugin version to Cekura. They are cekura-bot-test-writer, cekura-eval-design, cekura-generate-scenarios, cekura-infra-test-suite, cekura-metric-design and cekura-self-improving-agent. Several also ask the agent to tag its writes.
- **Telemetry.** Synthflow's create-assistant, create-call and manage-actions tell the agent to send a usage event to a PostHog endpoint. It is on by default and stops when `DO_NOT_TRACK` or `DISABLE_TELEMETRY` is set. The event calls itself anonymous, but its identifier is an unsalted hash of the user name. Synthflow's create-eval and create-simulation contain telemetry commands with the same opt-outs.
- **Other vendor behavior.** The Plivo CLI skill installs with a script piped from a mutable branch into bash, and the CLI checks GitHub for updates daily and can send optional feedback telemetry. Resemble's detect skill can add a vendor script to every page of your site, and that script records visitor signals such as pointer, click and scroll. A SignalWire example runs `eval` on model-supplied text. Read these before you run them.
- **No license file.** These repositories have no license file at the checked commit, so they are linked only, not copied: [AssemblyAI/assemblyai-skill](https://github.com/AssemblyAI/assemblyai-skill), [VapiAI/skills](https://github.com/VapiAI/skills), [deepgram/skills](https://github.com/deepgram/skills), [SynthFlowAI/synthflow-skills](https://github.com/SynthFlowAI/synthflow-skills), [bluejay-ai-dev/bluejay-skills](https://github.com/bluejay-ai-dev/bluejay-skills), [elevenlabs/plugin](https://github.com/elevenlabs/plugin), [OpenRouterTeam/skills](https://github.com/OpenRouterTeam/skills), [smallest-inc/skills](https://github.com/smallest-inc/skills). The Azure-Samples/Cognitive-Speech-TTS license says MIT applies to SDK code only. Docs-hosted skills carry no confirmed license.
- **Docs-hosted skills can change without notice.** They have no commit or tag. Compare a file's SHA-256 hash with the one in [linked-skills.json](../linked-skills.json) before you rely on it.
- **Shared names.** Several skills use the same name: assemblyai, configure-metrics, create-assistant, create-call, speech-to-text, text-to-speech, voice-agent and voice-agents. Install each from its original source into its own folder, or rename it, so one does not replace another.
- **Real calls, real costs, real data.** Many skills create billable resources, place calls, or read call transcripts. Many say nothing about consent, recording or retention. The concerns for each skill are in [linked-skills.json](../linked-skills.json).
- **Left out on purpose.** The iFlytek voice-clone skill: its script turns off TLS certificate checks and sends voice samples and auth tokens over plain http, with no consent guidance. The Vobiz skill set: its guides contradict each other about stop events and media formats. Other exclusions and their reasons are under `excluded_manifests` in [linked-skills.json](../linked-skills.json) and in the [research notes](research.md).

## What was checked

<details>
<summary>Source checks, technical discrepancies and remaining limits</summary>

Every selected manifest resolved on its repository's current default branch and matched the checked commit. Repository stars describe the whole project, and each language variant is counted as a separate skill. The source index records retrieval times, commits, licenses, dependencies, and known limitations.

The selection uses canonical skill paths and excludes provider plugin mirrors. Selected manifests were read from pinned archives and checked against their live default-branch URLs. SDK example references were checked where explicit paths were provided. Context7 supplied current technical documentation, with package registries and repository files used to confirm the concrete discrepancies described above.

On September 30, 2026 (UTC) the index grew from 103 to 297 linked skills. Each of the 176 new repository manifests was fetched at the commit recorded for its repository, hashed with SHA-256, and compared with the Git blob hash from the repository tree. The repositories with new skills were checked again after the scan and none had moved. Six repositories from the earlier index had moved to a newer commit. Their indexed manifests were hashed again at the new commit and had not changed, so the recorded commits were updated. The 18 docs-hosted files returned HTTP 200 and matched the digest in each vendor's skill index.

Purpose, dependencies and concerns for the new skills were written by reviewing agents that read each manifest and its script files. Supporting reference files were mostly not read. A separate pattern scan over the script files of the skills that ship scripts found no unsafe behavior that the concerns do not already record. No second-model review of these records was done, and nothing was run.

No provider calls, installations, or runtime tests were performed. The index does not certify every SDK example or guarantee that an installed skill will work with a different package version. The [structured index](../linked-skills.json) records the checks and remaining limits.

</details>
