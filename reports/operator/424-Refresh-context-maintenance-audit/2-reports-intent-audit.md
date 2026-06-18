---
title: 424/2 — Reports and intent audit
role: operator
variant: Audit
date: 2026-06-18
topics: [reports, intent, criome, signal-standard, mentci]
parent_meta_report: reports/operator/424-Refresh-context-maintenance-audit
slot: 2
description: |
  Bounded report and intent audit for operator reports 406-423, with
  targeted designer and system-designer context. Builds the current
  supersession spine for criome policy language, object-update pulse,
  signal-standard, Mentci, and remotes/daemon runtime.
---

# 424/2 — Reports and intent audit

## Scope

Inspected operator reports `406` through `423`, plus targeted current
cross-lane reports where they supersede or validate the operator trail:
designer `674` through `689` where relevant, and recent system-designer
reports `132` through `140` where they change the current fan-out,
signal-standard, router, or Mentci state.

Safe Spirit reads only. No Spirit writes. Lookups used:

| Record | Current read |
|---|---|
| `m0p2` | Router-sole object-update pulse: criome emits references, router is the sole operational matcher for non-direct message passing, and criome-local subscription is observation/audit only. |
| `l2ha` | Fork A resolved: components subscribe; router fans references out; criome does not compute per-object impact. |
| `lt44` | Two transport lanes: ordinary router fabric plus direct criome-to-criome agreement lane for time-sensitive quorum work. |
| `9s52` | criome is per-Unix-user; no shared multi-user system criome with in-process user lanes. |
| `7x5z` | Mentci is a first-class component triad and state-bearing programmable UI daemon. |
| `eeeo` | `signal-standard` is the shared cross-component standards crate, not `signal-frame` and not `signal-system`. |
| `q1le` | criome key custody moves toward encrypted multi-key store with sub-keys; real Mentci verdict signing depends on it. |
| `gc0n` | Adjudication verdicts are closed typed outcomes over already-submitted objects; edited answers are separate typed proposals. |
| `vhs2` | criome policy language is limited, typed, identity-policy language, not a VM. |
| `ay3y` | criome time is quorum-attested crystallized past; operation time is carried as a proof, not ambient clock reads. |

## Supersession Spine

