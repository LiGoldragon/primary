# lojix vision gap audit

## Scope

Audits `reports/system-specialist/154-lojix-signal-migration-vision-2026-05-20.md`
against:

- workspace-wide psyche intent (`intent/component-shape.nota`,
  `intent/signal.nota`, `intent/deploy.nota`, `intent/arca.nota`,
  `intent/nota.nota`, `intent/horizon.nota`);
- landed Signal three-layer model
  (`reports/operator/144`, `reports/designer/254`,
  `reports/system-specialist/153`);
- adjacent system-specialist reports `137`, `138`, `139`, `140`, `141`,
  `142`, `143`, `149`, `152`, `153`.

The vision targets the rewrite stack
(`horizon-leaner-shape` worktrees for `signal-lojix` and `lojix`,
plus the new `lojix-daemon`). Production `lojix-cli` on `main` is
out of scope.

Confirmed repo state under `/git/github.com/LiGoldragon/`:

```
arca        criome        lojix-archive    signal-criome
            lojix         lojix-cli        signal-lojix
```

`owner-signal-lojix`, `signal-arca`, `owner-signal-arca`,
`owner-signal-criome` do NOT exist yet.

## Summary of gaps

1. Owner contract `owner-signal-lojix` is missing from the triad
   shape — Maximum-certainty universal rule.
2. Policy state vs working state taxonomy is absent (and the
   `bootstrap-policy.nota` first-start path is not named).
3. Criome-mediated authorization is mentioned once as an "effect" but
   does not appear in the migration order.
4. Daemon-to-daemon mesh (lojix-daemon → local criome-daemon; future
   peer lojix-daemons) is not addressed.
5. `lojix-daemon` ownership of nix.conf + per-node Nix signing key is
   not in the command vocabulary.
6. CLI two-socket dispatch (working + policy) is not in the migration
   order — the vision still treats the CLI as one-socket.
7. Pilot-first sequencing (`persona-spirit` before `lojix` daemon
   work) from `/153` is not carried forward to the later migration
   steps.
8. Three-layer trait surface (`Lowering::Command`, `OperationPlan`,
   `CommandExecutor`, `BatchErrorClassification`,
   `ObservedLowering`) is only named — the wiring inside `lojix-
   daemon` is not concretely shown.
9. Reply-error mapping (which lojix domain failures are
   `OperationAborted` vs `BatchAborted`, with what `RetryClassification`
   / `CommitStatus`) is unspecified.
10. Observable surface — whether lojix is a "persona component"
    (mandatory `Tap`/`Untap`) or non-persona (no universal observer
    block at all) — is unresolved.
11. Arca dependency for content-addressed deploy artifacts is
    deferred without being acknowledged.
12. Open question #2 (Submit-only vs split Build/Activate/Deploy/
    Rollback) leans toward Submit-only, which sits against the
    workspace's settled "verbs are cheap; splitting is usually
    better than collapsing" principle.

## Top-tier — contradicts Maximum-certainty intent or skips mandatory triad piece

### Gap 1 — owner-signal-lojix is missing from the triad

The vision never mentions `owner-signal-lojix`. Migration order §1
("Stabilize signal-lojix") names only the working contract.

Conflicts with:

- `intent/component-shape.nota` 2026-05-18T22:15:57Z Constraint
  Maximum: *"owner-signal-`<component>` is part of the triad, not a
  follow-up arc. A daemon with only the ordinary signal-`<component>`
  surface is not yet triad-shaped. The next implementation arc for
  any new component ships both authority contracts together."*
- `intent/signal.nota` 2026-05-20T12:11:26Z Decision Maximum: *"Every
  stateful component has an owner contract because management and
  configuration must enter through an owner-only signal surface that
  can be protected by filesystem permissions."*
- AGENTS.md Hard override `Component triad`.

What's load-bearing on the owner surface for lojix specifically:

- builder selection policy mutations (which nodes count as builders);
- cache selection / trust policy mutations
  (per `intent/deploy.nota` 2026-05-17T13:30:00Z, transient
  substituter trust keys are installed/removed per deploy);
