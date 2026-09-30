# Tool execution, uncertain writes, and handoffs

Reviewed **2026-09-30 UTC**, using Context7 and current LiveKit documentation.
The application patterns below are engineering recommendations. Provider behavior
is cited separately; no live transaction or transfer was executed in this review.

[Action states](#define-the-action-contract) ·
[Interruptions](#decide-what-interruption-can-cancel) ·
[Recovery example](#work-through-an-uncertain-booking) ·
[Handoffs](#transfer-control-with-evidence) ·
[Test cases](#test-side-effects-separately-from-dialog)

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

Define which state changes require durable storage. Useful fields include a
tenant-scoped action identifier, normalized request values, authorization evidence,
external idempotency key if supported, upstream request/result identifiers, state,
and the reconciliation owner. Store only the sensitive detail required by the
application's retention and access rules.

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

For a read-only lookup, cancellation may save resources and suppress an obsolete
answer. For a write, preserve the durable action and finish or reconcile it under
the service's contract. Keep any non-interruptible commit section short. Use a
supported background workflow for long work while the caller can continue talking;
changing the prompt does not make a blocking function non-blocking.

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

If the caller changes the date while A remains unresolved, keep that corrected
intent separately from A's original arguments and key K. Validate the new values
and preserve any required authorization without dispatching a competing booking.
If A committed, use the supported, authorized change or compensation workflow.
If authoritative evidence establishes that A did not commit, submit the corrected
request with its own action identity. If A remains unknown, keep the corrected
intent pending and give the recovery owner both records. A late result must update
A's ledger without silently replacing the caller's latest intent.

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

The context packet should contain confirmed facts, the unresolved request, pending
action IDs and states, and the smallest useful transcript or summary. Identify who
owns reconciliation after transfer. A human receiving a caller with an unknown
booking result should not have to guess whether creating another booking is safe.

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
