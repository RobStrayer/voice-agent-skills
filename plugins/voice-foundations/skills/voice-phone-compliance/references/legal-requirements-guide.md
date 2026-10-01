# Legal requirements for AI phone agents

[Handbook](https://github.com/RobStrayer/voice-agent-skills/blob/main/docs/handbook.md) / [Phone compliance skill](../SKILL.md)

**This is not legal advice.** It is a research summary for developers and their coding agents. Rules differ by country, state, call type and industry, and some points are unsettled. Confirm your plan with counsel for every place you call, call from, or record.

Checked against primary sources on **September 30, 2026 UTC**. This is a check date, not a publication date. "Opened" means I fetched the page that day and read the passage I cite, in full or as an extract returned by a scraper. CFR text came from the eCFR API for September 28, 2026, and the links point to the same sections on the eCFR site. A line marked "secondary" rests on a law-firm, news or advocacy summary, not on the law itself. A line that says "not opened" or "not read" is a pointer only. Laws in this area change often. Re-open the source before you rely on a claim for a launch.

## Contents

- Find the rule
- US federal law
  - AI voices count as artificial or prerecorded voices
  - Who can sue, and what it costs
  - Consent: which kind do you need?
  - What the call must say and offer
  - Stop requests
  - Lists, hours and abandoned calls
  - Caller ID
  - Voicemail
- State telemarketing laws
- AI disclosure
- Recording and transcripts
- Outside the US
  - European Union
  - United Kingdom
  - Canada
- Unsettled and unverified

## Find the rule

| Question | Start here |
| --- | --- |
| Do I need consent to call someone with an AI voice? | [Consent](#consent-which-kind-do-you-need) |
| What must the call say and offer at the start? | [Identification and opt-out](#what-the-call-must-say-and-offer) |
| Someone said "stop". What now? | [Stop requests](#stop-requests) |
| Which lists, hours and pacing rules apply? | [Lists, hours and abandoned calls](#lists-hours-and-abandoned-calls) |
| Which caller ID rules apply? | [Caller ID](#caller-id) |
| Do states add rules for automated calls? | [State telemarketing laws](#state-telemarketing-laws) |
| Must I say it is AI? | [AI disclosure](#ai-disclosure) |
| Can I record or transcribe the call? | [Recording and transcripts](#recording-and-transcripts) |
| Calling or answering in Europe, the UK or Canada? | [Outside the US](#outside-the-us) |
| What is unsettled or unverified? | [Unsettled and unverified](#unsettled-and-unverified) |

Caller ID reputation, HIPAA, PCI, retention, call scripts and consent logs are in the [numbers, data and call behavior guide](numbers-data-and-call-behavior-guide.md).

## US federal law

### AI voices count as artificial or prerecorded voices

- The Telephone Consumer Protection Act (TCPA) limits calls made with an autodialer and, separately, calls that use an "artificial or prerecorded voice" ([47 U.S.C. § 227(b)](https://www.law.cornell.edu/uscode/text/47/227)). A voice agent falls under the voice limit even if your dialer is not an autodialer.
- The FCC's Declaratory Ruling FCC 24-17 (adopted February 2, 2024; CG Docket 23-362) says the limit covers current AI that generates human voices (paragraph 2), including voice cloning (paragraph 5). It says there is no carve-out for technology that acts like a live agent (paragraph 6), and that a human choosing what the voice says does not change the result (paragraph 8). The identification and opt-out rules in 47 CFR 64.1200(b) apply to these calls (paragraph 9). Telemarketing calls need written consent (note 13). [FCC 24-17](https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf)
- Courts are not bound by the FCC's reading. In *McLaughlin Chiropractic Associates v. McKesson* (U.S. June 20, 2025) the Supreme Court held that district courts in civil suits decide what the TCPA means for themselves ([opinion at Justia](https://supreme.justia.com/cases/federal/us/606/23-1226/)). The Ninth Circuit has described an "artificial voice" as including a sound resembling a human voice that is originated by AI, in a case holding that silent text messages are not voice messages (*Trim v. Reward Zone USA*, 76 F.4th 1157, 1163 (9th Cir. 2023), cited in FCC 24-17 note 16). Plan as if the FCC's reading holds.
- **Proposed, not final.** FCC 24-84 (adopted August 7, 2024) proposes to define an "AI-generated call", to add consent-form language about AI calls, and to require a disclosure at the start of each call that it uses AI ([FCC 24-84](https://docs.fcc.gov/public/attachments/FCC-24-84A1.pdf)). The rule text has no AI provision today ([47 CFR 64.1200 in the eCFR, current through September 28, 2026](https://www.ecfr.gov/current/title-47/part-64/section-64.1200)).

### Who can sue, and what it costs

- A called person can sue for the greater of actual loss or $500 per violation. A court may triple that for willful or knowing violations ([47 U.S.C. § 227(b)(3)](https://www.law.cornell.edu/uscode/text/47/227)).
- The default federal time limit is four years for claims under laws passed after December 1, 1990 ([28 U.S.C. § 1658(a)](https://www.law.cornell.edu/uscode/text/28/1658)). The TCPA dates from 1991. That is my reading of the statute; I did not open a case applying it. Keep consent evidence at least four years after the last call (five years for telemarketing consent records, under 16 CFR 310.5), and ask counsel whether state claims need longer.
- The FTC can add civil penalties under its Telemarketing Sales Rule (TSR). Its guide lists $53,088 per violation, adjusted yearly ([FTC guide](https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule)).

### Consent: which kind do you need?

| Your call | Number called | Federal consent for an AI voice | Rule |
| --- | --- | --- | --- |
| Sales, marketing or other telemarketing | Mobile, or a home landline | Prior express **written** consent | 64.1200(a)(2), (a)(3) |
| Not sales (service, reminder, notice) | Mobile | Prior express consent | (a)(1) |
| Not sales | Home landline | Prior express consent, unless a narrow exemption fits. Examples: three calls in any 30 days if you honor opt-outs; HIPAA health-care messages at most once a day and three a week | (a)(3)(ii) to (v) |
| Emergency purpose | Any | None | (a)(1), (a)(3)(i) |

Source for the table and the points below: [47 CFR 64.1200](https://www.ecfr.gov/current/title-47/part-64/section-64.1200).

- **Written consent** is a signed agreement (an e-signature counts) that clearly authorizes *the seller* to deliver telemarketing with an autodialer or artificial or prerecorded voice and names the number. It must carry a clear disclosure that signing authorizes such calls and is not a condition of any purchase ((f)(9)).
- **No business-relationship shortcut.** The FTC says an established business relationship lets a seller place live calls to numbers on the registry, but not automated calls or robocalls ([FTC guide](https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule)).
- **Lead lists.** On January 24, 2025 the Eleventh Circuit vacated the FCC's 2023 "one-to-one" consent rule, and the matching rule that consent must be "logically and topically associated" with the interaction that prompted it ([*Insurance Marketing Coalition v. FCC*, No. 24-10277](https://media.ca11.uscourts.gov/opinions/pub/files/202410277.pdf), opinion opened). The current definition in (f)(9) still says the agreement must authorize "the seller". Ask any lead vendor for the exact consent text, timestamp, page and named seller. A line that says "our partners" is weak evidence. Have counsel read it.
- **Reassigned numbers.** A number can change hands after consent. The safe harbor in (m) helps only a caller who queried the FCC's reassigned-number database and can show it. The caller carries the burden of proof. Query before calling numbers with older consent.
- **Business numbers.** The FTC says most calls to businesses are outside its rule and the registry does not cover business-to-business calls ([FTC guide](https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule)). The AI-voice consent rule for mobile numbers still applies, and many owners use mobile phones. Treat such calls as consumer calls unless counsel says otherwise.

### What the call must say and offer

| Requirement | What it says | Rule |
| --- | --- | --- |
| Name the caller up front | At the start, state who is responsible for the call. A business must use the name it is registered under | 64.1200(b)(1) |
| Give a callback number | During or after the message. For telemarketing to homes, and for exempt messages to homes under (a)(3)(ii) to (v), it must take do-not-call requests in business hours | (b)(2) |
| Offer an automated opt-out | For AI-voice telemarketing or advertising calls to homes, emergency lines, hospital rooms and mobile numbers, and for exempt messages to homes under (a)(3)(ii) to (v): a voice or keypress opt-out within 2 seconds of the identification. Using it adds the number to your do-not-call list and ends the call | (b)(3) |
| Voicemail | If the message lands on voicemail, also give a toll-free number that reaches the same opt-out | (b)(3) |
| Sales calls | Say promptly who the seller is and that the call is meant to sell | [FTC guide](https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule) |

Design note: put the opt-out offer right after the name. The 2-second clock in (b)(3) starts when you give the identification.

### Stop requests

- **Current rule.** A person can revoke consent by any reasonable method that clearly shows they want no more calls. You cannot force one channel. A voice or keypress opt-out on the call always counts. Honor the request within a reasonable time, at most 10 business days ([64.1200(a)(10) and (d)(3)](https://www.ecfr.gov/current/title-47/part-64/section-64.1200)). A request by voicemail or email creates a presumption of revocation ((a)(11)).
- **Scope was in flux.** The FCC's 2024 rule made a stop request on one kind of informational message cover all automated calls and texts from you. The FCC has waived that part until January 31, 2027 ([DA 26-12](https://docs.fcc.gov/public/attachments/DA-26-12A1.pdf)).
- **New order, text not yet seen.** On September 30, 2026 the FCC adopted a Report and Order and Further Notice on revocation (FCC 26-67; Chairman Carr and Commissioners Gomez and Trusty approving). The release says consumers will be able to stop specific categories of robocalls and use a clearly designated revocation method ([news release](https://docs.fcc.gov/public/attachments/DOC-425498A1.txt)). I could not find the adopted text or its effective dates. The draft circulated on September 9 would let callers read a stop request as covering only the category of informational calls it answered, and let them designate one revocation method. The further notice asks about shortening the 10-day window and requiring a "revoke all" method ([draft and fact sheet](https://docs.fcc.gov/public/attachments/DOC-424844A1.pdf)). Adopted text may differ from the draft.
- **Safe default.** Treat any clear stop request, spoken, keyed or typed, as "no more automated calls from us". End the call, write the suppression at once, and apply it across campaigns and vendors. It is simpler than tracking categories and it holds up whichever text the FCC publishes. Keep the record five years ((d)(6)).

### Lists, hours and abandoned calls

| Rule | What it says | Source |
| --- | --- | --- |
| National Do Not Call Registry | No telemarketing calls to registered numbers unless the person gave signed written permission naming you, or has a personal relationship with the caller. The FCC safe harbor needs written procedures, trained staff, an internal list, a registry copy no more than 31 days old, and records | [64.1200(c)(2)](https://www.ecfr.gov/current/title-47/part-64/section-64.1200) |
| Registry access | Sync at least every 31 days. FY2026 fee: $82 per area code, first five free | [FTC guide](https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule) |
| Internal do-not-call list | Written policy, trained staff, record each request when made, honor within 10 business days, keep 5 years. A request binds the entity that called; it reaches affiliates only if the person would expect them to be included | [64.1200(d)](https://www.ecfr.gov/current/title-47/part-64/section-64.1200) |
| Hours | Not before 8 a.m. or after 9 p.m. at the called person's location, for telephone solicitations to homes | 64.1200(c)(1); [16 CFR 310.4(c)](https://www.ecfr.gov/current/title-16/part-310) |
| Abandoned calls | Of telemarketing calls answered live, at most 3% abandoned per campaign over 30 days. A call is abandoned if it is not connected to a live sales representative within 2 seconds of the person's greeting | 64.1200(a)(7); 16 CFR 310.4(b)(1)(iv) |
| AI-voice path | An artificial or prerecorded telemarketing message to a consenting home or mobile number is not "abandoned" if it begins within 2 seconds of the greeting | 64.1200(a)(7)(ii) |
| Prerecorded telemarketing (FTC) | Written agreement naming the specific seller; ring at least 15 seconds or four rings; within 2 seconds of the greeting play the required disclosures and an opt-out; a healthcare message from a HIPAA covered entity is exempt | [16 CFR 310.4(b)(1)(v)](https://www.ecfr.gov/current/title-16/part-310) |
| Records | Keep 5 years: scripts, each unique prerecorded message, a record of each call, consent records, the registry version used, each do-not-call request, service-provider contracts | [16 CFR 310.5](https://www.ecfr.gov/current/title-16/part-310) |

- **Unsettled.** Neither the FCC rule nor the TSR says whether an AI voice counts as the "live sales representative" that stops a call being abandoned, or whether the TSR treats an AI voice as a "prerecorded message". I found no FTC statement on it. Design for the AI-voice path: consent in hand, first words within 2 seconds of the greeting, and the TSR disclosures. A slow turn-taking setup that waits several seconds after "hello" can turn answered calls into abandoned ones.
- The FTC says banks, some nonprofits and a few other entities fall outside its rule ([FTC guide](https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule)). The FCC's rules still cover them.

### Caller ID

- Telemarketers must transmit caller ID: the calling number and, when the carrier supplies it, a name. You may substitute the seller's name and customer-service number. That number must let anyone make a do-not-call request during business hours. You may not block caller ID ([47 CFR 64.1601(e)](https://www.ecfr.gov/current/title-47/part-64/section-64.1601)).
- It is unlawful to cause caller ID to show misleading or inaccurate information with intent to defraud, cause harm, or wrongfully obtain something of value ([47 U.S.C. § 227(e)](https://www.law.cornell.edu/uscode/text/47/227)). Do not spoof.
- The TSR asks for proof that you may use each caller ID number and name ([16 CFR 310.5(a)(2)(ix)](https://www.ecfr.gov/current/title-16/part-310)). Keep the number contracts.

### Voicemail

- An AI voice that leaves a message is using an artificial or prerecorded voice. The consent rules above apply to it.
- Telemarketing voicemails need the identification and the toll-free opt-out number described above.
- Answering-machine detection that hangs up on a real person makes a silent or abandoned call. Keep that error rate low and log it. Mechanics are in the [call reliability skill](../../voice-call-reliability/SKILL.md).

## State telemarketing laws

Many states add their own rules on top of the federal ones. The FTC tells callers to check each state's attorney general ([FTC guide](https://www.ftc.gov/business-guidance/resources/complying-telemarketing-sales-rule)). I checked the three "mini-TCPA" states below, Florida's separate Telemarketing Act, Texas's calling-hours and identification rule, and California's older rules on automatic dialing-announcing devices. I did not check Texas telephone-seller registration (Bus. & Com. Code ch. 302), Virginia, Washington's automatic-dialer law or others. Look up each state where you call.

| State | What it adds | Source |
| --- | --- | --- |
| Florida (Telephone Solicitation Act, Fla. Stat. § 501.059) | Prior express written consent for unsolicited telephonic sales calls that involve an automated system for the selection and dialing of numbers, or the playing of a recorded message (§ 501.059(8)(a)). Whether a live AI voice is a "recorded message" is untested; get the consent anyway. A call to a Florida area code is presumed to reach a person in Florida (§ 501.059(8)(d)), so apply Florida rules by area code as well as by known address. The caller must give a true first and last name and the business at once. Caller ID must carry a number that connects back. Bans altering the voice to disguise identity with intent to defraud, confuse or injure. Private suit: actual damages or $500, up to three times for willful violations. The state keeps its own "no sales solicitation calls" list. Section 501.059 sets no calling hours; the Telemarketing Act in the next row does. How "true first and last name" applies to an AI caller is untested | [Fla. Stat. § 501.059](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.059.html) |
| Florida (Telemarketing Act, Fla. Stat. §§ 501.601 to 501.626) | A commercial telephone seller must be licensed before doing business in Florida. That includes soliciting purchasers located in Florida from other states (§ 501.605). No commercial solicitation calls, including calls by automated dialing or recorded message, before 8 a.m. or after 8 p.m. in the called person's time zone, and no more than three such calls from any number to a person in 24 hours on the same subject (§ 501.616(6)). Within the first 30 seconds the caller must state a true name, the company and what is being sold (§ 501.613). The Act has exemptions (§ 501.604) that I did not check | [§ 501.605](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.605.html), [§ 501.613](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.613.html), [§ 501.616](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0500-0599/0501/Sections/0501.616.html) |
| Oklahoma (Telephone Solicitation Act of 2022) | Written consent for commercial calls that use automated dialing or a recorded message (§ 775C.3). Calls only 8 a.m. to 8 p.m. local time, and at most three commercial solicitation calls in 24 hours on the same subject (§ 775C.4). Caller ID must connect back. Private suit: actual damages or $500, up to three times for willful violations (§ 775C.6). Sources are Justia copies of the 2025 statutes | [§ 775C.3](https://law.justia.com/codes/oklahoma/title-15/section-15-775c-3/), [§ 775C.4](https://law.justia.com/codes/oklahoma/title-15/section-15-775c-4/), [§ 775C.6](https://law.justia.com/codes/oklahoma/title-15/section-15-775c-6/) |
| Maryland (Stop the Spam Calls Act, Com. Law § 14-4502) | Prior express written consent for solicitations that use automated dialing or a recorded message. No solicitation from 8 p.m. to 8 a.m. in the called party's time zone. No more than three calls in 24 hours on the same subject. Bans altering the voice to disguise identity with intent to defraud or injure. The consent rule has exemptions (§ 14-4502(a)(1)), for example isolated transactions, some business-to-business sales and some inquiry-response or existing-relationship calls. I did not check how they apply. Page current through July 1, 2026 | [Md. Com. Law § 14-4502](https://govt.westlaw.com/mdc/Document/NAE020871069411EF91F5DFA394D70191) |
| Texas (Bus. & Com. Code § 301.051) | Immediately after contact, the caller must give its name, the business it calls for, and the purpose. Calls only 9 a.m. to 9 p.m. Monday to Saturday and noon to 9 p.m. on Sunday. Exempt: calls at the consumer's express request, calls about an existing debt or contract, and calls to someone with a prior or existing business relationship. How "himself or herself by name" applies to an AI caller is untested | [§ 301.051](https://tcss.legis.texas.gov/resources/bc/htm/bc.301.htm) |
| California (Public Utilities Code §§ 2871 to 2876) | An "automatic dialing-announcing device" is equipment that stores or generates numbers and can disseminate a *prerecorded* message (§ 2871). Since January 1, 2025, § 2874 lets such a device run only after an unrecorded, natural-voice announcement that states the nature of the call and the caller's name, address and number, asks whether the person consents to hear the message, and tells them if the message uses an artificial voice. Whether a live LLM agent is a "prerecorded message" device is untested | [§ 2871](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PUC&sectionNum=2871), [§ 2874](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PUC&sectionNum=2874) |

Design rule: apply the strictest window and cap of any state on your list. Among the states checked, Florida, Oklahoma and Maryland set the earliest end (8 p.m.) and Texas the latest start (9 a.m., or noon on Sunday). Combined: 9 a.m. to 8 p.m. Monday to Saturday, noon to 8 p.m. Sunday, and no more than three calls per 24 hours on the same subject. Unchecked states may be stricter.

## AI disclosure

No final federal rule requires an AI call to say it is AI. The FCC proposal is above. Some states have rules, and they differ.

| Law | What it says about AI | Status | Source |
| --- | --- | --- | --- |
| Utah Code ch. 13-77 (SB 226) | A business using generative AI with a consumer must say it is AI, not a human, if the person clearly and unambiguously asks. Licensed professions must disclose high-risk AI interactions prominently, verbally at the start of a verbal interaction. Safe harbor: the AI says clearly, at the outset and throughout, that it is AI. Fines up to $2,500 per violation. Generative AI includes audio | In force since May 7, 2025 | [chapter text](https://le.utah.gov/xcode/Title13/Chapter77/C13-77_2025050820250508.pdf), [enrolled SB 226](https://le.utah.gov/Session/2025/bills/enrolled/SB0226.pdf) |
| Maine, 10 M.R.S. § 1500-DD | Using a chatbot or other computer technology with a consumer in a way that may mislead a reasonable person into thinking they are talking to a human is unlawful unless you notify them clearly and conspicuously. "Chatbot" includes aural communication. A violation is an unfair trade practice. Effective date not checked | Enacted June 2025 | [statute](https://www.mainelegislature.org/legis/statutes/10/title10sec1500-DD.html) |
| California Health and Safety Code § 1339.75 (AB 3030) | Health facilities, clinics and physician offices that use generative AI for patient messages about clinical information must add an AI disclaimer (for audio, verbally at the start and end) and tell the patient how to reach a human. Does not cover administrative messages such as scheduling or billing. Exempt if a licensed provider reviews the message | In force since January 1, 2025 | [statute](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=HSC&sectionNum=1339.75) |
| California Business and Professions Code § 17941 | The bot-disclosure law applies to bots that communicate online. Phone calls are outside its text | In force | [statute](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17941) |
| Colorado SB 26-189 and HB 26-1263 | SB 26-189 replaces the 2024 AI Act with a notice duty for automated decision tools used in consequential decisions. HB 26-1263 requires operators of a public-facing "conversational AI service" (text, visual or aural) to tell users it is AI. Both take effect January 1, 2027. Whether they reach a private phone agent is unclear. The bill page and the attorney general's page disagree on the signing date | Enacted, not yet in force | [SB 26-189](https://leg.colorado.gov/bills/sb26-189), [HB 26-1263](https://leg.colorado.gov/bills/hb26-1263), [AG page](https://coag.gov/ai/) |

More states are acting. Two trackers, both secondary: the [Center for Democracy and Technology 2026 update](https://cdt.org/insights/2026-state-and-federal-ai-legislation-updates/) (opened; the page shows an update on September 11, 2026) and [Orrick's interactive AI law tracker](https://ai-law-center.orrick.com/us-ai-law-tracker-see-all-states/) (not read: my scraper could not extract it). Use them to find new phone or chatbot rules, then read the statute itself.

**Policy for the build.** Say it is an AI in the first sentence of every call, in the caller's language, and answer "are you a robot?" truthfully every time. One habit then meets "disclose if asked", "clear and conspicuous", the FCC proposal and the EU rule below.

## Recording and transcripts

Federal law is one-party consent: recording is lawful if you are a party or one party consents, unless it is for a criminal or tortious purpose ([18 U.S.C. § 2511(2)(d)](https://www.law.cornell.edu/uscode/text/18/2511)). States can be stricter, and several are. When the parties are in different states, plan for the strictest state on the call.

| State | Rule in one line | Source |
| --- | --- | --- |
| California | All parties must consent to recording a confidential communication; fine up to $2,500 per violation. Cellular and cordless calls are covered too. Civil suit: the greater of $5,000 per violation or three times actual damages | [PC § 632](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PEN&sectionNum=632), [§ 632.7](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PEN&sectionNum=632.7), [§ 637.2](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=PEN&sectionNum=637.2) |
| Florida | Lawful when all parties gave prior consent | [§ 934.03](http://www.leg.state.fl.us/statutes/index.cfm?App_mode=Display_Statute&URL=0900-0999/0934/Sections/0934.03.html) |
| Illinois | Private conversations need all parties' consent; the offense requires a device used in a surreptitious manner | [720 ILCS 5/14-2](https://www.ilga.gov/legislation/ilcs/fulltext.asp?DocName=072000050K14-2) |
| Maryland | Lawful only if all parties gave prior consent; a felony, up to 5 years or $10,000 | [CJP § 10-402](https://mgaleg.maryland.gov/mgawebsite/Laws/StatuteText?article=gcj&section=10-402&enactments=false) |
| Massachusetts | Secretly recording without all parties' prior authority is an offense | [c. 272 § 99](https://malegislature.gov/Laws/GeneralLaws/PartIV/TitleI/Chapter272/Section99) |
| Montana | Recording with a hidden device, without all parties' knowledge, is an offense | [MCA 45-8-213](https://leg.mt.gov/bills/mca/title_0450/chapter_0080/part_0020/section_0130/0450-0080-0020-0130.html) |
| New Hampshire | A felony unless all parties consent | [RSA 570-A:2](https://www.gencourt.state.nh.us/rsa/html/LVIII/570-A/570-A-2.htm) |
| Pennsylvania | Lawful where all parties gave prior consent | [18 Pa.C.S. § 5704](https://www.legis.state.pa.us/WU01/LI/LI/CT/HTM/18/00.057.004.000..HTM) |
| Washington | All participants must consent. Consent is deemed given when one party announces, in a reasonably effective way, that the conversation is about to be recorded, and the announcement is itself recorded | [RCW 9.73.030](https://app.leg.wa.gov/rcw/default.aspx?cite=9.73.030) |

Secondary only (Reporters Committee for Freedom of the Press guides, last updated between 2019 and 2023): Connecticut (civil all-party rule with a notice route), Delaware (conflicting statutes, follow the stricter), Nevada (all-party for phone calls), Michigan (ambiguous for participants), Oregon (one-party for phone calls). Start at the [guide index](https://www.rcfp.org/reporters-recording-guide/) and confirm each state in its statute. I did not check the other states. Do not assume they are one-party.

**Default.** Announce recording and transcription at the start of every call, in every state. If the person objects, stop recording and transcription or move them to a path that does not record. If your product cannot work without processing audio, say so and end the call politely.

**Vendor risk in California.** In *Ambriz v. Google LLC* (N.D. Cal., No. 23-cv-05437-RFL) the court denied Google's motion to dismiss wiretap claims over its Contact Center AI. It applied a "capability" test: a vendor whose product can use call data for its own benefit may count as a third-party eavesdropper, whether or not it does. I opened the [order](https://www.courthousenews.com/wp-content/uploads/2025/02/ambriz-v-google-order-denying-motion-dismiss.pdf) (a Courthouse News copy). It is titled "Order Denying Defendant's Motion to Dismiss" and says the court will apply the capability test. The February 10, 2025 date and the "whether or not it does" reading come from two law-firm summaries (secondary): [Goodwin](https://www.goodwinlaw.com/en/insights/publications/2025/02/alerts-practices-dpc-ftec-ai-voice-products-subject-to-california-invasion-of-privacy-claims), [ZwillGen](https://www.zwillgen.com/privacy/federal-judge-allows-google-customer-service-ai-class-action-to-proceed/). This is a pleading-stage ruling, so it decides nothing final. Courts are split. Some N.D. Cal. judges ask only whether the vendor *could* use the data (the capability test: *Javier v. Assurance IQ*, 2023; *Ambriz*; *Taylor v. ConverseNow*, August 2025, an AI voice ordering vendor). Others ask whether it acts only as an extension of the business (*Graham v. Noom*, 2021). Outside California, a federal Wiretap Act claim over AI call transcription was dismissed under the ordinary-course-of-business exception (*Lisota v. Heartland Dental*, N.D. Ill., January 2026). All of these are early rulings (secondary: [Holland & Knight, May 2026](https://www.hklaw.com/en/insights/publications/2026/05/recent-genai-class-actions-build-on-early-successes)). Treat the capability test as the risk to design for. Practical steps: disclose that an AI vendor processes the call, and sign terms that bar vendors from using call audio or transcripts for their own purposes.

## Outside the US

### European Union

| Topic | What it says | Source |
| --- | --- | --- |
| AI Act, Article 50(1) | Systems meant to interact directly with people must be designed so the people are told they are dealing with an AI system, unless that is obvious to a reasonably well-informed, observant and careful person in context. Article 50(5): the information comes in a clear and distinguishable way at the latest at the first interaction. Applies from **2 August 2026** | [AI Act, consolidated 27.07.2026](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02024R1689-20260727) |
| Did the delay change this? | No. The Digital Omnibus on AI (Regulation (EU) 2026/1744 of 8 July 2026) moved the high-risk dates to 2 December 2027 (Annex III) and 2 August 2028 (Annex I). Consolidated Article 113 still says the Act applies from 2 August 2026 and lists no exception for Article 50. The Commission says the only Article 50 grace period is for marking AI-generated content under Article 50(2): providers of systems already on the market before 2 August 2026 have until 2 December 2026 | [Regulation 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng), [AI Act Article 113, consolidated](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02024R1689-20260727), [Commission FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act) |
| Commission reading | A system is in scope when it is an AI system, the exchange is genuinely two-way, it is direct, and it is with natural people. The "obvious" exception is read narrowly. Deployers of AI-generated audio that falsely appears to be a real person must disclose at first exposure, which matters for cloned voices. For voice, the Commission's final guidelines (C(2026) 5054, July 2026) give a spoken statement at the start as the example, with reminders in longer calls, after an interruption, and when the AI's role changes (for example, after a transfer back from a person). Outbound calls are in scope; the interaction need not be started by a human | [Commission FAQ](https://digital-strategy.ec.europa.eu/en/faqs/transparency-obligations-under-article-50-ai-act), [guidelines page](https://digital-strategy.ec.europa.eu/en/policies/guidelines-transparency-ai-generated-content), [C(2026) 5054](https://ec.europa.eu/newsroom/dae/redirection/document/131215) |
| Who carries the duty | Article 50(1) puts the duty on the provider. If you build or white-label the agent, assume it is yours | AI Act, as above |
| Fines | Article 99(4)(g) puts the transparency obligations of providers and deployers under Article 50 in the tier of fines up to EUR 15 million or, for a company, 3% of worldwide annual turnover, whichever is higher | [Article 99, AI Act Service Desk](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-99) |
| ePrivacy Directive, Article 13 | Automated calling systems without human intervention may be used for direct marketing only with the subscriber's prior consent. Other marketing calls follow national opt-in or opt-out rules. My reading is that an LLM voice agent can be such a system. That is unsettled | [Directive 2002/58/EC](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02002L0058-20091219) |
| ePrivacy Directive, Article 5 | Calls are confidential. Member states must bar listening, recording or other interception by persons other than the users without the users' consent (Article 5(1)). A third-party AI vendor in the audio path may be such a person. Article 5(2) allows legally authorised recording in lawful business practice as evidence of a commercial transaction or other business communication. Recording by a party to the call is governed by national law and the GDPR, so check each country | same |
| GDPR | Recordings and transcripts are personal data. Keep them no longer than needed (Article 5(1)(e)). Voiceprints used to identify a person are special-category data (Article 9(1)). People have a right not to be subject to solely automated decisions with legal or similarly significant effects, and to human intervention where the exemptions apply (Article 22). Also: give the Article 13 information when the data is collected (a short spoken notice at the start, with a link or number for the full notice); sign an Article 28 processor contract with each vendor in the audio path; check a transfer mechanism (Chapter V, Article 44 onward) for vendors outside the EEA; and ask counsel whether an Article 35 impact assessment is needed, which is likely for large-scale call recording or any voiceprint use | [GDPR](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679) |
| Regulator view on voice assistants | The EDPB's guidelines focus on consumer voice assistants. Treat them as related reading only | [EDPB Guidelines 02/2021](https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-022021-virtual-voice-assistants_en) |

Member states add their own telemarketing rules. I did not check them. Ask counsel per country.

### United Kingdom

| Topic | What it says | Source |
| --- | --- | --- |
| Automated calls (PECR reg. 19) | No recorded-message marketing calls by an automated calling system unless the subscriber has previously notified the caller that they consent to such calls from that caller, and the caller shows its calling line identity or a line on which it can be contacted (reg. 19(2)). Regulation 24 separately requires the caller's name and an address or freephone number. An "automated calling system" can start a sequence of calls and send sounds that are not live speech. My reading: an AI voice can be one. That is unsettled | [reg. 19](https://www.legislation.gov.uk/uksi/2003/2426/regulation/19) |
| ICO guidance | Consent must specifically cover automated calls. General marketing consent, or consent for live calls, is not enough. Give your name and a contact address or freephone number, and let your number show | [ICO telephone marketing](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/telephone-marketing/) |
| Live marketing calls (reg. 21) | No unsolicited marketing calls to a line whose subscriber has said no, or to a number on the TPS or CTPS register (unless they consented to you). A person is not in breach if the number joined the register fewer than 28 days earlier. Calling line identity must not be hidden, or must be a contactable line | [reg. 21](https://www.legislation.gov.uk/uksi/2003/2426/regulation/21) |
| Fines | Since 5 February 2026, breaches of regs. 19 and 21 (among others) carry the higher maximum: GBP 17.5 million or 4% of worldwide turnover | [DUAA 2025 Sch. 13](https://www.legislation.gov.uk/ukpga/2025/18/schedule/13), [commencement SI 2026/82](https://www.legislation.gov.uk/uksi/2026/82/regulation/2/made), [DPA 2018 s. 157](https://www.legislation.gov.uk/ukpga/2018/12/section/157) |
| Silent and abandoned calls (Ofcom) | Repeated silent or abandoned calls can be persistent misuse under the Communications Act 2003, with penalties up to GBP 2 million. Dialers and automated calling systems must not generate them. Ofcom's 2016 policy statement says the old 3% abandoned-call figure is not a safe harbour | [Ofcom notice, 22 January 2026](https://www.ofcom.org.uk/phones-and-broadband/unwanted-calls-and-messages/refresher-messaging-on-silent-and-abandoned-calls), [policy statement](https://www.ofcom.org.uk/siteassets/resources/documents/consultations/category-1-10-weeks/7837-review-of-how-we-use-persistent-misuse-powers/summary/persistent-misuse-policy-statement.pdf?v=410974) |

### Canada

| Topic | What it says | Source |
| --- | --- | --- |
| Automatic dialing-announcing device (ADAD) | The CRTC defines an ADAD as automatic equipment that can store or produce numbers and convey a pre-recorded or synthesized voice message. My reading: an AI voice agent on an automated dialer likely fits. That is unsettled | [CRTC Unsolicited Telecommunications Rules](https://crtc.gc.ca/eng/trules-reglest.htm) (not re-opened on the check date) |
| ADAD consent | Solicitation calls with an ADAD only with the consumer's express consent, and you must be able to show authorization to call that number | [CRTC key rules](https://crtc.gc.ca/eng/phone/telemarketing/tobligations/rules-regles.htm) (not re-opened on the check date) |
| ADAD identification | The call begins with a clear message naming the person for whom it is made, the purpose, an email or mailing address and a local or toll-free number. The equipment must disconnect within 10 seconds of the person hanging up | [CRTC rules](https://crtc.gc.ca/eng/trules-reglest.htm) (not re-opened on the check date) |
| Hours | 9:00 a.m. to 9:30 p.m. on weekdays and 10:00 a.m. to 6:00 p.m. on weekends, the recipient's time. Provincial rules can be stricter | [CRTC key rules](https://crtc.gc.ca/eng/phone/telemarketing/tobligations/rules-regles.htm) (not re-opened on the check date) |
| Lists | Register with and subscribe to the National Do Not Call List, using a copy no more than 31 days old. Keep an internal list: add a request within 14 days and keep it 3 years and 14 days | [CRTC key rules](https://crtc.gc.ca/eng/phone/telemarketing/tobligations/rules-regles.htm) (not re-opened on the check date) |
| Recording | The Criminal Code offense of intercepting a private communication does not apply where the originator or the intended recipient consents ([s. 184](https://laws-lois.justice.gc.ca/eng/acts/C-46/section-184.html)). Privacy statutes may still require notice. I did not check them | Criminal Code |

I did not check Canada's caller authentication rules.

## Unsettled and unverified

Say these to the user. Do not paper over them.

- **FCC AI disclosure** is a proposal (FCC 24-84), not a rule.
- **Revocation.** The FCC adopted a new order on September 30, 2026. I could not read the adopted text. The waiver on the "revoke all" part runs to January 31, 2027.
- **Old legal labels and an LLM voice.** It is unsettled whether an LLM agent is a "live sales representative" (abandoned-call rule), a "prerecorded message" (TSR, California device law), an "automated calling system" (UK, EU) or an ADAD (Canada).
- **Florida's "true first and last name" and Texas's "by name"** rules for an AI caller are untested.
- **California wiretap claims against AI vendors.** Courts are split between a "capability" test and an "extension" test, and every AI-voice ruling so far is at the pleading stage (*Ambriz*, *Taylor v. ConverseNow*).
- **Colorado's 2027 AI laws** may or may not reach a private phone agent.
- **Not checked:** Texas telephone-seller registration (ch. 302), Virginia and other state telemarketing laws; the exemptions in Florida's Telemarketing Act and Maryland's § 14-4502(a); state biometric or voiceprint laws; debt collection, political and fundraising calls; EU member-state rules; Canadian privacy statutes and caller authentication; FCC forfeiture amounts.
- **Secondary sources only:** Connecticut, Delaware, Nevada, Michigan and Oregon recording rules; the date of the *Ambriz* order; the 2026 state AI-law trackers.
- **Third-party hosts and extracts.** The Oklahoma statutes are Justia copies, and the *Ambriz* order is a Courthouse News copy. I read the Eleventh Circuit opinion, the Ofcom policy statement and the CRTC pages as passages returned by a scraper, not as whole pages.