- believed-topology policy bootstrap + corrections (per
  `intent/deploy.nota` 2026-05-17T11:00:00Z);
- `criome-daemon` endpoint reference (which authorization fabric this
  daemon consults);
- per-node Nix signing key reference / rotation (per
  `intent/deploy.nota` 2026-05-17T13:30:00Z);
- ClaviFaber / certificate trust material for cluster-peer
  communication;
- GC retention policy;
- future: lifecycle (start/drain/reload), if not absorbed by the
  infrastructure supervisor.

Action: add `owner-signal-lojix` to Migration order §1 ("create the
working AND policy contracts; both ship together"); add an explicit
"Policy command layer" subsection alongside §3's `LojixCommand`
detailing the owner-only command variants the daemon executes when
mutated by its owner.

### Gap 2 — policy state vs working state taxonomy absent

The vision's `LojixCommand` enum (§3) is all working-state mutations
(allocate, record, authorize, build, query, pin, retire, watch).
Nothing names the policy-state side or the `bootstrap-policy.nota`
seed.

Conflicts with:

- `intent/component-shape.nota` 2026-05-19T01:30:00Z Decision
  Maximum: *"Every triad daemon has two state categories in one
  sema-engine DB: policy state (rules; owner-Mutate only;
  bootstrapped one-shot from bootstrap-policy.nota in the repo) and
  working state (records produced by operation; never bootstraps;
  mutated per contract variants)."*
- `intent/component-shape.nota` 2026-05-19T01:25:00Z Principle
  Maximum: *"Configuration is always a Mutate. … The way the daemon
  is configured is not some optional state."*

Lojix policy state to name:

- builder registry (which nodes are eligible builders);
- cache trust policy (which substituters are accepted);
- believed-topology baseline (cluster identity, peer references,
  routing-cost defaults);
- criome endpoint configuration;
- nix-config defaults (build-cores, max-jobs, store path, sandbox);
- per-deploy authorization-policy template (what kinds of deploys
  need what kinds of authorization).

Working state to name (vision implies these; the taxonomy should
make them explicit):

- deployments table (allocate, submitted, authorized, building,
  built, activating, current, failed);
- generations table (built, pinned, current, retired);
- effect-lifecycle observations (build started/finished, store-
  import started/finished, activation started/finished);
- watch subscriptions table.

Action: add a §"Daemon state taxonomy" before §3 that names policy
and working state categories, says `bootstrap-policy.nota` lives in
the `lojix` repo, and notes the first-start seed mechanism.

### Gap 3 — Criome authorization missing from migration order

§"Important split" mentions "Criome authorization" once as an
"effect" requiring actor-owned execution. Migration order §1-7 never
returns to it. A real deploy on the rewrite stack cannot land without
the criome path because authorization is the precondition for
build/activation.

Conflicts with:

- `intent/deploy.nota` 2026-05-17T15:30:00Z Decision Maximum:
  *"Authorization for a signal-lojix call is propagated through the
  criome-daemon topology. … lojix-daemon does not own permission and
  does not sign — it submits intent and waits for criome to authorize.
  The signature lives in criome, not in lojix."*
- system-specialist reports 140, 141, 142, 143 (Criome-mediated
  authorization design arc).

Action: add a migration-order step "Wire `lojix-daemon` as a Signal
client of `criome-daemon` over `signal-criome`; canonical signed
object is the `signal-lojix` request record"; add Nix witnesses
`lojix-daemon-is-a-signal-client-of-criome-daemon` and
`lojix-rejects-unauthorized-deploy-with-typed-reply`.

### Gap 4 — daemon-mesh shape not addressed

The CLI invariant ("exactly one peer, lojix-daemon") is preserved
in §2. But the new model's load-bearing pattern is that
`lojix-daemon` itself is a Signal client of `criome-daemon` (and
eventually of peer `lojix-daemon`s for distributed deploys per
`reports/system-specialist/138`).

Triad invariant 1 (CLI = one peer) is unchanged; carve-out 3
(daemons may be Signal clients of any number of peer daemons) is
the right home for this. The vision should explicitly assert it.

Conflicts with the spirit of:

- `intent/deploy.nota` 2026-05-17T15:30:00Z Decision Maximum:
  *"daemons talk to each other, the cli (or any client) only
  initiates the deploy. the daemon then forwards the request to the
  criome-daemon, which might route the request signature(s) to the
  concerned clients."*

Action: name the daemon-mesh shape in §"Desired end shape" and list
which peer daemons `lojix-daemon` opens client connections to
(`criome-daemon` minimum; future `arca-daemon`, peer `lojix-daemon`s).

## Middle-tier — underspecification of landed shape

### Gap 5 — lojix-daemon's control of nix.conf + signing keys not in commands

`intent/deploy.nota` 2026-05-17T13:30:00Z Maximum: *"lojix-daemon
takes control of nix configuration. It can change /etc/nix/nix.conf
(or an include slot the daemon owns per the
NixDaemonConfigurationActor pattern) and restart nix-daemon whenever
the deploy plan requires."* Same turn: *"all nodes should have a nix
signing key (clavifaber populated on first boot)."*

These are part of the deploy flow on the lean stack (transient
substituter trust per-deploy, signed binary caches between cluster
nodes). They don't appear in `LojixCommand` and don't appear in the
effects list.

Action: add `InstallSubstituterTrust(...)` / `RemoveSubstituterTrust(...)`
and `RestartNixDaemon` (or equivalents) to the command enum sketch;
name the `NixDaemonConfigurationActor` in §"Important split"
alongside the other effect actors; document the per-node signing-key
read path (likely just a config reference, since ClaviFaber populates
it on first boot).

### Gap 6 — CLI two-socket dispatch not in migration order

`intent/signal.nota` 2026-05-20T13:00:00Z Clarification Maximum:
*"Every CLI talks to two sockets, both belonging to its one peer
daemon: the working socket (the peer-callable, signal-`<component>`
socket — `working` and `public` are synonyms naming the same
socket) and the policy socket (the owner-only,
owner-signal-`<component>` socket). The CLI must dispatch each
incoming NOTA request to the correct socket based on which contract
the request belongs to."*

Migration order §2 ("Move `lojix` wire dependency to signal-frame")
treats the CLI as one-socket. Once owner-signal-lojix exists the CLI
needs the dispatch logic.

Action: add to Migration order §2 *"and add policy-socket dispatch in
the CLI: parse the NOTA request, look up which contract it belongs
to, send to the matching socket."* Same workspace-universal CLI
shape applies (`intent/signal.nota` 2026-05-20T13:00:00Z Principle
Maximum: "CLI design is workspace-universal").

### Gap 7 — pilot-first sequencing dropped after step 2

`reports/system-specialist/153` is by the same lane and explicitly
said *"Do not start `lojix` migration from the old report order.
`lojix` is deployment infrastructure; it should consume the proven
shape after the persona-spirit pilot proves the real daemon path."*

Vision §"Next action" captures part of this (start with the
contract/docs/test cleanup before editing `lojix`), but Migration
order §3-7 reaches into `lojix-daemon` code without acknowledging
the persona-spirit-pilot gate.

Action: split Migration order into "Phase A — independent of
persona-spirit pilot" (§1, §2, partial §6 deploy.rs split for
preparedness) and "Phase B — requires the proven shape from the
pilot" (§3-5, §7). Restate the §153 gate at the start of Phase B.

