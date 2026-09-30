---
name: voice-turn-taking
description: Design, debug, and tune voice-agent turn boundaries and interruptions. Use for callers being cut off, slow endpointing, ignored corrections, backchannels stopping speech, unstable streaming transcripts, or audio and tool state diverging after barge-in.
license: MIT
---

# Voice turn taking

Read [the turn-taking guide](references/turn-taking-guide.md) before changing detection or interruption behavior. It covers completion signals, streaming transcripts, response state, a worked booking correction, tuning, instrumentation, and current integration requirements.

Establish the actual media path, languages, installed SDK/model versions, and who commits turns. Resolve the relevant library through Context7 and check its current primary documentation. Keep documented provider behavior separate from application policy and assumptions.

Trace one failed interaction before tuning: speech activity, transcript revisions, completion decision, user-turn commit, generated output, played output, interruption decision, and tool outcome. Use one clock or explicit causal events. Preserve missing observations as unknown.

Separate VAD from end-of-turn decisions and interruption eligibility. Test short corrections, backchannels, hesitation, and the target languages. A final STT segment need not end the conversational turn; an empty transcript need not mean no speech.

On an accepted interruption, invalidate obsolete response output, stop playback, and repair history using available played evidence. Reconcile external tool operations independently before retrying. Preserve existing task authorization; do not introduce routine approval for read-only diagnosis or replay fixtures.

Recommend the smallest change supported by the trace. Compare it on the same labeled cases, including failure and fallback paths, with explicit error costs and denominators. Report the configuration/version, deciding evidence, remaining unknowns, and regression result. Do not call an unexecuted configuration or synthetic timeline a measured improvement.
