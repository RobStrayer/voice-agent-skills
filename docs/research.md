# Curation and research notes

Expanded review: **2026-09-30 UTC**. Initial collection: September 29, 2026
(America/New_York). This page describes the sources actually searched and the
limits of the review. It is not an inventory of every voice skill on the internet.

## What is included

| Material | Coverage | Treatment |
| --- | --- | --- |
| Original NL foundations | 9 skills | Architecture, conversation, turn taking, audio frontends, recognition/synthesis, call reliability, latency, evaluation, and media debugging; maintained here. |
| Core provider skills | 27 skills from 6 repositories | Current original links, plus 104 licensed files preserved at recorded commits. |
| Additional source links | 297 skills: 279 from 62 repositories and 18 on vendor documentation sites | Voice-specific provider workflows, SDK language variants, and clearly marked optional entries; no new third-party copies. |
| Runtime resources | 43 unique projects | Frameworks, models, transport, evaluation, and learning material with dated metadata and license qualifications. |

A language variant counts as another skill file, not a new engineering capability.
A project that contains skills can also appear in the resource library; those
indexes are different views, not additive measures of coverage. Current counts and
source records are in [sources.json](../sources.json),
[linked-skills.json](../linked-skills.json), and [resources.json](../resources.json).

## Discovery and original sources

The initial local scan screened 1,654 installed `SKILL.md` headers plus 244 headers
in an available Hermes package. It found 133 voice-relevant copies, deduplicated to
80 provider/name entries: LiveKit 9, Deepgram 15, ElevenLabs 33, Twilio 18, and
Hermes 5. Some project directories were inaccessible, so project-local coverage
is incomplete. The private inventory stays outside this repository.

Installed files supplied leads. Published content came from the public original
sources, with their current branches, supporting folders, and licenses inspected.
Local variants and account-specific execution instructions were not exported.

The expanded pass covered public repository trees and archives, source manifests,
SDK examples, released package contents where a concrete discrepancy required it,
provider documentation, Context7, web search, and Reddit leads. It located selected
skills from Microsoft, Google, NVIDIA, Telnyx, Deepgram, AssemblyAI, Vapi, Coval,
Moonshine, Voximplant, Synthflow, and Shiny. Canonical skill paths were separated from
plugin mirrors before counting.

Stars are a discovery signal. Large runtime repositories and small skill packs
serve different purposes; their popularity does not establish instruction quality.
Source-level checks found defects in official repositories as well as community
material. The index records those defects where they affect the selected workflow.

## Selection rules

Include work that helps someone build, design, test, debug, or operate a voice
agent, and speech tasks directly useful to that work. Prefer clear triggers,
actionable instructions, maintained original sources, and usable supporting files.
Preserve the upstream name. Group language variants by task so readers can find the
right implementation without reading a long list of near-duplicates.

For copied content, inspect complete redistribution terms, nested licenses, and
supporting-file scope. Retain required notices and hash every copied file. A
useful original link can be indexed even when redistribution terms are unresolved;
that is not permission to copy its content.

Music generation, generic sound effects, animation, cybersecurity packs, and
broad platform skills with only a passing voice reference are outside this
collection's purpose.

## Deliberate exclusions and qualifications