### Gap 8 — three-layer wiring inside lojix-daemon is only named, not shown

§3 lists `LojixCommand` variants and §4 names `Lowering` /
`CommandExecutor` / `BatchErrorClassification`. It doesn't show:

- the `impl Lowering for LojixLowering` shape (Operation, Command,
  Reply associated types; the `lower()` signature returning
  `Result<OperationPlan<LojixCommand>, LojixReply>`);
- the `impl ToSemaOperation for LojixCommand` mapping (the
  vision sketches the mapping prose-wise but not the trait impl);
- the `impl ToSemaOutcome for LojixEffect` mapping
  (`intent/signal.nota` 2026-05-20T12:33:11Z Decision High);
- where `BatchErrorClassification` is implemented (lojix's engine
  error type? the executor wrapper?);
- the `impl ObservedLowering` projection for the observable
  declaration (per `intent/signal.nota` 2026-05-20T01:00:00Z
  Decision Maximum).

Action: add a §"Three-layer trait wiring" subsection in §"Desired
end shape" with the trait-impl skeletons.

### Gap 9 — reply-error mapping is unspecified

`intent/signal.nota` 2026-05-20T01:00:00Z Decision Maximum: three
accepted outcomes (`Committed`, `OperationAborted { failed_at,
reason }`, `BatchAborted { reason, retry, commit }`). Reply::Rejected
is reserved strictly for pre-acceptance failures.

