# synchronizer go-live + w46v — implementer evidence

Session: W46vGoLive. Role: general code implementer (go-live worker).
Task: publish the `synchronizer` tool as a PUBLIC GitHub remote, confirm the
config covers the w46v wire-skew, run the tool live, verify the whole-engine
gate on prometheus, and land producers→consumers only if GREEN (else STOP).

## Stage 1 — PUBLIC remote (DONE)

- Created `https://github.com/LiGoldragon/synchronizer`, visibility **PUBLIC**
  (`gh repo view` → `isPrivate:false, visibility:PUBLIC`).
- Wired `origin git@github.com:LiGoldragon/synchronizer.git`, pushed `main`.
- Remote `main` = `85bbd3d0d115306eff224fa42cb17e5b77432336` (matches local).
- Pre-publish safety: `src/` matches for LiGoldragon/criome are all doc-comment
  examples ("e.g. `LiGoldragon`", "no `synchronizer@criome.net` baked in"); no
  secrets, no tokens. Consistent with the audit PASS (zero runtime project data).

## Stage 2 — config coverage (DONE: added persona)

Edited criome config `goldragon/synchronizer.nota` (claimed via orchestrate;
committed + pushed to goldragon `main` = `219396b2`). Added `(persona AtRoot)`
to the component list (now 5: signal-frame, signal-router, signal-harness,
introspect, persona). `examples/validate` → "ok: 5 components configured".

persona is the stale writer of the w46v skew and a legitimate consumer of the
signal contracts, so it belongs in the sweep. router/message were deliberately
NOT added — see the structural diagnosis; a note to that effect is in the config
file.

### w46v drift facts (Cargo.lock pins; all sourced `branch=main`)

signal-router pin across consumers (3-way drift):
- persona   `f81d4646` (2026-06-17)  ← stale writer, PRE wire-field
- harness   `277bd153` (2026-06-23)
- router    `289c7de4` (2026-06-29)  ← via persona flake input, the reader
- main tip  `30be9b0f` (2026-07-02, docs-only above 289c7de4)

Intervening signal-router `d212ea8` (2026-06-28) APPENDS wire field
`attestation_issued_at` on RouterPeerAttestation. persona@f81d4646 is below it
(writer omits the field); router-daemon@289c7de4 is above it (reader expects it)
→ the witnessed `router-daemon.rkyv` decode failure.

signal-frame pin across consumers:
- persona   `166bda84` = v0.2.1 (PRE 0.3.0)
- router    `d0dd5c0b` = v0.2.1 (PRE 0.3.0)  ← the frozen router-daemon uses this
- main tip  `0027ea3c` = v0.3.0

signal-frame `b78c807` "bump to 0.3.0 for caller identity" ADDS an rkyv field
`identity: Option<CallerIdentity>` to the archived `Caller` struct — an archive
layout change. signal-router's wire frames are built directly on
`signal_frame::ExchangeFrame/Request/Reply/ShortHeader` (src/schema/lib.rs), so
signal-frame flows into the router wire path.

## The structural diagnosis — why the tool cannot GREEN the w46v gate