| Topic | Current canonical surface | Superseded trail | Open edge |
|---|---|---|---|
| Criome policy language | Spirit `vhs2`, `ay3y`, `gc0n`, `z9d6`; current `signal-criome` and `criome` main; designer `674.15 — criome internal policy language implementation architecture and constraints`; designer `677 — criome, the agreement machine within Telos`; designer `678 — criome agreement-machine visual`; designer `683 — design review and direct criome networking lane`; designer `688 — handoff to system-designer`. | operator `406 — Criome Internal Language POC` → operator `407 — audit of designer 674.11 content-addressed BLS prototype` → operator `408 — policy triad schema branches` → operator `409 — attested moment architecture and POC` → operator `410 — policy language main landing`. Later code and reports close parts of `410`: persisted contract SEMA landed at `criome 3c05122`; strict schema migration landed at `signal-criome ca3624c` and `criome 068f9db`. | Direct criome agreement lane, BLS aggregate verification, scoped attested-moment majority guard, and full adjudicator ladder remain outside operator `410`'s completed slice. |
| Object-update pulse | Spirit `m0p2`, `l2ha`, `lt44`; current code has reference-only pulse, interest-bearing token, and `signal-standard`; system-designer `139 — unblocked attendance fan-out and scoped majority guard` is the active build handoff. | operator `414 — classified object pulse POC` → operator `415 — interest-bearing token landing` → operator `416 — signal-standard catch-up` → operator `417 — pass-through feedback on designer 682` → operator `418 — review of designer 683`. Designer `682` and `684` are partially stale because the m0p2/l2ha fork is now resolved router-sole. | Router `Attend`/`Withdraw` attendance table and reference fan-out are not confirmed on main in this audit. Criome's existing local registry must remain observation/audit, not operational delivery. |
| Signal-standard | Spirit `eeeo`; code `/git/github.com/LiGoldragon/signal-standard` at `aa672cc`, with GitHub remote and `ComponentKind`, `Differentiator`, `AuthorizedObjectInterest`, `AuthorizedObjectReference`, and `StandardSocket`. operator `423 — Mentci remotes and daemon runtime` confirms remotes; system-designer `138/3 — signal-standard crate` is the build proof. | designer `681 — signal-standard design/report` and operator `416 — signal-standard catch-up` are superseded by the crate existing. system-designer `138/3`'s "no remote" note is superseded by operator `423`. | Consumer migration is still open: `signal-criome`, `signal-persona`, and `signal-message` still declare local component rosters; `signal-mentci` and `meta-signal-mentci` still carry local `StandardSocket` / `ComponentKind` stand-ins and stale comments saying `signal-standard` is not yet a crate. |
| Mentci component | Spirit `7x5z`, `gc0n`, `9s52`, `q1le`; code remotes exist for `signal-standard`, `signal-mentci`, `meta-signal-mentci`, `mentci`, and `mentci-lib`; operator `423 — Mentci remotes and daemon runtime` is the current operator surface. | operator `419 — Mentci approval surface and Prometheus Spirit` → operator `420 — Mentci daemon state and programmable UI` → operator `421 — Mentci component PoC feedback` → operator `422 — Mentci component implementation slice` → operator `423 — remotes and daemon runtime`. designer `685`, `686`, and `687` supply the design; designer `689` validates operator `422` but is now behind operator `423` for runtime/remotes. | Persist Mentci SEMA state, wire notification fan-out, connect verdict egress through real criome key custody (`q1le`), add missing flakes where desired, and collapse local duplicate types into `signal-standard` imports. |
| Remotes / daemon runtime | operator `423 — Mentci remotes and daemon runtime`; current repo state confirms all five remotes and `mentci` daemon runtime on main. | operator `422 — Mentci component implementation slice` is superseded where it says the daemon binary is not landed and remote creation is still gated. designer `689` is valid as an audit of `422`, not as the current runtime ledger. | New runtime still has in-memory state and incomplete Nix gating for the newer component repos. |

## Operator Reports 406-423