The vision lists witnesses
`lojix-domain-rejection-is-operation-aborted-not-frame-rejected`
and `lojix-engine-failure-is-batch-aborted-with-classification`
but doesn't map lojix's domain failures to specific reasons:

- invalid deployment request → `OperationAborted`, reason?
- criome denied → `OperationAborted`, reason?
- builder unavailable → `OperationAborted` or `BatchAborted`?
- cache source unavailable → `OperationAborted` or
  `BatchAborted`?
- Nix build failed → effect-lifecycle observation
  (asynchronous), not a synchronous reply at all?
- activation failed → effect-lifecycle observation, same as
  above?
- engine commit failure → `BatchAborted` with what
  `RetryClassification` / `CommitStatus` defaults?

Action: add a table in §"Desired end shape" mapping each lojix
failure mode to the right reply variant + classification metadata.

## Lower-tier — worth flagging

### Gap 10 — observable surface for lojix is unresolved

`intent/signal.nota` 2026-05-20T02:00:00Z Decision Maximum: *"Tap/
Untap is mandatory for persona components, no author override. …
Non-persona small utilities don't declare an observable block at all;
they have no observability surface."*

lojix is deployment infrastructure, not a `persona-*` component. So
the mandatory-Tap/Untap rule does not apply. But the vision proposes
`WatchDeployments` / `WatchCacheRetention` — domain observation. The
question is whether lojix *also* declares a universal observer block
(introspection via `persona-introspect`) on top of its domain
streams, or whether domain streams are the entire observation
surface.

Report 149 §6 raised this and recommended both surfaces; the vision
inherits that direction implicitly but doesn't state it.

Action: in §"Contract layer", explicitly state whether
`signal-lojix` declares a universal observable block (with
contract-authored open/close verbs per the macro redesign) or only
the domain streams. If both, the bridge between executor facts and
contract event records (per report 149 §6 and report 152) must be
named.

### Gap 11 — Arca dependency deferred but not acknowledged

`intent/arca.nota` establishes Arca as the content-addressed
substrate for cross-node artifacts. `reports/system-specialist/137`
and `/138` explicitly route generated Nix inputs / deploy plans /
authorization objects through Arca.

The vision lists "generated Nix inputs" in §"Important split"
without referencing Arca. `signal-arca` doesn't yet exist as a repo;
the deferral is reasonable but should be acknowledged.

Action: add a sentence in §"Important split" — *"Generated Nix
inputs, deploy plans, and topology snapshots will move into
Arca-mediated content-addressed storage once `signal-arca` lands;
until then they live as local filesystem artifacts owned by
lojix-daemon."*

### Gap 12 — Open question #2 conflicts with verbs-are-cheap principle

Vision Open question #2: *"Should `Deploy` remain one broad public
operation … or should the public contract split into `Build`,
`Activate`, `Deploy`, and `Rollback` before the command-layer work?
My preference is to keep `Deploy` until activation/rollback semantics
are real enough to deserve public verbs."*

`intent/signal.nota` 2026-05-19T20:30:00Z Decision Maximum: *"signal-
persona-mind's channel-choreography family splits into multiple
contract-local verbs … rather than collapsing under one Adjudicate
verb. The split makes the logic clearer; verbs aren't to be feared.
Apply the split rule generally: when the choice is between one verb
covering many sub-actions and multiple verbs naming each
sub-action, prefer multiple verbs."*