The whole-engine gate (`persona-daemon-launches-nix-built-*-topology`,
`persona-dev-stack`) builds the **router-daemon it launches from persona's own
flake input** `persona-router.url = "git+ssh://git@github.com/LiGoldragon/router.git?ref=main"`,
locked at `rev 14f855747d0a...` = router main `14f8557` (the exact "pinned
router-daemon" from the bead). That router build carries signal-router
`289c7de4` and signal-frame `d0dd5c0b` (0.2.1).

Two tool facts make this input immovable by the synchronizer:
1. **git+ssh flake inputs are not matched.** `flake_lock.rs` `is_github()`
   requires `source_type == "github"`; `github_inputs()` filters to that.
   `persona-router` is `type:git` (ssh URL), so `topology.rs` discovers no
   persona→router flake edge and never repins that node.
2. **The tool never lands to main.** Even if it bumped router's Cargo pins on a
   `synchronizer` staging branch, the gate resolves `persona-router` at
   `ref=main` from persona's committed flake.lock (14f8557), not the staging tip.

So the gate's router-daemon is FROZEN at signal-frame 0.2.1 / signal-router
289c7de4 regardless of the run. For the gate to pass, persona-daemon (built at
persona's synchronizer rev) must be wire-compatible with that frozen build. But
the synchronizer bumps persona's producers to their **main tips**:
- signal-router → 30be9b0f: wire-identical to 289c7de4 (docs-only) ✓
- signal-frame → 0027ea3c (0.3.0): adds `Caller.identity` rkyv field, INCOMPATIBLE
  with the frozen 0.2.1 router-daemon ✗

Net: the run trades the signal-router `attestation_issued_at` skew for a
signal-frame `Caller.identity` skew — the SAME failure class. **Predicted gate:
RED**, for a structural reason, not a transient one.

(Residual uncertainty: only that the topology check might not exercise a
Caller-bearing frame at runtime. The live run resolves it empirically.)

Currently persona (166bda84) and the frozen router-daemon (d0dd5c0b) are BOTH
signal-frame 0.2.1 — mutually compatible, which is why the only witnessed skew
was signal-router. Bumping persona to 0.3.0 is what introduces the new break.

## Transport prerequisites (verified GREEN)

- `ssh git@github.com` authenticates (push works); git credential helper
  `!gh auth git-credential` supplies GH_TOKEN for https push.
- Tool constructs `https://github.com/LiGoldragon/<repo>.git`; anonymous
  ls-remote/fetch works on these public repos.
- prometheus reachable (`ssh prometheus` → nix 2.34.6); builder role resolves to
  prometheus from `goldragon/datom.nota` (`NixBuilder (Some 6)`).

## Stage 3 — live run (DONE; tool exited 1 = report carries failures)

First-live NOTA report at `SyncNotaReport.nota` (187s wall). The tool's core
mechanics all worked: config decode (5 components), topology discovery (correct
DAG L0 signal-frame → L1 signal-router/signal-harness → L2 introspect → L3
persona), the cascade rule (bumped-this-run producers targeted their
`synchronizer` tips; leaves targeted main tips), object-level commit + staging
force-push, builder resolution (prometheus from the datom), and verify-check
enumeration. Per repo:

| repo | action | verify gate | result |
|---|---|---|---|
| signal-frame | AlreadyAligned (leaf) | — | NotAttempted |
| signal-harness | Bumped signal-frame→0027ea3c (CargoLock); pushed `synchronizer` e98c3104 | DefaultPackage | **Verified GREEN** |
| signal-router | Bumped signal-frame→0027ea3c (CargoLock); pushed `synchronizer` 963ddb00 | DefaultPackage | **Verified GREEN** |
| introspect | Bumped signal-router main→synchronizer (manifest) + signal-frame→0027ea3c + signal-router CargoLock→963ddb00; pushed `synchronizer` 4f65c5a8 | WireChecks (enumerated) | **VerifyFailed** |
| persona | Bumped signal-harness+signal-router main→synchronizer (manifest) + signal-frame→0027ea3c + signal-harness→e98c3104 + signal-router→963ddb00 + introspect FlakeLock→4f65c5a8; pushed `synchronizer` a2e21fbf | WireChecks (whole-engine gate) | **VerifyFailed** |

The cascade behaved exactly as designed: because signal-router/signal-harness
were bumped this run, introspect and persona pinned their SYNCHRONIZER tips
(CargoManifest redirected `branch=main`→`branch=synchronizer`, CargoLock →
963ddb00 / e98c3104), while leaves targeted main tips.

Two failure classes were collected:

1. **Transitive-lock fallback bug (introspect + persona LockEdit).** The
   `cargo update --precise` fallback failed with `error: no matching package
   named nota-next found ... location searched: .../nota-next.git`. The crate in
   that repo is `nota` (declared `{ package = "nota", ... }` by most consumers);
   the fallback used the repo/table-key identifier `nota-next`, which cargo
   cannot match. This left introspect's + persona's bumped Cargo.locks invalid.
   introspect's verify then failed downstream: `schema-rust-next ... requires a
   lock file to be present first before it can be used against vendored source`.
   This is the exact package-name≠repo-name≠table-key hazard ARCHITECTURE §4
   calls out — the transitive fallback did not apply that discipline.

2. **persona whole-engine gate (VerifyFailed) — the w46v proof.** The tool
   enumerated the full gate (persona-daemon-launches-nix-built-message-router-
   topology, -prototype-topology, persona-router-daemon-*, wire-*, engine-
   supervisor topologies) and built them on prometheus at persona `a2e21fbf`.
   It failed at nix EVAL: `Host key verification failed ... error: Failed to
   fetch git repository 'ssh://git@github.com/LiGoldragon/router.git'`.

## Stage 4 — whole-engine gate: EMPIRICALLY RED

Confirmed twice, independently of the tool:
- Direct: `ssh prometheus nix build github:LiGoldragon/persona/a2e21fbf#checks.x86_64-linux.persona-daemon-launches-nix-built-message-router-topology`
  → `error: Failed to fetch git repository 'ssh://git@github.com/LiGoldragon/router.git'`.
- Root cause reproduced: `ssh prometheus git ls-remote ssh://git@github.com/LiGoldragon/router.git`
  → `No ED25519 host key is known for github.com and you have requested strict
  checking. Host key verification failed.`

So the gate's router-daemon / message-router (sourced via persona's git+ssh
inputs `persona-router` @ router 14f8557 and `persona-message` @ message
d7dfb005) are unfetchable on the push-first builder, and the derivation cannot
even evaluate. RED at eval — before the predicted signal-frame `Caller.identity`
runtime skew is even reached (that skew still stands behind it: persona bumped to
signal-frame 0.3.0, the frozen router-daemon would be 0.2.1).

## Stage 5 — STOP (gate not green)

- Landed to NO component `main`. All mains verified UNTOUCHED post-run:
  signal-frame 0027ea3c, signal-harness 52cd2ed, signal-router 30be9b0f,
  introspect 7b53b37e, persona bbb7f070.
- The four `synchronizer` staging branches are left pushed and unmerged
  (signal-harness e98c3104, signal-router 963ddb00, introspect 4f65c5a8,
  persona a2e21fbf) — tool-owned staging surface, safe by design.
- `primary-w46v`: left OPEN (its close condition was a GREEN gate). A note with
  this evidence was added for morning review.
- The goldragon config addition (persona) is kept and pushed — persona is a
  legitimate consumer that belongs in the sweep; it is criome config, not a
  component main.

## Answer to "is git+ssh flake-input support the complete durable fix?"

**No — necessary but not sufficient.** Repointing git+ssh inputs is one of
several required pieces to clear w46v durably:

1. **git+ssh (type:git) github flake-input matching + repointing** in the tool
   (`flake_lock.rs::is_github` requires `type:github`; persona-router /
   persona-message are `type:git` ssh). Without it the launched
   router-daemon/message-router never move off 14f8557 / d7dfb005. NECESSARY.
2. **Add router + message to the configured set** — repointing needs a target
   (their `synchronizer` tips bumped to signal-frame 0.3.0 etc.). Not configured
   today. NECESSARY.
3. **The repointed input must be FETCHABLE on the push-first builder.** The
   empirical killer was `Host key verification failed` for `ssh://git@github.com/...`
   on prometheus. Preserving `original` (per §4) keeps the input git+ssh →
   still unfetchable. So the fix needs EITHER the tool to rewrite these inputs to
   `github:LiGoldragon/<repo>` form (which mutates `original`, colliding with the
   §4 preservation rule / Nix re-resolution — a real design question) OR the
   builder to trust github.com's host key. NECESSARY, and partly non-code.
4. **Fix the transitive-lock `cargo update --precise` package-identity bug**
   (nota-next → package `nota`). persona's own bumped lock was broken by it;
   even past the fetch, persona would fail on an invalid lock. NECESSARY.
5. **persona source must compile against signal-frame 0.3.0 / signal-harness
   tip.** signal-router+signal-harness built green against 0.3.0, but persona
   never got past the fetch, so this is UNVERIFIED. A consumer-source-lag the
   tool cannot mechanically fix. POSSIBLE additional step.

**`Caller.identity` is NOT a separate blocker** — it is the wire divergence that
alignment resolves. Once the router-daemon is rebuilt at the SAME signal-frame
0.3.0 as persona (items 1+2), Caller.identity matches on both ends and the skew
clears. No non-github forge assumption bites (all repos are github/LiGoldragon;
the forge abstraction handles github). The one transport assumption in play is
the git+ssh-vs-github mismatch itself.

**Cheapest durable unblock (recommended for morning):** change persona's flake
`persona-router` / `persona-message` (and any sibling git+ssh github inputs) from
`git+ssh://git@github.com/LiGoldragon/<repo>.git` to `github:LiGoldragon/<repo>`.
That single persona-repo edit makes the builder fetch them (github: works — it
fetched persona + nixpkgs), AND lets the tool's EXISTING github matcher cascade
them (once router/message are configured) — sidestepping both the tool gap (#1)
and the builder host-key wall (#3) at once. Still pair it with #2 and #4.

## Follow-ups / tool gaps (provisional, for morning review)

1. **git+ssh github flake inputs must cascade.** The tool's flake matcher is
   github-type only; the criome's cross-daemon wire flows through
   `git+ssh://git@github.com/...` inputs (persona-router, persona-message). Until
   the tool repins those, it cannot align daemons sourced through them.
2. **The durable w46v fix** needs the router-daemon the persona gate launches to
   be built from contracts matching persona's: land router's contract bumps to
   router `main`, re-lock persona's `persona-router` (+`persona-message`) flake
   inputs to that router rev, and align every consumer's signal-frame to ONE rev
   (do not bump persona to signal-frame 0.3.0 while the frozen router-daemon
   stays 0.2.1). The synchronizer bumping consumers to divergent producer main
   tips, with a frozen flake-input daemon, cannot achieve this in one pass.
