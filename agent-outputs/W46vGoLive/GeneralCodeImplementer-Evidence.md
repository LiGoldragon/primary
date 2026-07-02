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

## Stage 3 — live run (IN PROGRESS)

Command: `synchronizer goldragon/synchronizer.nota`, backgrounded.
Report → `SyncNotaReport.nota`; stderr → `run-stderr.log`.
Expected bumps (all stale on signal-frame main tip): signal-router,
signal-harness, introspect, persona; signal-frame is the leaf (AlreadyAligned).

<run result + gate result + landing decision + primary-w46v disposition: TO BE
FILLED after the background run completes>

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
