# 17 — Review of SYS/136 horizon-rs + lojix state audit

Date: 2026-05-17
Role: system-assistant
Scope: Audit-of-audit. Cross-check every checkable claim in
`reports/system-specialist/136-horizon-rs-lojix-state-audit-2026-05-17.md`
against the live worktrees, flag drift, weigh the recommendations.

Worktrees inspected:
- `/home/li/wt/github.com/LiGoldragon/lojix/horizon-leaner-shape`
- `/home/li/wt/github.com/LiGoldragon/horizon-rs/horizon-leaner-shape`

---

## Verdict

The audit is **solid and trustworthy**. Every claim I could
mechanically check holds; the recommendations are concrete, well-named,
and sequenced sanely. Two small numeric drifts (one stale-by-57-lines
test count, one fuzzy "repo files" figure) do not change any
conclusion. The audit's biggest contribution is naming the
`src/deploy.rs` split surface (seven noun-named modules) **before**
the next large feature lands — that is exactly the right time to do
it, and the names are well-chosen.

Outstanding issue to surface to the operator/system lane: this audit
overlaps `primary-766g` (replace agent-minted `deployment_id` with a
sema-engine slot). The recommended `deploy/ledger.rs` split is the
natural place to land that BEADS task. Best done together; otherwise
they'll touch the same file twice.

---

## Claim-by-claim verification

### Magnitude — lojix

| Audit claim | Verified | Drift |
|---|---|---|
| `src/` 3,434 lines | 3,434 | exact |
| `tests/` 1,188 lines | **1,245** | +57 lines (~5%) |
| total Rust 4,622 | 4,679 actual | +57 |
| `src/deploy.rs` 2,083 | 2,083 | exact |
| `tests/build_pipeline.rs` 552 | 552 | exact |
| `src/socket.rs` 520 | 520 | exact |
| `tests/socket.rs` 362 | 362 | exact |
| `src/runtime.rs` 340 | 340 | exact |
| "`src/deploy.rs` is about 45% of all Rust" | 2083/4679 = **44.5%** | confirmed |

The 57-line test drift is well within "audit was written today, then
tests grew slightly" tolerance. Does not affect any conclusion.

### Magnitude — horizon-rs

| Audit claim | Verified |
|---|---|
| total Rust 7,223 | **7,223** exact |
| `lib/tests/view_json_roundtrip.rs` 754 | 754 |
| `lib/tests/horizon.rs` 418 | 418 |
| `lib/src/proposal/cluster.rs` 328 | 328 |
| `lib/src/view/node.rs` 302 | 302 |
| `lib/tests/user.rs` 292 | 292 |

"repo files: 68" — could not confirm cleanly (`jj files` in this
jj-colocated worktree returned 7; `git ls-files` returned 1, both look
like tooling quirks rather than ground truth). I did count 54
`*.rs` files outside `target/`. The exact figure doesn't load-bear
anything in the audit's conclusions, so I left it un-resolved.

### Commit hashes claimed as pushed

All verified by `jj log` lookup in each worktree:

**lojix:**
- `1cf5d15c` — `lojix: witness cli daemon boundary` ✓
- `77bd4009` — `lojix: align actor constraints with current root` ✓
- `e28da1e4` — `lojix: remove report links from architecture` ✓

**horizon-rs:**
- `6df7ec1b` — `horizon-rs: clarify current projection contract` ✓
- `340e5cc3` — `horizon-rs: remove stale cli stub note` ✓

### Configuration-boundary witnesses

Audit claims five tests added/in-place; I read
`tests/configuration_boundary.rs` and confirmed exactly five `#[test]`
functions with the matching names:

1. `production_code_has_no_socket_environment_control_plane`
2. `production_binaries_decode_typed_configuration_sources`
3. `daemon_runtime_gets_horizon_source_from_typed_configuration`
4. `cli_has_exactly_one_runtime_peer_the_daemon_socket` *(new from audit)*
5. `daemon_deployment_path_owns_horizon_projection` *(new from audit)*

### Structural claims

| Claim | Check method | Verdict |
|---|---|---|
| `src/deploy.rs` combines multiple durable nouns | grep top-level items: found `DeploymentLedger`, `DeploymentLedgerActor`, `GarbageCollectionRoots`, `DeploymentActor`, `BuildJobActor` all in one file (~71 `pub struct`/`impl` items in 2083 lines) | **confirmed; recommendation well-founded** |
| `ClusterProposal::project(&HorizonProposal, &Viewpoint)` is the single projection entrypoint | grep `lib/src/proposal/cluster.rs:76: pub fn project(&self, horizon: &HorizonProposal, viewpoint: &Viewpoint)` | **confirmed** |
| `TransitionalIpv4Lan` remains an authored pan-horizon value | `lib/src/horizon_proposal.rs:23` `pub transitional_ipv4_lan: TransitionalIpv4Lan` | **confirmed** |
| horizon-rs flake exposes only `checks.<system>.default` | `nix flake show --json` returns only `default` | **confirmed** |
| lojix has stronger check surface | actual: `build`, `clippy`, `fmt`, `test`, `daemon-cli-integration`, plus broken-out `test-build-pipeline`, `test-configuration-boundary`, `test-event-log`, `test-smoke`, `test-socket` | **confirmed — much stronger** |

---

## Recommendations — weighed

### R1 — Split `lojix/src/deploy.rs` before adding activation/cache retention

