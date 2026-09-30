# More voice skills

[Home](../README.md) / [Engineering handbook](handbook.md) / [Core skills](catalog.md) / More upstream skills

**102 additional skill files** · **20 original repositories** · **Checked September 30, 2026 UTC**

Open the original source for current instructions. This index groups voice APIs, client calling, SDK language variants, evaluation, and optional migrations. [Usage notes](usage.md) cover installation and host assumptions; [linked-skills.json](../linked-skills.json) retains exact source metadata.

## Choose a task

| Your next step | Collections | Selected files |
| --- | --- | --- |
| Build assistants and connect phone or browser calls | [Telnyx](#telnyx) · [Vapi](#vapi) · [Voximplant and Synthflow](#voximplant-and-synthflow) | 32 · 10 · 4 |
| Integrate recognition, synthesis, or voice SDKs | [Deepgram SDKs](#deepgram-sdk-skills) · [Deepgram product guides](#deepgram-product-guides) · [AssemblyAI](#assemblyai) | 29 · 6 · 1 |
| Use managed cloud voice and speech services | [Cloud voice and speech](#cloud-voice-and-speech) | 10 |
| Evaluate agents or integrate local speech | [Evaluation and local speech](#evaluation-and-local-speech) | 9 |
| Build a native .NET audio frontend | [Native .NET audio](#native-net-audio) | 1 |

Counts describe skill files, including language variants, not independent capabilities. Stars describe the whole repository. Optional migration and prerelease entries are marked in their sections.

## Telnyx

[Official collection](https://github.com/team-telnyx/ai/tree/main/skills) ·
**220 repository stars** · [MIT license](https://github.com/team-telnyx/ai/blob/main/LICENSE)

Choose the guide for your server language. Backend WebRTC guides create credentials
and tokens; the client guides below handle browser or mobile calling. Live operations
require `TELNYX_API_KEY` and the matching SDK. Keep account keys on the server.

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

### Speech and client calling

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

### Optional migrations

<details>
<summary>Migration from Twilio, Vapi, Retell or ElevenLabs (4 optional skills)</summary>

Use these when migrating an existing provider integration. They can change
application code, provision resources, transfer configuration, and store integration
secrets. The Twilio migration includes non-voice products and bundled scripts,
and requires bash 4+, jq, curl, and Python. Review the requested scope and current
prices before authorizing its paid test workflow.

| Starting point | Original skill |
| --- | --- |
| Twilio | [Migration guide](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-twilio-migration/SKILL.md) |
| Vapi | [Migration guide](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-import-vapi/SKILL.md) |
| Retell | [Migration guide](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-import-retell/SKILL.md) |
| ElevenLabs | [Migration guide](https://github.com/team-telnyx/ai/blob/main/skills/telnyx-import-elevenlabs/SKILL.md) |

</details>

## Vapi

[Official collection](https://github.com/VapiAI/skills/tree/main) ·
**66 repository stars** · **Source links only: licensing scope needs clarification**

The manifests declare MIT, but the repository has no LICENSE or NOTICE file in
the checked archive. This index links to ten voice-specific workflows. Generic
credential setup and the opt-in Bun bootstrap scaffold are excluded.

| Task | Original skill |
| --- | --- |
| Configure a Vapi voice assistant, model, voice, and conversation behavior | [create-assistant](https://github.com/VapiAI/skills/blob/main/create-assistant/SKILL.md) |
| Build grounded voice prompts with intake, capability, and trust-boundary reviews | [vapi-prompt-builder](https://github.com/VapiAI/skills/blob/main/vapi-prompt-builder/SKILL.md) |
| Configure callable tools for a voice assistant | [create-tool](https://github.com/VapiAI/skills/blob/main/create-tool/SKILL.md) |
| Coordinate assistants and voice handoffs using Squads | [create-squad](https://github.com/VapiAI/skills/blob/main/create-squad/SKILL.md) |
| Create inbound or outbound voice call workflows | [create-call](https://github.com/VapiAI/skills/blob/main/create-call/SKILL.md) |
| Configure outbound calling campaigns | [create-campaign](https://github.com/VapiAI/skills/blob/main/create-campaign/SKILL.md) |
| Attach or configure a phone number for voice calls | [create-phone-number](https://github.com/VapiAI/skills/blob/main/create-phone-number/SKILL.md) |
| Define structured extraction of call outcomes | [create-structured-output](https://github.com/VapiAI/skills/blob/main/create-structured-output/SKILL.md) |
| Configure server events and call-related webhooks | [setup-webhook](https://github.com/VapiAI/skills/blob/main/setup-webhook/SKILL.md) |
| Plan and run voice simulations and focused evaluations | [simulations](https://github.com/VapiAI/skills/blob/main/simulations/SKILL.md) |

Live operations require `VAPI_API_KEY` and current schema checks. Calls, campaigns,
number provisioning, and simulation runs can change external resources or consume
usage. Text simulations help test logic; voice tests are needed to assess speech
recognition, audio delivery, and interruptions.


## Voximplant and Synthflow

| Original skill | Use it for | Qualification |
| --- | --- | --- |
| [create-eval](https://github.com/SynthFlowAI/synthflow-skills/blob/main/create-eval/SKILL.md) | Define post-call custom evaluations and business outcomes. | Optional provider workflow; no complete LICENSE found. Contains telemetry commands with DO_NOT_TRACK / DISABLE_TELEMETRY opt-outs. |
| [create-simulation](https://github.com/SynthFlowAI/synthflow-skills/blob/main/create-simulation/SKILL.md) | Build caller scenarios and simulation tests for Synthflow agents. | Optional provider workflow; no complete LICENSE found. Contains telemetry commands with DO_NOT_TRACK / DISABLE_TELEMETRY opt-outs. |
| [voximplant-voxengine-dev](https://github.com/voximplant/ai-agent-skills/blob/main/plugins/voximplant-ai-agent-skills/skills/voximplant-voxengine-dev/SKILL.md) | Build VoxEngine call flows and media bridges with current API references. | Apache-2.0; use current docs.voximplant.ai references and narrowly scoped account roles. |
| [voximplant-management-api](https://github.com/voximplant/ai-agent-skills/blob/main/plugins/voximplant-ai-agent-skills/skills/voximplant-management-api/SKILL.md) | Manage voice application configuration, scenarios, rules, and call logs. | Apache-2.0; use current docs.voximplant.ai references and narrowly scoped account roles. |

Inspect Synthflow's telemetry section before running its instructions. No telemetry,
provider changes, or calls were performed for this index. Use its current
[custom evaluations](https://docs.synthflow.ai/create-a-custom-evaluation) and
[simulation documentation](https://docs.synthflow.ai/simulations) for API details.
Voximplant's current [voice orchestration examples](https://docs.voximplant.ai/voice-ai-orchestration/openai/inbound.md)
are preferable to copying an older indexed snippet without checking the API.


## Deepgram SDK skills

Each SDK repository carries product-specific instructions for its own code and
examples. Choose the language you use, and keep that repository’s reference context
available. Live requests require `DEEPGRAM_API_KEY` or an appropriate temporary
token. These six SDK repositories have MIT licenses.

| Product | JavaScript | Python | Java | Go | Rust | .NET |
| --- | --- | --- | --- | --- | --- | --- |
| Standard STT | [Skill](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-speech-to-text/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-speech-to-text/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-java-sdk/blob/main/.agents/skills/deepgram-java-speech-to-text/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-go-sdk/blob/main/.agents/skills/deepgram-go-speech-to-text/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-rust-sdk/blob/main/.agents/skills/deepgram-rust-speech-to-text/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/.agents/skills/deepgram-dotnet-speech-to-text/SKILL.md) |
| Conversational STT / Flux | [Skill](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-conversational-stt/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-conversational-stt/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-java-sdk/blob/main/.agents/skills/deepgram-java-conversational-stt/SKILL.md) | [Current examples](https://github.com/deepgram/deepgram-go-sdk/blob/main/examples/speech-to-text/websocket/flux_channel/README.md)¹ | [Skill](https://github.com/deepgram/deepgram-rust-sdk/blob/main/.agents/skills/deepgram-rust-conversational-stt/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/.agents/skills/deepgram-dotnet-conversational-stt/SKILL.md) |
| TTS | [Skill](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-text-to-speech/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-text-to-speech/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-java-sdk/blob/main/.agents/skills/deepgram-java-text-to-speech/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-go-sdk/blob/main/.agents/skills/deepgram-go-text-to-speech/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-rust-sdk/blob/main/.agents/skills/deepgram-rust-text-to-speech/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/.agents/skills/deepgram-dotnet-text-to-speech/SKILL.md) |
| Voice agents | [Skill](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-voice-agent/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-voice-agent/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-java-sdk/blob/main/.agents/skills/deepgram-java-voice-agent/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-go-sdk/blob/main/.agents/skills/deepgram-go-voice-agent/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-rust-sdk/blob/main/.agents/skills/deepgram-rust-voice-agent/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/.agents/skills/deepgram-dotnet-voice-agent/SKILL.md) |
| Audio intelligence | [Skill](https://github.com/deepgram/deepgram-js-sdk/blob/main/.agents/skills/deepgram-js-audio-intelligence/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-python-sdk/blob/main/.agents/skills/deepgram-python-audio-intelligence/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-java-sdk/blob/main/.agents/skills/deepgram-java-audio-intelligence/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-go-sdk/blob/main/.agents/skills/deepgram-go-audio-intelligence/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-rust-sdk/blob/main/.agents/skills/deepgram-rust-audio-intelligence/SKILL.md) | [Skill](https://github.com/deepgram/deepgram-dotnet-sdk/blob/main/.agents/skills/deepgram-dotnet-audio-intelligence/SKILL.md) |

¹ The Go conversational-STT manifest says that a v2 client and Flux examples do
not exist. Its current repository already contains both, including a
[typed v2 client example](https://github.com/deepgram/deepgram-go-sdk/blob/main/examples/speech-to-text/websocket/flux_channel/main.go).
The stale manifest is excluded from the skill count.

The Java skills reference a root `reference.md` file that is absent from the
checked repository. Use its [README](https://github.com/deepgram/deepgram-java-sdk/blob/main/README.md)
and current source examples. Rust’s voice-agent guide uses a raw WebSocket fallback
with extra crates. Python’s force-end-turn support requires the documented Flux
provider or deployment enablement; it is not interchangeable with standard v1 STT.

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

## Deepgram product guides

[Official collection](https://github.com/deepgram/skills/tree/main/skills) ·
**22 repository stars** · **Source links only: no repository LICENSE found**

Use these for cross-language API guidance and deployment choices. The browser
guide covers core, React, UI, and widget packages; browser authentication requires
a server-issued temporary token. Self-hosting requires the appropriate entitlement
and infrastructure.

| Task | Original skill |
| --- | --- |
| Speech recognition | [Guide](https://github.com/deepgram/skills/blob/main/skills/speech-to-text/SKILL.md) |
| Speech synthesis | [Guide](https://github.com/deepgram/skills/blob/main/skills/text-to-speech/SKILL.md) |
| Interactive voice agents | [Guide](https://github.com/deepgram/skills/blob/main/skills/voice-agent/SKILL.md) |
| Speech analytics | [Guide](https://github.com/deepgram/skills/blob/main/skills/audio-intelligence/SKILL.md) |
| Browser agents and voice widgets | [Guide](https://github.com/deepgram/skills/blob/main/skills/browser-agent/SKILL.md) |
| Self-hosting, optional deployment | [Guide](https://github.com/deepgram/skills/blob/main/skills/self-hosted/SKILL.md) |

The central README advertises Swift, Kotlin, and browser SDK repository URLs that
returned HTTP 404 in this check. Those repositories are not indexed here. The browser
packages documented by the browser-agent skill are available on npm; a broken
repository link does not establish that a package is unavailable.


## AssemblyAI

[AssemblyAI skill](https://github.com/AssemblyAI/assemblyai-skill/blob/main/skills/assemblyai/SKILL.md) ·
**15 repository stars** · **Source link only: no repository LICENSE found**

One comprehensive skill covers prerecorded and streaming transcription, dictation,
speech analytics, and voice-agent integrations. Keep its reference guides beside
the manifest and use a supported SDK or REST client.

The skill calls Python 1.5.4 and JavaScript 4.41.1 current. On September 30, 2026,
the [Python registry](https://pypi.org/project/assemblyai/) reports 1.6.1 and the
[JavaScript registry](https://www.npmjs.com/package/assemblyai) reports 4.41.5.
Check the installed version and current API surface before using release-sensitive
features.


## Cloud voice and speech

These official skills cover different account and deployment models. Gemini
Developer API credentials and Google Cloud authentication are not interchangeable.
Azure samples may use preview versions. Resolve the current service and SDK
reference before adopting a sample endpoint or model name.

| Original skill | Use it for | Source terms |
| --- | --- | --- |
| [Azure Voice Live .NET](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-dotnet/skills/azure-ai-voicelive-dotnet/SKILL.md) | Bidirectional voice applications using Azure.AI.VoiceLive; VAD, session events, tools, audio lifecycle. | [MIT](https://github.com/microsoft/skills/blob/main/LICENSE) |
| [Azure Voice Live Java](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-java/skills/azure-ai-voicelive-java/SKILL.md) | Reactive Java voice sessions over WebSocket with Azure AI VoiceLive. | [MIT](https://github.com/microsoft/skills/blob/main/LICENSE) |
| [Azure Voice Live Python](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-python/skills/azure-ai-voicelive-py/SKILL.md) | Python bidirectional voice sessions, events, VAD, function calling, transcription and Azure voices. | [MIT](https://github.com/microsoft/skills/blob/main/LICENSE) |
| [Azure Voice Live TypeScript](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-typescript/skills/azure-ai-voicelive-ts/SKILL.md) | Node/browser Voice Live SDK patterns, streaming, function calling and lifecycle. | [MIT](https://github.com/microsoft/skills/blob/main/LICENSE) |
| [Azure short-audio STT REST](https://github.com/microsoft/skills/blob/main/.github/plugins/azure-sdk-python/skills/azure-speech-to-text-rest-py/SKILL.md) | Short-file recognition utility, explicitly excludes real-time streaming and long audio. **Optional.** | [MIT](https://github.com/microsoft/skills/blob/main/LICENSE) |
| [Gemini Live API development](https://github.com/google-gemini/gemini-skills/blob/main/skills/gemini-live-api-dev/SKILL.md) | Developer API audio/video/text sessions, VAD, nonblocking tools, ephemeral tokens, transcription and migration. | [Apache-2.0](https://github.com/google-gemini/gemini-skills/blob/main/LICENSE) |
| [Gemini Enterprise Live client](https://github.com/google/skills/blob/main/skills/cloud/gemini-live-api/SKILL.md) | Scaffold cloud-authenticated Live API client, session resumption, token refresh, protobuf messages and demo. | [Apache-2.0](https://github.com/google/skills/blob/main/LICENSE) |
| [Google Cloud bidirectional streaming architecture](https://github.com/google/skills/blob/main/skills/cloud/google-cloud-solution-agentic-ai-bidirectional-streaming/SKILL.md) | Multimodal cloud solution design and deployment planning, including voice; broader than voice agents. **Optional.** | [Apache-2.0](https://github.com/google/skills/blob/main/LICENSE) |
| [Azure Speech official docs skill](https://github.com/MicrosoftDocs/Agent-Skills/blob/main/skills/azure-speech/SKILL.md) | Live official-doc index for STT/TTS, Voice Live, containers, streaming, security and quotas. | [CC-BY-4.0 documentation; MIT code](https://github.com/MicrosoftDocs/Agent-Skills/blob/main/LICENSE) |
| [NVIDIA Nemotron Speech](https://github.com/nvidia-riva/Nemotron-speech-skills/blob/main/skills/nemotron-speech/SKILL.md) | ASR/TTS/NMT NIM selection, streaming, pronunciation, hosted and self-hosted deployment workflows. | [CC-BY-4.0 documentation; Apache-2.0 code](https://github.com/nvidia-riva/Nemotron-speech-skills/blob/main/LICENSE) |

The Azure AI Transcription Python manifest was excluded: its streaming and batch
method examples are absent from the released SDK checked in this review. Use the
[current SDK README](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/transcription/azure-ai-transcription/README.md)
for supported file-transcription methods.

MicrosoftDocs' Azure Speech entry is a generated documentation index, dated
2026-09-27 in its metadata. Use its live documentation links; its illustrative
`security.md` reference is not a file in that skill folder. NVIDIA's manifest
mentions Apache-2.0, but the repository license distinguishes documentation
(CC-BY-4.0) from source code (Apache-2.0). The table preserves that distinction.
Model, hosted-service, and container terms need their own review.

### Azure SDK version notes

Checked against released package contents on **2026-09-30 UTC**. These are focused
source checks; none of the provider workflows was executed.

| Skill | Qualification for current use | Primary API reference |
| --- | --- | --- |
| Voice Live Java | Its `1.0.0-beta.2` pin accepts `startSession(String)`. Release `1.1.0` uses a model-plus-options overload; preserve the pin or migrate deliberately. | [Java client source](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/voicelive/azure-ai-voicelive/src/main/java/com/azure/ai/voicelive/VoiceLiveAsyncClient.java) |
| Voice Live TypeScript | The quick-start handler should be `onConversationItemInputAudioTranscriptionCompleted`. The shorter name is absent from both the pinned beta and released `1.1.0`. | [Public API declarations](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/voicelive/ai-voicelive/review/ai-voicelive-node.api.md) |
| Voice Live .NET | The hierarchy's `SendAudioAsync` name should be `SendInputAudioAsync`. Checked in `1.0.0` and released `1.2.0`; other sampled lifecycle methods exist. | [.NET public API](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/voicelive/Azure.AI.VoiceLive/api/Azure.AI.VoiceLive.netstandard2.0.cs) |
| Voice Live Python | Central session, audio-buffer, and response methods exist in released `1.3.0`. This check does not cover every model, endpoint, or authentication branch. | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/voicelive/azure-ai-voicelive/README.md) |


## Evaluation and local speech

Coval's selected workflows cover evidence review, test suites, evaluator
calibration, and matched comparisons. They can evaluate voice or chat agents;
choose actual audio tests when the claim concerns speech. Hosted runs require an
authorized workspace and budget. Keep helper scripts and references with the
skill, and set a bounded run size before execution.

| Original skill | Use it for |
| --- | --- |
| [coval-eval-start](https://github.com/coval-ai/coval-external-skills/blob/main/skills/evaluation/coval-eval-start/SKILL.md) | Choose an evaluation workflow and define the evidence needed next. |
| [coval-discover-failures](https://github.com/coval-ai/coval-external-skills/blob/main/skills/evaluation/coval-discover-failures/SKILL.md) | Find recurring failure patterns in existing evaluation evidence. |
| [coval-calibrate-metric](https://github.com/coval-ai/coval-external-skills/blob/main/skills/evaluation/coval-calibrate-metric/SKILL.md) | Compare a scoring metric with labeled examples and inspect disagreements. |
| [coval-compare-runs](https://github.com/coval-ai/coval-external-skills/blob/main/skills/evaluation/coval-compare-runs/SKILL.md) | Compare matched runs without hiding retries, missing cases, or changed conditions. |
| [coval-eval-audit](https://github.com/coval-ai/coval-external-skills/blob/main/skills/evaluation/coval-eval-audit/SKILL.md) | Audit evaluation coverage, evidence quality, and unsupported conclusions. |
| [quick-eval](https://github.com/coval-ai/coval-external-skills/blob/main/skills/runs/quick-eval/SKILL.md) | Run a bounded evaluation against an authorized agent and test set. |
| [build-test-suite](https://github.com/coval-ai/coval-external-skills/blob/main/skills/test-cases/build-test-suite/SKILL.md) | Turn a task and its known failure modes into a focused test suite. |
| [configure-metrics](https://github.com/coval-ai/coval-external-skills/blob/main/skills/metrics/configure-metrics/SKILL.md) | Define task-specific evaluation metrics and scoring criteria. |
| [moonshine-voice](https://github.com/moonshine-ai/moonshine/blob/main/.agents/skills/moonshine-voice/SKILL.md) | Integrate local speech recognition and supported speech workflows with Moonshine. |

Coval's source files are MIT licensed. Older specialist launch recipes have
whole-set defaults and less bounded retry/watch behavior; this selection favors
the newer evaluation workflows. Moonshine's skill guides local speech integration.
Its current LICENSE assigns MIT to streaming STT and English STT models, while
listed legacy nonstreaming non-English models have noncommercial terms. TTS/G2P
assets carry separate source terms. See the [resource qualifications](resources.md#current-source-caveats)
and the exact source licenses in [linked-skills.json](../linked-skills.json).


## Native .NET audio

[Shiny Speech skill](https://github.com/shinyorg/skills/blob/main/plugins/shiny/skills/shiny-speech/SKILL.md)
provides microphone capture, playback, recognition, synthesis, and platform audio
processing guidance. **Optional prerelease workflow:** the inspected core APIs are
in `3.0.0-beta-0030` packages targeting .NET 10; stable Shiny.Speech `2.1.0` and the
SDK's default branch do not expose the same surface. Follow the versioned package
and [current documentation](https://shinylib.net/speech/), preserving
`reference/api-reference.md` with the skill. Source license: MIT; repository stars: 4.

The upstream overview and later sections disagree about monitor/device support
on Linux. Verify each target platform before using those features. Processing
flags do not guarantee echo cancellation or suppression on every device, driver,
or recognition backend. The reviewed package XML confirms selected API members;
no integration was compiled or run. This skill supplies a frontend, not an entire
voice-agent runtime.


## What was checked

<details>
<summary>Source checks, technical discrepancies and remaining limits</summary>

Every selected manifest resolved on its repository’s current default branch and matched the checked commit. Repository stars describe the whole project, and each language variant is counted as a separate skill. The source index records retrieval times, commits, licenses, dependencies, and known limitations.


The selection uses canonical skill paths and excludes provider plugin mirrors.
Selected manifests were read from pinned archives and checked against their live
default-branch URLs. SDK example references were checked where explicit paths were
provided. Context7 supplied current technical documentation, with package registries
and repository files used to confirm the concrete discrepancies described above.

No provider calls, installations, or runtime tests were performed. The index does
not certify every SDK example or guarantee that an installed skill will work with
a different package version. The [structured index](../linked-skills.json) records
the checks and remaining limits.

</details>