| Report | Disposition | Landing witness / reason | Later action |
|---|---|---|---|
| operator `406 — Criome Internal Language POC` | Retire candidate after refresh. | Superseded by schema-first public contract and evaluator in operator `410 — policy language main landing`, by designer `674.15 — policy-language constraints`, and by Spirit `vhs2`. Its concept-schema placement question is closed: policy vocabulary lives in `signal-criome`, not a daemon-local sketch. | Keep only if a current Criome refresh wants the historical "typed policy evaluator, not VM" rationale. Otherwise retire after the refresh carries the spine. |
| operator `407 — audit of designer 674.11 content-addressed BLS prototype` | Retire candidate. | The duplicate-quorum blocker and fmt blocker were branch-gate findings. Current criome rejects duplicate quorum members; designer `683 — design review` and operator `418 — review of designer 683` both mark the distinctness blocker closed. | Retire once the current refresh names the closure. Do not use it as current security state. |
| operator `408 — Criome policy triad schema branches` | Superseded branch report. | Absorbed by operator `410 — policy language main landing`; later code closes the in-memory SEMA gap. | Retire after current Criome policy refresh. |
| operator `409 — Criome attested moment architecture and POC` | Superseded branch report with one migrated idea. | Absorbed by operator `410 — policy language main landing` and Spirit `ay3y`. The "shared stamped frame/envelope" next-step wording is now better expressed as the broader rule that quorum-signed objects carry attested moments. | Migrate any surviving stamped-envelope nuance into criome/signal-frame architecture if still desired; retire the report. |
| operator `410 — criome policy language main landing` | Still useful, but stale as a current-state report. | It is the best operator narrative of the schema-first policy surface and tests. Its deferred SEMA storage item is now closed by `criome 3c05122`, and later strict-schema migration changed the code surface. | Forward its live proof into the final synthesis/current Criome refresh, then retire or leave only until permanent criome docs carry the same detail. |
| operator `411 — Nested Schema Namespace POC` | Side-thread; migrate then retire. | It proves namespace feasibility and exposes grammar ambiguity, but the current schema-next main chose strict positional/explicit-role syntax globally. | Migrate any still-needed namespace rule to schema docs/skills; otherwise retire as POC evidence. |
| operator `412 — Schema strict positional structs` | Keep temporarily; migrate upward. | It is still a useful landing witness for strict struct syntax and the migration surface. Current code confirms schema-next main enforces strict syntax. | Move the rule and current syntax into `skills/structural-forms.md` / schema docs if not already current, then retire. |
| operator `413 — Schema strict positional open questions` | Partially stale; migrate remaining open questions. | Composite explicit-role syntax is no longer open: current schema-next supports explicit structural field roles. Metadata macro positionality, scalar shorthand, visibility/private helpers, shared parser object, and diagnostics remain possible design notes. | Convert surviving questions into a schema-design issue/report or skill note; retire the obsolete questions. |
| operator `414 — criome classified object pulse POC` | Superseded by intent and code. | Its "extract only when router needs it" boundary was superseded by Spirit `eeeo` and `signal-standard`. Its criome-local filter path is superseded as operational delivery by Spirit `m0p2`/`l2ha` router-sole. | Retire after current pulse refresh; preserve only the distinction between reference pulses and payload movement. |
| operator `415 — criome interest-bearing token landing` | Forward, then retire after router fan-out lands. | The subscriber+interest token shape landed and remains relevant as a matching coordinate, but current intent says the operational matcher belongs to router, not criome. | Migrate the token/interest rationale to router attendance and `signal-standard` consumer migration docs. |
| operator `416 — Operator catch-up: signal-standard and router fan-out` | Superseded. | `signal-standard` now exists at `aa672cc` with remote; it includes the full cross-component vocabulary and StandardSocket. | Retire after noting that `signal-message::ComponentName` and local rosters still need migration. |
| operator `417 — Pass-through feedback on designer 682` | Superseded with two surviving corrections already absorbed elsewhere. | The strict syntax snapshot is now older than code; `signal-criome` strict migration is done. `Attend`/`Withdraw` survives and is now repeated in Spirit/recent system-designer reports. | Retire after current fan-out refresh. |
| operator `418 — Operator review of designer 683` | Partially load-bearing, mostly forwardable. | The correction that duplicate quorum-member distinctness is fixed remains useful. The majority-guard question is now reconciled by system-designer `139`: general policy threshold remains caller-declared; attested moment/head quorum needs a scoped `required > n/2` guard. | Migrate the corrected split into current criome direct-lane/attestation report, then retire. |
| operator `419 — Mentci approval surface and Prometheus Spirit` | Superseded. | Mentci spelling, component shape, and open questions have all advanced through Spirit `7x5z`, `9s52`, `gc0n`, `q1le`, and operator `420`-`423`. Prometheus live-node work belongs to system/designer head-loop reports, not this early implementation ledger. | Retire after this audit and the final synthesis preserve the Prometheus/system handoff if needed. |
| operator `420 — Mentci daemon state and programmable UI` | Forward, then retire. | It is the landing witness for `mentci-lib`'s daemon-state/subscription model. It is stale where it says the long-lived daemon binary does not exist. | Ensure `mentci-lib`, `mentci`, and repo architecture docs carry the state-ownership invariant; retire afterward. |
| operator `421 — Mentci component PoC feedback` | Mostly implemented; retire after rationale migrates. | Its fixes were absorbed by operator `422` and validated by designer `689`: closed verdict, daemon-minted identifiers/tokens, filtered subscriptions, local monotonic revision. Its psyche questions are resolved. | Migrate the rationale for closed verdict / edited-answer proposal into Mentci architecture or skills if not already there; retire. |
| operator `422 — Mentci component implementation slice` | Superseded by runtime/remotes for current state, still a useful implementation ledger. | operator `423` closes the remote gate and lands the daemon runtime; designer `689` validates `422` but predates `423`. | Forward any schema-specific detail not in repo docs, then retire in favor of `423` plus current code. |
| operator `423 — Mentci remotes and daemon runtime` | Keep as current operator report. | Current audit confirmed all five remotes and the daemon/runtime shape. Remaining-work list is still live. | Retire only after SEMA persistence, notification fan-out, verdict egress, and Nix gates are either landed or carried by a newer current report. |

