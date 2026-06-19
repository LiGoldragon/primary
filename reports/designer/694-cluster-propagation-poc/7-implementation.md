# 694 — implementation + result

The self-contained PoC harness at `/tmp/cluster-propagation-poc` is **GREEN
end-to-end**: machine A's spirit accepts a new state object → its criome
authorizes the new authorized head under a 2-of-3 root contract → the router
fans the reference by TYPE to B and C (not a non-matching control) → B and C
acquire the head and are byte-identically interchangeable with A. The full
`cargo test` runs four binaries, four tests, zero failures.

The build plan's nine steps were carried by the four prior implement passes
(scaffold + criome unit, criome actor leg, spirit leg, router leg). This step
(step 5 — "wire the e2e green") found the e2e already wired and passing: the
last unimplemented hop (binding the spirit committed head to the criome
operation digest D) was closed in the spirit pass, which flipped the e2e from
red to green as a side effect. This pass re-ran the full suite, traced the one
real build-graph wrinkle to ground (a build-deps-only schema-chain duplicate,
benign), ran an adversarial fan-set probe on the e2e itself, and reverted all
probes — the harness on disk is unchanged from the prior pass.

## Harness layout

One library crate + four integration-test binaries; 1568 lines total
(`wc -l`). Touches only `/tmp/cluster-propagation-poc`; no `/git` repo edited,
nothing committed.

| File | Lines | Role |
|---|---|---|
| `Cargo.toml` | 115 | git-dep pins + a 20-line path-`[patch]` table forcing the OLD schema chain via OLD-rev signal-* clones at `/tmp/cpp-deps` (harness-only resolution) |
| `src/lib.rs` | 44 | `Machine` noun (A/B/C self-quorum, `p3td`); module roots |
| `src/criome_quorum.rs` | 370 | `ClusterMember` / `ClusterQuorum` / `ClusterCriome` — real BLS keys, 2-of-3 root contract, ermr admission minting, evidence + attested-moment assembly, `CriomeRoot` authorize + observe |
| `src/spirit_propagation.rs` | 239 | `Mirror` (real mirror daemon over loopback) + `ProducerSpirit` (real Engine accept/checkpoint/ship + acquire-into); `head_digest()` binds the committed head to criome's `OperationDigest` D |
| `src/router_fanout.rs` | 85 | `TypeRouter` / `Attendee` over the real `RouterRuntime` + `AuthorizedObjectFanout` |
| `src/glue.rs` | 94 | glue seam 1 — `AuthorizedHead` carrier owning `From<criome ref>` then `From<carrier> for signal_standard ref` (orphan-rule-safe three-field cross-vocabulary conversion) |
| `tests/end_to_end.rs` | 158 | the falsifiable loop: `cluster_propagation_three_spirits_interchangeable` |
| `tests/criome_quorum.rs` | 166 | standalone 2-of-3 witness (positive + two load-bearing negatives) |
| `tests/spirit_propagation.rs` | 111 | standalone accept → ship → B/C acquire interchangeability witness |
| `tests/router_fanout.rs` | 186 | standalone type-fan witness (4 match rungs + control exclusion + adversarial second head) |

## The e2e loop, hop by hop (real-vs-shimmed map)

The boundary is drawn at TRANSPORT, never at LOGIC. Every falsifiable claim
runs against the real component crate; only the host (one process) and the
cross-host/cross-criome transports are cut.

