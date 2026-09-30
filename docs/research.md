# Curation and research notes

Initial research: September 29, 2026 (America/New_York). Machine records include
UTC observation times that fall on September 30. This collection is a curated
starting point, with demonstrated coverage below, rather than an exhaustive
inventory of every voice skill on the internet.

## Sources searched

- Installed Codex, Claude, shared agent, and plugin-cache skill directories.
- A locally available Hermes foundation package containing additional skills.
- Public upstream repositories, their skill folders, supporting material, licenses,
  immutable commits, and current repository metadata.
- Web search, official documentation, Reddit discussions, and community links.

The local scan screened 1,654 installed `SKILL.md` headers plus 244 Hermes-package
headers. It found 133 voice-relevant copies, deduplicated to 80 provider/name
entries: LiveKit 9, Deepgram 15, ElevenLabs 33, Twilio 18, and Hermes 5.
Different versions and content variants were retained in the private research
inventory. Some project directories were inaccessible, so project-local coverage
is incomplete. The research inventory stays outside this publishable repository.

A [sanitized discovery index](local-skills.md) preserves all 80 names and links
to reviewed public counterparts. It contains no local paths or copied specialist
prose. Indexed discoveries are separate from the 31 included skills.

The installed collection was a discovery source. Public upstream snapshots supply
the vendored content. This avoids exporting local execution customizations or
private project information. Local files were not assumed to be latest or licensed
for redistribution merely because they were installed.

## Inclusion rules

Include skills that help build, debug, test, operate, or design voice agents, plus
speech workflows directly useful to that work. Preserve the supporting folder and
upstream name. Favor official and maintained sources, clear task triggers, and
meaningful engineering guidance over duplicate prompts or generic skill bundles.

Repository popularity was checked as a discovery signal. Actual voice-specific
skill packs often have far fewer stars than framework or general-skill repositories.
The skill-source counts in `sources.json` and framework counts in `resources.json`
refer to different repositories and should not be combined as an endorsement.

## Included and indexed

| Source | Treatment | Reason |
| --- | --- | --- |
| ElevenLabs, LiveKit, Pipecat, Cartesia, Twilio, OpenAI | 27 selected skills copied at pinned commits | Clear license files covering the selected content; supporting material retained. |
| [Deepgram skills](https://github.com/deepgram/skills) | External index | No root or nested redistribution license found in the searched pinned repository tree. This is a source-search result, not a claim that permission can never be obtained. |
| [Vapi skills](https://github.com/VapiAI/skills) | External index | Skill frontmatter declares MIT, but no complete license/notice file was located to establish supporting-file scope. |
| ElevenLabs connector architect specialists | Official documentation links | Installed specialist prose lacked a located redistribution license; public SDK/agent skills and documentation cover the main workflows. |
| Twilio Conversation Intelligence | Full upstream link | Selected skill depends on other non-voice skills and contains environment-specific absolute links. |
| [Generovo voice skills](https://github.com/Generovo/claude-voice-skills) | Discovery record in sources.json | Smaller community pack with limited adoption evidence; retained for exploration rather than promoted over official sources. |
| [Community Retell pack](https://github.com/bachhao-tech/RETELL-AI) | Discovery record in sources.json | Limited adoption/provenance evidence; no official-provider endorsement inferred. |
| Hermes package and local custom variants | Private inventory only | Provenance, account side effects, and portability need further review before redistribution. |

Music generation, generic sound effects, animation, cybersecurity, and broad
non-voice platform skills were excluded. Additional Twilio product skills stay in
the upstream collection instead of broadening the voice-only scope here.

## Verification and remaining limits

All 104 copied upstream files were compared byte-for-byte with their commit-pinned
archive entries. Licenses and nested OpenAI licenses were retained. Source review
covered copied text and the two included Python scripts; no upstream code, paid
speech request, model, phone call, or deployment was executed.

The four original foundation skills received an independent scenario review for
latency evidence, interrupted tool actions, stack selection, and spoken prompts.
That review checks instruction quality; it is not a field trial of a deployed agent.

The resource library contains 28 unique projects. Eighteen metadata records use the
GitHub REST API; ten use explicitly identified GitHub HTML metadata after the
shared unauthenticated API quota was exhausted. Their READMEs and license
qualifications were inspected. Eight documentation links returned HTTP 200.

Docker Firecrawl was unavailable from the active environment. Standard web search,
public GitHub retrieval, and primary documentation supplied the research. Reddit
supplied candidate projects and reported concerns; community claims and published
benchmark results were not independently reproduced.

`scripts/verify.py` checks structure, unique skill names, source coverage and
checksums, resource records, Python syntax, and local Markdown paths. It does not
certify agent-host compatibility, API currency, audio quality, or provider behavior.

All 31 frontmatter blocks parsed as YAML. The bundled Codex quick validator passed
22 skills, including all four originals; it rejected eight upstream `compatibility`
fields and one custom Twilio `tier` field. Those source fields are preserved and
documented in [usage notes](usage.md). The local negative regression check also
confirmed that unrecorded changes to upstream content fail checksum verification.
