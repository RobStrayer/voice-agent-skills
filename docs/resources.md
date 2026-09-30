# Voice AI resource library

[Home](../README.md) / [Engineering handbook](handbook.md) / Runtime resources

**43 projects** for the runtime behind a voice agent: frameworks, media tools, speech models, examples and evaluation utilities. For instructions that guide a coding agent, browse the [core skills](catalog.md) or [expanded skill index](more-skills.md).

Reviewed and expanded: **2026-09-30 UTC**. The original 28 records retain their September 29 (America/New_York) observations; 15 additions have fresh UTC timestamps. Exact dates and commits are in [resources.json](../resources.json).

## Choose the part you need

| You are working on… | Browse |
| --- | --- |
| Agent sessions and provider orchestration | [Frameworks](#frameworks-and-orchestration) |
| What the microphone captures and when to reply | [Noise processing](#input-noise-processing) · [Turn taking](#turn-taking-and-speech-activity) |
| Words, speech generation or speech models | [Recognition](#speech-recognition-and-speech-research) · [Synthesis](#local-speech-synthesis-and-audio-inference) · [Speech language models](#speech-language-models) |
| Phone calls and realtime media | [Telephony and transport](#telephony-and-media-transport) |
| Debugging, evaluation or a runnable reference | [Evaluation](#evaluation-debugging-and-observability) · [Examples](#examples-to-learn-from) |
| Provider APIs and concepts | [Official learning paths](#primary-documentation-and-learning-paths) · [Community leads](#community-discovery) |

Selection favors direct usefulness to voice-agent engineers, primary documentation, maintenance visibility, and adoption. Stars provide an adoption signal, not a quality score. Small projects are retained when they address a specific gap.

**Read the terms before choosing a model or deployment.** The tables give a short orientation; each category's expandable notes preserve the full qualifications. Code licenses may differ from model, voice, data and service terms.

## Start here

- **Build a complete agent:** [LiveKit Agents](https://github.com/livekit/agents) or [Pipecat](https://github.com/pipecat-ai/pipecat).
- **Build a TypeScript realtime app:** [OpenAI Agents SDK](https://github.com/openai/openai-agents-js), using its realtime package.
- **Build a local speech stack:** [Hugging Face speech-to-speech](https://github.com/huggingface/speech-to-speech), then inspect each selected model's license and hardware requirements.
- **Improve conversational timing:** [Silero VAD](https://github.com/snakers4/silero-vad), [Smart Turn](https://github.com/pipecat-ai/smart-turn), and [eot-bench](https://github.com/livekit/eot-bench). Voice activity and end-of-turn prediction solve different problems.


## Frameworks and orchestration

Choose where sessions, providers, tools and media are coordinated.

| Resource | Use it for | Dated stars | Terms at a glance |
| --- | --- | ---: | --- |
| [LiveKit Agents](https://github.com/livekit/agents) | Voice-agent sessions, provider plugins, tool calls, handoffs, and testing over LiveKit media. | 14,427 | Apache-2.0; separate turn-model license |
| [Pipecat](https://github.com/pipecat-ai/pipecat) | Composable Python pipelines for streaming speech, transport, interruptions, and multimodal services. | 16,017 | BSD-2-Clause |
| [OpenAI Agents SDK, JavaScript/TypeScript](https://github.com/openai/openai-agents-js) | Realtime agents, tools, handoffs, and browser/server transport integrations. | 3,880 | MIT SDK; hosted-service terms |
| [Hugging Face speech-to-speech](https://github.com/huggingface/speech-to-speech) | Local speech pipelines with WebSocket/WebRTC serving and configurable speech components. | 13,355 | Apache-2.0 code; model terms vary |
| [TEN Framework](https://github.com/TEN-framework/ten-framework) | Realtime multimodal agent examples and extension architecture. | 11,144 | Custom Apache-based restrictions |
| [Bolna](https://github.com/bolna-ai/bolna) | Python orchestration for streamed STT, language models, TTS and telephony. | 778 | MIT; hosted service is separate |

<details>
<summary>Full license and deployment notes (6 projects)</summary>

**LiveKit Agents**

Apache-2.0 framework; turn-detector models have a separate LiveKit Model License.

**Pipecat**

BSD-2-Clause.

**OpenAI Agents SDK, JavaScript/TypeScript**

MIT SDK; hosted model usage has separate service terms and costs.

**Hugging Face speech-to-speech**

Apache-2.0 code; selected model weights can have different terms.

**TEN Framework**

Custom Apache-based license with additional use restrictions; individual packages may differ.

**Bolna**

MIT. Telephony requires a bidirectional provider integration and provider credentials. Open-source orchestrator is distinct from Bolna hosted services.

</details>

## Input noise processing

Improve captured speech without treating noise suppression as echo cancellation.

| Resource | Use it for | Dated stars | Terms at a glance |
| --- | --- | ---: | --- |
| [RNNoise](https://gitlab.xiph.org/xiph/rnnoise) | Microphone noise suppression before recognition or turn detection. | 5,873 on the [GitHub mirror](https://github.com/xiph/rnnoise) | BSD-3-Clause code; model data separate |

<details>
<summary>Full license and deployment notes (1 project)</summary>

**RNNoise**

BSD-3-Clause code. GitLab is authoritative; both sources match the recorded commit. Main last changed 2025-02-22. The official example expects 48 kHz mono raw PCM. Test speech distortion and recognition/turn behavior; noise suppression does not replace acoustic echo cancellation. Build helpers download model data.

</details>

## Turn taking and speech activity

Distinguish speech activity from a conversational decision to respond.

| Resource | Use it for | Dated stars | Terms at a glance |
| --- | --- | ---: | --- |
| [Smart Turn](https://github.com/pipecat-ai/smart-turn) | Audio-based end-of-turn prediction to distinguish hesitations from completed turns. | 1,599 | BSD-2-Clause |
| [Silero VAD](https://github.com/snakers4/silero-vad) | Lightweight speech/non-speech detection with ONNX and PyTorch paths. | 10,326 | MIT |

<details>
<summary>Full license and deployment notes (2 projects)</summary>

**Smart Turn**

BSD-2-Clause; tune and evaluate on the intended conversation conditions.

**Silero VAD**

MIT; VAD does not establish semantic turn completion.

</details>

## Speech recognition and speech research

Choose recognition around the language, device, streaming path and task.

| Resource | Use it for | Dated stars | Terms at a glance |
| --- | --- | ---: | --- |
| [Whisper](https://github.com/openai/whisper) | Reference multilingual recognition models and inference implementation. | 109,764 | MIT code and weights |
| [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | CTranslate2 inference, batching, quantization, and practical Whisper deployment. | 25,631 | MIT |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Local C/C++ Whisper inference, quantization, and microphone examples. | 54,022 | MIT; naive microphone example |
| [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx) | Streaming/offline speech recognition, synthesis, and related speech inference across platforms. | 15,047 | Apache-2.0 code; check each model |
| [NVIDIA NeMo Speech](https://github.com/NVIDIA-NeMo/Speech) | Speech model training and inference, including streaming recognition and diarization. | 18,527 | Apache-2.0 code; check model cards |
| [SpeechBrain](https://github.com/speechbrain/speechbrain) | Speech research recipes for recognition, diarization, enhancement, and evaluation. | 11,848 | Apache-2.0 |
| [Kyutai streaming STT/TTS](https://github.com/kyutai-labs/delayed-streams-modeling) | Kyutai streaming STT and TTS implementations with Rust WebSocket serving. | 3,034 | MIT/Apache-2.0 code; STT weights CC-BY-4.0 |
| [Moonshine](https://github.com/moonshine-ai/moonshine) | On-device voice toolkit and an official moonshine-voice coding-agent skill. | 11,160 | MIT streaming/English STT; legacy restrictions |
| [Qwen3-ASR](https://github.com/QwenLM/Qwen3-ASR) | Multilingual ASR with streaming inference support and separate alignment tooling. | 3,629 | Apache-2.0; vLLM-only streaming |

<details>
<summary>Full license and deployment notes (9 projects)</summary>

**Whisper**

MIT code and model weights; streaming behavior needs an appropriate wrapper/policy.

**faster-whisper**

MIT; throughput benchmarks do not establish conversational latency.

**whisper.cpp**

MIT; its microphone streaming example is explicitly described upstream as naive.

**sherpa-onnx**

Apache-2.0 code; check each chosen model separately.

**NVIDIA NeMo Speech**

Apache-2.0 code; model cards govern individual checkpoints. Former `NVIDIA/NeMo` URL redirects here.

**SpeechBrain**

Apache-2.0; research toolkit rather than a complete realtime-agent runtime.

**Kyutai streaming STT/TTS**

MIT Python/client; Apache-2.0 Rust. Pinned README explicitly gives STT weights CC-BY-4.0; inspect the selected TTS model card independently. Throughput claims or simulated pacing do not establish user-heard latency.

**Moonshine**

MIT code with third-party exceptions. Current LICENSE makes streaming STT and English STT models MIT; enumerated legacy nonstreaming non-English models are noncommercial. TTS/G2P assets have separate source terms. Context7 indexed license summary is older and contradicts the current pinned LICENSE.

**Qwen3-ASR**

Apache-2.0. Checked Qwen3-ASR-1.7B model card declares Apache-2.0. Streaming support is documented for vLLM only and lacks batching/timestamps in the pinned README; language coverage is a project claim, not our measured accuracy.

</details>

## Local speech synthesis and audio inference

Compare engines and checkpoints separately, including their streaming and license limits.

| Resource | Use it for | Dated stars | Terms at a glance |
| --- | --- | ---: | --- |
| [Kokoro](https://github.com/hexgrad/kokoro) | Compact local TTS model and Python inference pipeline for conversational speech. | 9,079 | Apache-2.0; upstream states licensed weights |
| [Piper](https://github.com/OHF-Voice/piper1-gpl) | Local TTS engine suited to on-device and self-hosted speech output. | 5,716 | GPL-3.0 code; voice terms vary |
| [F5-TTS](https://github.com/SWivid/F5-TTS) | Flow-matching TTS research and inference with reference-audio conditioning. | 15,313 | MIT code; pretrained weights CC-BY-NC |
| [MLX-Audio](https://github.com/Blaizzy/mlx-audio) | Apple Silicon speech recognition, synthesis, and speech-to-speech inference. | 7,964 | MIT library; loaded models vary |
| [Chatterbox](https://github.com/resemble-ai/chatterbox) | Local speech synthesis and voice-cloning models with multilingual variants. | 26,617 | MIT; checked model card MIT |
| [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) | Speech synthesis and voice-cloning research with streaming-capable model design. | 13,594 | Apache-2.0; backend streaming limits |

<details>
<summary>Full license and deployment notes (6 projects)</summary>

**Kokoro**

Apache-2.0 repository; upstream describes Apache-licensed weights.

**Piper**

GPL-3.0 code; voice-model licenses vary. Upstream is looking for maintainers.

**F5-TTS**

MIT code; upstream pretrained weights are CC-BY-NC, a material commercial-use limitation.

**MLX-Audio**

MIT library; each loaded model retains its own license.

**Chatterbox**

MIT. The checked ResembleAI/chatterbox model card declares MIT. Hardware, chosen checkpoint, language, pacing and synthesis API determine practical agent suitability; provider preference benchmarks do not establish transport latency.

**Qwen3-TTS**

Apache-2.0. Checked Qwen3-TTS-12Hz-1.7B-Base model card declares Apache-2.0. The pinned repository documents offline-only vLLM inference with online serving planned; do not claim every backend provides streaming today. Pinned Python API also documents non_streaming_mode=false as simulated streaming text input, without true streaming input or generation.

</details>

## Speech language models

These projects make different choices about input, output, and full-duplex interaction. Check the actual model interface before assuming it replaces an entire voice stack.

| Resource | Use it for | Dated stars | Terms at a glance |
| --- | --- | ---: | --- |
| [Ultravox](https://github.com/fixie-ai/ultravox) | Speech-input language model that emits streaming text without a separate ASR stage. | 4,574 | MIT code; speech input, text output |
| [Moshi](https://github.com/kyutai-labs/moshi) | Full-duplex speech conversation research with streaming Mimi audio codec and local inference paths. | 11,162 | MIT/Apache-2.0 code; weights CC-BY-4.0 |

<details>
<summary>Full license and deployment notes (2 projects)</summary>

**Ultravox**

MIT code. The open model is audio-to-text; a voice agent still needs output speech synthesis and turn/media orchestration. Check selected model card and underlying base-model terms separately from repo code.

**Moshi**

MIT Python/client; Apache-2.0 Rust. Model weights are separately CC-BY-4.0 according to the pinned README. Codec frame latency is not whole-agent acoustic response latency; deployment still needs hardware and orchestration.

</details>

## Telephony and media transport

Connect and control the media path. Signaling and usable audio need separate proof.

| Resource | Use it for | Dated stars | Terms at a glance |
| --- | --- | ---: | --- |
| [jambonz Feature Server](https://github.com/jambonz/jambonz-feature-server) | Programmable telephony application server for building SIP and voice workflows. | 103 | MIT; wider deployment required |
| [drachtio-srf](https://github.com/drachtio/drachtio-srf) | Node.js SIP application framework for call signaling and session control. | 224 | MIT; SIP signaling |
| [Pion WebRTC](https://github.com/pion/webrtc) | Go implementation for custom realtime audio/video transport and server media handling. | 16,812 | MIT |
| [aiortc](https://github.com/aiortc/aiortc) | Python asyncio WebRTC implementation for custom media processing. | 5,108 | BSD-3-Clause |
| [coturn](https://github.com/coturn/coturn) | STUN/TURN relay server for WebRTC media connectivity through restrictive networks. | 14,440 | BSD-3-Clause; verify authenticated relay |
| [SIPp](https://github.com/SIPp/sipp) | SIP scenario and load-test tool for signaling, call routing and media-path checks. | 1,141 | GPL-2.0-or-later; README disagrees |

<details>
<summary>Full license and deployment notes (6 projects)</summary>

**jambonz Feature Server**

MIT; one component of the wider jambonz deployment.

**drachtio-srf**

MIT; signaling infrastructure, not an AI orchestration framework.

**Pion WebRTC**

MIT.

**aiortc**

BSD-3-Clause.

**coturn**

BSD-3-Clause. A successful STUN exchange is not proof of bidirectional relayed media. Verify selected ICE candidate, authenticated allocation and advertised relay port mapping. No network configuration was changed.

**SIPp**

GPL-2.0-or-later per LICENSE.txt; file exceptions. Pinned LICENSE.txt says GPL-2.0-or-later and separate send_packets files, while the README template says GPL-3.0-or-later. Record that discrepancy instead of choosing the README badge. SIP success does not prove agent behavior; live calls need an authorized target and budget.

</details>

## Evaluation, debugging, and observability

Choose evidence for the layer you are testing: speech, transport, task or model/tool behavior.

| Resource | Use it for | Dated stars | Terms at a glance |
| --- | --- | ---: | --- |
| [LiveKit eot-bench](https://github.com/livekit/eot-bench) | Reproducible end-of-turn evaluation with pause decisions, false-cutoff budgets, and multilingual artifacts. | 60 | Apache-2.0; vendor-maintained benchmark |
| [Pipecat Audio Metrics](https://github.com/jptaylor/pipecat-dev-tools) | Audio-level turn timing and optional RTVI event overlays to inspect framework/audio timing differences. | 1 | MIT |
| [Langfuse](https://github.com/langfuse/langfuse) | LLM/tool traces, evaluation, and prompt inspection inside a voice pipeline. | 35,212 | MIT outside enterprise directories |
| [Arize Phoenix](https://github.com/arize-ai/phoenix) | Trace inspection and evaluation for the model/tool layers of a voice agent. | 11,655 | Elastic License 2.0 |
| [Coval evaluation skills](https://github.com/coval-ai/coval-external-skills) | Coval workflows for evidence review, bounded runs, judge calibration and matched regressions. | 2 | MIT skills; hosted runs need budget |
| [EVA](https://github.com/ServiceNow/eva) | End-to-end voice-agent benchmark with multi-turn synthetic callers and task and speech-quality evaluation. | 221 | MIT; caller/provider usage may cost |
| [Future AGI Simulate SDK](https://github.com/future-agi/simulate-sdk) | LiveKit voice simulation SDK with per-speaker recordings, transcripts and evaluation helpers. | 58 | Apache-2.0; check current SDK consolidation |

<details>
<summary>Full license and deployment notes (7 projects)</summary>

**LiveKit eot-bench**

Apache-2.0; emerging and vendor-maintained. Evaluate the methodology before interpreting rankings.

**Pipecat Audio Metrics**

MIT; emerging specialist utility, not widely adopted.

**Langfuse**

MIT outside specified enterprise directories; generic LLM observability needs audio-specific instrumentation.

**Arize Phoenix**

Elastic License 2.0; generic observability, not a complete voice timing recorder.

**Coval evaluation skills**

MIT. Skills are open source; executing hosted simulations requires an authorized Coval account and provider/call budget. Newer evaluation skills are preferred over older specialist launch loops.

**EVA**

MIT. Caller models and evaluation providers require API credentials and can incur cost. OpenAI Realtime caller is marked experimental in the pinned README. Synthetic caller success does not prove production prevalence.

**Future AGI Simulate SDK**

Apache-2.0. Text cloud simulation uses hosted Future AGI; voice caller/provider dependencies may incur costs. Compare pinned SDK docs with Agent Learning Kit before choosing imports because repositories document consolidation differently.

</details>

## Examples to learn from

Read a complete path, then check the APIs and model assets it depends on.

| Resource | Use it for | Dated stars | Terms at a glance |
| --- | --- | ---: | --- |
| [Pipecat Examples](https://github.com/pipecat-ai/pipecat-examples) | Practical telephony, web clients, realtime APIs, translation, and deployment examples. | 387 | BSD-2-Clause; provider usage may cost |
| [OpenAI Realtime Console](https://github.com/openai/openai-realtime-console) | Browser WebRTC sample for inspecting realtime session events and tool interactions. | 3,611 | MIT; example application |
| [Twilio Call GPT](https://github.com/twilio-labs/call-gpt) | Reference for phone-call streaming, conversational state, and tool execution. | 492 | MIT; check current APIs |
| [Voice Agents from Scratch](https://github.com/pguso/voice-agents-from-scratch) | Chaptered runnable guide to STT, language models, TTS and streamed voice-agent pipelines. | 47 | MIT; downloaded models need review |

<details>
<summary>Full license and deployment notes (4 projects)</summary>

**Pipecat Examples**

BSD-2-Clause; provider-dependent examples require credentials and may incur costs when run.

**OpenAI Realtime Console**

MIT; example application, not a production template guarantee.

**Twilio Call GPT**

MIT; inspect current provider API compatibility before reuse.

**Voice Agents from Scratch**

MIT. A learning repository, not an installable SKILL.md pack. Setup downloads model assets, whose licenses and hardware needs must be checked separately. No chapters were executed in this research.

</details>

## Primary documentation and learning paths

- [LiveKit Agents documentation](https://docs.livekit.io/agents/) for agent sessions, media, turn handling, metrics, and tests.
- [Pipecat documentation](https://docs.pipecat.ai/overview/introduction) for pipelines, processors, transports, and client SDKs.
- [OpenAI Agents SDK voice guide](https://openai.github.io/openai-agents-js/guides/voice-agents/) for realtime agents and browser/server connections.
- [Twilio Media Streams documentation](https://www.twilio.com/docs/voice/media-streams) for phone-audio WebSocket integration.
- [jambonz documentation](https://docs.jambonz.org/) for programmable telephony and deployment.
- [WebRTC for the Curious](https://webrtcforthecurious.com/) for media negotiation, network traversal, and realtime transport concepts.
- [Pipecat open benchmarks](https://www.pipecat.ai/benchmarks) for published speech and voice-agent studies. Treat vendor-published results as methodology and artifacts to inspect, not universal rankings.
- [LiveKit eot-bench methodology](https://github.com/livekit/eot-bench#evaluation-model) for causal pause decisions and the latency/false-cutoff tradeoff.

### Cloud voice and native speech services

- [Azure Voice Live](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live) for Microsoft's managed voice service and integration choices. The source page records an update on 2026-09-29.
- [Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api) for direct live sessions; [ADK live and voice agents](https://adk.dev/live/) for ADK orchestration.
- [Strands bidirectional streaming](https://strandsagents.com/docs/user-guide/sdk/bidirectional-streaming/) and [Bedrock Nova Sonic](https://strandsagents.com/docs/user-guide/sdk/bidirectional-streaming/models/bedrock/) for the current Python experimental integration. Verify current class names; older indexed examples use a different API.
- [Cloudflare Agents voice](https://developers.cloudflare.com/agents/communication-channels/voice/) for its voice integration. This is a focused reference within the general Agents SDK, not another dedicated voice skill counted here.
- [NVIDIA Speech NIM](https://docs.nvidia.com/nim/speech/latest/) for speech microservices and deployment documentation. Older `/nim/riva/latest/` links were unavailable during this review.

## Community discovery

- [LiveKit Community](https://community.livekit.io/) and [Pipecat community link](https://docs.pipecat.ai/overview/introduction#community) for maintainer discussions and support.
- [r/VoiceAIAgent](https://www.reddit.com/r/VoiceAIAgent/) and [r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) for engineering experiences and local speech experiments.
- [Orchestration-platform discussion](https://www.reddit.com/r/VoiceAIAgent/comments/1uj2qsg/what_is_your_choice_for_voice_ai_orchestration/) surfaces customization and transport concerns. Some comments are vendor-affiliated.
- [Local voice and automation discussion](https://www.reddit.com/r/LocalLLaMA/comments/1rytwl6/oss_local_voice_and_automation_in_2026/) describes faster-whisper, Kokoro, and LiveKit combinations. These are personal reports, not controlled performance measurements.
- [TTS selection discussion](https://www.reddit.com/r/LocalLLaMA/comments/1ud6z9s/best_text_to_speech/) highlights local-model tradeoffs. Validate model availability, licenses, and performance from primary sources.

Reddit supplied discovery leads and user-reported concerns. Vote totals, personal anecdotes, and promotional comments were not used as proof of technical correctness or production reliability.

## How to read voice benchmarks

<details>
<summary>Measurement checklist for comparing voice results</summary>

- Define every timing boundary. User speech end, VAD stop, transcript final, first model token, first TTS byte, and first audible playback are different events.
- Use a monotonic clock for durations. Timings from browser, worker, provider, and audio-device clocks cannot be subtracted directly without alignment. Framework event time can differ from captured acoustic time.
- Keep time-to-first-token, time-to-first-audio-byte, end-to-end audible response latency, and end-of-turn delay separate. Summing component spans can double-count overlapping streaming work.
- Match hardware, language, codec/sample rate, transport, region, model version, concurrency, dataset, warmup, and streaming policy before comparing results.
- WER, semantic WER, MOS, task success, false cutoffs, latency percentiles, and real-time factor measure different things. Report units, sample count, failures, and percentiles rather than one opaque score.
- Deduplicate by unique trial/turn ID. Multiple timing fields or a summary and its raw record are not additional trials.
- Offline throughput and inference time do not establish live conversational performance. Run microphone-to-speaker and phone-path checks for the actual application.

</details>

## Current source caveats

- **Moonshine:** the current LICENSE narrows noncommercial restrictions to listed legacy nonstreaming non-English models. Context7 returned an older, broader summary; the current original LICENSE controls this entry.
- **Future AGI:** the Simulate SDK and Agent Learning Kit describe consolidation differently. Check the maintained voice client examples before migrating imports.
- **SIPp:** the LICENSE.txt and README template disagree on the GPL version. The table preserves that discrepancy.
- **Local models:** an engine advertising streaming does not establish that each backend, checkpoint, or language supports the same mode. Qwen backend limits and model-card terms are recorded above.

## Provenance and scope

<details>
<summary>Observation methods, source coverage and research limits</summary>

[resources.json](../resources.json) holds 43 unique projects with source URLs, exact star counts, observation timestamps, and observed default-branch commits. Of the original 28 projects, eighteen were verified through the unauthenticated GitHub API. The shared public API quota was exhausted during research; ten were verified through GitHub's embedded repository JSON instead. The fallback and each new observation method are explicitly marked per record. License classification for fallback entries was checked against commit-pinned license files. No models or third-party code were executed. New skill sources are also indexed in the [expanded skill catalog](more-skills.md); their presence in this resource library does not add another unique skill.

This is a curated starting collection, not a claim to inventory every voice project. Docker Firecrawl was unavailable in this run. General web search, Reddit pages, GitHub API/HTML, and primary READMEs were covered. Community opinions and benchmark numbers were not independently reproduced. Library licenses do not automatically cover model weights, datasets, sample audio, or hosted services. Keep third-party projects linked unless their redistribution terms have been reviewed and required notices preserved.

</details>
