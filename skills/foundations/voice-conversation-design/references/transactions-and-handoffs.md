# Tool execution, uncertain writes, and handoffs

[Handbook](../../../../docs/handbook.md) / [Conversation design skill](../SKILL.md)

Reviewed **2026-09-30 UTC**, using Context7 and current provider documentation.
The application patterns below are engineering recommendations. Provider behavior
is cited separately; no live transaction or transfer was executed in this review.

## Use the right recovery path

| Situation | Start here | Preserve |
| --- | --- | --- |
| Define or review a write tool | [Action contract](#define-the-action-contract) | Authorization, action identity, and authoritative state |
| Caller interrupts pending work | [Cancellation boundaries](#decide-what-interruption-can-cancel) | The action ledger after speech stops |
| Write timed out or its result was lost | [Uncertain booking](#work-through-an-uncertain-booking) | Original arguments/key and corrected intent separately |
| Hand off to another agent or human | [Transfer phases](#transfer-control-with-evidence) | Pending action IDs and the new reconciliation owner |
| Verify the implementation | [Side-effect tests](#test-side-effects-separately-from-dialog) | Business records as well as spoken output |

A voice agent can stop speaking while a booking continues. It can announce a
transfer before the destination answers. Designing these transitions requires
business state that survives the conversational turn.

## Define the action contract

For each tool, identify the authoritative service, required inputs, authorization,
possible side effects, timeout, cancellation semantics, and status lookup. Distinguish
the caller's intent from the model's proposal and the service's committed result.

| State | Evidence | What the agent can say |
| --- | --- | --- |
| Proposed | Intent and candidate arguments | A question or description of the proposed action. |
| Authorized | The task's required permission and validated values | That the action will be attempted. |
| In flight | A request was dispatched | That work is underway, without claiming success. |
| Committed | Authoritative result or durable record | The confirmed outcome and any relevant identifier. |
| Failed | Evidence that the operation did not commit | The supported retry or alternative. |
| Unknown | Transport error or ambiguous timeout | That the outcome is being checked. |
| Compensated | A separate cancellation/reversal succeeded | What was reversed and what remains. |

Define which state changes require durable storage. For each action, record:

- Tenant-scoped identity, normalized request values, and authorization evidence.
- External idempotency key if supported, plus upstream request/result IDs.
- State and reconciliation owner.

Store only sensitive detail required by the application's retention and access rules.

Concurrent requests need one action owner. A model retry, webhook redelivery,
reconnect, or transfer should refer to that existing action where appropriate.
Do not use the last spoken sentence as the transaction ledger.

## Decide what interruption can cancel

![Sequence showing a caller correction stopping old playback while the original booking action remains pending until an authoritative result arrives.](../assets/interrupted-action.svg)

[Editable diagram](../assets/interrupted-action.html). This is a conceptual
application sequence, not a provider event specification.

Cancellation has several boundaries: the response generator, queued speech, local
task, network request, and remote business operation. Stopping one does not prove
the others stopped. A client timeout describes the client's wait, not the service's
final state.

Current LiveKit tool documentation says interrupted work can continue in the
background. It provides Python and Node.js interruption mechanisms and recommends
disallowing interruption for external actions that cannot be rolled back. Its
async-tool API separately exposes
opt-in cancellation. Inspect which execution path and SDK version you use before
applying either contract.
[Tool definition and interruptions](https://docs.livekit.io/agents/logic/tools/definition.md#interruptions),
[Async-tool cancellation](https://docs.livekit.io/agents/logic/tools/async.md#cancellation).

| Work | Interruption policy |
| --- | --- |
| Read-only lookup | Cancel when useful to save resources and suppress an obsolete answer |
| External write | Preserve the durable action; finish or reconcile under the service contract |
| Non-interruptible commit section | Keep it short |
| Long-running work | Use a supported background workflow so the caller can continue talking |

Changing the prompt does not make a blocking function non-blocking.

### Defer a speculative tool before dispatch

Deepgram's Voice Agent API offers `defer_until_eot: true` on individual functions
in `agent.think.functions`. It holds dispatch until the user's turn is confirmed
and discards the held call if the user continues. The default is `false`; other
functions remain immediate. This control applies across listen providers.
[Published September 8, 2026; reviewed September 30](https://developers.deepgram.com/changelog/2026/9/8).

That gate does not replace task authorization or reconciliation after a request
reaches the business service. For a client-side call already delivered, a
`FunctionCallCancelled` event identifies the cancelled function ID; the documented
client behavior is to stop its work and omit its `FunctionCallResponse`. Preserve
any remote action outcome in the application ledger. Test resumed speech before
dispatch separately from interruption after a write has started.

Progress must reflect actual state. "Checking available times" can describe a
lookup. "Almost done" needs a real basis. A repeated filler every few seconds can
make recovery harder to follow; report meaningful changes and answer the caller's
current question while preserving the pending action.

## Work through an uncertain booking

This synthetic case is intentionally awkward:

1. The caller authorizes Friday at two. The application creates action A and sends
   the booking request with key K, if the service supports that key.
2. The service commits the booking, but the response is lost.
3. The caller interrupts the status message and asks whether it worked.
4. A replica-backed lookup temporarily returns no booking.

The correct result is still unknown to the application at step four. An empty
lookup from an eventually consistent system does not prove failure. Do not retry
with a new idempotency key or issue a second non-idempotent request because the
conversation has moved on.

Reconcile using the service's supported status endpoint, original key, authoritative
record, or operator process. Reuse K only under the API's documented idempotency
semantics, including scope, expiry, and behavior when request values differ. If the
service provides neither safe retry nor authoritative reconciliation, retain the
unknown state and use the configured human recovery path.

If the caller changes the date while A is unresolved, retain the corrected intent
separately from A's original arguments and key K. Validate new values and preserve
required authorization without dispatching a competing booking.

| Authoritative outcome for A | Next step |
| --- | --- |
| Committed | Use the supported, authorized change or compensation workflow |
| Did not commit | Submit the corrected request with its own action identity |
| Still unknown | Keep corrected intent pending; give the recovery owner both records |

A late result updates A's ledger without silently replacing the caller's latest intent.

Application deduplication helps suppress repeated dispatch from your own system.
It does not create exactly-once behavior across a non-idempotent external API.
A lock that expires while the first request is still running can permit a second
write. Test recovery after a process restart and after a lost response, not only
two simultaneous calls in one process.

LiveKit's current async duplicate controls are based on tool name, not arguments;
the documented default is `allow`. That mechanism cannot substitute for action
identity or a business-service idempotency key. Its `AsyncToolset` can retain tools
and pending updates across agent handoffs, but the application's durable records
still need their own lifetime.
[Duplicate handling and lifecycle scope](https://docs.livekit.io/agents/logic/tools/async.md).

## Transfer control with evidence

Define whether the handoff is between software agents, to a human on the same media
session, or through a telephone transfer. Each has different completion evidence.
The destination appearing in a configuration file does not establish availability.

| Phase | Required handling |
| --- | --- |
| Request | Record the reason and destination; preserve any pending actions. |
| Prepare | Build the permitted context packet and establish destination readiness. |
| Connect | Track the actual control/media operation and its timeout. |
| Accept | Confirm the recipient has taken responsibility under the selected workflow. |
| Release | End or detach the old agent only when the handoff contract allows it. |
| Recover | Resume, queue, or offer the configured alternative if connection fails. |

Handoff packet checklist:

- [ ] Confirmed facts and the unresolved request.
- [ ] Pending action IDs and states.
- [ ] Smallest useful permitted transcript or summary.
- [ ] Named owner of reconciliation after transfer.

The recipient must be able to determine whether another booking is safe.

For software handoffs, check interrupted transitions as well as successful ones.
The current LiveKit tool guide states that an interrupted agent handoff does not
switch agents, with different history recording in Python and Node.js. Preserve
that distinction when writing assertions or importing example code.
[Tool handoffs](https://docs.livekit.io/agents/logic/tools/definition.md).

For telephone handoffs, test busy, no answer, voicemail, hold, recipient decline,
media failure, and caller hangup while connecting. Choose which participant stays
connected during a warm transfer and what happens if one call leg ends. Use the
transport's actual events to decide when to release resources and stop billing.

## Test side effects separately from dialog

Text assertions can prove that the agent said the expected thing while the business
record is wrong. Check the record, number of write attempts, input values, and action
owner separately from spoken output.

| Injected condition | Invariant to verify |
| --- | --- |
| Caller corrects a value during a lookup | Stale lookup result cannot overwrite the corrected intent. |
| Interrupt before dispatch | No unauthorized or obsolete write is sent. |
| Interrupt after commit | Committed result survives even if its confirmation is unheard. |
| Timeout and lagging status lookup | The action stays unknown until authoritative evidence resolves it. |
| Duplicate request after restart | Existing action identity prevents unsafe redispatch. |
| Two similar actions with different arguments | Deduplication does not silently merge legitimate requests. |
| Transfer while work is pending | Exactly one designated owner continues reconciliation. |
| Destination unavailable | Caller retains a supported path; no false connection claim. |

Use mocked business services first. A useful fixture can commit a write, drop the
response, and delay its lookup visibility. Record expected state transitions before
running it, then inspect the actual ledger and conversation. Escalate to live tests
only within the user's authorized account, destination, and spending scope.

Context7 used `/websites/livekit_io_agents`; the cited current primary pages were
also retrieved directly. The examples above use conceptual action states, not
promised SDK event names or compiled application code.