## Cross-Lane Report Disposition

| Report or cluster | Current use |
|---|---|
| designer `674.15 — criome internal policy language implementation architecture and constraints` | Still load-bearing as the criome policy-language constraint catalog. Some "missing SEMA" details are now closed by code. Migrate durable constraints into criome architecture/INTENT; keep until that permanent surface is complete. |
| designer `677 — criome, the agreement machine within Telos` and designer `678 — agreement-machine visual` | Useful framing, but stale where they mark pulse forks as open. Superseded by Spirit `m0p2`/`l2ha` router-sole and by later code. Forward the one-primitive/quorum framing; retire or refresh the open-fork sections. |
| designer `681 — signal-standard design/report` | Superseded by `signal-standard` code for existence and machine validation; still useful for migration rationale and roster reconciliation until all consumers import from `signal-standard`. |
| designer `682 — overview and context maintenance` | Good baseline for the June 18 state, but now stale on `signal-standard` existence, remotes, and `signal-criome` strict migration. Retire after the final `424` synthesis or a fresher overview. |
| designer `683 — design review and direct criome networking lane` | Still carries direct-lane and BLS aggregate rationale. Its registry-owner fork is superseded by router-sole; its duplicate-quorum warning is corrected. Keep only the direct-lane sections until a newer direct-lane report absorbs them. |
| designer `684 — design woes` and designer `684/4 — BLS aggregate verification explained` | `684/3` is stale where it calls router-sole unresolved; the inline "RESOLVED" note is current but noisy. `684/4` remains load-bearing: aggregate BLS is a v1 value-prop requirement for the direct lane. |
| designer `685 — cross-machine self, Mentci, criome tiers, keystore` | Mentci parts are superseded by `687`, `422`, `423`, and Spirit `7x5z`/`gc0n`; q1le key custody and AuthorizedHead / MirrorAdopter remain live design topics outside operator `423`. |
| designer `686 — Mentci PoC furthering` and designer `687 — Mentci full component` | Superseded by operator `422`/`423` for what exists; still useful for design rationale until repo architecture absorbs it. Stale comments about `signal-standard` not being a crate should not be copied forward. |
| designer `688 — handoff to system-designer` | Current for router-sole, closed verdict, per-user criome, and the signal-criome migration correction. Stale where it says remotes remain the operational gate; operator `423` closed that part. |
| designer `689 — audit of operator 422` | Validates `422` completely, but is not current after `423`. Keep as audit evidence until the final synthesis states that `423` supersedes it for runtime/remotes. |
| system-designer `138/3 — signal-standard crate` | Superseded by operator `423` for remote creation, but still useful as the original build proof. |
| system-designer `138/5 — synthesis and decisions` | Stale on the router/fan-out decision: Spirit `m0p2`/`l2ha` have resolved router-sole. |
| system-designer `139 — unblocked attendance fan-out and scoped majority guard` | Current for active fan-out and scoped majority-guard build framing. Stale where it says `signal-standard` remote and `signal-criome` migration remain operator gates; both are now closed in current repo state. |
| system-designer `140 — deploy cross-host router transport handoff` | Current for transport deployment ladder. Stale in its "not for system-operator" note that lists signal-standard remote creation and signal-criome positional migration as still open. |

