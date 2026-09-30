---
name: voice-data-capture
description: Capture phone numbers, emails, names, addresses, dates, amounts, confirmation codes and yes or no answers correctly on a voice call. Use when a voice agent mishears or misspells what callers say, treats a transcript as truth, flips a negation, or fails on long digit strings or spelled codes, or when spoken data is read back, validated or written to a CRM, booking or payment system. Also for slot filling, E.164 phone numbers, spelling alphabets such as NATO, keypad or DTMF entry, SSML say-as read-back, and keyterms or phrase lists for speech recognition. Covers per-field protocols, asking and read-back, recognition aids, validation in code, test fixtures and keeping card data off the model path. Needs no tools. The optional script needs Python 3.
license: MIT
---

# Voice data capture

A speech model writes a guess, and a language model will treat that guess as fact. Phone audio is narrow, callers have accents and noise, and they speak numbers in fragments. Illustrative failures, not measured ones: "five five" comes back as "nine", "never took it" comes back as "took it", and the wrong value lands in your CRM. This skill's answer is a pipeline: the model proposes a value, code normalizes and checks it, the caller confirms it, and only then does anything write.

Read these with the skill and keep them together:

- [Capture protocols by field type](references/entity-protocols.md): phone, email, names, addresses, dates and times, amounts, codes, yes and no.
- [Asking, correcting and reading back](references/ask-and-read-back.md): how to ask, the retry ladder, read-back, making the voice say it right, keypad input.
- [Recognition aids and stage-aware settings](references/recognition-aids.md): keyterms, phrase lists and prompts by provider, and settings to change per field.
- [Validate in code and keep the evidence](references/validate-and-store.md): the write gate, the transcript-support check, what to store, framework capture tasks.
- [Test set](references/test-fixtures.md): fixtures per field, safe test data and pass criteria.
- [`scripts/readback.py`](scripts/readback.py): read-back text with ambiguity flags, a transcript-support check and a check symbol. Standard library only. `python scripts/readback.py --selftest` runs its checks. It helps with speaking and sanity checks and does not replace a phone library, an address service or your own lookups.

## Set scope first

This skill builds and reviews capture flows. Do not place calls, record, send provider API requests or write to a real customer system without the user's existing authorization for that work. Test with fictional data, as the [test set](references/test-fixtures.md#safe-test-data) describes. This is engineering guidance, not legal advice. Recording, consent and card-data rules are in the [phone compliance skill](../voice-phone-compliance/SKILL.md).

## Ask before you design

- Which fields does the call need, and what does each one feed: a CRM, a booking system, a payment step?
- What can check each value: a customer list, a calendar, an address service, an issued-code table?
- Which recognizer, voice and framework run the call, and in which languages and accents?
- Is a keypad available to the caller, and can you text a link?
- Are calls recorded, and for how long is audio kept?
- Which fields cost the most when wrong? Start there.

## Capture a field, step by step

1. **Decide what you need and by which path.** Capture fewer fields. Take a value without speech where you can: a signed-in session, a lookup by something you already hold, a link to a short form, a choice from your own list. Caller ID is a candidate, never proof.

   | Field | Default path | Fallback |
   | --- | --- | --- |
   | Phone | Confirm caller ID, or say it in groups | Keypad |
   | Email | Link to a form | Spelled, letter by letter |
   | Name | Said, then spelled | Link or person |
   | Address | Address lookup, number and street confirmed apart | Link or person |
   | Date and time | Choose from slots you offer | Link |
   | Amount | Your system's own number | Person |
   | Code | Keypad if digits. Otherwise spelled, with a check symbol | A link to a form where the caller types it, or a person |
   | Yes or no | One claim per question, bound to that question | Ask again in other words |
   | Card, PIN, ID number | Keypad into the processor, never the model | Person |

