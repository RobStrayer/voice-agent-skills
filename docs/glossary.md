# Voice AI glossary

[Home](../README.md) / Glossary

Plain-English definitions for the terms you'll meet when building voice agents.
Each entry says what the thing is and why it matters to you.

**Jump to:** [A–C](#ac) · [D–L](#dl) · [M–R](#mr) · [S](#s) · [T–Z](#tz)

## A–C

**AEC (acoustic echo cancellation).** Removes the agent's own voice from the
microphone signal when it leaks out of a speaker and back in. It needs a copy of
what was played (the "reference"). Without AEC, an agent on a laptop speaker can
hear itself and interrupt itself.
See [audio frontends](../skills/foundations/voice-audio-frontends/SKILL.md).

**AMD (answering machine detection).** Deciding whether an outbound call reached
a person or voicemail. It usually costs a few seconds at the start of the call and
is never perfect, so plan what the agent says in both cases.

**ASR (automatic speech recognition).** Another name for speech-to-text (STT).

**BAA (business associate agreement).** The contract a US healthcare provider
needs with any vendor that handles patient data. Signing one is required under
HIPAA but doesn't make a voice agent compliant on its own.
See [phone compliance](../skills/foundations/voice-phone-compliance/SKILL.md).

**Backchannel.** Short listener noises such as "mm-hm", "yeah" and "right". People
say them while the other person talks. A good agent doesn't treat every backchannel
as an interruption.

**Barge-in.** The caller talks over the agent. The agent should stop speaking
quickly, drop the rest of its planned reply, and listen. Getting this wrong is
one of the most common complaints about voice agents.
See [turn taking](../skills/foundations/voice-turn-taking/SKILL.md).

**Cascade (or pipeline).** The classic architecture: speech-to-text, then a text
language model, then text-to-speech. You pick each part and can read the text in
between. Compare with [speech-to-speech](#s).

**Codec.** How audio is compressed for transport. Phone networks commonly use
G.711 (μ-law or A-law) at 8 kHz; WebRTC usually uses Opus. Mixing up codecs or
sample rates gives you silence, chipmunk voices or static.
See [media debugging](../skills/foundations/voice-media-debugging/SKILL.md).

**Cold transfer.** Handing the call to another number without introducing it
first. The caller may land in a queue or voicemail. Compare with *warm transfer*.

**Concurrency.** How many calls run at the same time. Providers often limit it,
and it drives your server and cost planning more than total minutes do.

## D–L

**Diarization.** Labelling who spoke when in a recording ("speaker 1", "speaker 2").
Useful for call analytics; usually not needed for a live one-to-one agent.

**DTMF.** The tones made by pressing phone keys. Still useful for collecting PINs
or card numbers without saying them aloud, and for navigating other companies' menus.

**Endpointing.** Deciding that the caller has finished speaking. Simple endpointing
waits for a fixed silence (say, 500 ms). Smarter *turn detection* also looks at
the words and tone. Too short cuts people off; too long feels slow.

**Filler.** A short phrase ("Let me check that for you") played while a slow tool
or model call runs. It helps if it's honest; it annoys if it's repeated or promises
something that isn't happening.

**First token / TTFT (time to first token).** How long a language model takes to
start producing text. One of several delays that add up to response time.

**Full duplex.** Both sides can talk and listen at the same time, as in a real
conversation. Most agents are effectively half duplex: they talk or listen, and
handle overlap with barge-in rules.

**Function calling (tools).** The language model asks your code to do something,
such as look up an order or book a slot, and gets the result back. Voice adds a
twist: the caller can interrupt or change their mind while a tool is running.
See [conversation design](../skills/foundations/voice-conversation-design/SKILL.md).

**Idempotent.** Safe to repeat: running the same action twice has the same
effect as running it once. Booking and payment tools should be idempotent,
because a timeout or a retry can make the model call them again.
See [call reliability](../skills/foundations/voice-call-reliability/SKILL.md).

**IVR (interactive voice response).** The classic "press 1 for billing" phone menu.
Many voice agents replace or sit behind an IVR.

**Jitter buffer.** A small audio queue that smooths out packets arriving unevenly
over the network. It adds a little delay in exchange for fewer glitches.

**Latency (voice-to-voice).** The time from when the caller stops talking to when
they hear the agent start answering. This is the number callers feel. It's made up
of turn detection, speech-to-text, the model, text-to-speech, network and playback.
See [latency audit](../skills/foundations/voice-latency-audit/SKILL.md).

## M–R

**Media stream.** A live feed of raw call audio from a telephony provider to your
server, usually over a WebSocket. You then run speech-to-text and text-to-speech
yourself.

**μ-law (mu-law).** The G.711 audio encoding used on North American and Japanese
phone networks: 8-bit samples at 8 kHz. A-law is the version used in most other
countries.

**Noise suppression.** Reduces background sound such as traffic, fans or TV.
Applied too hard, it can also delete quiet speech, including short words like "no".

**Opus.** The standard audio codec for WebRTC. It handles wideband speech and
packet loss well.

**p50, p95 (percentiles).** The p50 (median) is the value half your calls beat;
the p95 is the value 95% beat, so it shows the slow calls. Report both for
latency. Adding each stage's p95 does not give the end-to-end p95.

**PCM.** Uncompressed audio samples. Most speech APIs want 16-bit PCM at a stated
sample rate. Always check the rate: 8, 16, 24 and 48 kHz are all common.

**Prosody.** The rhythm, stress and intonation of speech. It's why the same words
can sound friendly, bored or sarcastic, and why some synthetic voices sound flat.

**PSTN.** The public switched telephone network: the ordinary phone system.
Getting an AI agent "on a phone number" means connecting to the PSTN through a
telephony provider.

**RAG (retrieval-augmented generation).** Looking up relevant documents and giving
them to the model before it answers. In voice, retrieval time adds directly to the
caller's wait, so keep it fast or cover it with an honest filler.

**Realtime API.** A provider API that streams audio in and out of a model over a
persistent connection (WebSocket or WebRTC). Often used to mean speech-to-speech
models, such as OpenAI's Realtime API or Google's Gemini Live API.

## S

**Sample rate.** How many audio samples per second. Phone audio is 8 kHz
(narrowband); many speech models prefer 16 kHz or more. Upsampling phone audio
does not restore detail that was never captured.

**SIP (Session Initiation Protocol).** The signalling protocol most VoIP and
business phone systems use to set up calls. A **SIP trunk** connects a phone
provider to your own SIP-capable system, such as LiveKit SIP or a PBX.

**Speech-to-speech (S2S).** One model hears audio and produces audio directly,
without a separate text step you control. It can sound more natural and has fewer
parts, with less control over each stage.

**Speech-to-text (STT).** Turns speech into text. Streaming STT sends partial
("interim") results that can still change before a final result. Treat interim
text as a draft.
See [speech pipeline](../skills/foundations/voice-speech-pipeline/SKILL.md).

**SSML.** A markup language for controlling text-to-speech: pauses, emphasis,
pronunciation, how to read numbers. Support varies by provider; some newer models
use their own tags or plain-language instructions instead.

**STIR/SHAKEN.** The caller-ID authentication framework used by US and Canadian
carriers. It affects whether your outbound calls show as verified or get labelled
"Spam Likely".

## T–Z

**TCPA.** The US Telephone Consumer Protection Act. It governs calls that use an
artificial or prerecorded voice, and the FCC ruled in 2024 that AI-generated
voices count. See [phone compliance](../skills/foundations/voice-phone-compliance/SKILL.md).

**Text-to-speech (TTS).** Turns text into audio. For live agents, the key numbers
are how quickly the first audio arrives and whether it can stream while text is
still being generated.

**TTFB (time to first byte).** How long until the first chunk of a response
arrives. For TTS, the first audio chunk. A fast TTFB doesn't help if your player
waits for the whole file.

**Turn detection.** Deciding whose turn it is to speak. It combines silence, the
words said so far, and sometimes tone. It's the main cause of agents that cut
people off or feel sluggish.
See [turn taking](../skills/foundations/voice-turn-taking/SKILL.md).

**VAD (voice activity detection).** Detects whether audio contains speech.
Used to notice that someone started or stopped talking. On its own it can't tell
a thinking pause from the end of a sentence.

**Voice cloning.** Creating a synthetic voice from recordings of a real person.
Requires that person's consent and is restricted by several providers and laws.

**Warm transfer.** Connecting the caller to a person after the destination
accepts, often with a summary, while keeping the caller on the line if nobody
answers. See [call reliability](../skills/foundations/voice-call-reliability/SKILL.md).

**WebRTC.** The browser standard for real-time audio and video. It handles echo
cancellation, jitter and network changes, which is why many voice frameworks
use it for web and app clients.

**WebSocket.** A persistent two-way connection over HTTP. Simple and widely
supported, and used by many speech APIs and phone media streams. It runs over TCP,
so poor networks cause delays rather than dropped audio.

**WER (word error rate).** The share of words a transcript gets wrong. A useful
average, but it hides the errors that matter, such as a wrong digit in a phone
number or a missed "not". Test on the words your task depends on.
