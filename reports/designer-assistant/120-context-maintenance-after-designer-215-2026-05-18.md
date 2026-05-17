# 120 - Context maintenance after designer/215

Date: 2026-05-18  
Role: designer-assistant  
Status: context-maintenance rollover after reading
`skills/context-maintenance.md` and
`reports/designer/215-workspace-state-of-art-2026-05-18.md`.

## 0. What this pass did

This pass treats designer/215 as the current master compendium and does not
try to restate all eight topic reports. It extracts the active workspace
status and the questions that most need user attention.

No reports were deleted in this pass. Reason: designer/215 is itself a
forwardable compendium and contains some minor keep-vs-retire tensions across
its per-topic reports. Example: designer/215 marks DA/117 as a retire
candidate, while designer/218 says DA/117 is fine as an authority-decision
audit trail. A later cleanup pass should delete the clear stale reports after
the relevant lane owners confirm the final keep/drop ledger.

## 1. Current status

### 1.1 Workspace shape has converged

The dominant shape is now stable:

- every stateful component is a triad: daemon + thin CLI + Signal contract;
- daemon state goes through sema-engine;
- privileged authority gets a separate `owner-signal-*` contract and socket;
- `Mutate` is the top-down authority verb;
- ordinary and owner surfaces are permission surfaces, not separate state
  owners;
- the full Signal executor means a component-local actor plane, not
  sema-engine becoming a protocol host.

This is the main win from the recent work.

### 1.2 Full Signal executor

Canonical status:

- sema-engine remains a contract-blind database executor;
- no speculative sema-engine APIs now (`validate_write`, `commit_multi`,
  `unsubscribe` are dissolved or deferred);
- first executor implementation target is `persona-terminal`;
- second target is `lojix-daemon`;
- only after both prove the same shape should a small `signal-executor`
  library be extracted.

Open implementation constraint: each component's `SemaEngineOwnerActor` must
prove exclusive redb handle release before restart is trusted.

### 1.3 Persona terminal

Landed:

- `owner-signal-persona-terminal` exists;
- `CreateSession` and `RetireSession` moved out of ordinary terminal Signal;
- `persona-terminal` has a Kameo owner request path that returns typed
  `OwnerTerminalRequestUnimplemented { reason: NotBuiltYet }`.

Missing:

- owner-terminal Unix socket listener;
- real `CreateSession` execution;
- real `RetireSession` execution;
- one-daemon consolidation;
- CLI collapse;
- `persona-terminal-view` should resolve sessions through daemon Signal, not
  direct Sema reads.

### 1.4 Persona orchestrate

Orchestrate is the biggest architectural bottleneck.

Settled:

- real triad daemon, not just `tools/orchestrate`;
- owned by `persona-mind`;
- ordinary + owner Signal surfaces;
- first OwnerSignal chain:
  `mind -> orchestrate -> router/harness -> terminal`;
- roles become runtime lane records, not hardcoded enums.

Missing:

- `signal-persona-orchestrate` contract repo;
- `owner-signal-persona-orchestrate` contract repo;
- `persona-orchestrate` daemon repo/schema;
- `owner-signal-persona-router`;
- `owner-signal-persona-harness`;
- harness executor-management relation;
- lane registry finalization.

Bead `primary-699g` is the designer pickup for this.

### 1.5 Criome + Lojix + Arca

Lojix lean rewrite and Criome routed authorization have real code now.

Landed:

- Lojix daemon/CLI shape is on `horizon-leaner-shape`;
- Lojix has a `CriomeAuthorization` actor gate;
- Criome has authorization coordinator state and expiry/replay guards;
- signal/criome contracts have policy/grant structures;
- signal-lojix has stable deployment request digest witnesses.

Missing:

- real `signal-criome` socket client in Lojix;
- BLS master-key signing;
- real BLS verification;
- `owner-signal-criome` design and implementation;
- unattended-system-daemon bootstrap;
- cross-user same-host routing;
- Arca daemon still needs implementation;
- production cutover has not happened. Production remains old Stack A.

### 1.6 Kameo and Persona engine

Kameo lifecycle arc is considered closed enough for component migration:

- terminal outcome model landed;
- lifecycle control mailbox landed;
- operator/designer reports agree on migration shape;
- old Kameo reports are mostly retire candidates.

Remaining implementation caution: every state-bearing actor that owns an
exclusive resource needs a resource-release witness before restart is trusted.

Persona engine sandbox exists and has real dev-stack progress, but full engine
prototype still depends on terminal/orchestrate/harness/router live paths.

### 1.7 Speech / Whisrs

This arc is research-only and has one live operational risk:

