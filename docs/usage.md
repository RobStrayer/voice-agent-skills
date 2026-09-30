# Installing and using the skills

[Home](../README.md) / Install

A skill is a folder with a `SKILL.md` file (plus any `references/`, `assets/` or
`scripts/` next to it). Your coding agent reads the short description of every
installed skill and loads the full instructions when a task matches. Install the
**whole folder**, not just `SKILL.md`.

## Claude Code: plugin marketplace

This repo is a Claude Code plugin marketplace. Add it once, then install the
bundles you want:

```text
/plugin marketplace add RBStrayer/nl-voice-skills
/plugin install voice-foundations@nl-voice-skills
```

Or from your shell:

```bash
claude plugin marketplace add RBStrayer/nl-voice-skills
claude plugin install voice-foundations@nl-voice-skills
```

| Plugin | What you get |
| --- | --- |
| `voice-foundations` | The provider-neutral skills written for this repo. Start here. |
| `voice-livekit` | LiveKit's official skills (dated copy) |
| `voice-pipecat` | Pipecat's official skills (dated copy) |
| `voice-elevenlabs` | ElevenLabs' official skills (dated copy) |
| `voice-twilio` | Twilio's official voice skills (dated copy) |
| `voice-cartesia` | Cartesia's official skills (dated copy) |
| `voice-openai-speech` | OpenAI's file-based speech and transcription skills (dated copy) |

Plugin skills are namespaced, so `voice-turn-taking` runs as
`/voice-foundations:voice-turn-taking`. Claude also picks skills automatically
when your request matches their description.

## Any agent: `npx skills`