| Hop | What runs | REAL (component @ rev, file:line) | CUT / shimmed (marked) |
|---|---|---|---|
| **1 — A accepts state** | `ProducerSpirit::accept` → real `Engine::handle_async(Input::record)` commits to the content-addressed log | spirit `fe04c12`; `src/spirit_propagation.rs:178-207` asserts `RecordAccepted` | none |
| **1b — A ships head** | `ship_head` → local `checkpoint` + `ship_unshipped_to_mirror` over real loopback TCP to a real mirror daemon + `publish_checkpoint_to_mirror`; captures `MirrorHead.entry_digest()` | mirror `b26c139`, sema-engine `73eea24`; `spirit_propagation.rs:214-238` | cross-host socket → loopback (host shared, transport real) |
| **D-binding** | `head_digest()` = `OperationDigest::from_bytes(head.entry_digest().bytes())` — blake3 over the committed log entry; the SAME identity criome authorizes and acquirers restore to | signal-criome `521a8ed` `lib.rs:79`; `spirit_propagation.rs:168-174` | none — the head is real committed state |
| **2 — criome authorizes** | `ClusterCriome::authorize_head` → real `CriomeRoot` actor `EvaluateAuthorization` handler runs `is_valid_majority` k>n/2 guard, distinct-signer `Threshold::decide`, real blst BLS verify over the canonical `OperationStatement`, the `ay3y` attested-moment window, the `ermr` admission gate; on `Authorized` emits the `AuthorizedObjectUpdate` pulse carrying `{Spirit, D, Operation}` | criome `22801af`: `language.rs:623-626` (guard), `:371-395` (tally), `:209` (op tag), `actors/root.rs:203-238` (handler + pulse); `src/criome_quorum.rs:281-348` | cluster-root ceremony harness-minted (684 Woe 6, `criome_quorum.rs:111-135`); cross-criome peer signature solicitation → local self-quorum assembly (the three co-resident keys, `p3td`) |
| **2 negative** | 1-of-3 evidence → `Rejected(QuorumShort)` on the standalone evaluate path | same criome tally; `tests/end_to_end.rs:96-114` | none — makes 2-of-3 falsifiable |
| **2→3 — glue seam 1** | `AuthorizedHead::from(reference)` then `.into()` → signal-standard `AuthorizedObjectReference` (three fields across two distinct-but-structural-identical vocabularies; digest crosses by string content, content-addressed) | `src/glue.rs:50-94` | none — a genuine conversion, not a no-op (the two crates each define their own `ComponentKind`/`ObjectDigest`/`AuthorizedObjectKind`) |
| **3 — router fans by TYPE** | `TypeRouter::publish` → real `RouterRuntime` forwards `PublishAuthorizedObjectReference` to `AuthorizedObjectFanout::publish`, which filters subscribers by `reference.matches_interest(&interest)` (the SOLE operational matcher, `m0p2`) and returns the type-matched `publication.deliveries` synchronously | router `ce578f1`: `router.rs:1580,1610`, `authorized_object.rs:119-135` (filter `:126`); signal-standard `0b7ae20` `lib.rs:70-79`; `src/router_fanout.rs` | cross-host socket push → in-process kameo ask reading `deliveries`; durable attendance table + restart-replay (attendance-fanout-139 branch) → main HEAD synchronous delivery (design contested-decision 1) |
| **3 match assertions** | B (`Component(Spirit)`) delivered; C (`ObjectKind(Operation)`) delivered; control (`Component(Mirror)`) NOT delivered; this pass probed `deliveries.len()==2` (exactly {B,C}) | real matcher; `tests/end_to_end.rs:126-137` | none — reference never payload (`57f9`): `AuthorizedObjectReference` is `{component,digest,kind}` only |
| **3→4 — glue seam 2 + acquire** | `Mirror::acquire_into` per delivery → real mirror `Restore` exchange + fresh `Store::import` (checkpoint + versioned-log suffix) for B and C | spirit/mirror restore path cloned from `spirit/tests/mirror_shipper.rs`; `src/spirit_propagation.rs:92-120` | live in-place `Store::adopt_head` → fresh `Store::import` (684) |
| **4 — interchangeable** | `store_b.database_marker() == store_a` and `== store_c` (marker = `commit_sequence` + blake3 `state_digest` over committed records); plus `len()` agreement | real `Store::database_marker` (spirit store/mod.rs:1138); `tests/end_to_end.rs:144-155` | none — three independently-restored stores with equal marker carry byte-identical content-addressed state (`nfvm`) |

No logic is shimmed. The only non-crate code is the 3-instance wiring + the two
glue seams + the tests, exactly per design. The cluster-root ceremony is
harness-minted (marked) and cross-host/cross-criome transports are cut to
in-process (marked) — both per the design and 684 Woe; neither sits on a
falsifiable claim.

## Observed test output

`cargo test` (multi-thread runtime), observed this pass:

```
unittests src/lib.rs        : 0 passed; 0 failed
tests/criome_quorum.rs      : 1 passed; 0 failed   (criome_authorizes_two_of_three_and_rejects_one_of_three)
tests/end_to_end.rs         : 1 passed; 0 failed   (cluster_propagation_three_spirits_interchangeable)
tests/router_fanout.rs      : 1 passed; 0 failed   (router_fans_authorized_head_by_type_to_matching_attendees_only)
tests/spirit_propagation.rs : 1 passed; 0 failed   (spirit_a_accepts_ships_and_b_c_acquire_interchangeable)
doc-tests                   : 0 passed; 0 failed
TOTAL: 4 passed, 0 failed across 4 test binaries.
```

`cargo build` → `Finished dev profile` clean, no warnings.

