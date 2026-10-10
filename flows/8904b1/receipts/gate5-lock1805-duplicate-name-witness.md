# Gate 5 lock rejection — lock 1805, DuplicateName, holder cf7879

Subflow 8904b1, read-only. Subject: Mind Astra 6fe957's Gate 5 blocker,
`LockRejected.DuplicateName 1805 Name cf7879`, against the Home main move.
No lock action taken by this subflow (no Lock, no Release, no probe request
submitted). No message sent to any flow.

## 1. Direct observation: `orchestrate 'Observe.Locks'`, run 2026-09-27

Full current lock set fetched live. The one matching ID 1805:

```
{ 1805 Name cf7879 [ /home/li/wt/github.com/LiGoldragon/codex-hijack/context-modules-cf7879
                      /home/li/wt/github.com/LiGoldragon/claude-hijack-stock-263-cf7879
                      /home/li/wt/github.com/LiGoldragon/primary/cf7879-report-recovery/flows/cf7879/reports ]
  «Order 11 module checks and indexed successor packet composition» }
```

- Lock ID: 1805
- Lock name (the literal string held in the `LockName` field): `Name`
- Holder FlowId: `cf7879`
- Paths: three, all under `codex-hijack`, `claude-hijack-stock-263-cf7879`,
  and `primary/cf7879-report-recovery/flows/cf7879/reports`
- Reason: «Order 11 module checks and indexed successor packet composition»
- Taken-at timestamp: not carried by the Lock datom and not observed anywhere
  else searched; UNKNOWN.

No other lock in the full `Observe.Locks` set (18 locks total at observation
time) names any Home/CriomOS-home path, any messenger-clj path, or any
6fe957 path.

**Relation to Home: none.** Lock 1805's three paths and its reason do not
touch `CriomOS-home`, `messenger-clj`, or any path Mind Astra's Gate 5 move
touches. It is unrelated work.

## 2. Holder cf7879 — state across three systems

- **Messenger (`hm-list`):** cf7879 does not appear in the roster at all —
  not even as STALE. Every other flow in the roster (including several
  STALE ones from the `messaging-build` session) is listed; cf7879 is
  absent. OBSERVATION, not inference: no binding exists to describe as
  live or stale.
- **Herdr (`herdr agent list`):** no agent/pane with flow id or name
  containing `cf7879` in the live agent list (10 agents listed, all
  identified). OBSERVATION: no live pane.
- **Flow / filesystem:** no `flows/cf7879` directory found under
  `/home/li/primary` or this checkout. Only stale `/tmp/*cf7879*` artifacts
  from around 2026-09-16 and a `/tmp/f55ec8-build/flows/cf7879/handoff`
  directory (also dated Sep 16) were found — old scratch material, not a
  live registration.
- **Stale-lock procedure's third leg (one hm-send returning `Held`)**: NOT
  PERFORMED. The brief's constraint against sending any message to any flow,
  probing included, forbids it. Two of the three stale-lock preconditions
  (no Messenger binding, no Herdr pane) are met by direct observation; the
  third is not attempted here.

INFERENCE (not direct witness): cf7879 presents as at least as absent as the
flows marked STALE in `hm-list`, since it is not even STALE — it is not
registered. This is consistent with staleness but does not by itself
complete the stale-lock procedure's evidence set.

## 3. The duplicate-name rule, from source

`orchestrate` skill (`Skill: orchestrate`) gives the request shape:
`Lock.{ <LockName> <FlowId> [ <path> ... ] <LockReason> }`.

Server-side check, `/git/github.com/LiGoldragon/orchestrate/crates/orchestrate-nexus/src/store/normalize.rs`:

```
fn duplicates_name_of(&self, lock: &Lock) -> bool {
    self.request.lock_name == lock.lock_name
}
```

and in `transition.rs`, `lock()` rejects with
`LockRejection::DuplicateName(holder)` — carrying back the **complete
existing Lock** (its exact ID, Name, FlowId, Paths, Reason) — the first
existing lock whose `lock_name` exactly string-equals the requested
`LockName`. The uniqueness dimension is `LockName` alone, checked as exact
string equality across every current lock, regardless of FlowId or paths.
Paths are checked separately (`PathOverlap`, a different rejection variant)
and were not the reason here.

