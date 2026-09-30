---
name: voice-speech-pipeline
description: Select, integrate, and evaluate streaming speech recognition and synthesis for a voice agent, including transcript revisions, language support, pronunciation, text buffering, and playable audio delivery.
license: MIT
---

# Voice speech pipeline

Use the [speech pipeline guide](references/speech-pipeline-guide.md) when choosing
STT/TTS components or diagnosing incorrect words, unstable transcripts, delayed
speech, or poor pronunciation. It includes decision criteria, streaming contracts,
a synthetic failure case, and a comparison worksheet.

Inspect the current pipeline and its installed versions. Establish the input
channel, languages, acoustic conditions, required entities, output voice, and
actual player or carrier format. Preserve an accepted voice/persona unless the
user asks to reconsider it.

1. Locate the first boundary where the evidence diverges: captured audio,
   transcript segment, assembled turn, tool argument, spoken text, generated audio,
   or playback. Do not attribute every wrong answer to recognition.
2. Identify which transcript events are provisional, final for a segment, and
   evidence for turn completion. Reconcile overlapping revisions and duplicate
   delivery before committing text. Verify the selected API's event contract.
3. Define the speech output contract: streaming input or complete text, phrase
   boundaries, normalization, pronunciation, codec/rate/channels, cancellation,
   and a generation identifier for rejecting late audio.
4. Compare candidates on representative task audio. Keep recognition accuracy,
   critical-entity correctness, endpoint timing, intelligibility, first useful
   audio, and successful task completion separate. A language-support claim needs
   the exact model, mode, region, and selected voice.
5. Change the demonstrated cause, then repeat the affected case with the same
   input and configuration. Check whether a pronunciation or buffering improvement
   harms another language, response delay, or interruption handling.

Deliver the chosen configuration and reasons, one representative event trace,
the comparison results and denominators, and unresolved compatibility questions.
Distinguish offline replay, synthetic examples, and observed live behavior.
Provider calls, recordings, model downloads, and paid tests require the user's
existing authorization for that work.

Sources reviewed 2026-09-30 UTC. The guide records primary references and current
documentation caveats; verify runtime behavior against the installed SDK.