The [`skills` CLI](https://github.com/vercel-labs/skills) finds every skill in the
repo and installs it for Claude Code, Codex, Cursor and other agents it supports:

```bash
npx skills add RBStrayer/nl-voice-skills --list
npx skills add RBStrayer/nl-voice-skills --skill voice-turn-taking
```

## Copy a folder by hand

Clone the repo and copy the skill folders you want into your agent's skills
directory:

| Agent | Personal skills | Project skills |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` |
| OpenAI Codex | `~/.agents/skills/<name>/` (older Codex versions: `~/.codex/skills/`) | `.agents/skills/<name>/` ([Codex skills docs](https://learn.chatgpt.com/docs/build-skills)) |

```bash
git clone https://github.com/RBStrayer/nl-voice-skills.git
cp -r nl-voice-skills/skills/foundations/voice-turn-taking ~/.claude/skills/
```

## Fresh copies versus snapshots

The `foundations` skills are written and maintained here. The provider folders
(`livekit`, `pipecat`, `elevenlabs`, `twilio`, `cartesia`, `openai`) are **dated
copies** of each vendor's official skills, pinned to the commits in
[`sources.json`](../sources.json). They don't update themselves. For the newest
version, install from the vendor's own repo; every entry in the
[catalog](catalog.md) links to it.

Provider skills describe real products and sometimes expect a vendor CLI, SDK or
MCP server. This repo supplies the instructions, not those tools, API keys or
accounts. Skills never expand what you've authorized: live calls, phone numbers
and paid API requests still need your go-ahead.

Provider snapshots were collected on 2026-09-29. See the
[documentation review](documentation-review.md) for the sources checked.

## Runtime notes

| Collection | Prerequisites and material caveats |
| --- | --- |
| Foundations | Project files, traces, or test artifacts appropriate to the task. Current documentation access is needed for version-sensitive claims; stack selection calls for Context7, with direct official documentation when its index is missing or stale. No paid vendor runtime is required for a review. |
| LiveKit | Relevant SDK/CLI and LiveKit documentation access. Some upstream instructions expect the LiveKit Docs MCP. Simulations and operations can create billable or live resources. Current skills replace the older `livekit-agents` and `livekit-simulations` pack. |
| ElevenLabs | SDK/API or ElevenLabs MCP/CLI as described by the skill. Some references show shell installers; review the current official installation method before executing them. Voice cloning/conversion and dubbing require rights to the source material. |
| Pipecat | Python project and Pipecat CLI; hosting credentials for deploy. The pinned init/deploy skills use older `pipecat-ai-cli` installation wording. Use the current CLI instructions below. |
| Cartesia | Cartesia API access or Line CLI. The pinned Line skill includes shell installer examples and operational commands. |
| Twilio | Account/API or Twilio MCP access appropriate to the workflow. Additional Twilio skills are mentioned by name but are outside this voice subset; get them from the full upstream pack if needed. Phone numbers, outbound calls, recordings, and infrastructure changes need task-specific authorization. |
| OpenAI | Python and the OpenAI SDK for the included scripts; API access for actual speech/transcription requests. These are file-oriented workflows, not a realtime conversational runtime. |

Pipecat init/deploy mention Claude-specific `AskUserQuestion`; talk expects MCP
start/speak/listen/stop tools and its own confirmations. Hosts without those tools
need an equivalent supported workflow. OpenAI script examples assume paths below
`~/.codex/skills/`; adjust the CLI path to the folder where you actually copied the
skill. Markdown format compatibility doesn't prove runtime compatibility.

Eight upstream skills use the Agent Skills specification's `compatibility` field;
Twilio's architect skill also uses a provider-specific `tier` field. The bundled
Codex skill-creator validator rejects these extra fields, although all 39 headers
parse as YAML and their required names/descriptions pass the collection checks.
Upstream content is preserved. If a host requires a narrower schema, adapt a local
installation copy and retain the original snapshot and attribution here.

## Included executable examples

Two upstream Python scripts are included, under OpenAI speech and transcribe.
They were read and syntax-checked during curation; paid operations were not run.

- **Transcribe:** output paths can overwrite existing transcript files. Use a
  fresh output directory and distinct input basenames. `--out-dir` alone does not
  prevent two files such as `customer-a/call.wav` and `customer-b/call.wav` from
  producing the same output name. Known-speaker reference
  audio is request data; dry-run output can include its encoding. Do not log or
  share dry-run payloads containing private audio.
- **Speech:** batch output names are trusted-input examples and can contain parent
  path segments. Supply controlled paths; do not expose the script directly as an
  untrusted upload endpoint.

No install hooks, background jobs, or provider accounts are configured by this repo.
Skills and sample commands do not expand the user's authorization. Keep live
operations within the requested account, destination, budget, and recording scope.

## Current documentation notes

These notes qualify examples in the dated copies. They do not modify upstream
files or certify every combination of model, SDK, and transport.

### Pipecat CLI installation

The current [Pipecat CLI overview](https://docs.pipecat.ai/api-reference/cli/overview)
installs the CLI from the main package. Cloud commands need the extra dependency:

```sh
uv tool install "pipecat-ai[cli]"
# For Pipecat Cloud commands:
uv tool install "pipecat-ai[cli]" --with pipecatcloud
```

Choose the command for your task and verify the installed version and help. The
older package name in the skill snapshot does not mean its entire workflow is
obsolete. The current [init reference](https://docs.pipecat.ai/api-reference/cli/init)
still documents interactive setup and noninteractive options.

### Telephony speech and playback

[ConversationRelay](https://www.twilio.com/docs/voice/twiml/connect/conversationrelay)
exchanges transcribed caller speech and response text with your application.
[Media Streams](https://www.twilio.com/docs/voice/media-streams/websocket-messages)
exchanges audio. Pick the boundary your application needs to control.

For bidirectional Media Streams, returned `mark` messages can follow completed
playback or a `clear` operation. Correlate them with clear events before counting
audio as played. These are transport acknowledgments, not acoustic measurements
at the caller's device. ConversationRelay has its own
[interruption messages](https://www.twilio.com/docs/voice/conversationrelay/websocket-messages);
do not apply one product's message schema to the other.

### Turn taking and interrupted speech

ElevenLabs exposes separate controls for waiting through user silence, taking a
turn, and filling a delay while the LLM is still working. A soft-timeout filler
doesn't prove that the requested answer is ready. Its
[conversation-flow documentation](https://elevenlabs.io/docs/eleven-agents/customization/conversation-flow)
describes these controls. For tools, use the current
[`interruption_mode` settings](https://elevenlabs.io/docs/eleven-agents/customization/tools/tool-configuration/tool-interruptions).
The preserved skill already documents this field. Suppressing speech interruptions
doesn't prove that an external action can be rolled back.

Cartesia's [context cancellation documentation](https://docs.cartesia.ai/use-the-api/tts-websocket/contexts)
states: "Any currently generating request will continue sending responses until
completion." For an interrupted turn, your application must also discard obsolete
chunks and stop queued playback. Test that behavior on the actual transport.
[Cartesia Line](https://docs.cartesia.ai/line/introduction) provides managed speech
orchestration; using the standalone speech API leaves more of that work with your
application.

For LiveKit metrics, tools, and turn handling, use the dated source notes in
[latency audit](../skills/foundations/voice-latency-audit/SKILL.md) and
[agent evaluation](../skills/foundations/voice-agent-evaluation/SKILL.md). Match
examples to the installed SDK version before copying event handlers.

## Refreshing a snapshot

Use `sources.json` to identify the exact upstream revision. Inspect a proposed
upstream diff, retain licenses and notices, update the affected checksums, and
rerun `python scripts/verify.py`. A current provider API can outpace a skill
snapshot; validate relevant behavior against official docs before live operation.

The [maintenance procedure](maintenance.md) covers source refreshes, new entries,
and checks required before publishing an update.
