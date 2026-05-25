*Kind: Audit + Plan · Topic: parallel-implementation pivot, spirit nspawn sandbox upgrade test · Date: 2026-05-24 · Lane: designer*

# 330 · Parallel-implementation pivot + spirit nspawn sandbox upgrade plan

## §1 What changed in the lane model

Psyche directive 2026-05-24 shifted designer/operator interaction. Captured as Spirit records 508, 509, 511, 512 plus system clarification 510.

The old model: designer specified, operator implemented, designer reviewed deliveries (e.g. tasks 218/221 — "review operator delivery on primary-ezqx.1 / primary-l6pc"). The new model: both lanes carry their own implementation paths, sandbox-test them, and communicate through running code. Reports stay short and lookup-shaped; the substantive deliverable is a passing nspawn upgrade test.

Designer may stay higher-level per pass than operator (record 509). Operator carries production depth — multiple migration paths, retry, error injection, scale. Designer demonstrates the shape end-to-end. Both lanes file beads on each other so the comparison can happen against the same surface.

Three old tasks deleted (218, 221, 225 — the /328 critique-final-report). Five new tasks queued (227-231) per this report.

## §2 Worktree freshness audit

Three designer worktrees from the /327 sweep, audited against current main.

| Worktree | Base | Main now | Drift | Verdict |
|---|---|---|---|---|
| `signal-frame/mockup-stable-caller-id-1` | `70812f3` | `e509710` | 1 commit, macro refactor | RE-IMPLEMENT |
| `nota-codec/designer-327-mockup-2-schema-parser` | `139217d` | `139217d` | 0 commits | REUSE as-is |
| `signal-frame-worktrees/designer-327-mockup-3-dispatch` | `e509710` | `e509710` | 0 commits, but sibling work landed | OBSOLETE (operator's `src/operation_dispatch.rs` supersedes) |

Mockup-2 (nota-codec schema parser) sits on the exact main commit as production. Operator independently built a schema parser in `signal-frame` (commit `e5097105`) — different repo, different architectural choice. Under the parallel-implementation model these are two legal paths, not a winner-loser. Mockup-2 stays as designer's path; operator's signal-frame parser is theirs.

Mockup-3 (dispatch trait) is functionally superseded by operator's `signal-frame/src/operation_dispatch.rs`. Designer abandons that path.

Mockup-1 (Caller stable id for upgrade session resumption) — main drifted underneath the session-resumption code. Designer re-implements on fresh main only if/when upgrade resumption becomes acute; defer.

## §3 Operator current state

Per Spirit pilot work (signal-persona-spirit `74ce98cd`):

- **Sandbox migration witness exists.** `upgrade/src/bin/upgrade-spirit-sandbox-test.rs` copies the live v0.1.0 redb, runs the prototype 0.1.0→0.1.1 migration on the copy, reads back as v0.1.1 shape. Last live run: `(SandboxUpgradeSucceeded 500 500 ...)`.
- **It is in-process, not nspawn.** The test runs as a single Rust binary on the host (Ouranos/Prometheus/wherever). The v0.1.0 and v0.1.1 daemons are not separate processes; the upgrade-socket handover protocol is not exercised end-to-end; no full OS environment.
- **73 concept .schema files at v0.1** across reachable repos (`/175.3`). Validated by `upgrade/scripts/check_concept_schemas.py`. Not yet consumed by a real schema engine.
- **`/175.4` answers the macro-extensibility question** with `NodeDefinitionPoint` cursor + `BuiltinSchemaMacro` data-carrying enum + `SchemaMacro` trait. Structurally convergent with designer `/329`; operator's `NodeDefinitionPoint` naming is sharper than designer's "positional dispatch filtering". Convergence: each macro variant carries its typed input struct.

The schema repo itself has not been edited yet — that is the next major operator pass.

## §4 Designer implementation path — spirit nspawn sandbox upgrade test

This is what designer builds under the new acceptance gate (record 512).

### §4.1 Target

End-to-end upgrade test of the deployed spirit component inside a systemd-nspawn container on Prometheus. Container boots a minimal NixOS, runs spirit v0.1.0 as a user service, accepts records via the spirit CLI, then runs the v0.1.1 upgrade and verifies the records survive.

### §4.2 Where it lives

Mirror the existing `dune-nspawn-toplevel` + `nspawn-dune-on-prometheus` pattern in `/git/github.com/LiGoldragon/CriomOS-test-cluster`. New worktree:

- `flake.nix` adds `spirit-nspawn-toplevel = fixtureSystem "spirit" [ <module that installs spirit + upgrade packages> ]`
- `scripts/nspawn-spirit-upgrade-on-prometheus` mirrors `nspawn-dune-on-prometheus`: push main, SSH to Prometheus, build toplevel, criomos-nspawn create+start, exec test commands, cleanup
- New `checks/spirit-nspawn-can-build` is a pure nix check that the toplevel evaluates and builds

### §4.3 What runs inside the container

1. Boot NixOS toplevel with `persona-spirit` v0.1.0 + v0.1.1 + `upgrade` packages installed
2. As container user: start `persona-spirit-daemon` v0.1.0 with `XDG_STATE_HOME=/var/lib/spirit-state` 
3. Write N records via `spirit '(Record (workspace Decision "test-N" "test-context" Maximum "test-quote"))'` — fixed test corpus, say N=10
4. Capture pre-upgrade record set via `spirit '(Observe (Records (None None SummaryOnly)))'`
5. Trigger upgrade — designer's first cut uses operator's existing in-process `upgrade-spirit-sandbox-test` binary against the live container state directory; the v2 cut wires the real handover protocol via private upgrade socket
6. Start `persona-spirit-daemon` v0.1.1
7. Verify N records survive: `spirit '(Observe (Records (None None SummaryOnly)))'` returns the same N records as step 4 (modulo enum normalization e.g. Certainty→Magnitude per record 70)

### §4.4 Designer-high-level scope (record 509)

What designer ships in v1:
- Spirit-nspawn-toplevel that boots cleanly
- Test script that does steps 1-4 + 7 (writes records, runs operator's existing in-process migration via the binary, verifies)
- One green check: pre-upgrade and post-upgrade record counts match

What operator carries (own implementation): real handover socket protocol inside container, multiple migration steps, error injection, retry, scale to 500+ records, parallel daemon coexistence during handover window.

### §4.5 Concrete invocation pattern (mirroring nspawn-dune)

```sh
# from ouranos (designer host)
cd /git/github.com/LiGoldragon/CriomOS-test-cluster
jj git push --bookmark main
ssh prometheus.goldragon.criome 'bash -s' <<'REMOTE'
machine=spirit-upgrade-test
system_path="$(nix build github:LiGoldragon/CriomOS-test-cluster#spirit-nspawn-toplevel --refresh --no-link --print-out-paths -L)"
trap 'criomos-nspawn terminate "$machine"; criomos-nspawn remove "$machine"' EXIT
criomos-nspawn create "$machine" "$system_path"
criomos-nspawn start "$machine"
# wait for boot ...
criomos-nspawn shell "$machine" /run/current-system/sw/bin/spirit-nspawn-upgrade-test-runner
REMOTE
```

The `spirit-nspawn-upgrade-test-runner` is a small shell script baked into the toplevel that does the inside-container sequence (steps 2-7 above).

## §5 Operator beads to file (mirror tasks)

After designer's v1 lands and is green, file these beads via `bd`:

1. **operator-mirror-spirit-nspawn-v1** — replicate designer's spirit-nspawn-toplevel test in operator's own implementation. Use the same `criomos-nspawn create/start/shell` surface; operator decides internal sequencing and may diverge architecturally. Cite designer's worktree + commits for comparison.

2. **operator-extend-spirit-nspawn-handover-socket** — extend designer's v1 (or operator's mirror) to exercise the real handover protocol via the private upgrade socket per operator/161. v1 uses the in-process binary; this bead replaces that with the socket-driven handover.

3. **operator-mirror-spirit-nspawn-scale** — replicate at 500-record scale matching the existing `(SandboxUpgradeSucceeded 500 500 ...)` witness, inside nspawn. Establishes the nspawn path is not slower than the in-process path past trivial sizes.

Each bead names the designer's worktree branch + commits so operator can read designer's path. Operator's mirror lands its own worktree branch. The two implementations sit side by side until either lane absorbs the others insights.

## §6 Lower-priority parallel paths (deferred)

- **Mockup-2 forward to current main** — base unchanged, no rebase needed. Designer can land a bead asking operator to read it and decide whether to integrate the nota-codec parser approach vs continue with signal-frame parser. (Task 231.)
- **Mockup-1 re-implementation** — only if upgrade session resumption becomes a real blocker. Currently signal-frame moved past it.
- **Mockup-3** — closed. Operator's `operation_dispatch.rs` supersedes.

## §7 Open questions for psyche (only when blocked)

1. v1 acceptance: is "pre-upgrade and post-upgrade record counts match (N=10) inside nspawn, using operator's existing in-process migration binary" enough for the designer pass to count as green under record 512? Or does v1 already need the real handover socket?
2. Should the spirit-nspawn-toplevel live in `CriomOS-test-cluster` (mirroring dune) or in a new repo (`spirit-nspawn-sandbox` for symmetry with `spirit-smart-handover-sandbox`)?

Designer default: ship v1 with the in-process binary in `CriomOS-test-cluster`; the socket-handover variant becomes operator's bead 2.

## §8 Outcome — v1 landed end-to-end (2026-05-24)

Designer v1 passed the new acceptance gate (record 512) on Prometheus.

- **Branch:** `spirit-nspawn-upgrade-test` on `github.com/LiGoldragon/CriomOS-test-cluster` (head `5abfa3e6e99f`)
- **Worktree:** `~/wt/github.com/LiGoldragon/CriomOS-test-cluster/spirit-nspawn-upgrade-test`
- **Test invocation:** `nix run github:LiGoldragon/CriomOS-test-cluster/spirit-nspawn-upgrade-test#nspawn-spirit-upgrade-on-prometheus`
- **Last run output (N=10):** `(SandboxUpgradeSucceeded 10 10 [.../source-copy.redb] [.../target-v0.1.1.redb])` — `spirit nspawn upgrade test passed`
- **Container:** `spirit-test` (NixOS toplevel `nixos-system-spirit-upgrade-test-26.05`, IP `10.233.1.2`), torn down cleanly after run

Two implementation deviations from the original plan in §4:

1. Switched from criomos-module-based toplevel to a **minimal `nixpkgs.lib.nixosSystem`** call, because the existing CriomOS-test-cluster flake has pre-existing baseline breakage (sops-nix missing, horizon-fixture `services` shape drift). The minimal toplevel skips criomos modules entirely; it just brings systemd + the spirit/upgrade packages + the runner. This is cleaner anyway — the spirit pilot doesn't need the CriomOS feature surface.
2. The `nspawn-spirit-upgrade-on-prometheus` wrapper carries `# shellcheck disable=SC2029` for the deliberate client-side `$record_count` expansion in the SSH heredoc invocation.

The minimal-toplevel choice is documented in the flake; the criomos approach can be revisited once the test-cluster baseline is repaired (separate cluster-operator concern; not blocking this).

## §9 Operator beads filed

- **`primary-db49`** (P1) — Mirror designer spirit-nspawn upgrade test in operator implementation. Operator builds their own implementation; comparison after both ship.
- **`primary-dlut`** (P2) — Extend spirit-nspawn upgrade test with real handover socket protocol (per operator/161 private upgrade socket).
- **`primary-axuk`** (P2) — Replicate spirit-nspawn upgrade test at 500-record scale (matches existing `(SandboxUpgradeSucceeded 500 500 ...)` in-process witness).
- **`primary-1jql`** (P1) — Implement in-transition messages probe (per spirit record 528 — see §10 below).

## §10 In-transition messages — analysis + plan (per spirit record 528)

Psyche asked: send messages to the socket between transition to the new daemon, see if a caching actor replays them after transition. Plus: is the version type change schema-diff driven?

**Caching actor / replay state today.** No. Spirit's current design is **hard cutover**, not replay:

- `persona-spirit-daemon` writes the redb synchronously per request inside its operation handler (see `src/store.rs` `SpiritStore::assert_entry`). Once the handler commits and replies, the client sees the ack and the record is durable.
- Per operator/161 the v0.1.1 daemon now owns a private upgrade socket exposing `AskHandoverMarker` / `ReadyToHandover` / `HandoverCompleted`. The third call **removes the ordinary + owner socket paths**. After that point, new ordinary connections go to the v0.1.1 daemon; old connections error out.
- Per operator/160 the smart-handover-sandbox already exercises the `LegacyHighRejected` probe: writes sent to the legacy daemon AFTER the cutoff marker are explicitly **rejected**, not queued.

So the boundary today is: **acked = durable, in-flight = retry-required**. There is no kernel/library actor that buffers in-flight requests through a handover and replays them on the new daemon. The contract is: client retries on `ECONNRESET` / `ConnectionRefused`; new connections route to the new daemon; the new daemon serves them.

This is a deliberate design choice — caching+replay adds an "at-most-once vs at-least-once" duality, and spirit is currently at-most-once-per-connection-attempt with explicit client retry.

**The test that surfaces this:** would need to be Rust-level (uses `persona_spirit::ordinary::SignalClient`), not shell. Shell tools only see request-response pairs; they can't probe in-flight semantics. A meaningful in-transition test:

1. Start v0.1.0 daemon with `signal-frame` client connected.
2. Spawn N parallel client threads sending Record requests asynchronously.
3. Trigger handover initiation (call upgrade socket `AskHandoverMarker` then `HandoverCompleted`) from a coordinator thread mid-stream.
4. After handover completes: count how many records made it to the migrated v0.1.1 redb; count how many client send-calls returned errors; verify the sum equals N.
5. If a caching actor were added in the future, the same test would show some "would-be-error" requests succeeded — the test design surfaces the gap.

This test belongs in `persona-spirit` (or the upgrade-test wrapper) — Rust-level. It's filed as `primary-1jql` for either-lane implementation. Designer high-level note: per record 509 designer may stay at the analysis level here; operator carries implementation depth.

**Schema-diff driven type changes?** No, not yet. Current state per operator/175.3:

- `upgrade/src/lib.rs` has hand-written `V010ToV011` typed projection (the `Certainty` → `Magnitude` enum mapping per record 70's widening).
- The two-submodule pattern from `skills/spirit-cli.md` §"Canonical pattern" (private `historical` rkyv reproduction + `current_shape` override + `From`-chain) is the explicit template — manually coded, one migration step at a time.
- The aspiration is schema-diff-driven: diff `<component>.schema` v0.1.0 vs v0.1.1 → derive the migration shape via the `UpgradeRule` macro variant per operator/175.4. That schema engine doesn't exist yet (operator/175.5: "the concept files are not yet consumed by a real schema engine").

So today's version transitions are hand-written and well-typed; tomorrow's are intended to be derived from the schema-diff. Bridge work is the schema engine itself (operator's next major slice).

## §11 References

- Spirit records 508 (parallel implementation), 509 (designer high-level), 510 (Prometheus nspawn), 511 (audit cycle), 512 (sandbox-test acceptance gate)
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/nspawn.nix` — criomos-nspawn wrapper definition
- `/git/github.com/LiGoldragon/CriomOS-test-cluster/scripts/nspawn-dune-on-prometheus` — invocation pattern to mirror
- `/git/github.com/LiGoldragon/CriomOS-test-cluster/flake.nix` — `dune-nspawn-toplevel` fixtureSystem to mirror
- `/git/github.com/LiGoldragon/upgrade/src/bin/upgrade-spirit-sandbox-test.rs` — existing in-process migration binary that v1 wraps
- `reports/operator/175-schema-engine-prep/` — operator concept-schema + sandbox witness wave
- `reports/operator/161-spirit-private-handover-socket-2026-05-22.md` — handover socket plumbing for bead 2
- `reports/designer/329-schema-macro-component-extensibility.md` — converged with operator/175.4 NodeDefinitionPoint design
- Worktrees: `nota-codec/designer-327-mockup-2-schema-parser` (REUSE), `signal-frame/mockup-stable-caller-id-1` (RE-IMPLEMENT later), `signal-frame-worktrees/designer-327-mockup-3-dispatch` (OBSOLETE)
