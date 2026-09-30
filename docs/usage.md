# Using the collection

Start with the original upstream links in the [catalog](catalog.md). Those links
track the source collection's default branch. Follow the upstream installation
guide for the latest version. Bundled provider folders are dated reference copies;
they do not refresh automatically. The foundation skills are original to this repo.

Each folder containing `SKILL.md` is a skill unit. Preserve the whole folder when
copying it. Frontmatter names remain unchanged from upstream. Select individual
skills rather than copying a provider parent as though it were one skill.

Provider skills describe real products and sometimes assume a vendor CLI or MCP.
The collection supplies their instructions and supporting files, not those tools,
credentials, services, model weights, or a portable adapter for every agent host.
Read the [catalog](catalog.md) for prerequisites and verify current SDK/CLI help.

## Runtime notes

| Collection | Prerequisites and material caveats |
| --- | --- |
| Foundations | Project files, traces, or test artifacts appropriate to the task; no vendor tool required. |
| LiveKit | Relevant SDK/CLI and LiveKit documentation access. Some upstream instructions expect the LiveKit Docs MCP. Simulations and operations can create billable or live resources. Current skills replace the older `livekit-agents` and `livekit-simulations` pack. |
| ElevenLabs | SDK/API or ElevenLabs MCP/CLI as described by the skill. Some references show shell installers; review the current official installation method before executing them. Voice cloning/conversion and dubbing require rights to the source material. |
| Pipecat | Python project and Pipecat CLI; hosting credentials for deploy. The pinned init skill includes older `pipecat-ai-cli` installation wording. Verify the currently documented package and `pipecat --help` rather than running a historical command blindly. |
| Cartesia | Cartesia API access or Line CLI. The pinned Line skill includes shell installer examples and operational commands. |
| Twilio | Account/API or Twilio MCP access appropriate to the workflow. Additional Twilio skills are mentioned by name but are outside this voice subset; get them from the full upstream pack if needed. Phone numbers, outbound calls, recordings, and infrastructure changes need task-specific authorization. |
| OpenAI | Python and the OpenAI SDK for the included scripts; API access for actual speech/transcription requests. These are file-oriented workflows, not a realtime conversational runtime. |

Pipecat init/deploy mention Claude-specific `AskUserQuestion`; talk expects MCP
start/speak/listen/stop tools and its own confirmations. Hosts without those tools
need an equivalent supported workflow. OpenAI script examples assume paths below
`~/.codex/skills/`; adjust the CLI path to the folder where you actually copied the
skill. Markdown format compatibility does not establish runtime compatibility.

Eight upstream skills use the Agent Skills specification's `compatibility` field;
Twilio's architect skill also uses a provider-specific `tier` field. The bundled
Codex skill-creator validator rejects these extra fields, although all 31 headers
parse as YAML and their required names/descriptions pass the collection checks.
Upstream content is preserved. If a host requires a narrower schema, adapt a local
installation copy and retain the original snapshot and attribution here.

## Included executable examples

Two upstream Python scripts are included, under OpenAI speech and transcribe.
They were read and syntax-checked during curation; paid operations were not run.

- **Transcribe:** output paths can overwrite existing transcript files. Choose a
  fresh output path or preserve the existing file first. Known-speaker reference
  audio is request data; dry-run output can include its encoding. Do not log or
  share dry-run payloads containing private audio.
- **Speech:** batch output names are trusted-input examples and can contain parent
  path segments. Supply controlled paths; do not expose the script directly as an
  untrusted upload endpoint.

No install hooks, background jobs, or provider accounts are configured by this repo.
Skills and sample commands do not expand the user's authorization. Keep live
operations within the requested account, destination, budget, and recording scope.

## Refreshing a snapshot

Use `sources.json` to identify the exact upstream revision. Inspect a proposed
upstream diff, retain licenses and notices, update the affected checksums, and
rerun `python scripts/verify.py`. A current provider API can outpace a skill
snapshot; validate relevant behavior against official docs before live operation.
