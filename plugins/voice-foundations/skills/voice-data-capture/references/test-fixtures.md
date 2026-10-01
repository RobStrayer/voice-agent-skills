# Test set for spoken data capture

[Handbook](https://github.com/RobStrayer/voice-agent-skills/blob/main/docs/handbook.md) / [Data capture skill](../SKILL.md)

Reviewed **2026-09-30 UTC** using current provider documentation and standards pages. This is the review date, not a publication date. Provider and standards facts are linked where they appear. Paragraphs marked *Inference* are engineering judgment, not documented provider behavior. The fixtures are a starting set built from the failure shapes in the [protocols](entity-protocols.md). Add the wrong values your own calls produce. Do not run them against real customers, real people's voices or live card data.

## Contents

- What the tests measure
- Safe test data
- Conditions to cover
- Fixtures by field
  - Phone (PH)
  - Email (EM)
  - Names (NM)
  - Addresses (AD)
  - Dates and times (DT)
  - Amounts (AM)
  - Codes and reference numbers (CD)
  - Yes, no and negation (YN)
  - Private data and framework paths (PR)
- Aids and settings
- Pass criteria
- Sources

## What the tests measure

Test the whole capture flow and not only the recognizer. A wrong transcript that the flow catches and re-asks about is a pass. A wrong value that reaches a write is a failure, even when the transcript looked fine.

| Layer | Input | Catches | Speed |
| --- | --- | --- | --- |
| Code | Written transcripts, including wrong ones | Normalizers, read-back text, validators, the transcript-support check. The [script self-test](../scripts/readback.py) shows the pattern (`python scripts/readback.py --selftest`) | Seconds. Run on every change |
| Transcript replay | Recorded or written recognizer output fed into the flow | Retry ladder, corrections, confirmation binding, fallback | Minutes |
| Audio | Test audio through the real telephony path and recognizer | Accents, noise, codecs, turn splitting, aids and settings | Slower. Run on changes to the recognizer, aids or turn settings |
| Live call | A few calls on a test line with test accounts | Everything joined up, including the voice saying the read-back | Rarely |

The [evaluation skill](../../voice-agent-evaluation/SKILL.md) covers the harness. The [speech pipeline guide](../../voice-speech-pipeline/references/speech-pipeline-guide.md#build-a-pronunciation-fixture-set) covers pronunciation fixtures for the voice.

## Safe test data

- **Phone numbers.** In North America use 555-0100 through 555-0199, the only part of the 555 exchange reserved for fictional use. Other 555 numbers can be assigned, and the exchange is not reserved in area codes used for toll-free numbers ([Wikipedia, a secondary source](https://en.wikipedia.org/wiki/555_(North_American_Numbering_Plan)), edited 2026-09-01). For other countries, libphonenumber's `getExampleNumber` returns valid example numbers by region ([README](https://github.com/google/libphonenumber)). The README does not say they are unassigned, so treat them as format examples. Fixture numbers are for transcripts and recorded audio. Never dial them.
- **Emails.** Use `example.com`, `example.net` and `example.org`, or the reserved `.test`, `.example`, `.invalid` and `.localhost` top-level names ([RFC 2606](https://www.rfc-editor.org/rfc/rfc2606.html)).
- **Addresses.** Use your own test premises or a mocked validation service. Google's overview says USPS evaluates requests for artificially created addresses. If USPS identifies an input address as artificial, Google must stop validating addresses for the customer and report the customer's contact information, the input address and aggregated usage data to USPS. So do not send invented addresses to the real API ([overview](https://developers.google.com/maps/documentation/address-validation/overview)).
- **Names and voices.** Invented names. Speakers who have agreed to be recorded, or licensed text-to-speech voices. No real customer's recording unless your policy and consent allow it, and no cloned voice of a real person without documented consent ([security skill](../../voice-agent-security/SKILL.md)).
- **Cards.** Only the payment processor's published test numbers, in its test mode. Canary values should be unique to each run so you can search for them later ([red-team scripts, DX-1 to DX-3](../../voice-agent-security/references/red-team-scripts.md#data-exposure-dx)).

## Conditions to cover

Run each field's fixtures across these conditions, and record the condition with the result.

- **Speakers.** The accents and speaking styles of your real callers, from your own call data. Several speakers per fixture, not one.
- **Noise.** Street, car, office and TV. A clip with no speech at all.
- **Speed and pauses.** Fast speech, deliberate speech, long pauses inside a number, "um" and "uh".
- **Channel.** Telephone-quality audio, speakerphone and a compressed voice-over-IP leg. OpenAI's realtime transcription page says to test with telephony audio, accents and background noise, and its production checklist says to put numbers, dates, currency and email addresses in the evaluation set ([OpenAI](https://developers.openai.com/api/docs/guides/realtime-transcription)).
- **Languages.** Each language you serve, and the number, date and name forms of each locale. The fixtures below are written in English, so translate and extend them. The same page's checklist says to test each target language.
- **Turn boundaries.** An answer split across turns, the caller talking over the read-back, and a correction that starts mid-read-back.
- **Other voices.** Someone else in the room saying "yes", and the agent's own voice returning into the recognizer.
- **Several fields at once.** "My number is ... and my email is ...".

## Fixtures by field

"Assert" is what must hold. A note such as (script: the flag) marks the part of a row that `python scripts/readback.py --selftest` asserts. The rest needs your own flow tests, and the script does not parse speech into emails or codes. Numbers in the fixtures are fictional.

### Phone (PH)

| ID | Caller says, or condition | Assert |
| --- | --- | --- |
| PH-1 | "four one five, five five five, oh one two three" | Stored `+14155550123`. "oh" becomes 0. Read back as "plus one, four one five, five five five, zero one two three" (script: digit parsing and read-back) |
| PH-2 | The same digits run together, fast, in noise | The right value is stored, or the flow re-asks. No wrong value is written |
| PH-3 | One digit dropped: "four one five five five oh one two three" | The transcript-support check fails, nothing is written, the flow re-asks in groups (script: the check) |
| PH-4 | Number words: "four fifteen five fifty five oh one twenty three" | The number words are not turned into digits. The flow asks for the digits one at a time (script: the words are reported and the support check fails) |
| PH-5 | "double five", "double 5", "triple seven", and a value with three equal digits in a row | "double" and "triple" expand correctly, before words and numerals (script). The read-back says every digit and never "triple" (script) |
| PH-6 | After the read-back: "no, the last four are two zero one three" | Only the last group changes. The whole value is read back again. The old value is discarded and the attempt is logged |
| PH-7 | A pause after "four one five" ends the turn, then "five five five, zero one two three" | The two parts are joined, or the flow re-asks. A 3-digit number is never written |
| PH-8 | The answer window holds only noise, a TV or breathing | No value is proposed and nothing is written. No digits appear in the transcript that nobody said |
| PH-9 | A number in national format from a caller outside your assumed country | No country code is added silently. The flow names the country it assumes and gets a yes, or asks |
| PH-10 | "Use the number I'm calling from" | Caller ID is treated as a candidate. The last digits are read back and confirmed. The record notes the source |
| PH-11 | Ten keypad digits and `#`, then nine digits and `#` | Ten are accepted, the `#` is not part of the value, nine are re-asked. The keypad text is not parsed as speech |
| PH-12 | A filler or a homophone between digits: "four one five um five five five zero one two three", or "for" for "four" | The word breaks the run, so the support check fails and the flow re-asks (script) |
| PH-13 | The model proposes a value one digit shorter than what the caller said | Fails an exact-match check, nothing is written, and the flow re-asks (script: `--exact`) |
| PH-14 | A number word, or a "double" with no digit after it, at either end of the answer: "four one five five five five zero one two three twenty", "four one five five five five zero one two double" | The support check fails, with or without `--exact`, and the flow asks for the digits one at a time (script) |

### Email (EM)

| ID | Caller says, or condition | Assert |
| --- | --- | --- |
| EM-1 | "j, o, n, dot, s, m, i, t, h, four, two, at, example, dot, com" | Stored `jon.smith42@example.com`. Read back with letters spelled and digits as words. Digits are flagged (script: read-back and flags. It does not parse speech) |
| EM-2 | Spelling alphabet: "J as in Juliet, O as in Oscar, N as in November" | The letters are decoded, and no word from the alphabet appears in the address |
| EM-3 | "at gmial dot com" | The flow asks whether the caller means `gmail.com`. It never corrects silently (script: the flag) |
| EM-4 | "at company dot co" | `.co` is kept. The read-back spells the last part. It is not changed to `.com` |
| EM-5 | "it's john" / "smith" / "at example dot com" as three turns | The parts are joined before validation, or the flow re-asks. A partial address is never written |
| EM-6 | "john dot smith underscore 42 dash work" | The symbols are produced and read back as words (script: the read-back of the symbols) |
| EM-7 | Names with doubled letters, such as "anna" | Both letters are kept and said, and the doubled letter is flagged (script) |
| EM-8 | A long local part with `+` | The validator accepts it. It is not rejected only for being unusual (script: the `+` is accepted and said as "plus") |
| EM-9 | No `@`, two, or a domain with no dot | Rejected in code and re-asked (script) |
| EM-10 | A domain that does not exist | The flow asks again and writes nothing |

### Names (NM)

| ID | Caller says, or condition | Assert |
| --- | --- | --- |
| NM-1 | A common name, said and then spelled | The stored value is the spelled letters |
| NM-2 | A name your recognizer returns as an ordinary word (look in your own logs for examples) | The flow asks for spelling. The stored value is the spelled letters, not the heard word |
| NM-3 | "O apostrophe Neil", "Smith dash Jones" | The symbols are stored and the read-back says "apostrophe" and "dash" |
| NM-4 | "M as in Mike, no, N as in November" | The correction replaces one letter |
| NM-5 | Your keyterm list holds one name and the caller says and spells a near neighbor | The spelled value wins. Run it with and without the list |
| NM-6 | A name with accented or non-Latin characters | The value survives storage and read-back, or follows your stated rule for what you cannot store |
| NM-7 | The caller cannot or will not spell | After two attempts the flow uses the link or a person. The record is marked unverified |

### Addresses (AD)

| ID | Caller says, or condition | Assert |
| --- | --- | --- |
| AD-1 | A house number and street | The number is read back alone, then the street. A correction changes one part |
| AD-2 | "fifteen" and "fifty" for a house number | The flow asks for digits one at a time |
| AD-3 | "apartment four B" | The unit is captured and the letter is spelled back |
| AD-4 | An alphanumeric postcode, spelled | Handled with the code protocol. The letters are read back with the alphabet |
| AD-5 | A mocked validation result that inferred a component | The flow says what was added and waits for a yes before using it |
| AD-6 | A mocked result with an unconfirmed or missing component | The flow asks for that part. It does not guess |

### Dates and times (DT)

| ID | Caller says, or condition | Assert |
| --- | --- | --- |
| DT-1 | "next Friday" and "this Friday", asked on a Wednesday and on a Friday | Your stated rule is applied. The resolved date is read back with its weekday |
| DT-2 | "the fourth of March", "March fourth", "3/4" | Day and month are resolved by your locale rule and read back in words |
| DT-3 | "at two" with no AM or PM | The flow asks, or offers slots |
| DT-4 | A caller in a different time zone from the business | Stored with the IANA zone, the UTC instant and the anchor. Read back with the zone name |
| DT-5 | A local time that does not exist, or occurs twice, on a daylight-saving change | Flagged and re-asked. Not shifted silently |
| DT-6 | "Tuesday the fourteenth" when the fourteenth is another weekday | The flow asks which one is meant |
| DT-7 | A date of birth with a two-digit year | The full year is read back, using your stated rule |
| DT-8 | A past date for a booking | Rejected in code |
| DT-9 | "the second one" or "the later one" after a list of slots | Maps to one slot ID and reads it back. An unclear answer re-offers the list |

### Amounts (AM)

| ID | Caller says, or condition | Assert |
| --- | --- | --- |
| AM-1 | "fifteen" and "fifty" dollars | The amount is read back in words and digits before any write |
| AM-2 | "two fifty" | The flow asks whether that is two dollars fifty or two hundred fifty |
| AM-3 | "twelve hundred" and "one thousand two hundred" dollars | Both store the same integer, 120000 minor units, with the currency code `USD`. No float is stored |
| AM-4 | A different currency word from the flow's currency | The flow asks. The ISO 4217 code is stored |
| AM-5 | An amount above the caller's limit | Refused in code, not by the prompt |

### Codes and reference numbers (CD)

| ID | Caller says, or condition | Assert |
| --- | --- | --- |
| CD-1 | "B seven D four, P zero T nine" | Parsed to `B7D4P0T9`. Read back in groups with the alphabet for ambiguous letters (script: read-back and flags, not the parsing of speech) |
| CD-2 | A code with B, D, P, T and V, said fast | Ambiguous letters are flagged for the alphabet read-back (script: the flag). A wrong letter is caught by the check symbol or the lookup |
| CD-3 | "oh" inside a code whose alphabet has both 0 and O | The flow asks "zero, or the letter O?" |
| CD-4 | A code with one wrong character, and one with two characters swapped | The check symbol fails both. The flow re-asks before any lookup (script: the check symbol) |
| CD-5 | A code that does not exist, but is one character from a real one | No near match from another customer is offered. After two misses the flow changes channel |
| CD-6 | A long pause in the middle of the code | The turn is not ended early, or the parts are joined. Nothing is looked up on half a code |
| CD-7 | A numeric code on the keypad, and a short one | The exact digits are kept and a short entry is re-asked |
| CD-8 | A code whose check symbol is `*`, `~`, `$`, `=` or `U` | Not issued, or callers are given a spoken name for the symbol. `checksym` shows which codes get one (script) |

### Yes, no and negation (YN)

| ID | Caller says, or condition | Assert |
| --- | --- | --- |
| YN-1 | "I never took it" | Stored as negative. The read-back says "You did not take it" |
| YN-2 | "yeah, no" and "no, yeah" | Treated as unclear and asked again |
| YN-3 | "uh-huh" or "okay" during the read-back | Not a confirmation |
| YN-4 | A "yes" that answers an earlier question | Not bound to the pending question. The flow asks again |
| YN-5 | A lint over your prompts | No question is worded negatively, and none joins two claims with "or" |
| YN-6 | Silence after the read-back | Not a yes. The read-back is repeated once, then the channel changes |
| YN-7 | Another person says "yes", or the agent's own words return into the recognizer | Not counted as the caller's confirmation |
| YN-8 | "stop" at any point, including during a read-back | It is not a yes to the value. The flow stops, writes the suppression first, and says it is done only if the write succeeded, with no confirmation question ([stop requests](../../voice-phone-compliance/references/numbers-data-and-call-behavior-guide.md#stop-requests)) |
| YN-9 | "cancel" while a booking exists | The flow asks whether the caller means the booking or the flow. A booking cancel is read back with its exact details and confirmed before it is written |

### Private data and framework paths (PR)

| ID | Condition | Assert |
| --- | --- | --- |
| PR-1 | A canary value shaped like a card number, taken from the processor's published test numbers, is spoken when payment is asked for | The agent sends the caller to the keypad path. The digits appear in no transcript, prompt, log, trace or analytics event. Search every store, as in DX-3 |
| PR-2 | The same canary keyed on the keypad | The digits reach only the payment or verification service. They are not in the model's context. Check what your framework does with keypresses ([by framework](ask-and-read-back.md#keypad-input-by-framework)) |
| PR-3 | A caller asks the agent to read back the phone or email on file, before verification | Refused. The caller is asked to say the value, and code compares it |
| PR-4 | A framework capture task is used for a field | Its result goes through the same gate as a spoken proposal, and `require_explicit_ask` is set where needed ([validate and store](validate-and-store.md#use-framework-capture-tasks-with-care)) |

## Aids and settings

Run the field fixtures with the aid or setting on and off, on the same audio: keyterms, phrase lists, `numerals`, and the end-of-turn values for long answers ([recognition aids](recognition-aids.md)). The speech pipeline guide makes the same point: provider benchmarks do not establish your task's accuracy, so compare short answers, identifiers and turn boundaries on your own audio ([guide](../../voice-speech-pipeline/references/speech-pipeline-guide.md#check-model-and-text-transform-changes-before-migrating)).

*Inference:* also test the spoken form. Synthesize each read-back with the shipped voice, run it through a phone-quality path and your recognizer, and assert that the digits you meant come back. It catches a voice that reads a bare string as one big number, or says zero as the letter O ([read-back guide](ask-and-read-back.md#make-the-voice-say-it-correctly)).

## Pass criteria

- **Count runs, and show the denominator.** Write "0 wrong writes in N runs" with your real N, never "0% wrong". Zero in a small run does not show the true rate is zero.
- **Score the value, not the transcript.** *Inference:* word error rate averages across a whole transcript, so it can look fine while one digit is wrong. Score each fixture on an exact match of the canonical value, and report separately: right write, wrong write, safe re-ask, fallback.
- **A wrong write is the failure that counts.** A safe re-ask costs the caller time, so track it, but it is not a wrong value.
- **Track empty, truncated and delayed transcripts on their own,** as OpenAI's checklist says, apart from word error rate.
- **Set thresholds with the owner of each field.** They depend on what a wrong value costs. This guide gives none, because no source supplies a number that fits your calls.
- **Keep a per-field table** of attempts, corrections, fallbacks, wrong writes and which check caught each miss. The fields corrected most are the ones to give an aid, a fixture and a fallback first.

## Sources

Retrieved 2026-09-30. "Shown" is a date printed on the page, when there was one. Context7 was not used for this file.

| Source | Supports | Shown |
| --- | --- | --- |
| [555 (North American Numbering Plan)](https://en.wikipedia.org/wiki/555_(North_American_Numbering_Plan)) | The reserved fictional range, and the toll-free exception. A secondary source | Edited 2026-09-01 |
| [RFC 2606](https://www.rfc-editor.org/rfc/rfc2606.html) | Reserved example domains and top-level names | 1999-06 |
| [libphonenumber README](https://github.com/google/libphonenumber) | Example numbers by region | none shown |
| [Google Address Validation overview](https://developers.google.com/maps/documentation/address-validation/overview) | Artificially created addresses | Updated 2026-09-24 |
| [OpenAI realtime transcription](https://developers.openai.com/api/docs/guides/realtime-transcription) | Evaluation checklist | none shown |

The rows are an engineering starting set built from the cited failure shapes. No provider requests, audio tests or accuracy measurements were run to write this file. The script self-test is the only code that ran.
