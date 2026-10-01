# Provider landscape

[Home](../README.md) / Provider landscape

This page compares 181 voice agent products in nine categories, from managed
platforms and speech models to phone carriers and testing tools. Everything here
is as of September 30, 2026, unless a row gives another date. Prices and
products change often, so follow the links before you rely on a number.

![The voice agent stack by category: a caller reaches telephony and transport, then turn detection and audio cleanup, then either a cascade of streaming speech-to-text, a language model and text-to-speech, or a single speech-to-speech model. Orchestration frameworks wire the pieces together, managed platforms bundle them, and testing tools watch the whole thing.](../assets/diagrams/provider-landscape.svg)

**On this page:** [How to choose](#how-to-choose) ·
[What it costs per minute](#what-it-costs-per-minute) ·
[What changed recently](#what-changed-recently) ·
[How to read the product tables](#how-to-read-the-product-tables) ·
[A. Managed voice-agent platforms](#a-managed-voice-agent-platforms) ·
[B. Speech-to-speech and realtime models](#b-speech-to-speech-and-realtime-models) ·
[C. Orchestration frameworks](#c-orchestration-frameworks) ·
[D. Streaming speech-to-text](#d-streaming-speech-to-text) ·
[E. Low-latency text-to-speech](#e-low-latency-text-to-speech) ·
[F. Telephony and transport](#f-telephony-and-transport) ·
[G. Turn detection, VAD and noise](#g-turn-detection-vad-and-noise) ·
[H. Testing, evals and observability](#h-testing-evals-and-observability) ·
[I. Language models](#i-language-models) ·
[Skills for these providers](#skills-for-these-providers) ·
[How this was researched](#how-this-was-researched)

## How to choose

No single provider fits everyone. The right starting point depends on what you
need to control and how much you want to run yourself. This table is general
guidance with pointers into the rest of this page. It is not a vendor claim.

| If this is you | Start with | Watch for |
| --- | --- | --- |
| You need a phone agent soon and don't want to run servers | A managed platform ([A](#a-managed-voice-agent-platforms)) | Pass-through costs, concurrency caps, prompts and flows that live in the vendor's tool, and consolidation: Aircall bought Vogent, Inworld bought Ultravox and Vocode is listed as bought by OpenEvidence |
| You want control of turn-taking, tools, telephony or where data lives, or your volume makes per-minute platform fees matter | An open-source framework ([C](#c-orchestration-frameworks)) plus provider APIs | You run it yourself. Some frameworks add license terms: the TEN Framework has extra conditions, and self-hosting jambonz needs a paid license key after a one-month trial |
| A natural flow from one end-to-end model matters more than choosing each piece | A speech-to-speech API ([B](#b-speech-to-speech-and-realtime-models)) | Less control over the voice, speech-to-text and language model pieces. Builders report weaker tool use, so many keep phone and tool-heavy agents on a cascade ([common problems](common-problems.md#12-speech-to-speech-or-a-cascade)). Re-billed context raises the cost of long calls. Models retire: OpenAI removes its older realtime models on January 20, 2027 |
| You already have a SIP trunk or carrier | A framework with SIP support, such as LiveKit SIP, jambonz or Pipecat with Daily ([C](#c-orchestration-frameworks), [F](#f-telephony-and-transport)) | Media-streaming add-ons (Twilio Media Streams is $0.0044/min), number rental and toll-free surcharges |
| You must self-host models | Open-weight speech-to-text, text-to-speech and language models with a framework ([D](#d-streaming-speech-to-text), [E](#e-low-latency-text-to-speech), [I](#i-language-models)) | Read each license. Some weights are non-commercial or carry conditions, such as Voxtral TTS (CC BY-NC 4.0), Fish Audio and Higgs Audio v3. Many open text-to-speech projects have had no pushes for months |
| You are about to ship | Testing ([H](#h-testing-evals-and-observability)) and turn detection ([G](#g-turn-detection-vad-and-noise)), early | Several testing tools publish prices, for example Cekura at $0.25 per voice testing minute, Roark at $0.15/min for simulation and Future AGI from $0.08/minute. Hamming is sales only |

A reasonable order of decisions:

1. Pick the call path: a phone number, or a web or mobile app.
2. Choose a managed platform, a framework or a single speech-to-speech model.
3. Pick the speech and language model pieces by measured latency on your own audio, not by list price.
4. Add turn detection and testing before you scale.

The getting started guide has a longer version in
[Pick a starting path](getting-started.md#pick-a-starting-path). The
[stack selection skill](../skills/foundations/voice-stack-selection/SKILL.md)
walks a coding agent through the same decision with you.

## What it costs per minute

All figures are US dollars per minute of live conversation, worked out from list
prices seen on September 30, 2026. None of them is a quote. Volume tiers,
promotions, free allowances, regions and currency all change the result.

**Assumptions for the estimates.** The cascade arithmetic
uses the defaults in LiveKit's published pricing calculator: 3,000 language
model input tokens, 175 output tokens and 600 text-to-speech characters per
minute. The speech-to-speech rows derived from token prices use OpenAI's stated
audio rates (10 user and 20 assistant tokens per second). The cascade defaults come from LiveKit's docs MCP server (its `get_pricing_info` tool),
read on September 30, 2026. They describe a short conversation. Real agents
re-send a growing history, so the language model line is a floor. Turn taking,
silence billing, minimum billing increments and recording are not modeled.

| Approach | Typical range per minute, at list prices | What it leaves out |
| --- | --- | --- |
| Managed platform | $0.05 to $0.31 for the platforms tabled below (vendor-published; what each figure includes differs) | Telephony on some, the language model on some, concurrency add-ons, HIPAA and SLA tiers |
| Assembled cascade | $0.015 to $0.132, mid stack about $0.056 (estimate) | Your engineering and operations time, language model growth as history is re-sent, recording, free tiers and volume discounts, and self-hosted compute in the low case |
| Speech-to-speech API | $0.023 to $0.096 for the audio alone (estimate, a floor) | Telephony, backend model and tool calls, re-billed context and any platform markup |

### Managed platforms

Vendor-published figures. They are not like-for-like: the third column shows
what each one covers.

| Platform | Published per-minute figure | What the figure includes |
| --- | --- | --- |
| [Telnyx AI Assistants](https://telnyx.com/pricing/voice-ai-agents) | $0.0596/min (vendor example: voice engine $0.05 + telephony $0.0032 + language model $0.0064, local inbound US) | Voice engine (orchestration, speech-to-text, text-to-speech), telephony, and a language model on Telnyx-hosted models |
| [Deepgram Voice Agent API](https://deepgram.com/pricing) | $0.050 (bring your own LLM and TTS) to $0.163 (Advanced tier) per minute on Pay As You Go; Standard $0.075 | Speech-to-text and orchestration, plus the language model and text-to-speech depending on tier; telephony not listed |
| [Twilio ConversationRelay](https://www.twilio.com/en-us/products/conversational-ai/pricing) | $0.07/min + $0.0085/min inbound US local voice = $0.0785/min before your language model and hosting | Relay with speech-to-text and text-to-speech (itemization not published); voice billed separately; the language model and app hosting are yours |
| [Vapi](https://vapi.ai/pricing) | $0.05/min hosting fee; vendor calculator example (Deepgram + OpenAI + ElevenLabs, Vapi telephony/SIP) $0.082-$0.129/min | Hosting fee plus pass-through speech-to-text, language model and text-to-speech; PSTN carrier not included in the example |
| [ElevenAgents](https://elevenlabs.io/pricing/agents) | $0.080/min beyond plan-included minutes | Agent platform minutes; the language model (passed through) and telephony (at cost) are extra |
| [Bland AI](https://www.bland.ai/pricing) | $0.14/min (Start) or $0.12/min (Build, plus $299/month) | Language model, speech-to-text and text-to-speech included; telephony billed separately |
| [Retell AI](https://www.retellai.com/pricing) | $0.07-$0.31/min vendor-stated range; the page's calculator default is $0.11/min (LLM $0.04 + voice infra $0.055 + TTS $0.015) | Voice infrastructure, text-to-speech and language model; telephony $0.015/min extra on Retell numbers |
| [Bolna](https://www.bolna.ai/pricing) | From 6.00 cents/min (standard volume-based rate); pilot packs about 4.2-4.6 cents/min | Platform rate; the recorded entry does not itemize what it includes (bring-your-own keys supported, credits billed on tokens) |
| [Dasha](https://dasha.ai/pricing) | Growth plan from $0.08/min (the button reads Contact Us) | Platform; VoIP and language model tokens extra |
| [AssemblyAI Voice Agent API (launched April 25, 2026)](https://www.assemblyai.com/changelog) | $4.50/hr all-in = $0.075/min (derived: $4.50 / 60) | Speech understanding, language model reasoning and voice generation on AssemblyAI's own models; telephony not stated |

**Range.** Among the ten platforms in this table, published figures run from
$0.05/min (Deepgram Voice Agent API with your own language model and
text-to-speech, so those costs are extra) to $0.31/min (the top of Retell AI's
stated range). Some base or connectivity fees in section A are lower (Millis AI
$0.02/min, Voximplant $0.004/min) but cover less. The lowest figure that already
includes telephony and a language model is Telnyx's own example at $0.0596/min.
Sales-only platforms (Sierra, Decagon, PolyAI, Parloa, Regal, Synthflow
enterprise contracts and Voiceflow plan prices) publish no per-minute price and
are left out.

### Assembled cascade

Your own speech-to-text, language model, text-to-speech, telephony and runtime.
Each cell shows the per-minute cost and the product it comes from.

| Line item | Low | Mid | High |
| --- | --- | --- | --- |
| Speech-to-text | $0.0025: [AssemblyAI Universal-Streaming English](https://www.assemblyai.com/pricing) | $0.0077: [Deepgram Nova-3 monolingual streaming, regular price](https://deepgram.com/pricing) | $0.01667: [Azure Speech real-time standard](https://azure.microsoft.com/en-us/pricing/details/speech/) |
| Language model | $0.00056: [gpt-oss-120b on GroqCloud](https://console.groq.com/docs/models) | $0.00148: [OpenAI gpt-4.1-mini](https://developers.openai.com/api/docs/pricing) | $0.03875: [OpenAI gpt-6-astra](https://developers.openai.com/api/docs/pricing) |
| Text-to-speech | $0.009: [Deepgram Aura-1 (Pay As You Go)](https://deepgram.com/pricing) | $0.024: [ElevenLabs Flash v2.5 / Turbo row](https://elevenlabs.io/pricing/api) | $0.048: [ElevenLabs Eleven v4, list price](https://elevenlabs.io/pricing/api) |
| Telephony | $0.0032: [Telnyx SIP trunk, inbound US local](https://telnyx.com/pricing/elastic-sip) | $0.0129: [Twilio inbound US local $0.0085 + Media Streams $0.0044](https://www.twilio.com/en-us/voice/pricing/us) | $0.0184: [Twilio outbound US local $0.014 + Media Streams $0.0044](https://www.twilio.com/en-us/voice/pricing/us) |
| Runtime | not priced (self-hosted compute is not counted) | $0.01: [LiveKit Cloud agent session, beyond included minutes](https://livekit.com/pricing) | $0.01: [LiveKit Cloud agent session](https://livekit.com/pricing) |
| **Total per minute (estimate)** | **$0.015** | **$0.056** | **$0.132** |

Arithmetic: language model = 3,000 x input price per token + 175 x output price
per token; text-to-speech = 600 characters x price per character; speech-to-text
= hourly price / 60; telephony lines are the per-minute carrier rates as
displayed. Low uses the lowest-priced streaming components documented in this
study and no runtime charge. Mid uses common list-price components with LiveKit
Cloud's $0.01/min agent session fee as the runtime. High uses higher-priced
components: Azure real-time speech-to-text, OpenAI gpt-6-astra, ElevenLabs
Eleven v4 at list price and Twilio outbound. Promotional prices (Deepgram
Nova-3's current price, ElevenLabs v4 until Oct 12) are left out on purpose.

### Speech-to-speech APIs

Audio-token or per-minute pricing.

| Model or API | Per minute | Basis |
| --- | --- | --- |
| [Gemini Live gemini-3.8-live (audio in + audio out)](https://ai.google.dev/gemini-api/docs/pricing) | $0.023 | Vendor-stated per-minute figures: $0.005/min in + $0.018/min out |
| [OpenAI GPT-Live-1](https://developers.openai.com/api/docs/pricing) | $0.05 | Vendor-stated flat per-minute price, billed per second; backend model and tool usage extra |
| [xAI Grok Speech to Speech](https://docs.x.ai/developers/pricing) | $0.08 | Vendor-stated flat per-minute price |
| [OpenAI gpt-realtime-2.1-mini (audio tokens only)](https://developers.openai.com/api/docs/pricing) | $0.03 | Derived lower bound: 600 user tokens per minute x $10/1M + 1,200 assistant tokens per minute x $20/1M (OpenAI states 1 token per 100 ms of user audio and per 50 ms of assistant audio in its [voice cost guide](https://developers.openai.com/api/docs/guides/voice-latency-cost)) |
| [OpenAI gpt-realtime-2.1 (audio tokens only)](https://developers.openai.com/api/docs/pricing) | $0.096 | Derived lower bound: 600 x $32/1M + 1,200 x $64/1M |
| [Azure Voice Live Pro, native audio (audio tokens only)](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/) | $0.096 | Derived lower bound: 600 x $32/1M + 1,200 x $64/1M (same token rates as OpenAI) |

**Range.** $0.023 to $0.096 per minute for the audio itself. These leave out
telephony (add about $0.0032 to $0.0184/min from the carrier lines above),
backend model and tool calls, and conversation context: OpenAI and Google both
state that the conversation is re-billed on each turn, so long sessions cost
more per minute than the floor. The derived rows assume both sides speak for the
whole minute. Amazon Nova 2 Sonic ($3.00 in / $12.00 out per 1M speech tokens)
has no per-minute figure on the AWS pages opened, so none is derived.

**Why real bills run higher.** The language model reads the conversation again
on every turn. If the cascade above re-sent ten times as many input tokens
(output unchanged), its three language model lines would go from $0.00056,
$0.00148 and $0.03875 to $0.0046, $0.01228 and $0.30875 per minute (estimate).
Telephony, recording, concurrency, minimum billing increments and add-ons come
on top. Builders report the same gap between headline price and invoice in
[Cost: headline price versus the invoice](common-problems.md#5-cost-headline-price-versus-the-invoice).
To work out your own number, use the
[cost estimation skill](../skills/foundations/voice-cost-estimation/SKILL.md).

## What changed recently

These changes touch products listed on this page, each with a source. Where a
date is a range or rests on one source, the bullet says so.

**Shut down**

- **PlayHT / PlayAI** ([E](#e-low-latency-text-to-speech)). TechCrunch reported
  on July 13, 2025 that Meta had acquired the company and that its team would
  join Meta
  ([TechCrunch](https://techcrunch.com/2025/07/13/meta-acquires-voice-startup-play-ai/)).
  Archived copies of play.ht (January 6, 2026) and play.ai (January 11, 2026)
  show a banner saying the service has been shut down
  ([archived play.ht](https://web.archive.org/web/20260106201747id_/https://play.ht/)).
  Sources disagree on when the API went offline. Pipecat's changelog gives
  December 31, 2025
  ([Pipecat changelog](https://github.com/pipecat-ai/pipecat/blob/main/CHANGELOG.md)),
  and Groq retired its hosted PlayAI voice models on the same day
  ([Groq](https://console.groq.com/docs/deprecations)). A competitor's migration
  guide says the API went offline around July 26, 2025, before the platform
  closed on December 31
  ([Inworld](https://inworld.ai/resources/migrate-from-playht)). No announcement
  from PlayHT with the dates was found, so the exact date is unverified.
- **LMNT** ([E](#e-low-latency-text-to-speech)). Its website and docs show only
  a shutdown message on September 30, 2026. Archived copies place the change
  between August 3 and September 1, 2026. No acquirer or migration notice was
  found ([lmnt.com](https://www.lmnt.com/)).

**Acquired or re-homed (Gladia, Hume AI and Groq are still listed as active)**

- **Vogent** ([A](#a-managed-voice-agent-platforms)). Aircall announced the
  acquisition on May 6, 2026. The announcement does not say whether Vogent stays
  a standalone developer platform
  ([press release copy on Yahoo Finance](https://finance.yahoo.com/sectors/technology/articles/aircall-acquires-vogent-advance-ai-100300337.html)).
- **Ultravox** ([B](#b-speech-to-speech-and-realtime-models)). Inworld announced
  on September 30, 2026 that it acquired Ultravox. Existing agents keep running.
  Ultravox's site carries the same notice
  ([Inworld blog](https://inworld.ai/blog/inworld-acquires-ultravox),
  [Ultravox](https://www.ultravox.ai/pricing)).
- **Vocode** ([C](#c-orchestration-frameworks)). Two staff bios on OpenEvidence's
  About page read "Founder @ Vocode (Acquired by OpenEvidence)", and Y
  Combinator's directory lists Vocode as acquired. Neither gives a date or terms
  ([OpenEvidence](https://www.openevidence.com/about),
  [Y Combinator](https://www.ycombinator.com/companies/vocode)). Its hosted API
  host names no longer resolve, and no shutdown notice was found.
- **Langfuse** ([H](#h-testing-evals-and-observability)). ClickHouse announced
  the acquisition on January 16, 2026. Langfuse says it stays open source and
  self-hostable
  ([ClickHouse](https://clickhouse.com/blog/clickhouse-raises-400-million-series-d-acquires-langfuse-launches-postgres)).
- **Gladia** ([D](#d-streaming-speech-to-text)). A post dated September 21, 2026
  says OVH Groupe's acquisition of Gladia was announced on July 31 and that
  Gladia keeps its brand and API. The same post says the deal is still subject
  to regulatory approvals and closing conditions, so it may not have closed yet
  ([Gladia](https://www.gladia.io/blog/gladia-joins-ovh-groupe)).
- **Hume AI** ([B](#b-speech-to-speech-and-realtime-models),
  [E](#e-low-latency-text-to-speech)). WIRED reported on January 22, 2026 that
  Google DeepMind signed a licensing deal with Hume and hired its CEO and about
  seven engineers
  ([Wired](https://www.wired.com/story/google-hires-hume-ai-ceo-licensing-deal-gemini/)).
  Hume continues under a new CEO.
- **Groq** ([D](#d-streaming-speech-to-text), [I](#i-language-models)). On
  December 24, 2025 Nvidia took a non-exclusive license to Groq's inference
  technology and hired its founder. Groq says GroqCloud continues
  ([Groq](https://groq.com/newsroom/groq-and-nvidia-enter-non-exclusive-inference-technology-licensing-agreement-to-accelerate-ai-inference-at-global-scale)).

**Renamed or folded in**

- **ElevenLabs** ([A](#a-managed-voice-agent-platforms)). Its changelog for the
  week of February 9, 2026 lists the Agents Platform as renamed ElevenAgents
  ([changelog](https://elevenlabs.io/docs/changelog/2026/2/9)).
- **VideoSDK AI Agents** ([C](#c-orchestration-frameworks)) is now Zero Runtime
  AI, according to notices on VideoSDK's docs and pricing pages read on
  September 30, 2026
  ([VideoSDK docs](https://docs.videosdk.live/ai_agents/introduction)).
- **Daily Bots** ([C](#c-orchestration-frameworks)). Its old product pages
  redirect to Pipecat Cloud (September 30, 2026). No written notice was found,
  so the entry is marked unverified
  ([Daily](https://www.daily.co/products/daily-bots/)).
- **xAI** ([B](#b-speech-to-speech-and-realtime-models),
  [I](#i-language-models)). SpaceX acquired xAI in an all-stock deal on
  February 2, 2026
  ([Slashdot, citing CNBC](https://slashdot.org/story/26/02/03/0346252/spacex-acquires-xai-in-125-trillion-all-stock-deal)).
  On July 6, 2026 the company's X account announced the name SpaceXAI
  ([Not a Tesla App](https://www.notateslaapp.com/news/4410/spacex-unveils-new-xai-logo)).
  The docs.x.ai pages now call the provider SpaceXAI but still call the product
  the xAI API, and Grok keeps its name
  ([xAI release notes](https://docs.x.ai/developers/release-notes)).

### Upcoming dates

Dates to plan around, sorted by day. All were still ahead on September 30, 2026.

| Date | What changes | Source |
| --- | --- | --- |
| Oct 1, 2026 | Cartesia: language model use in Managed Agents is free until this date. Per-minute agent rates are unchanged. | [migration guide](https://docs.cartesia.ai/agents/migrate-from-line-sdk) |
| Oct 1, 2026 | Plivo: plan-based US account limits apply to accounts created on or after this date. The docs say earlier accounts keep custom limits. | [Plivo docs](https://plivo.com/docs/sip-trunking/concepts/account-limits) |
| Oct 12 (the page shows no year) | ElevenLabs: the 72% promotional price on Eleven v4 and v4 Turbo ends. List prices are $0.08 and $0.04 per 1K characters, against $0.022 and $0.011 now. | [pricing page](https://elevenlabs.io/pricing/api) |
| Oct 15, 2026 at the earliest (tentative) | Anthropic's tentative retirement date for Claude Haiku 4.5. Anthropic promises at least 60 days' notice and had given none on September 30, 2026, so retirement cannot come before late November 2026. | [deprecations page](https://platform.claude.com/docs/en/about-claude/model-deprecations) |
| After Oct 20, 2026 | Cartesia stops serving sonic-2, sonic-turbo and the sonic-3-2025-10-27 snapshot. The older models page still marks sonic-3-2025-10-27 as Stable. | [changelog](https://docs.cartesia.ai/changelog/2026), [older models page](https://docs.cartesia.ai/build-with-cartesia/tts-models/older-models) |
| Oct 22, 2026 | Twilio turns on provider failover for Real-Time Transcriptions by default. | [Twilio changelog](https://www.twilio.com/en-us/changelog) |
| Oct 23, 2026 | OpenAI shuts down gpt-4.1-nano. | [deprecations page](https://developers.openai.com/api/docs/deprecations) |
| Oct 29, 2026 | AWS closes the Amazon Chime SDK SIP Media Application to new customers. | [AWS](https://aws.amazon.com/chime/chime-sdk/) |
| Dec 1, 2026 | Cartesia stops hosting Line SDK agents. Managed Agents are the hosted path. | [migration guide](https://docs.cartesia.ai/agents/migrate-from-line-sdk) |
| Dec 2, 2026 at the earliest | Amazon Nova 2 Sonic: the end-of-life date on its Bedrock model card is "no sooner than" this day. Its lifecycle still shows Active. | [model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-2-sonic) |
| Dec 11, 2026 | OpenAI shuts down the gpt-5-2025-08-07, gpt-5-mini-2025-08-07 and gpt-5-nano-2025-08-07 snapshots. | [deprecations page](https://developers.openai.com/api/docs/deprecations) |
| Jan 1, 2027 | Google: paid rates for Gemini 3.8, 3.7 and 3.6 Flash double (for example 3.8 Flash from $0.75 / $3.75 to $1.50 / $7.50 per 1M tokens). Gemini 3.8 Flash TTS (Preview) goes from $0.50 / $9.00 to $1.00 / $18.00. | [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| Jan 20, 2027 | OpenAI removes gpt-realtime, gpt-realtime-mini, gpt-4o-realtime and gpt-4o-mini-realtime. The replacements are gpt-realtime-2.1 and gpt-realtime-2.1-mini. | [deprecations page](https://developers.openai.com/api/docs/deprecations) |
| Feb 26, 2027 | OpenAI removes whisper-1 and the gpt-4o transcription models. | [deprecations page](https://developers.openai.com/api/docs/deprecations) |

## How to read the product tables

- **Product.** The name links to the vendor's docs or its main official page. A
  label in italics follows the name when a product is not plainly active:
  *acquired*, *renamed*, *deprecated*, *shut down*, *dormant* (an open-source
  project with no pushes in several months and no deprecation notice, which is a
  signal to check and not a verdict) or *status unverified* (the status could
  not be confirmed either way).
- **Price (headline).** The price as the vendor showed it on September 30, 2026,
  shortened. A price with a number links to the page where it was read. "Sales
  only" means there is no public price. "No vendor price" means open weights
  with nothing to buy from the vendor. "Unverified" means no price was seen.
  Check what each price includes: telephony, model and compute costs are often
  extra.
- **Open source.** "Yes" means the core product's source is published under a
  license that was read. "Partly" means open code around a closed hosted
  service, open weights with conditions, or paid licenses around open code. "No"
  means proprietary. "Unverified" means it could not be determined.
- **MCP server.** MCP lets a coding agent use a vendor's tools or documentation.
  "Official, hosted" means the vendor runs a server. "Official, local" means the
  vendor publishes one you run yourself. "Docs only" means the server only
  searches documentation. "Community only" means only third parties publish one.
  "None found" means the search found none. "Not checked" means no search was
  run or the search could not settle it. "(vendor-wide)" means the server covers
  the vendor's whole platform, not just this product. The link goes to a docs or
  GitHub page about the server where one exists.
- Each product appears once, under its main category, even if it also fits
  another.

## A. Managed voice-agent platforms

Platforms that run the voice agent for you, from developer-first hosts to
enterprise contact center suites.

### Developer and no-code platforms

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Vapi](https://docs.vapi.ai/quickstart/introduction) | Hosted platform where you pick the speech, language model and phone providers for each agent. | [$0.05/min hosting fee; provider costs extra](https://vapi.ai/pricing) | No | [Official, hosted](https://github.com/VapiAI/mcp-server) |
| [Retell AI](https://docs.retellai.com/general/introduction) | Hosted platform for voice and chat agents, with built-in phone numbers, tools and call analytics. | [$0.07-$0.31/min; telephony $0.015/min on Retell numbers](https://www.retellai.com/pricing) | No | [Official, hosted](https://docs.retellai.com/get-started/mcp-server) |
| [Bland AI](https://docs.bland.ai/welcome-to-bland) | Hosted platform with one per-minute rate that covers the language model, speech-to-text and text-to-speech. | [$0.14/min Start, $0.12/min Build; telephony extra](https://www.bland.ai/pricing) | No | [Official, hosted](https://docs.bland.ai/integrations/mcp/overview) |
| [Synthflow](https://docs.synthflow.ai/getting-started) | Hosted phone agent platform with an agent editor, an API and contact center links, sold on annual contracts. | [Sales only; contracts start at $30,000 annually](https://synthflow.ai/pricing) | No | [Official, hosted](https://docs.synthflow.ai/mcp-server) |
| [ElevenAgents (ElevenLabs Agents)](https://elevenlabs.io/docs/eleven-agents/overview) | ElevenLabs' hosted platform for voice, chat and text agents, built on its own speech models. | [Plans $0 to $990/month; extra minutes $0.080/min](https://elevenlabs.io/pricing/agents) | No | [Official, hosted](https://elevenlabs.io/mcp) |
| [Voiceflow](https://www.voiceflow.com/docs/documentation/introduction) | Visual builder for chat and voice agents, with a knowledge base, tools and analytics. | [Sales only; docs list phone usage at $0.05/min](https://www.voiceflow.com/docs/documentation/account-management/billing/credits-pricing-table) | No | [Official, hosted](https://www.voiceflow.com/docs/mcp) |
| [Air AI (Air.ai)](https://www.ftc.gov/news-events/news/press-releases/2026/03/air-ai-its-owners-will-be-banned-marketing-business-opportunities-settle-ftc-charges-company-misled) *(status unverified)* | Sold as AI phone agents plus a resale package. The FTC sued in Aug 2025; a stipulated settlement order was signed on March 30, 2026, in which the defendants neither admitted nor denied the allegations. | No current public price list | Unverified | None found |
| [Cartesia Line and Managed Agents](https://docs.cartesia.ai/agents/introduction) | Hosted agents on Cartesia speech models, plus the open Line SDK (Cartesia stops hosting Line code Dec 1, 2026). | [$0.06/min agent calling (+$0.014/min telephony)](https://www.cartesia.ai/pricing) | Partly (Line SDK is Apache-2.0) | [Official, hosted](https://github.com/cartesia-ai/cartesia-mcp) |
| [Vogent](https://docs.vogent.ai/introduction) *(acquired by Aircall, May 6, 2026)* | Platform for building and running voice agents through a dashboard and API, with SIP number import. | [$0.09/min standard voices, $0.14/min premium](https://docs.vogent.ai/platform-overview/billing) | No | None found |
| [Dasha (Dasha BlackBox)](https://blackbox.dasha.ai/docs/) | Hosted voice agent API with a dashboard builder, SIP or Twilio phone links and call analytics. | [Sales only; Growth plan from $0.08/min](https://dasha.ai/pricing) | No | None found |
| [Telnyx AI Assistants](https://developers.telnyx.com/docs/inference/ai-assistants/no-code-voice-assistant) | Voice and chat agents that run on Telnyx's own phone network. | [$0.05/min voice engine; language model billed per token](https://telnyx.com/pricing/voice-ai-agents) | No | [Official, hosted](https://developers.telnyx.com/docs/development/mcp/remote-mcp) |
| [Twilio ConversationRelay](https://www.twilio.com/docs/voice/conversationrelay) | Twilio handles the call and the speech, and sends text to your server over a WebSocket. | [From $0.07/min; voice costs billed separately](https://www.twilio.com/en-us/products/conversational-ai/pricing) | No | [Docs only](https://www.twilio.com/docs/ai/mcp) |
| [Deepgram Voice Agent API](https://developers.deepgram.com/docs/voice-agent) | One WebSocket API that runs speech-to-text, a language model and text-to-speech for an agent. | [Standard $0.075/min; Advanced $0.163/min; BYO LLM and TTS $0.050/min](https://deepgram.com/pricing) | No | [Official, local](https://github.com/deepgram/mcp) |
| [Voximplant Voice AI (VoxEngine)](https://docs.voximplant.ai/capabilities/features) | Serverless platform where JavaScript scenarios link phone, SIP and WebRTC calls to realtime voice models. | [$0.004/min Voice AI connectivity, plus telephony](https://voximplant.ai/pricing) | No | [Docs only](https://docs.voximplant.ai/_mcp/server) |
| [Bolna](https://www.bolna.ai/docs) | Open-source Python framework for voice agents, plus a hosted platform built on it. | [Hosted from 6.00 cents/min](https://www.bolna.ai/pricing) | Partly (framework is MIT; hosted APIs are closed) | [Official, hosted](https://mcp.bolna.ai) |
| [Millis AI](https://docs.millis.ai/introduction) *(status unverified)* | Hosted platform that links your choice of speech, model and voice providers, with SIP support. | [$0.02/min base, plus model, voice and speech costs](https://docs.millis.ai/pricing) | No | None found |

### Enterprise customer service platforms

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Regal](https://developer.regal.ai/docs/what-is-regal) | Contact center platform for AI agents on inbound and outbound calls, SMS and chat. | [Sales only](https://www.regal.ai/pricing) | No | [Official, hosted](https://developer.regal.ai/docs/regal-mcp) |
| [Sierra](https://sierra.ai/product/channels) | Customer service agent for chat, SMS, email and voice, sold to large brands through sales. | [Sales only (outcome-based)](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents) | No | None found |
| [Decagon](https://decagon.ai/product/voice) | Customer support agents for chat, email and voice, sold to enterprises. | [Sales only](https://decagon.ai/) | No | None found |
| [PolyAI](https://polyai.github.io/adk/) | Voice agent platform for customer service, sold to large contact centers. | [Sales only (priced per minute)](https://poly.ai/pricing) | No | [Official, hosted](https://docs.poly.ai/mcp/overview) |
| [Parloa](https://www.parloa.com/platform/) | Enterprise platform to build, test and monitor voice and chat agents for customer service. | [Sales only](https://www.parloa.com/platform/pricing/) | No | None found |

### Cloud provider agent builders

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Amazon Connect Customer (agentic voice)](https://docs.aws.amazon.com/connect/latest/adminguide/what-is-amazon-connect.html) | AWS contact center with a no-code builder for AI agents on voice, chat, email and SMS. | [$0.038 per voice minute, plus telephony rates](https://aws.amazon.com/products/connect/customer/pricing/) | No | Not checked |
| [Google Conversational Agents (Dialogflow CX)](https://docs.cloud.google.com/dialogflow/cx/docs/basics) | Google Cloud agent builder with fixed-flow and generative editions, for chat and voice. | [Voice $0.001/sec (Flows), $0.002/sec (Playbooks)](https://cloud.google.com/dialogflow/pricing) | No | Not checked |
| [Microsoft Copilot Studio (voice agents)](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-messages-management) | Microsoft low-code agent builder; voice agents are billed in Copilot Credits. | [10, 35 or 75 Copilot Credits/min; pack $200.00/month](https://www.microsoft.com/en-us/microsoft-365-copilot/pricing/copilot-studio) | No | Not checked |

## B. Speech-to-speech and realtime models

Single-model voice APIs that take audio in and return audio out, plus open
models you can run yourself.

### Hosted realtime voice APIs

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [OpenAI Realtime API (gpt-realtime)](https://developers.openai.com/api/docs/guides/realtime) | OpenAI's speech-to-speech API: audio in, audio out, over WebRTC, WebSocket or SIP. | [gpt-realtime-2.1 audio $32.00 in, $64.00 out per 1M tokens](https://developers.openai.com/api/docs/pricing) | No | [Docs only](https://developers.openai.com/learn/docs-mcp) |
| [OpenAI GPT-Live (gpt-live-1)](https://developers.openai.com/api/docs/guides/live) | Full-duplex voice model that listens and speaks at once and leaves reasoning to a backend you choose. | [$0.05/min, billed per second; backend extra](https://developers.openai.com/api/docs/pricing) | No | [Docs only](https://developers.openai.com/learn/docs-mcp) |
| [Google Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api) | Google's streaming audio-to-audio API for Gemini models, on the Gemini API or Google Cloud. | [Paid tier: audio in $0.005/min, audio out $0.018/min](https://ai.google.dev/gemini-api/docs/pricing) | No | [Docs only](https://developers.google.com/knowledge/mcp) (vendor-wide) |
| [Amazon Nova Sonic / Nova 2 Sonic](https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-conversational-speech.html) | Amazon's speech-to-speech model on Bedrock, with streaming audio and tool calling. | [Nova 2 Sonic speech: $3.00 in, $12.00 out per 1M tokens](https://aws.amazon.com/bedrock/pricing/) | No | [Official, hosted](https://github.com/aws/agent-toolkit-for-aws) (vendor-wide) |
| [Azure Voice Live API](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live) | Azure API that bundles speech recognition, a model you choose and text-to-speech in one session. | [Pro native audio: $32 in, $64 out per 1M tokens](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/) | No | [Official, local](https://github.com/microsoft/mcp) (vendor-wide) |
| [xAI Grok Speech to Speech API](https://docs.x.ai/developers/model-capabilities/audio/speech-to-speech) | Realtime voice API from xAI that follows the OpenAI Realtime protocol. | [$0.08/min ($4.80/hour)](https://docs.x.ai/developers/pricing) | No | [Docs only](https://docs.x.ai/developers/docs-mcp) |
| [Hume EVI (EVI 3, EVI 4-mini)](https://dev.hume.ai/docs/speech-to-speech-evi/overview) | Hosted realtime voice API that picks up tone of voice and replies with expressive speech. | [EVI 3 overage $0.06/min (Pro) to $0.04/min (Business)](https://www.hume.ai/pricing) | No | [Docs only](https://dev.hume.ai/docs/integrations/mcp) |
| [Inworld Realtime API](https://docs.inworld.ai/realtime/overview) | OpenAI Realtime-compatible API that joins Inworld speech, a model of your choice and Inworld voices. | [Billed on usage; TTS-2 $25 per 1M characters](https://inworld.ai/pricing) | No | [Official, local](https://docs.inworld.ai/tts/resources/inworld-cli) |
| [Alibaba Qwen Omni](https://www.alibabacloud.com/help/en/model-studio/realtime) | Multimodal realtime API on Alibaba Cloud, plus open Qwen3-Omni weights. | [Audio $0.93 in, $1.87 out per 1M tokens (Singapore)](https://www.alibabacloud.com/help/en/model-studio/model-pricing) | Partly (Qwen3-Omni weights are Apache-2.0) | [Official, hosted](https://api.alibabacloud.com/mcp) (vendor-wide) |
| [StepFun StepAudio](https://platform.stepfun.com/docs/zh/guides/models/stepaudio-3-realtime) | Realtime voice API for Chinese-language agents, plus the open Step-Audio 2 mini model. | [stepaudio-2.5-realtime: 10 CNY in, 70 CNY out per 1M tokens](https://platform.stepfun.com/docs/zh/guides/pricing/details) | Partly (Step-Audio 2 mini weights are Apache-2.0) | None found |
| [Zhipu AI GLM-Realtime](https://docs.bigmodel.cn/cn/guide/models/sound-and-video/glm-realtime) *(status unverified)* | Realtime audio and video call model on Zhipu's BigModel platform, priced per minute. | [Flash 0.18 CNY/min audio; Air 0.3 CNY/min audio](https://docs.bigmodel.cn/cn/guide/models/sound-and-video/glm-realtime) | Partly (GLM-4-Voice code is Apache-2.0; API is closed) | None found |
| [Ultravox](https://docs.ultravox.ai/overview) *(acquired by Inworld, announced Sept 30, 2026)* | Open-weight speech model plus a hosted realtime platform for voice agents. | [$0.05/min after 30 free minutes](https://www.ultravox.ai/pricing) | Partly (MIT model weights) | None found |
| [Mistral Voxtral (Realtime, Transcribe 2, Small, TTS)](https://docs.mistral.ai/studio/audio/overview) | Mistral audio models for a cascade: streaming speech-to-text, an audio-input model and text-to-speech. | [Realtime $0.006/min; TTS $16 per M characters](https://docs.mistral.ai/models/voxtral-mini-transcribe-realtime-26-02) | Partly (some weights Apache-2.0; TTS is CC BY-NC 4.0) | [Official, hosted](https://docs.mistral.ai/resources/mcp) |

### Open speech-to-speech models you run yourself

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Kyutai Moshi](https://github.com/kyutai-labs/moshi) | Open full-duplex speech-to-speech model from a research lab; its model card says it cannot use tools. | Free to self-host (open weights) | Yes (MIT and Apache-2.0 code; CC-BY 4.0 weights) | None found |
| [Kyutai Unmute](https://github.com/kyutai-labs/unmute) | Open-source voice stack that wraps any text model in Kyutai speech-to-text and text-to-speech. | Free to self-host | Yes (MIT code; CC-BY 4.0 speech weights) | None found |
| [Sesame (CSM-1B and Sesame agents)](https://github.com/SesameAILabs/csm) | Consumer voice agents plus CSM-1B, an open speech generation model. No developer API found. | Free during preview; no API price published | Partly (CSM-1B weights are Apache-2.0) | None found |
| [NVIDIA PersonaPlex](https://github.com/NVIDIA/personaplex) | Open 7B full-duplex speech-to-speech model, tuned from Moshi, with text and voice prompts for persona. | Free to self-host | Partly (MIT code; NVIDIA Open Model License weights) | None found |
| [NVIDIA NemotronLabs VoiceChat 11B](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-VoiceChat-11B) | Open 11B full-duplex speech model with tool calling; needs NVIDIA data center GPUs. | Free to self-host | Yes (Apache-2.0 code; OpenMDW-1.1 weights) | None found |
| [Liquid AI LFM2.5-Audio](https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B) | Small open 1.5B audio model for on-device speech chat, speech-to-text and text-to-speech. | [Free to self-host under $10M annual revenue](https://huggingface.co/LiquidAI/LFM2.5-Audio-1.5B) | Partly (custom license with a $10M revenue limit) | [Docs only](https://docs.liquid.ai/mcp) |

## C. Orchestration frameworks

Code frameworks and runtimes that connect the speech, model and phone pieces,
most of them open source.

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [LiveKit Agents (with LiveKit Cloud)](https://docs.livekit.io/agents/) | Framework for realtime voice agents in Python and Node.js, plus LiveKit Cloud hosting and phone numbers. | [Build $0 (1,000 min); Ship from $50/mo; Scale from $500/mo](https://livekit.com/pricing) | Yes (Apache-2.0) | [Docs only](https://docs.livekit.io/mcp) |
| [Pipecat (with Pipecat Cloud)](https://docs.pipecat.ai/overview/introduction) | Python framework that builds voice agents as pipelines, plus Daily's Pipecat Cloud hosting. | [Free framework; Pipecat Cloud from $0.01/min active](https://www.daily.co/pricing/pipecat-cloud/) | Yes (BSD-2-Clause) | [Official, local](https://github.com/pipecat-ai/pipecat-mcp-server) |
| [TEN Framework and TEN Agent](https://docs.agora.io/en/ai/ten-agent/framework-overview) | Open framework for realtime voice agents with a graph-based runtime; Agora's hosted engine is built on it. | Free; hosted option is the Agora engine below | Partly (Apache-2.0 with extra conditions) | None found |
| [Vocode](https://docs.vocode.dev/welcome) *(acquired; last code push Nov 15, 2024)* | Python library for voice agents. Its hosted API hostnames no longer resolve; the docs still describe it. | Free library; hosted price unverified | Yes (MIT) | None found |
| [Agora Conversational AI Engine (with Agent Studio)](https://docs.agora.io/en/ai) | Agora's hosted platform for voice agents, run through a REST API or the no-code Agent Studio. | [$0.10/min audio task; first 300 minutes free](https://docs.agora.io/en/ai/reference/pricing) | No | [Docs only](https://docs.agora.io/en/introduction/agora-mcp) |
| [OpenAI Agents SDK (realtime and voice agents)](https://openai.github.io/openai-agents-python/realtime/transport/) | Python and TypeScript SDKs with two voice paths: realtime agents and a chained speech pipeline. | Free SDK; OpenAI model usage billed separately | Yes (MIT) | [Docs only](https://developers.openai.com/learn/docs-mcp) (vendor-wide) |
| [Google Agent Development Kit (ADK)](https://adk.dev/live/index) | Agent framework whose live and voice agents run on Gemini Live; the docs mark that feature Experimental. | Free framework; Gemini usage billed by Google | Yes (Apache-2.0) | [Docs only](https://developers.google.com/knowledge/mcp) |
| [Vision Agents (Stream)](https://visionagents.ai/) | Python framework for voice and video agents that join calls over Stream's edge network. | [Free framework; Stream Video $0.30 per 1,000 audio participant minutes](https://getstream.io/video/pricing/) | Yes (Apache-2.0) | None found |
| [VideoSDK AI Agents (now Zero Runtime AI)](https://docs.zeroruntime.ai/introduction) *(renamed to Zero Runtime AI)* | Managed runtime: your agent code runs in your process and the vendor runs the realtime pipeline. | [Agent Cloud $0.005/min; $20 free credits](https://zeroruntime.ai/pricing) | No | [Docs only](https://docs.videosdk.live/ai-tools/mcp-server) |
| [jambonz](https://docs.jambonz.org/welcome) | Open-source telephony gateway that connects SIP carriers and WebRTC to speech and language services. | [Cloud $8/session (5-249 sessions), monthly; self-hosted $7/session](https://jambonz.org/pricing) | Partly (MIT code; self-hosting needs a paid license key after a one-month trial) | [Docs only](https://github.com/jambonz/mcp-server) |
| [Dograh](https://docs.dograh.com/getting-started) | Voice agent platform with a visual workflow builder; self-host it or use the hosted cloud. | [Cloud from 1 cent/min platform fee; self-host free](https://www.dograh.com/pricing) | Yes (BSD-2-Clause) | [Official, hosted](https://docs.dograh.com/integrations/mcp) |
| [Hugging Face speech-to-speech](https://github.com/huggingface/speech-to-speech) | Open voice pipeline that serves the OpenAI Realtime protocol from your own hardware. | Free; you supply hardware | Yes (Apache-2.0) | [Official, hosted](https://huggingface.co/mcp) (vendor-wide) |
| [Fonoster](https://docs.fonoster.com/introduction) | Open-source Twilio alternative with voice verbs and LLM-driven Autopilot apps. | [Free plan 30 min/month; self-host free](https://fonoster.com/) | Yes (MIT) | None found |
| [Daily Bots](https://www.daily.co/products/pipecat-cloud/) *(status unverified)* | Former Daily product. Its old addresses now redirect to Pipecat Cloud; no shutdown notice was found. | None found; see Pipecat Cloud | Unverified | None found |

## D. Streaming speech-to-text

Services and models that turn a caller's speech into text while the caller is
still talking.

### Hosted speech-to-text services

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Deepgram Nova-3 (streaming)](https://developers.deepgram.com/docs/models-languages-overview) | Deepgram's general streaming speech-to-text model. It has no built-in turn detection. | [Nova-3 streaming $0.0048/min (promo; regular $0.0077/min)](https://deepgram.com/pricing) | No | [Official, local](https://github.com/deepgram/mcp) |
| [Deepgram Flux](https://developers.deepgram.com/docs/flux/quickstart) | Deepgram streaming speech-to-text that also signals when a speaker's turn starts and ends. | [Flux English $0.0065/min (promo; regular $0.0077/min)](https://deepgram.com/pricing) | No | [Official, local](https://github.com/deepgram/mcp) |
| [AssemblyAI streaming speech-to-text](https://www.assemblyai.com/docs/streaming/select-the-speech-model) | Streaming speech-to-text over a WebSocket, with turn-based transcripts and end-of-turn detection. | [Universal-Streaming $0.15/hr; Universal-3.6 Pro $0.45/hr](https://www.assemblyai.com/pricing) | No | [Official, local](https://github.com/AssemblyAI/assemblyai-mcp) |
| [Speechmatics real-time speech-to-text](https://docs.speechmatics.com/speech-to-text/models) | Hosted speech-to-text with a Realtime API and a separate Agent STT API for voice agents. | [Real-time Standard $0.24/hr; Enhanced $0.43/hr (Pro column)](https://www.speechmatics.com/pricing) | No | Community only |
| [Soniox speech-to-text](https://soniox.com/docs/stt/rt/real-time-transcription) | Hosted real-time and async speech-to-text with semantic endpointing and in-call translation. | [Real-time $2.00 per 1M audio tokens (page says about $0.12/hour)](https://soniox.com/pricing) | No | Docs only |
| [Gladia real-time speech-to-text (Solaria-1)](https://docs.gladia.io/chapters/introduction/models) | Hosted speech-to-text with a live WebSocket endpoint and support for 100+ languages. | [Starter $0.75/hr; Growth 'as low as $0.25/hr' with commitment](https://www.gladia.io/pricing) | No | [Official, local](https://github.com/gladiaio/gladia-mcp) |
| [ElevenLabs Scribe v2 and Scribe v2 Realtime](https://elevenlabs.io/docs/overview/capabilities/speech-to-text) | ElevenLabs speech-to-text: Scribe v2 for files and Scribe v2 Realtime for streaming. | [Scribe v2 Realtime $0.39/hour; Scribe v2 (batch) $0.22/hour](https://elevenlabs.io/pricing/api) | No | [Official, hosted](https://elevenlabs.io/mcp) |
| [Cartesia Ink (Ink 2 and Ink-Whisper)](https://docs.cartesia.ai/build-with-cartesia/stt/latest) | Cartesia speech-to-text: ink-2 for streaming with turn events, and the older ink-whisper. | [ink-2: 3 credits/sec; ink-whisper: 1 credit/sec](https://cartesia.ai/pricing) | No | [Official, hosted](https://github.com/cartesia-ai/cartesia-mcp) |
| [OpenAI transcription models](https://developers.openai.com/api/docs/guides/realtime-transcription) | OpenAI speech-to-text models, from streaming transcription to file and token-priced models. | [Streaming models $0.017/min; gpt-transcribe $0.0045/min](https://developers.openai.com/api/docs/pricing) | No | [Docs only](https://developers.openai.com/learn/docs-mcp) |
| [Rev AI streaming speech-to-text](https://docs.rev.ai/api/streaming/) | Rev AI speech-to-text API with streaming over a WebSocket, plus the Reverb model. | [Reverb $0.20/hour (English); $0.30/hour foreign language](https://www.rev.ai/pricing) | No | Not checked |
| [Sarvam Saaras](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview) | Speech-to-text for 22 Indian languages plus English, with streaming and batch endpoints. | [30.00 INR/hour for real-time, streaming and batch](https://www.sarvam.ai/api-pricing) | No | Not checked |

### Cloud provider speech-to-text

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Google Cloud Speech-to-Text v2 (Chirp)](https://docs.cloud.google.com/speech-to-text/docs/models/chirp-3) | Google Cloud managed speech recognition with gRPC streaming and the Chirp 2 and Chirp 3 models. | [$0.016/min (0-500,000 min/month), falling to $0.004/min above 2M](https://cloud.google.com/speech-to-text/pricing) | No | [Docs only](https://developers.google.com/knowledge/mcp) |
| [Azure Speech (real-time speech to text)](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text) | Microsoft's speech service. Real-time transcription runs through the Speech SDK, CLI or REST. | [Standard real-time $1/hour; batch $0.18/hour (East US)](https://azure.microsoft.com/en-us/pricing/details/speech/) | No | [Official, local](https://github.com/microsoft/mcp) |
| [Amazon Transcribe (streaming)](https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html) | AWS managed speech recognition with streaming over SDKs, HTTP/2 and WebSockets. | [Standard streaming $0.01/min (US East)](https://aws.amazon.com/transcribe/pricing/) | No | [Official, hosted](https://github.com/aws/agent-toolkit-for-aws) (vendor-wide) |

### Open speech-to-text models you run yourself

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [OpenAI Whisper (open weights)](https://github.com/openai/whisper) | Open multilingual speech recognition model. It transcribes files, so it is not a streaming model. | No vendor price (open weights) | Yes (MIT) | [Docs only](https://developers.openai.com/learn/docs-mcp) |
| [NVIDIA Parakeet](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3) | NVIDIA open speech recognition models; one checkpoint does English streaming with end-of-utterance. | No vendor price (open weights) | Partly (CC-BY-4.0 and NVIDIA Open Model License, by checkpoint) | None found |
| [NVIDIA Nemotron ASR Streaming](https://huggingface.co/nvidia/nemotron-3.5-asr-streaming-0.6b) | NVIDIA open streaming speech recognition models: English, and 40 language-locales in the 3.5 model. | No vendor price (open weights) | Partly (NVIDIA Open Model License; OpenMDW-1.1 for 3.5) | None found |
| [NVIDIA Canary](https://huggingface.co/nvidia/canary-1b-v2) | NVIDIA open models for file transcription and speech translation; no streaming mode documented. | No vendor price (open weights) | Partly (CC-BY-4.0) | None found |
| [Kyutai STT](https://github.com/kyutai-labs/delayed-streams-modeling) | Open streaming speech-to-text models with a built-in semantic VAD, for English and French. | No vendor price (open weights) | Partly (MIT and Apache-2.0 code; CC-BY 4.0 weights) | None found |
| [Moonshine Voice](https://moonshine-voice.readthedocs.io/en/latest/) | On-device speech-to-text toolkit with streaming models, for phones, desktops and Raspberry Pi. | No vendor price (open weights) | Yes (MIT; a community license covers some legacy models) | None found |
| [Mistral Voxtral open weights](https://docs.mistral.ai/studio/audio/speech_to_text) | Mistral open-weight streaming transcription model for 13 languages, to self-host or call hosted. | Unverified here; see the Mistral Voxtral row in section B | Yes (Apache-2.0 weights) | [Official, hosted](https://docs.mistral.ai/resources/mcp) |
| [Qwen3-ASR](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) | Open speech recognition models with language ID for 30 languages and 22 Chinese dialects. | No vendor price (open weights) | Yes (Apache-2.0) | [Official, hosted](https://api.alibabacloud.com/mcp) (vendor-wide) |

### Hosted open speech-to-text models

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Groq (hosted Whisper)](https://console.groq.com/docs/speech-to-text) | Groq's hosted API for OpenAI's Whisper models. It takes files or URLs, not live streaming. | [whisper-large-v3-turbo $0.04/hour; whisper-large-v3 $0.111/hour](https://console.groq.com/docs/speech-to-text) | No | [Official, local](https://github.com/groq/groq-mcp-server) |
| [Together AI (hosted open speech-to-text)](https://www.together.ai/pricing) | Hosted open speech models (Whisper, Parakeet, Nemotron), including streaming variants. | [Whisper Large v3 $0.0015/min; streaming variant $0.0035/min](https://www.together.ai/pricing) | No | [Docs only](https://docs.together.ai/docs/agent-skills) |

## E. Low-latency text-to-speech

Services and models that turn the agent's text into speech fast enough to feel
like conversation.

### Hosted voice specialists

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [ElevenLabs text-to-speech models](https://elevenlabs.io/docs/overview/models) | Hosted text-to-speech API with several model families, from expressive long-form to low-latency. | [Per 1K chars: v4 $0.08 (promo $0.022 until Oct 12); Flash $0.04](https://elevenlabs.io/pricing/api) | No | [Official, hosted](https://elevenlabs.io/mcp) |
| [Cartesia Sonic](https://docs.cartesia.ai/build-with-cartesia/tts-models/latest) | Hosted streaming text-to-speech API over HTTP, SSE and WebSocket, billed in credits. | [About 1 credit per character; plans $0 to $299/mo](https://cartesia.ai/pricing) | No | [Official, hosted](https://github.com/cartesia-ai/cartesia-mcp) |
| [Rime TTS (Coda, Mist v3)](https://docs.rime.ai/docs/models) | Hosted and self-hostable text-to-speech API with two model lines, Coda and Mist v3. | [Per 1K chars on Starter: Coda $0.05, Mist v3 $0.03](https://www.rime.ai/pricing) | No | [Official, hosted](https://mcp.rime.ai) |
| [Deepgram TTS (Flux TTS, Aura-2, Aura-1)](https://developers.deepgram.com/docs/tts-models-languages-overview) | Deepgram text-to-speech with three model families, billed per 1,000 input characters. | [Per 1K chars: Flux TTS $0.0450, Aura-2 $0.030, Aura-1 $0.0150](https://deepgram.com/pricing) | No | [Official, local](https://github.com/deepgram/mcp) |
| [Inworld TTS (TTS-2, TTS-2 Flash)](https://docs.inworld.ai/tts/tts-models) | Hosted realtime text-to-speech with two models, TTS-2 and the lower-latency TTS-2 Flash. | [TTS-2 $25 per 1M characters; TTS-2 Flash $15 per 1M characters](https://inworld.ai/pricing) | No | [Official, local](https://docs.inworld.ai/tts/resources/inworld-cli) |
| [Hume Octave](https://dev.hume.ai/docs/text-to-speech-tts/overview) | Text-to-speech built on Hume's Octave model, with voice design, cloning and conversion. | [Plans $0 to $500/mo; Octave 1 overage $0.15 to $0.05 per 1,000 chars](https://www.hume.ai/pricing) | No | [Official, local](https://github.com/HumeAI/mcp-server-hume) |
| [OpenAI text-to-speech](https://developers.openai.com/api/docs/guides/text-to-speech) | OpenAI speech endpoint with three models; gpt-4o-mini-tts takes style instructions. | [tts-1 $15.00 per 1M characters; tts-1-hd $30.00 per 1M characters](https://developers.openai.com/api/docs/pricing) | No | [Docs only](https://developers.openai.com/learn/docs-mcp) |
| [Resemble AI](https://docs.resemble.ai/voice-generation/text-to-speech) | Hosted voice API (text-to-speech, speech-to-speech, cloning), plus the open-source Chatterbox model. | [$0.00067/second of audio (Flex); $0.0005/second (Team)](https://app.resemble.ai/billing/api/v1/plans) | Partly (Chatterbox is MIT; the hosted API is not) | [Official, hosted](https://github.com/resemble-ai/resemble-mcp) |
| [Murf Falcon and Gen 2](https://murf.ai/api/docs/introduction/overview) | Hosted text-to-speech API with Falcon 2 for voice agents and Gen 2 for studio voiceover. | [Falcon 2 $0.01 per 1000 characters; Gen 2 $0.03 per 1000 characters](https://murf.ai/pricing) | No | [Official, local](https://github.com/murf-ai/murf-mcp) |
| [Smallest.ai Lightning](https://docs.smallest.ai/) | Hosted streaming text-to-speech API from a vendor that also sells a voice agent platform. | [Lightning V3.1 $0.175 per 10K characters](https://smallest.ai/pricing/models) | No | [Official, local](https://github.com/smallest-inc/mcp-server) |
| [Fish Audio API and Fish Speech](https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits) | Hosted text-to-speech, speech-to-text and voice design API, plus open Fish Speech weights. | [$15.00 per million UTF-8 bytes of input text](https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits) | Partly (research license; some weights CC-BY-NC-SA-4.0) | [Official, hosted](https://docs.fish.audio/overview/mcp) |
| [SpeechifyAI API (Simba)](https://docs.speechify.ai/build/guides/welcome) | Hosted streaming text-to-speech API with voice cloning and SSML; not the Speechify reading app. | [Plans $0 to $499/month; extra characters $10 to $6 per 1M](https://speechify.ai/) | No | [Docs only](https://docs.speechify.ai/build/guides/get-started/connect-mcp) |

### Cloud provider text-to-speech

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Google Cloud Text-to-Speech](https://cloud.google.com/text-to-speech/docs/chirp3-hd) | Google Cloud text-to-speech with Chirp 3: HD voices and Gemini-TTS, plus streaming synthesis. | [Chirp 3: HD voices $30 per 1 million characters](https://cloud.google.com/text-to-speech/pricing) | No | [Docs only](https://developers.google.com/knowledge/mcp) |
| [Azure Speech text to speech](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech) | Azure text-to-speech with Neural and Neural HD voices, custom voices and a WebSocket endpoint. | [Neural / Neural HD Flash $15 per 1M characters](https://azure.microsoft.com/en-us/pricing/details/speech/) | No | [Official, local](https://github.com/microsoft/mcp) |
| [Amazon Polly](https://docs.aws.amazon.com/polly/latest/dg/generative-voices.html) | AWS text-to-speech with four engines; its streaming API takes text in pieces over HTTP/2. | [Per 1M characters: Standard $4.00, Neural $16.00, Generative $30](https://aws.amazon.com/polly/pricing/) | No | [Official, hosted](https://github.com/aws/agent-toolkit-for-aws) (vendor-wide) |

### Open text-to-speech models you run yourself

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Kokoro-82M](https://github.com/hexgrad/kokoro/blob/main/README.md) *(dormant; no pushes since Aug 6, 2025)* | Small open text-to-speech model (82 million parameters) with a Python library. | Free to self-host (compute not included) | Yes (Apache-2.0) | Community only |
| [Orpheus TTS (Canopy Labs)](https://github.com/canopyai/Orpheus-TTS/blob/main/README.md) *(dormant; no pushes since Dec 5, 2025)* | Open speech generation models from Canopy Labs, with a streaming inference example. | Free to self-host (compute not included) | Yes (Apache-2.0) | None found |
| [Chatterbox (Resemble AI)](https://github.com/resemble-ai/chatterbox/blob/master/README.md) | Open text-to-speech model family from Resemble AI, with voice cloning and watermarking. | Free to self-host (compute not included) | Yes (MIT) | [Official, hosted](https://github.com/resemble-ai/resemble-mcp) |
| [Sesame CSM-1B (open weights)](https://github.com/SesameAILabs/csm/blob/main/README.md) *(dormant; no pushes since May 27, 2025)* | Open 1B conversational speech model that generates speech from text and audio context. | Free to self-host (compute not included) | Yes (Apache-2.0) | None found |
| [Kyutai TTS](https://github.com/kyutai-labs/delayed-streams-modeling/blob/main/README.md) *(dormant; no pushes since Jan 26, 2026)* | Open streaming text-to-speech model with a Rust WebSocket server; it runs Unmute. | Free to self-host (compute not included) | Yes (MIT and Apache-2.0 code; CC-BY-4.0 weights) | None found |
| [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS/blob/main/README.md) *(dormant; no pushes since Mar 17, 2026)* | Open text-to-speech models from the Qwen team; Alibaba Cloud also offers a real-time API. | Free to self-host (compute not included) | Yes (Apache-2.0) | [Official, hosted](https://api.alibabacloud.com/mcp) (vendor-wide) |
| [F5-TTS](https://github.com/SWivid/F5-TTS/blob/main/README.md) | Open flow-matching text-to-speech model; the pretrained weights are non-commercial. | Free to self-host (compute not included) | Partly (MIT code; CC-BY-NC weights) | Not checked |
| [Piper](https://github.com/OHF-Voice/piper1-gpl/blob/main/README.md) | Local neural text-to-speech engine with a CLI, Python and C/C++ APIs and an HTTP server. | Free to self-host (compute not included) | Yes (GPL-3.0) | None found |
| [VibeVoice (Microsoft)](https://github.com/microsoft/VibeVoice/blob/main/README.md) | Microsoft open voice models: realtime text-to-speech, long-form text-to-speech and speech recognition. | Free to self-host (compute not included) | Yes (MIT) | None found |
| [Dia (Nari Labs)](https://github.com/nari-labs/dia/blob/main/README.md) *(dormant; no pushes since Nov 19, 2025)* | Open 1.6B text-to-dialogue model for scripted two-speaker audio; not documented for streaming. | Free to self-host (compute not included) | Yes (Apache-2.0) | Not checked |
| [Higgs Audio (Boson AI)](https://github.com/boson-ai/higgs-audio/blob/main/README.md) | Boson AI text-to-speech models; the v3 weights are research and non-commercial. | Unverified (commercial and hosted prices not checked) | Partly (Apache-2.0 v2 code; v3 weights are research only) | Not checked |
| [Coqui XTTS-v2](https://github.com/idiap/coqui-ai-TTS/blob/dev/README.md) *(deprecated; original repo unmaintained since Aug 2024)* | Multilingual voice-cloning text-to-speech model from Coqui; a community fork is the maintained route. | Free to self-host (compute not included) | Partly (MPL-2.0 code; Coqui Public Model License weights) | Not checked |
| [Zonos-v0.1 (Zyphra)](https://github.com/Zyphra/Zonos/blob/main/README.md) *(dormant; no pushes since Mar 5, 2025)* | Open text-to-speech model for English, Japanese, Chinese, French and German. | Free to self-host (compute not included) | Yes (Apache-2.0) | Not checked |

### Shut down

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [PlayHT / PlayAI](https://docs.play.ht/reference/api-getting-started) *(shut down; Meta acquisition reported July 13, 2025)* | Former text-to-speech API and voice agent platform. The service is shut down. | None (service shut down) | No | None found |
| [LMNT](https://docs.lmnt.com/) *(shut down; site notice appeared between Aug 3 and Sep 1, 2026)* | Former speech generation API. Its website and docs now show only a shutdown message. | None (service shut down) | No | None found |

## F. Telephony and transport

Phone carriers, SIP trunks and real-time networks that carry the call to your
agent.

### Phone networks and programmable voice

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Twilio Programmable Voice (with Media Streams)](https://www.twilio.com/docs/voice/media-streams) | Twilio's voice API for phone, SIP and browser calls; Media Streams sends call audio over a WebSocket. | [US local $0.0140/min out, $0.0085/min in; Media Streams $0.0044/min](https://www.twilio.com/en-us/voice/pricing/us) | No | [Docs only](https://www.twilio.com/docs/ai/mcp) |
| [Telnyx Voice API (Call Control and TeXML)](https://developers.telnyx.com/docs/voice/programmable-voice/voice-api-fundamentals) | Telnyx voice API on Telnyx's own carrier network, with WebSocket media streaming. | [$0.002/min Voice API fee plus SIP trunking per-minute fee](https://telnyx.com/pricing/voice-api) | No | [Official, hosted](https://developers.telnyx.com/docs/development/mcp/remote-mcp) |
| [Vonage Voice API (with SIP Trunking)](https://developer.vonage.com/en/voice/voice-api/overview) | Vonage voice API for phone, SIP, WebRTC and WebSocket calls, plus SIP trunking; owned by Ericsson. | [US domestic PSTN $0.00849/min to call, $0.00485/min to receive](https://www.vonage.com/communications-apis/voice/pricing/) | No | [Official, hosted](https://github.com/Vonage/vonage-mcp-server-documentation) |
| [Plivo Voice API (with Audio Streaming)](https://www.plivo.com/docs/voice-agents/audio-streaming/overview) | Plivo voice API with audio streaming over a WebSocket, built for AI voice agents. | [US local $0.0115/min outbound, $0.0055/min inbound; streaming included](https://www.plivo.com/voice/pricing/us/) | No | [Docs only](https://www.plivo.com/docs/faq/developer-tools/mcp-server) |
| [SignalWire Voice API](https://signalwire.com/docs) | SignalWire voice platform for phone, SIP and WebRTC with a Twilio-compatible API, from the FreeSWITCH team. | [US local inbound $0.00660/min, outbound $0.00800/min](https://signalwire.com/pricing) | Partly (SDKs are MIT; hosted platform is not) | None found |
| [SignalWire AI Agents](https://signalwire.com/docs) | Hosted AI agent runtime on SignalWire's phone network: speech, model and orchestration in one price. | [$0.16/min AI agent runtime, plus voice transport](https://signalwire.com/pricing) | Partly (SDK is MIT; hosted runtime is not) | None found |
| [Bandwidth Programmable Voice (BXML)](https://dev.bandwidth.com/docs/voice/programmable-voice/bxml/startStream) | Voice API from a US carrier, with WebSocket media streaming and OpenAI integration guides. | [US local outbound $0.0100/min, inbound $0.0055/min](https://www.bandwidth.com/pricing/) | No | [Official, local](https://github.com/Bandwidth/mcp-server) |
| [Sinch Voice API](https://developers.sinch.com/docs/voice) | Sinch voice API with WebSocket audio streaming and a relay mode, plus Elastic SIP Trunking. | [PSTN receive $0.008/min; make calls from $0.01/min (US)](https://sinch.com/voice/pricing/) | No | [Official, local](https://github.com/sinch/sinch-mcp-server) |

### SIP trunking

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Twilio Elastic SIP Trunking](https://www.twilio.com/docs/sip-trunking) | Twilio SIP trunking that connects a PBX, SBC or SIP app to the phone network. | [US termination $0.0100/min (48 states); origination local $0.0034/min](https://www.twilio.com/en-us/sip-trunking/pricing/us) | No | [Docs only](https://www.twilio.com/docs/ai/mcp) |
| [Telnyx SIP Trunking (Elastic SIP)](https://developers.telnyx.com/docs/voice/sip-trunking/get-started) | SIP trunks on Telnyx's network, with per-minute rates, inbound channels and numbers. | [Outbound local from $0.005/min; inbound local from $0.0032/min](https://telnyx.com/pricing/elastic-sip) | No | [Official, hosted](https://developers.telnyx.com/docs/development/mcp/remote-mcp) |
| [Plivo Zentrunk (SIP Trunking)](https://plivo.com/docs/sip-trunking/concepts/technical-specifications) | Plivo cloud SIP trunking that connects a PBX or SIP-based agent platform to the phone network. | [US outbound local from $0.0046/min; inbound local $0.0028/min](https://www.plivo.com/sip-trunking/pricing/us/) | No | [Docs only](https://www.plivo.com/docs/faq/developer-tools/mcp-server) |
| [Bandwidth SIP Trunking](https://dev.bandwidth.com/docs/voice/sip-trunking/sip-getting-started) | SIP trunking on Bandwidth's own network, with pricing by quote. | [Sales only](https://www.bandwidth.com/pricing/) | No | [Official, local](https://github.com/Bandwidth/mcp-server) |
| [Amazon Chime SDK SIP Media Application](https://docs.aws.amazon.com/chime-sdk/latest/dg/) *(closing to new customers Oct 29, 2026)* | AWS feature for programmable SIP applications. AWS stops taking new customers on Oct 29, 2026. | Unverified (AWS pricing page not opened) | No | [Official, hosted](https://github.com/aws/agent-toolkit-for-aws) (vendor-wide) |

### WebRTC and browser transport

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [LiveKit Cloud telephony (SIP and phone numbers)](https://docs.livekit.io/telephony/) | LiveKit Cloud phone numbers and SIP links that bring calls into rooms where agents run. | [US local inbound $0.01/min after included minutes](https://livekit.com/pricing) | Partly (Apache-2.0 server and SIP code; Cloud telephony is hosted) | [Docs only](https://docs.livekit.io/mcp) |
| [Daily (WebRTC, SIP and PSTN)](https://docs.daily.co/) | Hosted WebRTC with SIP and phone dial-in and dial-out; Daily also maintains Pipecat. | [Audio-only $0.00099 per participant-minute (as low as $0.00036)](https://www.daily.co/pricing/video-sdk/) | No | None found |
| [Agora RTC and Signaling](https://docs.agora.io/en/ai) | Agora's global real-time audio and video network, plus signaling and recording. | [RTC from $0.59 per 1,000 minutes; first 10,000 minutes free](https://www.agora.io/en/pricing/) | No | [Docs only](https://docs.agora.io/en/introduction/agora-mcp) |
| [Cloudflare Realtime (SFU, TURN, RealtimeKit)](https://developers.cloudflare.com/realtime/) | Cloudflare WebRTC network for web voice agents; it is not a phone or SIP provider. | [SFU and TURN $0.05 per GB egress; RealtimeKit audio $0.0005/min](https://developers.cloudflare.com/realtime/realtimekit/pricing/) | No | [Official, hosted](https://github.com/cloudflare/mcp) (vendor-wide) |

## G. Turn detection, VAD and noise

Models and tools that decide when someone has started or stopped speaking, and
clean up the audio before it reaches the agent.

### Voice activity detection

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Silero VAD](https://github.com/snakers4/silero-vad) | Small voice activity detection model that runs on CPU and labels audio chunks as speech or not. | Free (open source) | Yes (MIT) | None found |
| [TEN VAD](https://github.com/TEN-framework/ten-vad) *(status unverified; last commit Feb 2, 2026)* | Small, low-latency VAD from the TEN Framework team, with bindings for several languages. | Free (license conditions apply) | Partly (Apache-2.0 with added conditions) | None found |
| [Picovoice Cobra VAD](https://picovoice.ai/docs/cobra/) | On-device voice activity detection that returns a voice probability per audio frame. | [Sales only for commercial use; free trial](https://picovoice.ai/docs/terms-of-use/) | Partly (wrappers and demos are Apache-2.0; the engine needs an AccessKey) | None found |
| [WebRTC VAD](https://webrtc.googlesource.com/src/+/refs/heads/main/common_audio/vad) *(status unverified; last change not confirmed)* | Classic frame-based voice activity detector from the WebRTC source code. | Free (open source) | Yes (BSD-3-Clause; py-webrtcvad is MIT) | Not checked |

### Turn detection

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [LiveKit turn detector](https://docs.livekit.io/agents/logic/turns/turn-detector/) | LiveKit's end-of-turn model: a newer audio detector, plus an older open text model. | [Free on LiveKit Cloud; 7,500 free v1 requests per month for local testing](https://docs.livekit.io/deploy/admin/quotas-and-limits) | Partly (LiveKit Model License; the older text model has open weights) | [Docs only](https://docs.livekit.io/mcp) |
| [Pipecat Smart Turn](https://docs.pipecat.ai/api-reference/server/utilities/turn-detection/smart-turn-overview) | Open end-of-turn model that reads raw audio once silence is detected; on by default in Pipecat. | Free (open source); no hosted fee | Yes (BSD-2-Clause) | [Official, local](https://github.com/pipecat-ai/pipecat-mcp-server) |
| [Deepgram Flux end-of-turn detection](https://developers.deepgram.com/docs/flux/configuration) | Turn detection built into Deepgram Flux speech-to-text, with tunable thresholds. | [Flux English $0.0065/min (regular $0.0077/min)](https://deepgram.com/pricing) | No | [Official, local](https://github.com/deepgram/mcp) |
| [AssemblyAI streaming turn detection](https://www.assemblyai.com/docs/streaming/turn-detection) | End-of-turn detection inside AssemblyAI streaming speech-to-text, with tunable silence windows. | [Universal-3.6 Pro $0.45/hr; Universal-Streaming $0.15/hr](https://www.assemblyai.com/pricing) | No | [Official, local](https://github.com/AssemblyAI/assemblyai-mcp) |
| [Speechmatics turn detection](https://docs.speechmatics.com/speech-to-text/agent-stt/turn-detection) | Speechmatics end-of-utterance messages and turn events from the Agent STT API. | [Agent STT (Linden 1) $0.16/hr; Real-time Standard $0.24/hr](https://www.speechmatics.com/pricing) | No | Community only |
| [OpenAI Realtime API VAD modes](https://platform.openai.com/docs/guides/realtime-vad) | Turn detection settings of the OpenAI Realtime API: silence-based and meaning-based modes. | No separate price; model usage is priced per model (section B) | No | [Docs only](https://developers.openai.com/learn/docs-mcp) |
| [Gemini Live API activity detection](https://ai.google.dev/gemini-api/docs/live-api/capabilities) | Built-in voice activity detection in the Gemini Live API, on by default and tunable. | No separate price found; model usage is priced per model (section B) | No | [Docs only](https://developers.google.com/knowledge/mcp) (vendor-wide) |
| [TEN Turn Detection](https://github.com/TEN-framework/ten-turn-detection) *(status unverified; last push Dec 26, 2025)* | Text-based turn detection model (Qwen2.5-7B base) with a wait state; English and Chinese. | Free (license conditions apply) | Partly (Apache-2.0 with added conditions) | None found |
| [Namo Turn Detector v1](https://huggingface.co/videosdk-live/Namo-Turn-Detector-v1-Multilingual) *(status unverified; last push Oct 1, 2025)* | Small text-based end-of-turn classifier for 23 languages, run as a quantized ONNX model. | Free (open weights; self-hosted) | Yes (Apache-2.0) | Not checked |
| [Vogent Turn](https://github.com/vogent/vogent-turn) *(status unverified; last push Oct 28, 2025)* | Small end-of-turn model that uses both audio and transcript text. | Free (open code; gated weights with attribution terms) | Partly (Apache-2.0 code; weights under a modified Apache 2.0 license) | None found |
| [Kyutai STT semantic VAD](https://github.com/kyutai-labs/delayed-streams-modeling) *(status unverified; last push Jan 26, 2026)* | A semantic VAD built into Kyutai's streaming speech-to-text model, for English and French. | Free (open code and weights; self-hosted) | Partly (MIT and Apache-2.0 code; CC-BY 4.0 weights) | None found |

### Noise suppression and echo cancellation

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [LiveKit Cloud noise cancellation](https://docs.livekit.io/transport/media/noise-cancellation/) | Option in LiveKit Cloud that filters caller audio with Krisp and ai-coustics models. | [Suppression included; voice isolation $0.0012/min after included minutes](https://livekit.com/pricing) | No | [Docs only](https://docs.livekit.io/mcp) |
| [Krisp VIVA SDK](https://krisp.ai/developers/) | Krisp SDK for voice isolation, turn prediction, interruption prediction and VAD. | [Sales only; via Pipecat Cloud $0.0015/min after 10,000 free minutes](https://krisp.ai/pricing/) | No | None found |
| [ai-coustics SDK](https://docs.ai-coustics.com/) | Licensed SDK with speech enhancement, voice isolation and VAD models that run in your process. | [Startup $135/month billed annually for 100,000 minutes/month](https://ai-coustics.com/pricing) | No (language bindings are Apache-2.0) | [Docs only](https://docs.ai-coustics.com/reference/agents/mcp-server) |
| [Picovoice Koala noise suppression](https://picovoice.ai/docs/koala/) | On-device noise suppression for Linux, macOS, Windows, mobile and browsers. | [Sales only for commercial use; free trial](https://picovoice.ai/docs/terms-of-use/) | Partly (wrappers and demos are Apache-2.0; the engine needs an AccessKey) | None found |
| [RNNoise](https://github.com/xiph/rnnoise) *(status unverified; last commit Feb 22, 2025)* | Small C library for noise suppression using a recurrent neural network. | Free (open source) | Yes (BSD-3-Clause) | None found |
| [WebRTC echo cancellation (AEC3)](https://developer.mozilla.org/en-US/docs/Web/API/MediaTrackConstraints/echoCancellation) *(status unverified; last change not confirmed)* | Echo cancellation from libwebrtc (AEC3) and the browser echoCancellation setting. | Free (open source) | Yes (BSD-3-Clause) | Not checked |
| [Daily noise cancellation](https://docs.daily.co/reference/daily-js/instance-methods/update-input-settings) | Client-side noise cancellation in Daily's SDK, powered by Krisp. | [$0.0002 per participant minute](https://www.daily.co/pricing/video-sdk) | Unverified | None found |

## H. Testing, evals and observability

Tools that run test calls, score conversations and trace what happened on real
calls.

### Voice agent testing tools

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Coval](https://docs.coval.ai/welcome) | Hosted platform that simulates callers against agents, scores production calls and routes calls to reviewers. | [Starter $100/mo; Growth $500/mo; Enterprise 'Starting at $4,500/month'](https://www.coval.ai/pricing) | No | [Official, hosted](https://github.com/coval-ai/mcp-server) |
| [Hamming](https://hamming.ai/) | Hosted platform for automated test calls, red teaming and production monitoring of voice agents. | [Sales only](https://hamming.ai/pricing) | No | Not checked |
| [Cekura](https://docs.cekura.ai/documentation/introduction) | Hosted platform that runs simulated calls against agents, scores them and monitors production calls. | [Pay as you go: $0.25 per voice testing minute; Startup $500/month](https://www.cekura.ai/pricing) | No | [Official, hosted](https://docs.cekura.ai/mcp/overview) |
| [Roark](https://docs.roark.ai) | Hosted platform that simulates callers before launch and scores production calls, with alerts and tracing. | [Pay as you go: simulation $0.15/min plus provider costs; Team $500/mo](https://roark.ai/pricing) | No | [Official, local](https://github.com/roarkhq/mcp-roark-analytics) |
| [Bluejay](https://docs.getbluejay.ai/) | Hosted platform that tests agents with simulated callers, runs red-team attacks and monitors calls. | [Pay-as-you-go $0/mo plus usage; Growth $500/month; Scale $1,000/month](https://getbluejay.ai/pricing) | No | [Official, hosted](https://docs.getbluejay.ai/mcp/overview) |
| [Evalion](https://evalion.ai/) *(status unverified; site now describes a clinical-trials product)* | Current site describes clinical-trial software; a Dec 2024 Braintrust cookbook described a voice agent tester. | Unverified (no public pricing found) | Unverified | Not checked |
| [Future AGI (Simulate)](https://docs.futureagi.com/docs/simulation) | Open-source platform for tracing, evals and guardrails; its Simulate feature runs persona-driven voice tests. | [Free tier (60 voice minutes/month); then voice from $0.08/minute](https://futureagi.com/pricing) | Yes (Apache-2.0) | [Official, hosted](https://docs.futureagi.com/docs/falcon-ai/guides/use-the-mcp-server) |
| [ServiceNow EVA (EVA-Bench)](https://servicenow.github.io/eva/) | Open-source benchmark that runs bot-to-bot spoken conversations against a voice agent and scores them. | No charge (open source); needs your own provider API keys | Yes (MIT) | None found |

### Testing built into a platform or framework

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [LiveKit Agents testing and Simulations](https://docs.livekit.io/testing/) | Testing built into LiveKit Agents: unit tests with LLM judges, plus beta Agent Simulations. | No separate price found for Agent Simulations (beta) | Partly (Apache-2.0 SDK; simulations run on LiveKit Cloud) | [Docs only](https://docs.livekit.io/mcp) |
| [Vapi Evals and Simulations](https://docs.vapi.ai/observability/simulations-overview) | Vapi's built-in evals and AI-tester simulations for assistants and squads. | No separate price; listed as 'Included with every plan' | No | [Official, hosted](https://github.com/VapiAI/mcp-server) |
| [Retell simulation testing and AI QA](https://docs.retellai.com/test/test-overview) | Retell's built-in simulation tests, batch runs, call tests and AI QA scoring of live calls. | [Testing billed at production rates; AI QA $0.10/min after 100 free min](https://docs.retellai.com/test/testing-pricing) | No | [Official, hosted](https://docs.retellai.com/get-started/mcp-server) |
| [ElevenLabs Agent Testing](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing) | Automated tests for ElevenAgents: simulated users, reply checks and tool-call checks. | Unverified (no separate price found) | No | [Official, hosted](https://elevenlabs.io/mcp) |
| [Pipecat Evals and debugging tools](https://docs.pipecat.ai/pipecat/evals/overview) | Pipecat's built-in evals with simulated callers, plus debugging tools such as Whisker and Tail. | No charge (open source) | Yes (BSD-2-Clause) | [Official, local](https://github.com/pipecat-ai/pipecat-mcp-server) |

### General LLM tracing and evals

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [Langfuse](https://langfuse.com/docs/observability/features/multi-modality) *(acquired by ClickHouse, announced Jan 16, 2026)* | Open-source LLM tracing and evaluation platform that voice teams use through OpenTelemetry. | [Hobby free (50k units/mo); Core $29/month; Pro $199/month](https://langfuse.com/pricing) | Yes (MIT, except ee/ folders) | [Docs only](https://langfuse.com/docs/docs-mcp) |
| [Braintrust](https://www.braintrust.dev/docs/integrations/agent-frameworks/livekit-agents) | Hosted platform for tracing, evals and scoring of LLM apps; voice teams trace LiveKit or Pipecat into it. | [Starter $0/month; Pro $249/month; Enterprise custom](https://www.braintrust.dev/pricing) | No | [Official, hosted](https://www.braintrust.dev/docs/integrations/developer-tools/mcp) |
| [Arize Phoenix (and Arize AX)](https://arize.com/docs/phoenix) | Source-available tracing and evaluation app for LLM agents, plus the managed Arize AX platform. | [Phoenix free to self-host; Arize AX Pro $50/month](https://arize.com/pricing/) | Partly (Elastic License 2.0, source-available) | [Official, hosted](https://arize.com/docs/phoenix/integrations/mcp) |
| [LangSmith](https://docs.langchain.com/langsmith/observability) | Hosted tracing, evaluation and deployment platform for LLM agents; no voice-specific simulator. | [Developer $0/seat/month; Plus $39/seat/month](https://www.langchain.com/pricing) | No | [Official, hosted](https://docs.langchain.com/langsmith/langsmith-remote-mcp) |

## I. Language models

The models that do the thinking in a cascade, from model makers and fast
inference hosts, priced per million tokens and not per minute.

### Model makers

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [OpenAI GPT-6 family](https://developers.openai.com/api/docs/models) | OpenAI's GPT-6 text models; gpt-6-luna is the lowest-priced tier. | [gpt-6-luna $0.10 in / $0.50 out; gpt-6.1-sol $2.00 / $10.00 per 1M tokens](https://developers.openai.com/api/docs/pricing) | No | [Docs only](https://developers.openai.com/learn/docs-mcp) |
| [OpenAI earlier small tiers](https://developers.openai.com/api/docs/models) | Older and smaller OpenAI text models that voice platforms still list. | [gpt-5-nano $0.05 in / $0.40 out; gpt-4.1-mini $0.40 / $1.60 per 1M tokens](https://developers.openai.com/api/docs/pricing) | No | [Docs only](https://developers.openai.com/learn/docs-mcp) |
| [Claude Haiku 4.5](https://platform.claude.com/docs/en/about-claude/models/overview) | Anthropic's lowest-priced current Claude model. | [$1 / MTok input, $5 / MTok output](https://platform.claude.com/docs/en/about-claude/pricing) | No | None found |
| [Claude Sonnet 5.5](https://platform.claude.com/docs/en/about-claude/models/overview) | Anthropic's mid-tier Claude model; Opus 5.5 and Fable 5.1 prices are given for reference. | [Sonnet 5.5 $2 / MTok input, $10 / MTok output](https://platform.claude.com/docs/en/about-claude/pricing) | No | None found |
| [Gemini Flash-Lite](https://ai.google.dev/gemini-api/docs/models) | Google's low-cost Gemini 3 models for high-volume tasks, with a long context window. | [gemini-3.5-flash-lite $0.30 input / $2.50 output per 1M tokens](https://ai.google.dev/gemini-api/docs/pricing) | No | [Docs only](https://developers.google.com/knowledge/mcp) (vendor-wide) |
| [Gemini 3.x Flash and Pro](https://ai.google.dev/gemini-api/docs/models) | Google's larger Gemini 3 Flash models, plus a Preview Pro model; Flash prices step up Jan 1, 2027. | [gemini-3.8-flash $0.75 in / $3.75 out per 1M tokens through Dec 31, 2026](https://ai.google.dev/gemini-api/docs/pricing) | No | [Docs only](https://developers.google.com/knowledge/mcp) (vendor-wide) |
| [Grok text models](https://docs.x.ai/developers/models) | xAI's Grok text models on an OpenAI-compatible API. | [grok-4.3 $1.25 input / $2.50 output per 1M tokens](https://docs.x.ai/developers/pricing) | No | [Docs only](https://docs.x.ai/developers/docs-mcp) |
| [Mistral Small, Ministral, Medium and Large](https://docs.mistral.ai/models) | Mistral text and vision models on a serverless API, several with open weights. | [Mistral Small 4 $0.15 input / $0.6 output per 1M tokens](https://docs.mistral.ai/inference/pricing) | Partly (Apache-2.0 models; Medium 3.5 is Modified MIT) | [Official, hosted](https://docs.mistral.ai/resources/mcp) |

### Fast inference hosts

| Product | What it is | Price (headline) | Open source | MCP server |
| --- | --- | --- | --- | --- |
| [GroqCloud](https://console.groq.com/docs/models) | Groq's hosted inference for open-weight models on its own LPU chips. | [gpt-oss-20b $0.075 input / $0.30 output per 1M tokens](https://console.groq.com/docs/models) | No | [Official, local](https://github.com/groq/groq-mcp-server) |
| [Cerebras Inference](https://inference-docs.cerebras.ai/models/overview) | Cerebras hosted inference on its own chips; Shared Inference serves two models. | [gpt-oss-120b $0.35 input / $0.75 output per 1M tokens](https://www.cerebras.ai/pricing) | No | None found |
| [Fireworks AI Serverless](https://docs.fireworks.ai/serverless/pricing) | Fireworks serverless per-token inference for open-weight models, with Priority and Fast modes. | [OpenAI GPT OSS 120B $0.15 input / $0.60 output per 1M tokens (Standard)](https://docs.fireworks.ai/serverless/pricing) | No | [Docs only](https://docs.fireworks.ai/ecosystem/integrations/development-setup) |
| [Together AI Serverless](https://docs.together.ai/docs/serverless/models) | Together AI serverless API for 100+ open-source models, plus dedicated endpoints. | [gpt-oss-120B $0.15 input / $0.60 output per 1M tokens](https://www.together.ai/pricing) | No | [Docs only](https://docs.together.ai/docs/agent-skills) |
| [SambaNova SambaCloud](https://docs.sambanova.ai/docs/en/models/sambacloud-models) | SambaNova hosted inference for open-weight models on its own RDU chips. | [gpt-oss-120b $0.22 input / $0.59 output per 1M tokens](https://cloud.sambanova.ai/plans/pricing) | No | [Official, local](https://github.com/sambanova/sambanova-plugin-cc) |
| [Baseten Model APIs](https://docs.baseten.co/inference/model-apis/pricing-and-limits) | Baseten pay-as-you-go APIs for open-weight models, plus dedicated GPU deployments. | [GPT OSS 120B $0.10 input / $0.50 output per 1M tokens](https://www.baseten.co/pricing) | Partly (Truss is MIT; hosted platform is not) | [Official, hosted](https://docs.baseten.co/agent-setup) |

## Skills for these providers

Many of these vendors also publish agent skills or MCP servers. The MCP column
above shows which ones run an official MCP server: 72 of the 181 products have
one (hosted or local), and 42 more have a server that only searches
documentation. Many of these are vendor-wide rather than specific to one
product. For ready-made skills by provider, see
[More voice skills](more-skills.md) and the [skill catalog](catalog.md).

## How this was researched

- Research ran on September 30, 2026. Each product was checked against its own
  pages (pricing, docs, GitHub, changelogs). Every price, status, license and
  date kept a source URL, and anything not seen is marked unverified.
- Raw page text was preferred over summaries. Of 836 recorded price rows, 598
  matched their page verbatim and 212 held no number to test. Of the 26 that did
  not match in plain HTML, 24 matched by other means (a rendered page, decoded
  pricing data or a source document) and 2 stay unconfirmed: Vonage's $1.09
  number rental and one Together AI figure. 131 GitHub repositories cited as
  sources were re-read through the GitHub API. The research itself had no
  independent review beyond these checks.
- Known limits: web search quota and one fetch provider's credits ran out
  mid-study, so several deal and deprecation checks rely on vendor pages and not
  on news coverage, and some press sites returned 403.
- 275 fields across 121 products are marked unverified. 13 products have a
  status that could not be confirmed and 13 have sales-only pricing. Re-check
  these before you rely on them.
- Something out of date or wrong?
  [Open an issue](https://github.com/RobStrayer/nl-voice-skills/issues/new/choose)
  with a source.
