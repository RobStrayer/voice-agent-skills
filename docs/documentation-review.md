# Documentation review

Reviewed: **2026-09-30 UTC**.

Dates on NL guidance mean the page and its cited sources were reviewed on that
date. They do not mean the provider published its documentation that day.
Provider publication dates were not established for most living documentation
below; explicit source dates are identified where available. Snapshot commit dates and repository-star observations remain separate.

Context7 was used to find relevant documentation and compare API guidance.
Consequential claims were checked against the linked official pages or source
files. A Context7 result can contain an older example or miss a relevant page;
use the canonical reference for the version you are implementing.

## Architecture and runtime sources

All sources in this section were retrieved or reviewed on 2026-09-30 UTC.
The design worksheets and recommendations in the foundation skills are original
engineering guidance, not quotations or guarantees from a provider.

| Topic | Primary source | What the review supports |
| --- | --- | --- |
| OpenAI voice architecture | [Voice agents](https://developers.openai.com/api/docs/guides/voice-agents) | Compare documented voice architectures without treating a model family as a complete application. |
| OpenAI browser media | [WebRTC, Realtime section](https://developers.openai.com/api/docs/guides/voice-webrtc?api=realtime) | Browser media and session setup depend on the selected API. |
| OpenAI server media | [WebSockets, Realtime section](https://developers.openai.com/api/docs/guides/voice-websockets?api=realtime) | Server-side streaming has different media responsibilities from browser WebRTC. |
| OpenAI server controls | [Server controls, Realtime section](https://developers.openai.com/api/docs/guides/voice-server-controls?api=realtime) | Keep business logic and credentials on the server when controlling a realtime session. |
| OpenAI phone connections | [SIP, Realtime section](https://developers.openai.com/api/docs/guides/voice-sip?api=realtime) | Check the actual phone connection and call-control path. |
| OpenAI recorded speech | [TTS model](https://developers.openai.com/api/docs/models/gpt-4o-mini-tts), [transcription reference](https://developers.openai.com/api/reference/python/resources/audio/subresources/transcriptions/methods/create) | The dated TTS model snapshot is still documented; file transcription and diarization are distinct from realtime conversation. |
| Pipecat CLI | [Overview](https://docs.pipecat.ai/api-reference/cli/overview), [init](https://docs.pipecat.ai/api-reference/cli/init) | Current package installation differs from the preserved skill wording; init remains supported. |
| LiveKit turn handling | [Turns](https://docs.livekit.io/agents/logic/turns.md) | Check whether turn detection is controlled by the framework or realtime provider. |
| LiveKit tool work | [Function tools](https://docs.livekit.io/agents/logic/tools/definition.md#interruptions) | Speech interruption does not cancel running work by default. |
| LiveKit metrics | [Data hooks](https://docs.livekit.io/testing/observability/data.md) | Per-turn metrics, usage events, and playback reports have different meanings; fields depend on the active pipeline. |
| LiveKit behavior tests | [Test framework](https://docs.livekit.io/agents/start/testing/test-framework.md) | Ordered assertions and tool mocks support behavior tests; they do not exercise every media layer. |
| LiveKit spoken instructions | [Prompting](https://docs.livekit.io/agents/start/prompting.md) | Voice-oriented prompts, focused questions, and pronunciation guidance. |
| Twilio speech boundary | [ConversationRelay](https://www.twilio.com/docs/voice/twiml/connect/conversationrelay) | Application text exchange with managed speech processing. |
| Twilio relay interruptions | [WebSocket messages](https://www.twilio.com/docs/voice/conversationrelay/websocket-messages) | Relay events are distinct from raw Media Streams events. |
| Twilio audio boundary | [Media Streams messages](https://www.twilio.com/docs/voice/media-streams/websocket-messages) | A returned mark can follow playback or a clear operation. |
| ElevenLabs turn controls | [Conversation flow](https://elevenlabs.io/docs/eleven-agents/customization/conversation-flow) | Silence timeout, soft-timeout filler, interruption, and turn eagerness are separate controls. |
| ElevenLabs tool controls | [Tool interruptions](https://elevenlabs.io/docs/eleven-agents/customization/tools/tool-configuration/tool-interruptions) | Current interruption modes and the deprecated boolean mapping. |
| Cartesia generated speech | [Contexts and continuations](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts) | Cancelling a context does not stop a request already generating a response. |
| Cartesia managed agents | [Line](https://docs.cartesia.ai/line/introduction) | Managed speech orchestration has a different ownership boundary from the standalone speech API. |

Context7 library IDs used for these topics: `/websites/developers_openai_api`,
`/pipecat-ai/docs`, `/websites/livekit_io_agents`, `/livekit/agents`,
`/llmstxt/twilio_llms_txt`, `/websites/twilio_voice`, `/websites/elevenlabs_io`,
and `/websites/cartesia_ai`. Those IDs describe retrieval sources, not SDK versions.

For older OpenAI URLs that now lead to shared voice documentation, select the
Realtime section when implementing Realtime. Do not combine GPT-Live and Realtime
examples into one imagined API.

## Additional documentation checked

All entries below were checked on **2026-09-30 UTC**. Context7 library identifiers
are retrieval indexes, not installed SDK versions. Missing or contradictory
indexed material was checked against the current primary source.

| Topic | Current primary source | Finding or limit |
| --- | --- | --- |
| Shiny native speech | [Current documentation](https://shinylib.net/speech/), [skill](https://github.com/shinyorg/skills/blob/main/plugins/shiny/skills/shiny-speech/SKILL.md) | Selected APIs were confirmed in published .NET 10 prerelease package metadata/XML; platform inconsistencies remain qualified in the catalog. Context7: `/llmstxt/shinylib_net_llms_txt`. |
| RNNoise input processing | [Authoritative source](https://gitlab.xiph.org/xiph/rnnoise), [COPYING](https://gitlab.xiph.org/xiph/rnnoise/-/blob/main/COPYING) | GitLab and the GitHub mirror match. Main commit date is **2025-02-22**, not a claim of recent development. Context7 `/xiph/rnnoise` returned synthetic citations; the original source was checked. |
| Browser playback | [MDN play](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/play), [getStats](https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection/getStats) | Playback promises and media counters provide different evidence; a connected peer alone does not establish audible output. |
| WebRTC transport | [Peer connections](https://webrtc.org/getting-started/peer-connections), [TURN](https://webrtc.org/getting-started/turn-server) | Separate signaling, candidate selection, transport, and playback. |
| WebRTC timing | [W3C statistics](https://www.w3.org/TR/webrtc-stats/) | Published Candidate Recommendation Draft dated **2025-09-25**. Counter definitions support interval calculations; implementation support varies. |
| Azure Voice Live | [Overview](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live) | The page's own `updated_at` metadata is **2026-09-29T06:04:00Z**. It is distinct from this review date. |
| Azure SDK examples | [Version notes](more-skills.md#azure-sdk-version-notes) | Released Java, TypeScript, .NET, and Python package contents were inspected without installing or executing them. Preview pins and actual API typos are treated separately. |
| Azure file transcription | [Python SDK README](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/transcription/azure-ai-transcription/README.md) | The linked skill's streaming/batch methods are absent from released `1.0.0`; that skill is excluded. |
| Gemini Live | [Live API](https://ai.google.dev/gemini-api/docs/live-api), [ADK live](https://adk.dev/live/) | Direct live sessions and ADK orchestration have separate integration paths; the older ADK streaming page redirects. |
| Strands and Nova Sonic | [Current bidirectional guide](https://strandsagents.com/docs/user-guide/sdk/bidirectional-streaming/), [Bedrock model](https://strandsagents.com/docs/user-guide/sdk/bidirectional-streaming/models/bedrock/) | Current Python experimental API differs from older indexed class names. |
| Cloudflare voice | [Voice documentation](https://developers.cloudflare.com/agents/communication-channels/voice/) | Focused voice reference in a general SDK; not counted as a separate dedicated skill. |
| NVIDIA speech | [Speech NIM](https://docs.nvidia.com/nim/speech/latest/) | Current documentation prefix replaces an unavailable older Riva NIM URL. Model/container terms remain separate. |
| Telnyx | [Agent skills documentation](https://developers.telnyx.com/development/agent-skills.md) | The old skills repository alias resolves to `team-telnyx/ai`; canonical paths exclude plugin mirrors. |
| Deepgram SDKs | [Go Flux example](https://github.com/deepgram/deepgram-go-sdk/blob/main/examples/speech-to-text/websocket/flux_channel/main.go) | A current Go manifest incorrectly says the v2 client/example is absent. That manifest is excluded. Five Java skills reference an unavailable root `reference.md`. |
| AssemblyAI | [Python registry](https://pypi.org/project/assemblyai/), [JavaScript registry](https://www.npmjs.com/package/assemblyai) | Observed releases `1.6.1` and `4.41.5` supersede the constants in the skill. |
| Coval evaluations | [API introduction](https://docs.coval.ai/api-reference/v1/introduction), [accent testing](https://docs.coval.ai/guides/testing-across-accents) | Account-scoped simulations and scoring require bounded runs and authorized usage. |
| Moonshine | [Current LICENSE](https://github.com/moonshine-ai/moonshine/blob/main/LICENSE) | Current model-license exceptions are narrower than the older Context7 summary. See the resource entry for the distinction. |
| Synthflow | [Custom evaluations](https://docs.synthflow.ai/create-a-custom-evaluation), [simulations](https://docs.synthflow.ai/simulations) | No matching Context7 library was found; official pages were read directly. Skills include telemetry instructions with opt-outs. |
| Voximplant | [Current inbound example](https://docs.voximplant.ai/voice-ai-orchestration/openai/inbound.md) | The current documentation site supplies the integration contract; older indexed examples were not copied into this repo. |

Media references used `/mdn/content` and `/websites/webrtc`. Cloud/provider queries
used the resolved Azure SDK libraries, `/websites/learn_microsoft_en-us_azure`,
`/google/adk-python`, `/websites/ai_google_dev_gemini-api_live-api`,
`/websites/strandsagents`, `/websites/developers_cloudflare_agents`, and the matching
Telnyx, Deepgram, AssemblyAI, Coval, Moonshine, and Voximplant indexes. Individual
resource retrieval details are retained in [resources.json](../resources.json).

## Context7 coverage and fallback

Every one of the original 28 runtime projects received a Context7 resolution
attempt. Twenty-seven received a narrow documentation query: 22 exact repository
indexes, one official documentation index, and four related ecosystem indexes.
Hugging Face's speech-to-speech repository had no exact match. The fifteen new
resource entries were also checked through matching or related libraries, with
explicit primary-source fallback where no suitable index was found.

Some returned references were unavailable: 14 of 86 GitHub-backed source files
in the baseline audit returned 404. The separately audited expansion references
included nine unavailable generated paths. These were not accepted as source
proof. The primary README, license, model card, or released package was used for
the relevant claim. A successful Context7 query does not certify a source's
currency or an example's runtime compatibility.

## Engineering handbook source checks

The deeper handbook pass on **2026-09-30 UTC** queried Context7 for the relevant
provider and media topics, then compared the consequential claims with current
primary pages. The following distinctions affect implementation:

| Topic | Current primary evidence | Consequence for these guides |
| --- | --- | --- |
| LiveKit end-of-turn detection | [Turn detector](https://docs.livekit.io/agents/logic/turns/turn-detector.md) | Current audio detection differs from the deprecated text detector, which is slated for removal in SDK 2.0. Audio detection requires Python 1.6.1+ or Node.js 1.4.7+ and a minimum VAD silence duration of 0.25 seconds. This SDK validation requirement is not a universal endpoint tuning recommendation. |
| LiveKit audio processing | [Noise cancellation](https://docs.livekit.io/transport/media/noise-cancellation/) | Distinguish frontend BVC from current agent-side Krisp VIVA/VIVA telephony. Cloud-mediated enhancement and direct-auth ai-coustics deployments have different requirements. The frontend guide records the self-hosted exception. |
| Deepgram streaming recognition | [Finality and endpointing](https://developers.deepgram.com/docs/understand-endpointing-interim-results), [Flux migration](https://developers.deepgram.com/docs/flux/nova-3-migration) | Stable transcript segments and turn completion are separate. Nova and Flux event handling are not interchangeable. |
| ElevenLabs incremental synthesis | [WebSocket guide](https://elevenlabs.io/docs/eleven-api/guides/how-to/websockets/realtime-tts), [API reference](https://elevenlabs.io/docs/api-reference/text-to-speech/v-1-text-to-speech-voice-id-stream-input) | Text buffering and final flush affect output. The reference qualifies auto mode for full sentences; it is not an unconditional low-latency setting for arbitrary token chunks. The current API contract takes precedence over generated SDK summaries. |
| LiveKit action lifetime | [Tool definition](https://docs.livekit.io/agents/logic/tools/definition.md), [Async tools](https://docs.livekit.io/agents/logic/tools/async.md) | Interrupted work can continue. Async cancellation is opt-in; duplicate controls are based on tool name, not arguments. Toolset lifetime across an agent handoff does not supply a durable external transaction ledger. |
| Echo and local enhancement | [WebRTC audio processing](https://webrtc.googlesource.com/src/+/refs/heads/main/modules/audio_processing/include/audio_processing.h), [RNNoise](https://gitlab.xiph.org/xiph/rnnoise), [DeepFilterNet](https://github.com/Rikorose/DeepFilterNet) | Check reference audio, frame/sample contracts, deployment cost, and artifact-specific licensing. Code terms do not establish every model artifact's terms. |
| Telephone media and completion | [Twilio Media Streams](https://www.twilio.com/docs/voice/media-streams), [message contract](https://www.twilio.com/docs/voice/media-streams/websocket-messages), [Call resource](https://www.twilio.com/docs/voice/api/call-resource) | Direction, DTMF support, clear/mark semantics, and callback event versus final status need explicit handling. |
| Alternative media bridge | [jambonz listen contract](https://docs.jambonz.org/verbs/verbs/listen.md) | Binary streaming and buffered JSON return paths differ. The canonical Markdown document supplied the source when automated HTML retrieval was restricted. |

The handbook's diagrams, state names, example timings, failure policies, and
worksheets are original explanatory material. They do not claim to reproduce a
provider's exact event graph. Source retrieval was read-only; SDK execution,
audio-quality results, transfers, and capacity remain application-level tests.

## Snapshot freshness

The 27 bundled provider skills and all 104 copied files were rechecked against
freshly retrieved upstream heads on 2026-09-30 UTC. All matched the recorded
snapshots. This establishes file freshness at review time; a maintained skill can
still contain an old installation example or an incomplete recipe.

| Original source | Observed head | Repository commit time, UTC |
| --- | --- | --- |
| [ElevenLabs](https://github.com/elevenlabs/skills) | [279173d974ea](https://github.com/elevenlabs/skills/commit/279173d974ea5cf0c4c4f91d4e7e65202b406dab) | 2026-09-29 17:27:30 |
| [LiveKit](https://github.com/livekit/agent-skills) | [5d7488b118c2](https://github.com/livekit/agent-skills/commit/5d7488b118c279812b89e73a9bee8474d1fe00a1) | 2026-09-24 23:08:01 |
| [Pipecat](https://github.com/pipecat-ai/skills) | [cca35d3b8566](https://github.com/pipecat-ai/skills/commit/cca35d3b85665fb417fddb2bc8ec8a5c3805aa57) | 2026-07-13 19:50:54 |
| [Cartesia](https://github.com/cartesia-ai/skills) | [0ee3f4a4ad8e](https://github.com/cartesia-ai/skills/commit/0ee3f4a4ad8e9cf9d314962448b721cdc34fae42) | 2026-08-22 04:16:19 |
| [Twilio](https://github.com/twilio/ai) | [8aba46fb65dc](https://github.com/twilio/ai/commit/8aba46fb65dc8d9a20f4b301a68352064b4159a5) | 2026-08-13 21:08:28 |
| [OpenAI](https://github.com/openai/skills) | [49f948faa925](https://github.com/openai/skills/commit/49f948faa9258a0c61caceaf225e179651397431) | 2026-06-24 02:36:12 |

These are repository-head commit times, not each skill's last edit date. Full file
hashes and licenses remain in [sources.json](../sources.json). The current Pipecat
installation and OpenAI output-path caveats are in [usage notes](usage.md).

## Architecture graphic check, 2026-09-30 UTC

The three-pattern architecture comparison was checked against the current
[OpenAI voice agents guide](https://developers.openai.com/api/docs/guides/voice-agents).
It distinguishes a chain, speech-to-speech, and a delegated conversational layer.
Context7 library `/websites/developers_openai_api` returned useful chain guidance
but did not cover the requested GPT-Live distinction in its response; the
canonical page supplied that part. No model name, speed ranking, or compatibility
claim was inferred from the mixed-version snippets. The figure is a conceptual
comparison, with media and business-state responsibilities left to the full guide.

## What remains unverified

The review did not execute voice-provider APIs, paid voice inference, audio benchmarks,
phone calls, deployments, or third-party installers. It cannot establish runtime
compatibility or voice quality for a future application. The resource library's
original star counts retain their original observation dates; this documentation
review does not silently refresh those numbers.

## Illustrated timing and call flow review, 2026-09-30 UTC

The expanded README uses six compact original teaching diagrams and a task-based
skill directory. The cascade, call tree, conversational score, acoustic signal
path, and action ledger summarize the dated foundation guides. New provider skill links were
matched to the original `SKILL.md` URLs already recorded in the catalogs.

The timing chart is a fabricated single-turn trace, with its complete event
sequence stated in native text. Its numbers do not come from a vendor benchmark.
Context7 library `/websites/livekit_io_agents` returned no result for the focused
measurement-boundary query; a broader query returned tuning and avatar snippets
but did not establish the full latency contract. The canonical
[LiveKit data hooks page](https://docs.livekit.io/testing/observability/data.md)
was then retrieved through the official LiveKit documentation connector on
2026-09-30 UTC. It distinguishes per-plugin and per-turn metrics, identifies
pipeline-only fields, and qualifies reported playback timing. The README keeps
the distinction between instrumented events and observed caller playback.

Context7 retrieval was used where available, with the gap recorded here. The
current-source check supports measurement terminology; it does not turn the
illustrative trace into measured data or refresh unrelated repository statistics.