2. **Ask for one field at a time.** Name the format, give one example, end on the question, and allow a correction. [How to ask](references/ask-and-read-back.md#ask-one-field-at-a-time).
3. **Normalize in code.** Turn words and numerals into one canonical value. Send number words you cannot map, such as "fifteen" or "fifty", back to the caller for digits. The model never completes or fixes digits from context. Check that the transcript supports the value, and check its shape and checksum, before you read anything back.
4. **Read the value back from the stored value.** Digits in groups with pauses, the spelling alphabet for look-alike letters, weekday with date, amounts in words. Build the spoken form in code. Start with plain words and commas, and test the result with your voice. [Read-back](references/ask-and-read-back.md#read-the-value-back) and [making the voice say it right](references/ask-and-read-back.md#make-the-voice-say-it-correctly).
5. **Take a correction, not a restart.** "No, the last four are two zero one three" replaces one piece. Read the whole corrected value back again. [Corrections](references/ask-and-read-back.md#accept-corrections).
6. **Gate every write in code.** Every digit was said or keyed in answer to this question. The format and checksum pass. The real system agrees. The caller's yes belongs to this exact value, and the backend allows the write. Run the gate again at write time, because a lookup result or a verification level can change during the call. [The write gate](references/validate-and-store.md#gate-every-write).
7. **Limit retries, then change channel.** Start with two voice attempts per field, then keypad, a link or a person. Tune the number on your own calls. [The ladder](references/ask-and-read-back.md#give-the-caller-a-way-out).
8. **Keep the evidence.** The value, the raw transcript, audio offsets, recognizer settings, the read-back, the confirmation and the check results, with retention and access set on purpose. [What to store](references/validate-and-store.md#what-to-store-with-each-value).

Recognition aids (keyterms, phrase lists, prompts, end-of-turn settings) help with names and long answers and do not verify anything. [Use them with care](references/recognition-aids.md).

## Keep sensitive data off the model path

Card numbers, security codes, PINs and government ID numbers must not reach the transcript, the model prompt, a recognizer hint list or general logs. For an AI agent, a transcript or a prompt counts as storage ([PCI section of the compliance guide](../voice-phone-compliance/references/numbers-data-and-call-behavior-guide.md#pci-payment-cards)).

- **Keypad into the payment or verification service,** so the agent never hears the digits. Pausing a recording is not enough on its own: digits spoken to speech-to-text are already in the transcript, the prompt and vendor logs ([security guide](../voice-agent-security/references/security-guide.md#keep-cards-pins-and-ids-off-the-model-path)). The compliance guide also allows pausing recording and transcription for the step, with a check that the pause held. *Inference:* a speech-to-speech model takes in the audio itself (the security guide's [data table](../voice-agent-security/references/security-guide.md#sensitive-data-in-every-store) lists audio for speech-to-speech models under the LLM provider), so pausing a recording or a transcript does not keep spoken digits from it. Name what collects the digits during the pause, and keep them off the voice path. Recording-pause mechanics for Twilio are in the [call recordings skill](../../twilio/twilio-call-recordings/SKILL.md).
- **Keypad digits are not private by default.** Some frameworks turn keypresses into text for the model. Check what yours does ([by framework](references/ask-and-read-back.md#keypad-input-by-framework)).
- **Do not read them back.** Do not put them in hint lists, prompts or analytics.
- **Some vendor examples and prebuilt tasks collect card data by speech.** Do not copy them for real card data ([recognition aids](references/recognition-aids.md#change-settings-for-the-field-you-are-collecting), [framework tasks](references/validate-and-store.md#use-framework-capture-tasks-with-care)).
- The threat model, red-team scripts and store-by-store data map are in the [voice agent security skill](../voice-agent-security/SKILL.md) and its [guide](../voice-agent-security/references/security-guide.md#keep-cards-pins-and-ids-off-the-model-path).

## Never do

- Never treat a transcript as truth, or let the model add, complete or "fix" digits or letters.
- Never write a value the caller has not confirmed, or use a yes that belonged to another value or question.
- Never correct a value silently, such as a domain or a name. Ask.
- Never count silence, "uh-huh", another speaker or the agent's own echo as a yes.
- Never read on-file data back to a caller who has not been verified.
- Never offer near matches to a missed code from other customers' records.
- Never retry the same way past your retry limit. Change the channel.
- Never send the voice a digit string or markup that you have not heard the shipped voice read correctly.
- Never use real customers, real people's voices or live card data as test data.

## Test

Run the [test set](references/test-fixtures.md) across the languages and accents you serve, noise, telephone-quality audio, fast speech, corrections and negations. Score the captured value, not the transcript, and report counts with their denominators. Replay wrong transcripts through the flow: a wrong transcript that the flow catches is a pass, and a wrong value written is the failure. The [evaluation skill](../voice-agent-evaluation/SKILL.md) covers the harness.

## Deliver

- A per-field table: the path, the prompt, the read-back form, the validators, the retry limit and the fallback.
- The write gate as code, with tests for a missing digit, a number word, a wrong confirmation and noise-only input.
- The evidence schema and its retention and access.
- The fixtures run, with counts and denominators, and what each condition showed.
- A data-flow note: which vendors receive audio, transcripts and hint lists.
- What was verified and what was assumed, and the review date of the references.

## Related

- [Speech pipeline](../voice-speech-pipeline/SKILL.md) and its [guide](../voice-speech-pipeline/references/speech-pipeline-guide.md#treat-transcripts-as-an-event-stream): transcript events, normalization and the voice output path.
- [Conversation design](../voice-conversation-design/SKILL.md) and its [transactions guide](../voice-conversation-design/references/transactions-and-handoffs.md): action contracts and uncertain writes.
- [Turn taking](../voice-turn-taking/SKILL.md): end-of-turn tuning and corrections during speech.
- [Call reliability](../voice-call-reliability/SKILL.md): transfers and recovery.
- [Phone compliance](../voice-phone-compliance/SKILL.md) and [agent security](../voice-agent-security/SKILL.md): recording, consent, card data, caller verification.

Sources reviewed 2026-09-30 UTC. Each reference lists its sources, the dates the pages show and what was left out. Open the cited page again before you rely on a provider limit or setting.