The vision's stated preference sits against this. It's not a hard
contradiction because the broader principle says "usually," but
the psyche should rule rather than the vision defaulting to
Submit-only on lane preference.

Action: in Open question #2, name the split-is-usually-better
principle and frame the question as *"does Deploy have unusual
collapse-justifying properties, or should the split happen now?"*

### Gap 13 — stream-close grammar — verify macro owns the token

Vision §"Current reading" lists `WatchDeployments / UnwatchDeployments`
and `WatchCacheRetention / UnwatchCacheRetention`. Report 149 §6
sharpens: *"the close operation should name only the verb, because
the macro owns the observer token payload. In other words, prefer
`close Unwatch;` over making every contract author spell the token
type."*

Action: when verifying signal-lojix in Migration order §1, check
that the `signal_channel!` close grammar names only the verb and
does not redeclare the token payload type.

## Open questions worth psyche attention

1. **`owner-signal-lojix` creation timing.** The universal-owner-
   contract rule says both contracts ship together. Should
   `owner-signal-lojix` be created and stubbed out before the
   working contract is fully cleaned up (so the repo set is right
   from the start), or after Migration order §1?

2. **Policy state seed for lojix's believed-topology.** Does the
   first-start `bootstrap-policy.nota` declare an empty
   believed-topology (the daemon discovers from runtime
   observation), or does the cluster author write the initial
   topology declaratively (matching the spirit of `goldragon/
   datom.nota`)?

3. **Per-deploy substituter trust key — is this an owner Mutate
   on lojix, or a working-side effect command?** It's transient,
   per-deploy, and triggered by an authorized deploy submission
   — so it likely belongs in the working effect lifecycle rather
   than the owner surface. But the substituter trust list is
   policy. Worth ruling on.

4. **Submit vs split (Open question #2 in /154 + Gap 12 here).**
   The verbs-are-cheap principle (Maximum) leans split; the
   vision's preference is keep-Submit until activation/rollback
   semantics are real. Which way?

5. **Pilot-first sequencing strictness.** Is Migration order
   §1+§2 (contract cleanup, wire move) an acceptable parallel-
   to-pilot Phase A, or should everything wait for the persona-
   spirit pilot? `/153` reads as the latter; the vision implicitly
   acts as the former.

## Things the vision gets right (carry forward)

- Three-layer model named correctly (Contract Operation →
  Component Command → Sema classification).
- `lojix-daemon` (not `signal-lojix`) owns `LojixCommand`.
- `ToSemaOperation` + `ToSemaOutcome` projection mentioned.
- Domain rejection encoded as typed reply variant, not kernel
  rejection (`/149` §2 sharpened this; vision carries it).
- Effects stay actor-owned, not flattened into `signal-executor`
  (vision §"Important split"; matches `/149` §4).
- Deployment-identity smell named (`deployment_{n}` retirement).
- `deploy.rs` split by noun (§6) — well-spelled English filenames.
- Nix-backed binary witnesses required for runtime paths (§7).
- CLI invariant (one peer = `lojix-daemon`) preserved.
- Worktree-only edits on `horizon-leaner-shape` (production
  unaffected).

## See also

- `reports/system-specialist/154-lojix-signal-migration-vision-2026-05-20.md`
  — the audited vision.
- `reports/system-specialist/153-signal-refresh-144-system-impact.md`
  — pilot-first sequencing.
- `reports/system-specialist/149-lojix-signal-design-adjustments-after-244-245.md`
  — prior lojix design notes the vision builds on.
- `reports/system-specialist/137`, `138`, `139`, `140`, `141`,
  `142`, `143` — Arca + Criome + cache-coordination design arc.
- `skills/component-triad.md` — the triad invariants and
  single-argument rule.
- `intent/component-shape.nota`, `intent/signal.nota`,
  `intent/deploy.nota`, `intent/arca.nota` — the psyche-intent
  sources for each gap above.