**Strong support.** 71 top-level items in 2,083 lines with at least
four actor types (`DeploymentLedgerActor`, `GarbageCollectionRoots`,
`DeploymentActor`, `BuildJobActor`) and three independent effect
surfaces (artifact materialization, remote inputs, secrets). The
seven proposed module names (`deploy/ledger.rs`, `deploy/gc_roots.rs`,
`deploy/build_job.rs`, `deploy/artifact.rs`, `deploy/remote_inputs.rs`,
`deploy/secrets.rs`, `deploy/nix_build.rs`) correspond to actual
distinct concerns in the file. Verb-belongs-to-noun is satisfied; no
"helpers.rs" pile.

**Caveat I want to add:** `primary-766g` (BEADS, P2) is open and asks
to replace agent-minted `deployment_id` with a sema-engine slot.
That edit lands in the ledger area. **Land R1 and `primary-766g`
together** — otherwise the same file gets reshaped twice in close
succession. The split commit should *land first*, the slot change as
the immediate follow-up on `deploy/ledger.rs`.

### R2 — Add installed-binary deployment smoke with fake tools

**Strong support.** The audit correctly observes the gap: the
in-process `build_pipeline.rs` fake-tool logic is rich and trusted,
but doesn't prove that the **packaged** CLI talking to the **packaged**
daemon over a real socket can complete a full deployment-submission
with fake `nix`/`ssh`/`rsync`. `daemon-cli-integration` already
demonstrates the packaged-binary-over-socket pattern works as a Nix
check; extending it with the fake-tool environment is a natural next
step.

### R3 — Actor topology/trace witnesses before increasing actor count

**Support, with a note on scope.** The named topology
(`runtime root → ledger allocation → deployment actor → build job →
GC-root actor → ledger record → built observation`) is the right
thing to make observable. Concretely, this likely means either an
in-process trace event log per request, or a Kameo-side
supervision-tree dump. Worth scoping in a follow-up before
implementation; the audit doesn't say which.

### R4 — Decide the LAN derivation direction for Horizon

**Appropriately flagged as a designer question, not an operator task.**
The audit doesn't propose an answer, which is correct: this is a
shape decision and belongs in a designer report. Suggest filing
this back to the designer lane (or escalating to the user) before
any further LAN-related lojix work.

The current `TransitionalIpv4Lan` is explicitly authored on the
pan-horizon `HorizonProposal`. There's at least one downstream
implication worth naming: `criomos-horizon-config` ships the
authored LAN constants today (per the active-repositories.md row).
Any "derive a CIDR from cluster/host names" decision changes that
repo's shape too — not just horizon-rs.

### R5 — Add `horizon-rs` fmt/clippy flake checks

**Support, with the audit's own caveat.** The audit responsibly notes
*"do not make the check surface stricter blindly if it would block
unrelated downstream work."* The right discipline: run `cargo fmt
--check` and `cargo clippy --all-targets -- -D warnings` against the
current `horizon-leaner-shape` tree first; if clean, add the flake
checks; if not, fix-then-add rather than skip-and-defer.

---

## Things the audit got right that are easy to under-notice

- **Distinguishes "well-implemented" from "design gap" from
  "unclear/brittle."** Each surface gets all three readings instead
  of collapsing into a "what's missing" punch list. That makes the
  document useful for an incoming agent who needs to know what to
  *trust* as much as what to fix.
- **Doesn't claim more than it ran.** "This audit did not run an
  actual remote build" (line 192) is the kind of disclosure that
  prevents false confidence downstream.
- **Inlines the corrected-boundary diagram.** The mermaid at the top
  is doing real work — it's the single sentence ("CLI has exactly
  one runtime peer: lojix-daemon") rendered as a graph that an agent
  can verify against `tests/configuration_boundary.rs`. Worth
  imitating in future audits.
- **Identifies the next-feature *prerequisite*, not just the
  next-feature *list*.** R1 (split deploy.rs) is correctly framed
  as "before adding activation or cache retention" rather than
  "after". This is the right ordering.

---

## Gaps worth filling

1. **No cross-link to `primary-766g`.** The deploy.rs split should
   sequence with that task. Adding a one-line BEADS reference in the
   audit (or in this review's R1 weighting) closes the loop.
2. **R3 doesn't name a concrete witness shape.** "Actor topology
   manifest or trace" leaves open whether this is a compile-time
   declaration (a `topology.rs` enum), a runtime event-log assertion,
   or a Kameo supervision-tree dump. A small follow-up scoping note
   would help the operator pick.
3. **No mention of CriomOS-side smoke.** The audit covers `lojix` and
   `horizon-rs` in detail but doesn't trace the projection consumer
   on `CriomOS-{home,lib}` `horizon-leaner-shape`. The audit's stated
   scope is the two repos, so this isn't a defect — but a future
   "stack B end-to-end" audit should cover the CriomOS side too.
4. **Doesn't reconcile against `protocols/active-repositories.md` §"Two deploy stacks".** That section now exists (landed in
   `xvxwvxsv a162a5a7`, 2026-05-17). The audit was written the same
   day so this is forgivable, but a closing "consistent with
   protocols/active-repositories.md §Two deploy stacks" line would
   tie the docs together.

---

## What I did not check

- I did not run any of the Nix checks. The audit notes
  `test-configuration-boundary` passed on Prometheus; I trust that
  rather than rebuild. (Verifying it would mean a real Nix evaluation
  that the audit already paid for.)
- I did not read every Rust source file. The structural claims I
  spot-checked all held; line counts of unread files were verified
  by `wc -l`.
- I did not audit horizon-rs or lojix `AGENTS.md` / `skills.md`
  edits in detail — the audit names what it removed and added, and
  the commits exist with those titles. A skill-text audit is its
  own report.

---

## Recommendation to the user

The audit is publishable as-is. If you want me to file the
follow-ups (sequence R1 with `primary-766g`; create a BEADS task for
R2; ping the designer lane on R4), say the word and I'll do that as
a separate turn — none of it requires editing the audit itself.