## Intent Findings

The old m0p2/l2ha contradiction is resolved in Spirit, not merely in reports.
`m0p2` now says criome emits authorized-object references and the router is the
sole operational matcher for non-direct message passing. That makes older
phrasing in operator `414`, operator `415`, operator `417`, designer `677`,
designer `678`, designer `682`, designer `683`, designer `684`, and
system-designer `138/5` stale wherever they describe the registry-owner fork as
open or imply criome owns operational delivery.

`signal-standard` is no longer only a design. Spirit `eeeo` says it is the
shared cross-component standards crate, and code now exists with a remote. Any
report or schema comment saying "signal-standard is not yet a crate" is stale.
The remaining work is consumer migration, not crate creation.

Mentci's design questions from operator `419` and `421` are resolved:

- `7x5z` fixes Mentci as first-class component triad and state-bearing daemon.
- `gc0n` fixes the closed verdict model and the separate typed proposal path for
  authored answers.
- `9s52` fixes per-Unix-user criome and removes shared multi-user system criome
  as a Mentci premise.
- `q1le` keeps real verdict signing gated on encrypted criome key custody.

No intent maintenance action was taken. The report-only recommendation is that
future cleanup should edit reports and permanent docs to match these active
records rather than mint new sibling clarification records.

## Remaining Open Work

1. Router fan-out must land on main: `Attend` / `Withdraw`, router-local durable
   attendance table keyed by `signal-standard` interest/differentiator, and
   reference push to subscribers. The router is the sole operational matcher.

2. Criome local subscription code needs a clear role: observation/audit only.
   Future operator work must not treat criome's local registry as the
   cross-component delivery table.

3. `signal-standard` consumer migration remains open. Current scans still show
   local rosters in `signal-criome`, `signal-persona`, and `signal-message`; the
   Mentci contracts still carry local `StandardSocket` / `ComponentKind`
   stand-ins and comments that predate the crate.

4. Mentci runtime remains incomplete despite the daemon landing: SEMA state is
   in-memory, notification fan-out is not wired, `signal-mentci`,
   `meta-signal-mentci`, and `mentci` lack Nix gates in operator `423`, and real
   cryptographic verdict egress waits on `q1le`.

5. Criome direct-lane work remains separate from object fan-out: aggregate BLS
   verification, scoped attested-moment/head majority guard, replay/rate-limit
   protections, and the direct criome-to-criome peer protocol are not closed by
   the object-pulse reports.

6. The cross-machine head / MirrorAdopter design from designer `685` is still
   design-stage. It should not be inferred as implemented by Mentci or router
   transport work.

## Recommended Retirement Order

No deletions in this pass.

First retire the reports whose entire substance has a stronger current landing:
operator `406 — Criome Internal Language POC`, operator `407 — designer 674.11
audit`, operator `408 — policy triad schema branches`, operator `409 —
attested moment POC`, operator `416 — signal-standard catch-up`, operator `417
— designer 682 feedback`, operator `419 — Mentci approval surface`, and operator
`421 — Mentci PoC feedback`, after the final `424` synthesis carries their live
points.

Forward before retiring: operator `410 — policy language main landing`,
operator `414 — classified pulse POC`, operator `415 — interest-bearing token
landing`, operator `418 — designer 683 review`, operator `420 — Mentci daemon
state`, and operator `422 — Mentci component implementation`. Each still holds
some useful rationale, but not as the current state surface.

Keep for now: operator `412 — strict positional structs`, operator `413 —
strict positional open questions`, and operator `423 — Mentci remotes and
daemon runtime`. `412` and `413` should migrate into schema docs/skills; `423`
is current until the next Mentci runtime report supersedes it.