Confirmed against the client contract test
(`signal-orchestrate-0.20.1/tests/contract.rs`): `DuplicateName` renders as
`LockRejected.DuplicateName.{ <id> <name> <flowid> [ <paths> ] <reason> }` —
a 5-field echo of the *existing* lock. The 3-field form Mind Astra received
and logged, `LockRejected.DuplicateName 1805 Name cf7879`, is that same echo
with paths and reason cut for brevity; it is not a separate, shorter wire
shape.

## 4. The request as Mind Astra actually submitted it

Recovered from Mind Astra's own machine-message to Fable, read via
`transcript search`/`transcript raw` on session `8904b10d` (main flow's own
transcript, line 763; Mind Astra's own checkout at `/home/li/primary/flows/6fe957`
was also read — `log.md`, `summary.md`, `reports/home-messenger-pin.md`,
`witnesses/` — and none of them hold the literal `orchestrate` argv used,
only prose. The verbatim invocation is not preserved anywhere in Mind
Astra's own persisted records; only its self-report is):

```
Lock.{ Requested.«6fe957;6fe957-home-messenger-gate5»
       Result.«LockRejected.DuplicateName 1805 Name cf7879» }
```

and its report prose: "rejected both a `6fe957` and a unique
`6fe957-home-messenger-gate5` lock request with the same unrelated
response."

**Was it well formed?** Given the confirmed server rule (section 3), a
`DuplicateName` rejection against lock 1805 is only possible if the
`LockName` field the server actually parsed, on both attempts, string-equalled
`Name` — the literal word, not `6fe957` and not
`6fe957-home-messenger-gate5`. Those two strings differ from `Name` and from
each other, so they cannot both independently collide with the same
existing lock under exact-string-equality unless the field the service read
was, both times, the literal token `Name` rather than the intended distinct
value. Mind Astra's own `Requested.«6fe957;6fe957-home-messenger-gate5»`
field is best read as its own descriptive label for what it *intended* to
name the two attempts (flow-id-then-scoped-name), not a verbatim echo of the
`LockName` argument the server received. No verbatim argv survives to show
conclusively which field held the literal `Name`, but the two request
attempts, the single unchanging rejection, and the exact-string-equality
rule together are inconsistent with a well-formed request carrying the
intended `LockName`.

## 5. Which reading the evidence supports

**Not a real clash.** Lock 1805 has nothing to do with Home, messenger-clj,
or the paths Gate 5 touches; its holder cf7879 is unrelated work from
around 2026-09-16. The evidence instead supports a malformed request: on
both attempts the field the lock service read as `LockName` appears to have
been the literal string `Name` (not `6fe957`, not
`6fe957-home-messenger-gate5`), which happens to collide with lock 1805's
own (independently anomalous) name, also the literal string `Name`. This
reads as two unrelated flows each having, at some point, sent the bare word
`Name` as an actual `LockName` value — plausibly a templating mistake that
substitutes the field's label for its value — with cf7879 having gotten
there first.

## 6. What clears the block, and whose act it is

This is Mind Astra 6fe957's own request to re-form, not a stale-lock
release: no clash with cf7879's lock exists on paths, reason, or ownership,
so nothing needs releasing or retiring. Mind Astra should resubmit
`orchestrate 'Lock.{ <LockName> 6fe957 [ <Home paths> ] <reason> }'` with an
actual distinct `LockName` value in the first field — e.g.
`HomeMessengerGate5Move6fe957` or similar — never the bare word `Name`
literally, and never its FlowId or a semicolon-joined label standing in for
`LockName`. Should a genuine clash instead turn up later, the stale-lock
procedure's own preconditions on cf7879 are two-thirds met by this receipt
(no Messenger binding, no Herdr pane) and lack only a `hm-send` liveness
probe, which this subflow's constraints forbid performing.