| Source or finding | Decision and evidence |
| --- | --- |
| Central Deepgram, Vapi, AssemblyAI, Synthflow | Original links only. A complete repository license was not found in the inspected sources. Vapi frontmatter alone did not establish all supporting-file terms. Deepgram's separate SDK repositories have MIT licenses. |
| Azure AI Transcription Python skill | Excluded after released SDK inspection found its streaming/batch method examples absent. Use the [current SDK README](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/transcription/azure-ai-transcription/README.md). |
| Deepgram Go conversational-STT skill | Excluded because its claim that the v2 client and Flux examples do not exist contradicts the current repository. The current example is linked in the catalog. |
| Azure Voice Live language skills | Retained with explicit preview-version and API-name qualifications. A valid pinned Java preview example is not labeled broken merely because a later release changes the signature. |
| [Large community skills aggregator](https://github.com/sickn33/agentic-awesome-skills) | Searched, including its voice subset. Several voice guides trace to [Vibeship's original YAML skills](https://github.com/vibeforge1111/vibeship-spawner-skills/tree/main/ai-agents/voice-agents). Old snippets and unqualified timing claims did not justify promoting a mirror over maintained provider sources. |
| [Vobiz skills](https://github.com/vobiz-ai/Agent-Skills) | Inspected but not selected in this revision. Voice-agent and audio-stream guides disagree about stop events and media formats; current [WebSocket documentation](https://www.vobiz.ai/docs/integrations/websockets) distinguishes incoming messages from outbound commands. |
| [Generovo voice skills](https://github.com/Generovo/claude-voice-skills) | Discovery record retained. Several references/examples are marked unfinished, and a local research dependency is not portable. |
| [Community Retell pack](https://github.com/bachhao-tech/RETELL-AI) | Discovery record retained; limited evidence that it improves on current provider documentation. No official endorsement inferred. |
| Cloudflare and Strands general agent skills | Voice documentation linked as a learning resource. No dedicated realtime voice skill was established in the bounded trees/searches examined. This is not a claim that none exists anywhere. |
| Older Coval specialist launch workflows | Newer bounded evaluation workflows selected. Whole-set defaults and less bounded watch/relaunch behavior require additional care. |
| Installed ElevenLabs connector specialists and custom local variants | Private discovery only where a current redistributable original source was not established. Public agent skills and official documentation supply the published coverage. |

## Checks performed

All 104 copied files were rechecked against their pinned archives and freshly
observed upstream heads. The six heads and all selected copied files matched the
existing snapshots. Licenses and the nested OpenAI licenses remain intact. That
proves file identity at review time, not that every upstream example is current.

The linked catalog checks actual manifests and source identity. Selected SDK
references and central API workflows received deeper checks when conflicts were
found. [Documentation review](documentation-review.md) records those findings,
source dates, Context7 coverage, and direct-source fallbacks. Provider publication
dates are stated only where the source supplies them.

The original foundations received independent instruction reviews. A synthetic
media case exercised rate mismatch, blocked browser playback, cumulative timing
counters, reconnects, obsolete audio, clear acknowledgements, and an uncertain tool
write. The review led to explicit clear-before-new-output ordering and clock
alignment guidance. This checks how the instructions guide a diagnosis; it is not
an audio benchmark or a deployed-agent field trial.

A separate architecture scenario used a non-idempotent booking API, a regional
constraint, two channels, uncertain language support, and burst traffic. It led to
clearer text-checkpoint definitions and an explicit rule for unresolved write
outcomes.

A latency scenario combined overlapping stage summaries, different client/server
clocks, missing playback boundaries, mixed call and turn counts, and a mark returned
after clear. The instructions rejected the summed p95 without inventing a replacement
duration or a coverage denominator. These instruction checks do not establish provider
compatibility, measured latency, or production capacity.

Local checks cover snapshot hashes and licenses, unique bundled names, original
source URLs, catalog/count consistency, Python syntax, Markdown paths, and bounded
credential/private-path patterns. Negative checks reject modified upstream files,
substituted mirror URLs, a docs-hosted skill moved to GitHub, stale verification
counters, and a synthetic credential pattern. A separate review checks first-party
heading anchors and publication text.

All bundled frontmatter is checked as YAML. The narrower Codex skill-creator
validator rejects nine preserved upstream metadata extensions: eight
`compatibility` fields and one Twilio `tier` field. Required names/descriptions
remain valid; [usage notes](usage.md) explain host portability.

RNNoise is linked to its authoritative GitLab repository. Its GitHub mirror
provides the recorded popularity count; matching commits and README hashes were
verified. Shiny supplies an optional native .NET frontend skill with visible
prerelease and platform-support qualifications.

## Remaining limits

The reading structure was revised on 2026-09-30 UTC. The README is a substantial
illustrated introduction, with diagrams explaining the cascade, call routing,
timing, turns, acoustic processing, and action recovery. Relevant foundation and
original provider skills appear beside each topic. The [handbook](handbook.md)
groups eleven work areas into four longer reading paths; implementation guides
stay with each foundation skill. Catalog entries and their qualifications remain
intact. The front page begins with a task-based skill directory and uses compact
technical diagrams without a decorative cover. Timing values and conversation
traces in the new figures are explicitly synthetic teaching examples.

Five original figures explain system responsibilities, turn state, endpoint echo
processing, interrupted actions, and recoverable human handoff. Their editable
HTML and exported SVG remain with the associated skills. Semantic review checked
that the diagrams preserve action uncertainty and caller ownership; a handoff
arrow was corrected to retire only the bot leg. Diagram checks cover accessibility
metadata, SVG references, connector geometry, and local links. Browser review
included light/dark surrounds and narrow-screen scrolling. These checks establish
document behavior, not the runtime behavior of a voice application.

The deeper handbook revision added six packaged chapters: turn control, audio
frontends, speech recognition/synthesis, transactions/handoffs, telephony, and
production operations. The architecture chapter remains a separate decision
guide. New chapters include worked cases, failure analysis, and evaluation
worksheets; they are original engineering guidance with cited provider facts.
Independent reviewers exercised an interrupted booking with a lost response and
an echoing laptop that also clips quiet speech. Those reviews exposed overly
broad interruption and LiveKit enhancement statements, which were corrected
against the current primary documents. These were instruction exercises, not
executed calls or audio benchmarks.

No third-party helper, installer, voice-model inference, paid voice API request, voice call,
provider account mutation, or deployment was executed. Released package archives
were read as data. Source inspection cannot establish production compatibility,
voice quality, model accuracy, or end-to-end latency.

Docker Firecrawl was unavailable in this environment. Web search, Context7, public
GitHub retrieval, and primary documentation supplied the research. Reddit supplied
candidate projects and failure reports; anecdotes, vendor posts, and published
benchmark rankings were not independently reproduced. Current-source links can
change after the recorded review and are covered by the [maintenance procedure](maintenance.md).