**Adversarial probe this pass (then reverted):** added
`assert_eq!(delivered.len(), 2)` to the e2e immediately after the control
exclusion — observed PASS, confirming the router delivered the head to exactly
B and C and nothing else (the fan is type-matched, not a broadcast the negative
assertion happens to survive). Reverted; re-ran full suite → all four green;
confirmed no probe remnants (`grep` clean). The interchangeability green's
load-bearingness was already established by the spirit pass's documented probe
(replacing `marker(B)==marker(A)` with `marker(B)==genesis` FAILED, showing B
restores A's real non-genesis hash `StateDigest(2236392434272497022)`, not
`(0,0)`).

## Build-graph finding: a benign build-deps-only schema-chain duplicate

`cargo tree -d` reports two `schema-rust-next v0.5.3`:

- **OLD-chain `733b76d3`** — pinned directly by the harness; the **runtime**
  (`[dependencies]`) crate every wire type resolves through.
- **NEW-chain `bb4dfe29`** (`branch=main`) — pulled transitively.

I traced the NEW-chain rev: `cargo tree -i '…bb4dfe29…' --edges normal`
prints **"nothing to print"** — it has *zero* runtime reverse-dependencies. It
appears only under `[build-dependencies]` (the proc-macro / codegen crate the
signal-* `build.rs` invoke at build time). So the runtime type graph is a
**single** OLD-chain source — which is exactly why all wire types unify
(`AuthorizedObjectReference`, `Evidence`, `database_marker`, `matches_interest`)
and the tests pass. This matches the design's note that the OLD-vs-NEW
schema-chain delta is flake/codegen-orchestration only ("zero Rust/.schema/
codegen per research leg 5"), so either chain emits identical generated types;
the build-time duplicate generates the same types and never splits a runtime
boundary. It is a harness-resolution artifact, not a correctness concern.

## What is proven vs. what remains (operator beads)

**Proven (all against real component logic):** the k>n/2 majority tally + the
distinct-signer guard + real BLS + the a-priori attested-moment window + the
ermr admission gate (with a 2-of-5 sub-majority rejected at admission and a
1-of-3 evidence rejected as `QuorumShort`); match-by-type with a non-matching
`Mirror` control excluded and the delivery set exactly `{B,C}`; payload-blind
reference (`{component,digest,kind}` only); and content-addressed resulting-state
interchangeability across three real spirit stores (`marker(A)==B==C`).

**Not proven — the exact remaining red boundary / operator beads:**

1. **Physical multi-host network quorum** — the harness is single-host
   self-quorum logic (three in-process instances). Cross-host sockets and the
   real cross-criome peer signature lane are cut to in-process; the network
   leg is system-operator's downstream work.
2. **Live in-place `Store::adopt_head`** — the proven acquire path builds a
   *fresh* `Store::import`; adopting a head into a running store in place is a
   separate spirit bead.
3. **Durable router attendance + restart-replay** — main HEAD's
   `AuthorizedObjectFanout` returns the synchronous in-memory delivery set; the
   attendance-fanout-139 branch's SEMA-durable attendance table (deliveries
   survive a router restart; a late attendee replays prior matching heads) is a
   router bead, deliberately not used here (design contested-decision 1).
4. **Cross-criome peer signature solicitation** — collapsed to local
   self-quorum assembly (the three keys co-resident).
5. **BLS aggregation** — per-signature verify loop, not an aggregated
   signature.
6. **Production cluster-root ceremony** — the harness mints each machine's
   admission by signing its `RegistrationStatement` with a harness-held
   cluster-root key (684 Woe 6); the real ermr gate runs, but the ceremony is
   minted, not enacted.

**Stale-design / harness-resolution carry-over (for operator harvest):** the
DESIGN `gitDeps` snapshot predates criome main migrating to the NEW schema
chain (criome main is now past `22801af`). The buildable loop is therefore
pinned to **criome `22801af`** (the last OLD-chain criome, two-field
`AuthorizationEvaluation{contract,evidence}`, matching the design's
signal-criome `521a8ed` pin) + spirit `fe04c12` + router `ce578f1` + mirror
`b26c139`, all on OLD schema-rust-next `733b76d3`. The harness forces this one
chain via a path-`[patch]` table to OLD-rev signal-* clones at `/tmp/cpp-deps`
(cargo cannot `[patch]` a git source with a different rev of the same URL).
When operator harvests this into the real repos, the right move is to land all
four legs (criome / spirit / router / mirror) on **one** schema chain in-repo,
which removes the path-patch table and the build-deps duplicate entirely.

## Bottom line

The capstone loop closes green: every named mechanism — criome 2-of-3
authorize-from-root-contract, spirit validate-on-criome → propagate →
interchangeable, router fan-by-type — runs against real component crates in one
falsifiable end-to-end test, with the physical multi-host and durable-router
legs cleanly named as operator beads. Status: **Green** (with the schema-chain
pin and in-process transport cuts honestly marked).