- `primary-51pn` is a P0 live bug: service restart while recording can drop
  in-memory audio.
- Previous mitigation was rolled back.
- No `persona-transcription`, `persona-speech-synthesis`, or `persona-speech`
  component exists yet.

Speech implementation is blocked by seven user decisions, but the P0 Whisrs
bug may warrant a narrow fix independent of the long-term architecture.

## 2. Best questions for the user

### Q1. Superseded — should routine operator landings create short reports?

Original recommendation in this report: make one-screen operator session
reports mandatory for every code landing.

Superseded by the user's 2026-05-18 correction: routine code landings should
not duplicate their commit message into a report. The `jj` commit description
is the short implementation report: what changed, witnesses passed, stubs left,
and next slice when relevant. A future repository-change ledger daemon should
index those commits and make them queryable by repo, role/lane, time window, and
path. Reports stay for design, audits, implementation-consequence findings,
cross-repo synthesis, and user decisions.

### Q2. What is the owner-terminal socket path policy?

Operator can implement the owner-terminal listener next, but the path policy
should be explicit.

Current open options:

- persona-daemon assigns the owner socket path in the component spawn envelope
  under the per-engine run directory;
- `persona-terminal` hardcodes a path under its runtime directory;
- harness owns or co-locates the path.

Recommendation: persona-daemon should assign it through typed config/spawn
envelope. Hardcoded XDG paths make the engine less portable and weaken the
manager's correctness role.

### Q3. Should orchestrate lane identity be `Slot<LaneRecord>`?

The RoleName enum is going away. Lanes become registry records. The open
identity question is whether lane identity is a string, hash, or typed slot.

Recommendation: use a typed slot / store-minted identifier. It matches the
workspace rule that infrastructure mints identity and avoids stringly role
names becoming new enums by accident.

### Q4. On orchestrate startup, does config win over persisted lane state?

When `roles.nota` or equivalent config diverges from sema-engine
`LaneRegistry`, the daemon needs one rule.

Recommendation: config is desired state, persisted sema-engine state is
observed state. Startup reconciles toward config by appending typed registry
mutations, not by silently replacing the database. If a destructive change is
needed, require an owner-signal mutation.

### Q5. Can Criome v1 use unencrypted master key material protected by Unix
permissions for unattended daemon bootstrap?

This blocks cluster-side Criome.

Recommendation: yes for v1, with a loud architecture note. It matches the
local trust model already used elsewhere: Unix user + filesystem permissions
are the boundary. TPM sealing can be v2.

### Q6. What exactly is signed in a Criome `SignedObject`?

This blocks BLS verification and master-key signing.

Recommendation: sign canonical rkyv bytes of a typed object that includes all
security-relevant scope: request digest or content digest, action verb, target
cluster/node/environment, expiry, anti-replay nonce, issuing criome identity,
and the satisfied policy spec. Criome must receive the original bytes plus the
digest; digest-only is not enough for verification.

### Q7. Do you want to fix Whisrs P0 narrowly before the speech architecture
decisions?

The long-term speech component is blocked by seven product questions. The
live P0 bug is narrower: restart while recording can lose audio.

Recommendation: authorize a narrow durable-spool/restart-safe fix for Whisrs
now, separately from the full `persona-speech` design.

## 3. Next-session targets

1. Done in the follow-up pass: replace the mandatory short-session-report rule
   in `skills/operator.md` and `skills/reporting.md` with the commit-description
   discipline, and write a repository-change-ledger proposal.
2. If user answers Q2, hand operator a precise terminal-owner-socket
   implementation note.
3. If user answers Q3/Q4, feed designer/orchestrate pickup (`primary-699g`).
4. If user answers Q5/Q6, unblock Criome BLS/master-key signing and
   owner-signal-criome design.
5. If user answers Q7, hand system/operator a narrow Whisrs P0 fix track.

## 4. Report hygiene notes

Clear retire candidates from this lane:

- `reports/designer-assistant/118-signal-core-sema-engine-fit-investigation-brief-2026-05-17.md`
  — audit landed in second-OA/2 and the concept landed in DA/119 + second-OA/3.

Needs reconciliation before deletion:

- `reports/designer-assistant/117-review-operator-134-terminal-orchestrate-porting-decisions-2026-05-17.md`
  — designer/215 marks retire-eligible, designer/218 says keep as audit trail.
  It has a supersession note and is harmless; delete only after the terminal
  owner-socket work absorbs the remaining audit value.

Do not delete in this pass:

- `reports/designer-assistant/119-full-signal-executor-architecture-concept-2026-05-18.md`
  — canonical concept until executor shape lands in component ARCHs or a future
  `signal-executor` README/ARCH.
