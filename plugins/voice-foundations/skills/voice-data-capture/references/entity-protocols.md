# Capture protocols by field type

[Handbook](https://github.com/RobStrayer/voice-agent-skills/blob/main/docs/handbook.md) / [Data capture skill](../SKILL.md)

Reviewed **2026-09-30 UTC** using current provider documentation, standards pages and the papers cited below. This is the review date, not a publication date. Provider, standards and paper facts are linked where they appear, and [Sources](#sources) lists each page, any date it shows and when it was retrieved. Paragraphs marked *Inference* are engineering judgment, not something a source says. The protocols are engineering recommendations. Group sizes, retry counts and similar numbers are starting defaults to tune on your own calls, not findings.

## Contents

- Find your field
- Rules for every field
- Why letters and digits get mixed up
- Phone numbers
- Email addresses
- Names
- Addresses and postcodes
- Dates and times
- Amounts and currency
- Codes and reference numbers
- Yes, no and negation
- Sources

## Find your field

| Field | What goes wrong | Section |
| --- | --- | --- |
| Phone number | Dropped, swapped or merged digits; wrong country | [Phone numbers](#phone-numbers) |
| Email address | Letters, symbols and domains; answer split across turns | [Email addresses](#email-addresses) |
| Name | A common word replaces the real name; spelling differs | [Names](#names) |
| Address, postcode | Number or street wrong; parts missing | [Addresses and postcodes](#addresses-and-postcodes) |
| Date, time | Relative dates, day and month order, AM or PM, time zone | [Dates and times](#dates-and-times) |
| Amount | Fifteen and fifty, missing units, currency | [Amounts and currency](#amounts-and-currency) |
| Code, account or reference number | Look-alike letters, zero and O, long strings | [Codes and reference numbers](#codes-and-reference-numbers) |
| Yes, no, negation | Flipped polarity, an answer to an earlier question | [Yes, no and negation](#yes-no-and-negation) |
| Card number, PIN, government ID | Reaches the transcript and the model | [Keep sensitive data off the model path](../SKILL.md#keep-sensitive-data-off-the-model-path) |

## Rules for every field

1. **One field per turn.** Ask for one thing, wait for it, read it back, then move on. If the caller gives two fields in one answer, accept both but confirm each on its own.
2. **The caller's words are the only source of a value.** The model may help parse them. It must not add, complete or "fix" digits or letters from context, from the customer record or from what it expects. Check in code that every digit came from this caller's speech or keypad ([transcript-support check](validate-and-store.md#check-that-the-transcript-supports-the-value)).
3. **Read back from code, in a form the caller will recognize.** Then listen for a correction.
4. **A confirmation belongs to one value.** "Yes" confirms the value just read, for this field, and nothing else.
5. **Noise, silence and off-topic speech mean "no value".** A study of the Whisper model found that non-speech audio induces hallucinated text, and that a set of the same hallucinations appears often ([arXiv 2501.11378](https://arxiv.org/abs/2501.11378)). An empty or odd transcript leads to a re-ask, never to a guess.
6. **Two misses, then change channel.** Start with two voice attempts per field, then keypad, a link or a person ([give the caller a way out](ask-and-read-back.md#give-the-caller-a-way-out)).

## Why letters and digits get mixed up

Some letters sound alike. Cole and Fanty's 1990 paper on spoken letter recognition names fine distinctions a recognizer must make, such as B and D, B and P, D and T, T and G, C and Z, V and Z, M and N, and J and K. It also says almost all "E-set" and M-N confusions are with other letters in the same set ([ACL Anthology H90-1075](https://aclanthology.org/H90-1075/)). The paper does not list the E-set members in the text I read. The usual nine are B, C, D, E, G, P, T, V and Z (common usage, not from the paper). The paper describes two systems, one for letters spoken in isolation and one for letters spoken with brief pauses, which it used to retrieve spelled names. Its speech came from American English speakers, recorded at 16 kHz with a noise-canceling microphone. That is not telephone audio, so read the paper as a list of pairs to watch and not as error rates for your calls. Letters and digits also look alike: Crockford's Base32 leaves out I and L (which can be confused with 1) and O (which can be confused with 0) ([Crockford](https://www.crockford.com/base32.html)).

| Symbols | What to do |
| --- | --- |
| B C D E G P T V Z (the E-set) | Read back with the spelling alphabet, and accept it from the caller |
| M and N | Same |
| J and K | Same |
| 0 and O; 1, I and L | Say "zero" for the digit. Say "the letter O" or "O as in Oscar" for the letter |

**Spelling alphabet.** Read back with the ICAO and NATO code words: Alfa, Bravo, Charlie, Delta, Echo, Foxtrot, Golf, Hotel, India, Juliett, Kilo, Lima, Mike, November, Oscar, Papa, Quebec, Romeo, Sierra, Tango, Uniform, Victor, Whiskey, X-ray, Yankee, Zulu. The [alphabet's Wikipedia page](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet) is a secondary source, and it is not consistent about X-ray: it lists the words as ICAO spellings but shows Xray, and it says NATO changed X-ray to Xray. Spell the word the way your voice pronounces it best. The page also notes that information technology workers have used the code words to read out long serial numbers and reference codes by voice. Callers will use their own words ("D as in David"). Decode by the letter they say. If the caller gives a letter and a word and the word starts with a different letter, ask again. *Inference:* if your voice mispronounces "Alfa" or "Juliett", use "Alpha" and "Juliet". A recognizer may also return a spoken letter as an ordinary word, such as "be" or "tea", so build a mapping from your own test audio and test it.

## Phone numbers

**Ask.** "What number should we call you back on? You can say it in groups, like four one five, five five five, zero one two three, or type it on your keypad and press pound." If you have caller ID, offer it first: "Is it the number you're calling from, ending in zero one two three?" That turns ten digits of dictation into a yes or no. Caller ID is a hint, not proof of identity ([security guide](../../voice-agent-security/references/security-guide.md#caller-id-is-a-claim)).

**Decide the country by rule, and say it.** Use your service area, the caller ID country or a question. Never guess silently. Twilio's Lookup page says `CountryCode` defaults to US when you send none. It also warns that in some cases a non-US number in national format, with no `+` and no `CountryCode`, is processed as valid, which it calls unintended behavior that could give an ambiguous validation response ([Lookup v2](https://www.twilio.com/docs/lookup/v2-api)).

**Normalize in code.** Turn words, numerals, "oh", "double", "triple" and "plus" into a digit string, and strip separators. If number words like "fifteen" or "fifty" appear, do not guess whether they mean 1 5, 5 0 or 15: ask for the digits one at a time. Store E.164: a `+`, a country code that never starts with 0, and at most 15 digits in all ([Twilio on E.164](https://www.twilio.com/docs/glossary/what-e164), [ITU-T E.164](https://www.itu.int/rec/T-REC-E.164/en)).

**Read back.** Digits in groups with a pause between groups, "zero" for 0, every digit as a word in your own text. If your code added the country code, say it ("plus one") so the caller can correct it. US, Canadian and other +1 numbers read as 3, 3 and 4. For other countries take the national grouping from a phone library. [`readback.py`](../scripts/readback.py) falls back to groups of three, which is a speaking aid and not a national format, and `--cc 44` keeps a country code in its own group. Ask once, "Is that right?", and listen for "no, the last four are ...".

**Validate.** Use libphonenumber or Twilio's Basic Lookup. In libphonenumber, `isPossibleNumber` checks length only, and `isValidNumber` checks length and prefix for a region ([README](https://github.com/google/libphonenumber)). The README lists its Python port as a third-party port, from developers outside the project. Basic Lookup returns `valid` and `validation_errors`, and needs `CountryCode` for national-format numbers ([Lookup v2](https://www.twilio.com/docs/lookup/v2-api)). Twilio says a regular expression cannot guarantee a match with a valid number ([E.164 glossary](https://www.twilio.com/docs/glossary/what-e164)). A valid number is not proof that it belongs to this caller.

**Fall back.** Keypad digits ending on `#`, the caller ID number, a link to a form, or a person ([ways out](ask-and-read-back.md#give-the-caller-a-way-out)).

## Email addresses

**Avoid voice when you can.** An address mixes letters, digits, punctuation and a domain in one string, and short silence settings can split it across turns ([example with settings](recognition-aids.md#change-settings-for-the-field-you-are-collecting)). If the caller has a screen, send a link to a form ([text a link](ask-and-read-back.md#text-a-link)). If you already hold an address, do not read it out until the caller has reached the verification level that allows it ([security guide](../../voice-agent-security/references/security-guide.md#social-engineering-by-voice)); let them say a new one instead.

**Ask.** "Please spell the part before the at sign, one letter at a time." Then: "And the part after the at sign? If it's gmail, outlook, yahoo or iCloud, just say the name."

**Normalize in code.** Keep the tables in your code and test them with fixtures. Map "at" to `@`, and "dot", "underscore", "dash" or "hyphen" and "plus" to their symbols. Map "g mail" to "gmail", and handle "dot com" and "dot c o m". Handle the pattern where callers say a word and then spell it ("john, j o h n"). Some frameworks ship this. LiveKit's `GetEmailTask` converts "dot", "underscore", "dash" and "plus" and recognizes spelled-out words, is in beta and is run by an LLM ([GetEmailTask](https://docs.livekit.io/agents/prebuilt/tasks/get-email/)). Validate its result in code anyway. Spoken letters carry no case, so `readback.py` lowercases the address. RFC 5321 treats a local part as case-sensitive but discourages relying on that ([section 2.4](https://www.rfc-editor.org/rfc/rfc5321.html)).

**Read back.** Spell the part before the `@` letter by letter, using the alphabet for ambiguous letters. Say punctuation as words and digits as digit words. Say common domains as words and spell the rest. Pause after "at". `python scripts/readback.py email "jon.smith42@example.com"` prints `j, o, n, dot, s, m, i, t, h, four, two, at, e, x, a, m, p, l, e, dot, com`. It does not add the spelling alphabet, so apply that to the ambiguous letters in your own read-back. It flags digits, punctuation, doubled letters and domains that look like one in its short provider list (`PROVIDERS`, which you should replace with your own). It accepts only letters, digits and `. _ + - '` before the `@`, which is narrower than the address grammar: RFC 5321 also allows a quoted local part ([section 4.1.2](https://www.rfc-editor.org/rfc/rfc5321.html)). Widen it if your callers need more, and when it stops, ask the caller to spell the address.

**Validate.** Exactly one `@`, text on both sides, a dot in the domain. If the domain is close to a common provider (gmial.com, gmail.co), ask "did you mean gmail.com?" and never fix it silently. A DNS lookup catches domains that do not exist. RFC 5321's lookup rules report a non-existent domain as an error, and treat an empty list of MX records as an implicit MX pointing at the host ([RFC 5321 section 5.1](https://www.rfc-editor.org/rfc/rfc5321.html)). A domain that publishes a null MX, a single MX record with preference 0 and a "." target, is saying it accepts no mail, so count that as a failed check ([RFC 7505](https://www.rfc-editor.org/rfc/rfc7505.html)). *Inference:* such a check cannot catch a real domain that is the wrong one, and it cannot show the mailbox exists. Do not reject an address only because it looks unusual. The only proof that an address works and belongs to the caller is a message they act on, so treat it as unverified until then.

**Fall back.** A link to a form, or a person.

## Names

**Spell, don't guess.** A name is open vocabulary, and a recognizer can return a familiar word in its place. A keyterm or phrase list raises the chance that a listed term appears, including when the caller said something else: Google's adaptation page warns that boosting can add words to the transcript that were not spoken ([model adaptation](https://cloud.google.com/speech-to-text/v2/docs/adaptation-model)). Treat the heard name as a first guess and the spelled name as the value.

**Ask.** "Please say your last name, then spell it for me." Collect first and last names in separate turns unless your system needs one field. LiveKit's beta `GetNameTask` does this with optional spelling verification, letter-by-letter and phonetic-alphabet input, and "dash" and "apostrophe" conversion ([GetNameTask](https://docs.livekit.io/agents/prebuilt/tasks/get-name/)).

**Normalize.** Letter by letter, with hyphens, apostrophes and spaces. Keep the spelling the caller confirmed, including accents if your systems can store them. Do not "correct" it to a dictionary word or to a near match in your records.

**Read back.** Spell each part in chunks, with the alphabet for ambiguous letters, then ask "Is that right?". Accept a one-letter correction: "No, M as in Mike."

**Validate.** Length and allowed characters in your own system. If you use the name to look up a record, treat it as a search key and do not read anything from the record until the caller is verified.

**Fall back.** A person, or a form. Decide in advance how you will store a name your system cannot represent exactly.

## Addresses and postcodes

**Collect in parts and confirm each.** Number, street, unit, postcode or ZIP, then town. Read the number back on its own as digits ("one, five, one"), then the street. *Inference:* numbers and street names fail in different ways, so confirm them separately. Where a postcode plus a house number identifies a delivery point, collect just those two and look up the rest, after checking that your country's address data supports it.

**Use a lookup, not memory.** Send the parts to an address validation service and read back the standardized result. Google's Address Validation API returns a `verdict` with `addressComplete`, `hasUnconfirmedComponents`, `hasInferredComponents`, three granularity fields and `possibleNextAction` ([understand the response](https://developers.google.com/maps/documentation/address-validation/understand-response)). Check its coverage list for your countries ([overview](https://developers.google.com/maps/documentation/address-validation/overview)). Then:

- Incomplete or unconfirmed: ask for the missing or unclear part. Do not guess.
- Inferred component: say what was added and get a yes before you use it.
- Not validated: keep the address marked "unverified" and send it to a person.

**Postcodes.** Alphanumeric postcodes are letters and digits, so use the [code protocol](#codes-and-reference-numbers). Numeric ZIP or postal codes are digits in groups, with the keypad as a fallback. Google's speech-to-text class tokens for English (United States) include `$ADDRESSNUM` and `$POSTALCODE`, and `$STREET`, which covers numbered street names only, such as "fifty first" as 51st ([class tokens](https://cloud.google.com/speech-to-text/docs/class-tokens); see [recognition aids](recognition-aids.md)).

**Privacy.** The address goes to a third-party service, so check its terms. Do not read an on-file address to an unverified caller; let them say theirs.

**Fall back.** A link with address autocomplete, or a person.

## Dates and times

**Ask with an anchor and a format, or offer choices.** "What day works? You can say, for example, Tuesday the fourteenth." When the set is small, offer it: "I have Tuesday at two, Wednesday at ten, or Thursday at four." *Inference:* picking from a short list is safer than an open date, and it turns capture into a choice.

**Resolve in code.** Store an anchor (today's date and the caller's time zone) and resolve relative words against it. "Next Friday", "this Friday" and "Friday week" mean different things to different people, so choose a rule and show the result, or ask. Settle day and month order from the locale or by asking. Two-digit years need a rule and a full-year read-back. LiveKit's beta date-of-birth task handles two-digit years (its page gives "90" becoming 1990) and rejects future dates ([GetDOBTask](https://docs.livekit.io/agents/prebuilt/tasks/get-dob/)). Choose your own century rule, and read the full year back ("nineteen ninety") so the caller can correct it.

**Read back.** Weekday, month name, day, time with AM or PM, and the zone name, all from the resolved value: "Tuesday, March fourteenth, at two thirty in the afternoon, Eastern time." Say month names. Numeric dates depend on the markup and its defaults, and a provider's own date example can change the day with a `format` setting ([provider table](ask-and-read-back.md#make-the-voice-say-it-correctly)).

**Validate.**

- The date exists. If the caller gave a weekday and a date and they disagree ("Tuesday the 14th" when the 14th is a Wednesday), ask which.
- It is in the allowed range, and it fits the calendar and business hours.
- The local time exists and is not ambiguous: clocks skip or repeat an hour at daylight-saving changes.
- Zones are IANA IDs such as America/New_York, not abbreviations. The database changes with political decisions, so keep your tz data current ([IANA Time Zone Database](https://www.iana.org/time-zones)). Python's `zoneinfo` reads it and falls back to the `tzdata` package when the system has no data ([zoneinfo](https://docs.python.org/3/library/zoneinfo.html)).

**Store** the local date and time, the IANA zone ID, the resolved UTC instant and the anchor you used.

**Fall back.** Offer slots again, send a link, or use a person.

## Amounts and currency

**Prefer your own numbers.** If your system knows the amount (an order total, a balance), say it. When the caller must give one, ask with units: "How much, in dollars and cents?"

**Normalize to integer minor units and an ISO 4217 currency code. Never a float.** The number of minor-unit digits depends on the currency. For currencies that have minor units, ISO 4217 shows whether they divide into 100 or 1000 ([ISO 4217](https://www.iso.org/iso-4217-currency-codes.html)), so look the exponent up in a table and do not assume two decimal places. "Two fifty" can be 2.50 or 250, and "fifteen" and "fifty" sound alike: ask when the unit is missing.

**Read back** in words, then in digits when the amount is large or moves money: "one thousand two hundred fifty dollars, that's one, two, five, zero." Send the voice the spoken form, because voices read numbers differently ([provider table](ask-and-read-back.md#make-the-voice-say-it-correctly)).

**Validate.** Bounds, an accepted currency, business rules (a refund no larger than the payment) and whether this caller may take this action. Capture card details on the keypad path and never by voice through the model ([privacy](../SKILL.md#keep-sensitive-data-off-the-model-path)).

**Fall back.** A person.

## Codes and reference numbers

**Design codes for speech if you issue them.** Use an alphabet without look-alikes: Crockford's Base32 leaves out I, L, O and U, reads I and L as 1 and O as 0 when decoding, and allows hyphens for grouping. It also defines an optional check symbol (the code read as a number, modulo 37) that detects wrong and transposed symbols, so your code can reject a misheard code before any lookup ([Crockford](https://www.crockford.com/base32.html); `python scripts/readback.py checksym 16J` prints `16JD`). Five of the 37 possible check symbols fall outside the 32 ordinary symbols: `*`, `~`, `$` and `=`, which callers cannot say as a letter, and `U`, which the code alphabet leaves out. Issue only codes whose check symbol is one of the 32 ordinary symbols, or teach callers spoken names for the five. `checksym` marks them. Use digits only if you can, so the keypad works.

**Ask** with the length and the method: "It has eight characters. Please say them one at a time. You can use words like B as in Bravo." Relax end-of-turn for this field so a pause between characters does not split the code ([settings for the field](recognition-aids.md#change-settings-for-the-field-you-are-collecting)).

**Normalize.** Fold case, strip spaces and hyphens, map spelling-alphabet words to letters, check the length. "Oh" inside a code is ambiguous: ask "zero, or the letter O?" unless your alphabet has no O.

**Read back** in groups of about four, using the alphabet for ambiguous letters (`python scripts/readback.py code "B7D4-P0T9"` prints the plain groups and the same groups with the alphabet). Let the caller correct by position: "the third character".

**Validate** format, length and check symbol in code, then look the code up. If the lookup fails, do not offer near matches from other customers' records: a close code can belong to someone else. Suggest near matches only from codes already scoped to this verified caller. After two misses, move the entry to another channel: a link to a form where the caller types the code, the caller's app, or a person.

## Yes, no and negation

**Ask questions that have one yes.** One claim per question. No negative questions ("You don't want a reminder, right?"). No "or" questions that "yes" answers. For choices, give the options: "morning or afternoon?".

**Constrain the answer** to yes, no or unclear, taken from the caller's words and bound to the pending question. "Uh-huh", "okay", "yeah, no", "no, yeah", silence, and a late answer to an earlier question are all unclear: ask again. Google's confirmations guidance says not to confirm a plain yes or no answer, so spend read-backs on claims where a flipped polarity costs something, not on every answer ([Google confirmations](https://developers.google.com/assistant/conversation-design/confirmations)).

**Read negation back in full** for anything that matters: "You did not take the medication. Is that right?" The failure shape is documented outside phone agents. An ABC News report on clinical AI scribes cites mistakes listed in a Digital Rights Watch report, where a scribe recorded the wrong breast and said someone had epilepsy when they did not. It also quotes a GP saying a scribe can say right when the doctor said left ([ABC News, 14 August 2026](https://www.abc.net.au/news/2026-08-14/ai-medical-scribe-error-leaves-patient-devastated/107031672)). It is a news report about a different kind of product, so use it as an example of the failure and not as a rate. Keep audio offsets so a person can check.

**Stop and opt-out requests need no confirmation before you act.** Act on them at once: write the suppression first, then tell the caller it is done only if the write succeeded ([stop requests](../../voice-phone-compliance/references/numbers-data-and-call-behavior-guide.md#stop-requests)).

**Validate.** The answer is one of the allowed values, and a "yes" that arrives with no pending question does nothing.

## Sources

Retrieved 2026-09-30 by fetching each page. "Shown" is a date printed on the page; a retrieval date is not the provider's publication date. Context7 was not used for this file, because it relies on standards, papers and pages outside any library's documentation.

| Source | Supports | Shown |
| --- | --- | --- |
| [Cole and Fanty, Spoken Letter Recognition (1990)](https://aclanthology.org/H90-1075/) | Fine letter distinctions, E-set and M-N confusions, recording conditions | 1990 |
| [Crockford Base32](https://www.crockford.com/base32.html) | Excluded letters, decoding rules, check symbol | 2002-11-02 and 2019-03-04 both appear |
| [NATO phonetic alphabet (Wikipedia)](https://en.wikipedia.org/wiki/NATO_phonetic_alphabet) | Code words, use for codes by telephone. A secondary source: its ICAO list shows Xray, and it says elsewhere that ICAO keeps X-ray | Edited 2026-09-17 |
| [Twilio E.164 glossary](https://www.twilio.com/docs/glossary/what-e164) | E.164 rules, regex caveat | none shown |
| [ITU-T E.164](https://www.itu.int/rec/T-REC-E.164/en) | Recommendation in force (02/26) | Updated 2026-04-30 |
| [libphonenumber README](https://github.com/google/libphonenumber) | Possible and valid checks | none shown |
| [Twilio Lookup v2](https://www.twilio.com/docs/lookup/v2-api) | Basic validation, `CountryCode` default and warning | none shown |
| [RFC 5321](https://www.rfc-editor.org/rfc/rfc5321.html), [RFC 7505](https://www.rfc-editor.org/rfc/rfc7505.html) | Mail routing lookup rules, local part case and syntax, null MX | 2008-10 and 2015-06 |
| LiveKit [email](https://docs.livekit.io/agents/prebuilt/tasks/get-email/), [name](https://docs.livekit.io/agents/prebuilt/tasks/get-name/) and [date of birth](https://docs.livekit.io/agents/prebuilt/tasks/get-dob/) tasks | What each task handles (beta) | none shown (the pages print a render time only) |
| [Google speech-to-text adaptation](https://cloud.google.com/speech-to-text/v2/docs/adaptation-model), [class tokens](https://cloud.google.com/speech-to-text/docs/class-tokens) | Boost side effects, address class tokens | Updated 2026-09-24 |
| [Google Address Validation](https://developers.google.com/maps/documentation/address-validation/understand-response), [overview](https://developers.google.com/maps/documentation/address-validation/overview) | Verdict fields, coverage list | Updated 2026-09-24 |
| [Google Conversation Design: Confirmations](https://developers.google.com/assistant/conversation-design/confirmations) | No confirmation of plain yes or no answers. The page belongs to Conversational Actions, which Google deprecated in 2023, so it is used for the pattern only | Updated 2024-09-18 |
| [IANA Time Zone Database](https://www.iana.org/time-zones) | Database updates; release 2026e | Released 2026-09-29 |
| [Python zoneinfo](https://docs.python.org/3/library/zoneinfo.html) | IANA support, `tzdata` fallback | none shown |
| [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html) | Currency codes, minor units | none shown |
| [ABC News, 14 August 2026](https://www.abc.net.au/news/2026-08-14/ai-medical-scribe-error-leaves-patient-devastated/107031672) | Polarity and side errors in clinical scribes | Dated 2026-08-14 |
| [arXiv 2501.11378](https://arxiv.org/abs/2501.11378) | Whisper hallucination on non-speech audio | 2025-01-20 |

No provider requests, audio tests or accuracy measurements were run to write this file. The script self-test is the only code that ran.
