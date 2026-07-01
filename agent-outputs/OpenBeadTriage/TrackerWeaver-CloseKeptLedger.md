# Tracker Weaver — Open-Bead Verify-then-Close Ledger

## Task and scope

Authorized verify-then-close sweep over the 262-open `primary-` beads backlog:
verify real done-state per bead; CLOSE the already-done / moot / superseded /
stale ones with a recorded reason each; keep genuinely-still-needed open and
capture them in a tightened list. NOT authorized and NOT done: implementing any
bead, touching Spirit intent records, adjudicating the 9 contradiction beads.

## Method and a verification-integrity note

All `bd` reads and the serialized close writes ran through the lead (single DB;
`dolt.auto-commit=on`; the embedded-Dolt store is gitignored, so closes create
no jj-tracked change and bd persists them itself). Every close reason ends
"Reversible" — closes are reversible tracker state the psyche can reopen.

Integrity note the reader should know: verification was fanned out to read-only
git/repo inspector sub-workers, but several early sub-worker outputs were not
reliably received, and one relayed claim proved false on check (it asserted
9gkn's four named commits were ancestors of their mains; direct `merge-base`
showed they are NOT — the *features* had landed under rebased commits). Because
of that, **every single close in this ledger was independently re-grounded by the
lead against direct repo evidence** (grep of a named symbol/type, `git
merge-base`, `git ls-remote`, or file presence) visible in the run log. One
close made on a bad premise (ohpk) was caught by this re-grounding and reopened.
Treat the per-bead evidence below as lead-observed, not sub-worker-asserted.

Sources: `agent-outputs/OpenBeadTriage/Scout-OpenBeadInventory.md`,
`protocols/repos-manifest.nota`, live repos under `/git/github.com/LiGoldragon/`,
`git ls-remote` for two remote-only checks.

## Boundaries honored

- The 9 contradiction beads were NOT touched: bvsd, smwa, e191, zpgw, ptvb.9,
  ptvb.8, ptvb.10, ptvb.11, 4wvl.
- No bead implemented; no Spirit record touched; no code/doc edited.

## Tracker delta

- Open before: 262 → Open after: 224. Close actions: 39. Reopened: 1 (ohpk).
  **Net closed: 38.**

## CLOSED (38) — grouped, each with lead-observed evidence

### Schema / Nota stack — merges & migration (14)

- **primary-36iq (EPIC)+.3+.6+.7+.7.1+.7.2** — NOTA bracket-string migration
  complete. Bracket/block-string support on nota-next main (Delimiter::SquareBracket,
  is_square_bracket, demote_to_string; block_queries tests). Grep sweep: zero
  quote-delimited strings in any authored `.nota` file across
  nota-next/persona/signal-persona/signal-criome/signal-message/spirit/horizon-rs/nota-config;
  docs use bracket syntax. Core children .1/.2/.4/.5 already closed.
- **primary-60xf** — triad-runtime designer-strings integrated; witness fn
  `trace_client_prints_typed_events_at_display_boundary` at tests/trace.rs:218.
- **primary-9gkn** — schema-generics + reaction-frame landed (features present under
  rebased commits): nota-next/derive PascalHeadBody, schema-next
  `Application(Box<RootApplication>)` (schema.rs:292), schema-rust-next reaction-frame
  emission (lib.rs:1298), triad-runtime `NexusActionNextStep<Action>` (role.rs).
- **primary-cxyf** — structural-forms: StructuralMacroNode on nota-next main
  (lib.rs) + SchemaError::RetiredStructFieldSyntax on schema-next main (engine.rs).
- **primary-6eog** — family-identity SchemaHash::new newtype emission on
  schema-rust-next main (lib.rs + tests/family_emission.rs).
- **primary-k5fz** — streaming event-frame emission on schema-rust-next main
  (StreamingFrame + emit_signal_frame_* in daemon_emit.rs/lib.rs).
- **primary-l35n** — imported-head arity enforced: SchemaError::GenericArityMismatch
  (engine.rs:192) via Schema::arities_verified (source.rs:190).
- **primary-vllc** — schema-next dual-lowering bug removed by elimination:
  AssembledVariant gone from src; report-702 single-engine collapse unifies lowering.
- **primary-7xr4** — signal-version-handover Nota derives repaired: hand impls
  NotaDecode/NotaEncode for ComponentName/ContractVersion/RecordKind in version-projection.

### Sema / spirit integration (6)

- **primary-qu28** — sema-engine VC-hardening integrated + consumers repinned:
  sema-engine main v0.6.3 (rebuild_from_log + CHAIN_HEAD in commit_log.rs); spirit
  v0.19.0; router/criome/mind pin sema-engine branch=main. Mirror out of scope per
  bead's own deploy audit.
- **primary-4itq** — ResolveClarification maintenance op in spirit (guardian_journal.rs + daemon dispatch).
- **primary-kwm2** — spirit error enums on thiserror (Cargo thiserror=2; store/error.rs, transport.rs, daemon.rs derive Error).
- **primary-o2kc** — spirit-next→spirit internal rename done (package name=spirit; no spirit-next residue in src/).
- **primary-wk88** — CollectRemovalCandidates combined archive-then-retract op (meta_transport.rs + store/archive.rs).
- **primary-c4dz.3** — spirit single-sources meta types from meta-signal-spirit; schema/meta-signal.schema deleted; git dep in Cargo.toml.

### Cloud / CriomOS (6)

- **primary-hpkj** — DigitalOcean Phase-1 on cloud main: flake reads
  digitalocean.com/api-token, tests/digitalocean_live.rs + examples/write_config.rs
  present; Tier-1+Tier-2 live proven (report 70).
- **primary-omis** — cloud intent-curator-fold landed: origin/main=704213b0 (fold FF
  target; removes INTENT.md), confirmed by ls-remote.
- **primary-3dqf** — fetchHfModel + nix-prefetch-huggingface on CriomOS-lib main.
- **primary-gdb7** — prometheus llm API token minted+wired via sops-nix: CriomOS
  llm.nix sops.secrets.localLlmApiToken + goldragon secrets/localLlmApiToken.sops.
- **primary-ooh1** — browser-use packaged with OPENAI base wrapping (CriomOS-home
  packages/browser-use + browser-use.nix).
- **primary-0v2** — SSH host key resolved as sshd-owned; clavifaber reads
  /etc/ssh/ssh_host_ed25519_key.pub, no self-minted identity in CriomOS.

### Mentci (5)

- **primary-iy51.1** — real mentci daemon over mentci-lib (bin/mentci-daemon.rs,
  kameo::Actor). Durable resume tracked separately in still-open iy51.3.
- **primary-iy51.2** — mentci remote-name collision resolved; four component
  remotes live (mentci/signal-mentci/meta-signal-mentci/signal-standard).
- **primary-iy51.4** — daemon surfaces criome rejection (submit_criome_verdict + is_recorded + Rejection(UnauthorizedProjection), daemon.rs:181).
- **primary-iy51.11** — mentci README has zero criome:* CLI atoms.
- **primary-o7j2.6** — orchestrate contract-fidelity fixes + round-trip tests
  (signal-orchestrate 878601c + test round_trip.rs:538; meta-signal-orchestrate f7102e5).

### Rollup / retirement / stale / moot (7)

- **primary-iy51.13 (EPIC)** — all 8 intercept-policy MVP children closed; bd flagged eligible-for-close.
- **primary-mt02** — legacy orchestrator already retired (repo absent from /git + Active manifest; no live refs).
- **primary-g28b** — observation-only DEFERRED note ("NO change recommended or scheduled"); nothing to implement. (dispatch-named)
- **primary-b7qc** — target-repo-retired (lojix-cli gone). Corrective note added: the
  localLlmApiToken need WAS rehomed and satisfied via CriomOS sops-nix (see gdb7) —
  no fresh bead needed. (dispatch-named)
- **primary-bhox** — MOOT/superseded: the dead ~/primary/ESSENCE.md ref it targeted
  is gone from criome main (rewritten by INTENT→ARCHITECTURE rehome b996f93/3091f40);
  the essence-repoint branch is redundant.
- **primary-8jpa**, **primary-pibt** — MOOT: target persona-pi is Deprecated
  (remote archived + local deleted) and absent from /git.

### Reopened (1)

- **primary-ohpk** — REOPENED. Closed as moot on the premise persona-spirit was
  retired, but persona-spirit is Active in the manifest with a live remote
  (main=3701aac). Moot-ness unresolved → reopened, needs clarification (below).

## TIGHTENED STILL-NEEDED LIST (215 open implement beads, grouped)

Sizes: mechanical / normal / substantial. Epics counted by open children.

### criome-auth — epic primary-om4g (~17, SUBSTANTIAL)
Production gate, quorum plane, encrypted KeyStore, second-criome deploy, peer lane,
consumer sweep — all forward. Partials/quick-wins:
- om4g.11 (normal): 1-of-1 local gate landed (90875f26); typed AuthorizedObjectReference causal loop remains.
- kr40 (normal): real blst BLS + cluster-root admission gate landed; mlock/zeroize/passphrase remain.
- om4g.16 (mechanical): confirmed gap — no SO_PEERCRED on criome meta socket (daemon.rs:135).
- om4g.8 (mechanical): coarse PolicyRefused collapse not done.
- **om4g.14 (normal, BLOCKER — see contradictions):** signal-criome/persona/message .schema still use name-value field syntax that schema-next now REJECTS.
- Forward: om4g.1/.2/.3/.4/.5/.6/.7/.9/.10/.12/.13/.15/.17.

### mentci — epic primary-iy51 (~10 after 5 closed, SUBSTANTIAL)
Daemon exists; remaining: iy51.3 (persist SEMA/reconcile), iy51.5 (rollback/Defer/remote-guard),
iy51.6 (mechanical: mentci-lib Error surface + clear slot), iy51.7 (Observe-on-VerdictAccepted),
iy51.8 (signal-mentci-egui triad), iy51.9 (per-client view-state), iy51.10 (retract:/propose: atoms),
iy51.12 (nixosTest keystone — no nix/ dir yet). Epic iy51 itself.

### mirror — epic primary-9ppu (4, SUBSTANTIAL) + standalone
9ppu/.1/.2/.3 all unbuilt (RestoreQuery store-name-only; no MirrorObjectNotify; no EndpointKind::Mirror).
x3l7 (normal): stopgap configurable bind-addr done; real BLS/criome attestation remains.
85hv (normal): mirror-shipper OFF, gated on x3l7. ymww (normal): L1 KVM transport done; L2 Yggdrasil/L3 live remain.

### orchestrate — epic primary-fzwd (~6, SUBSTANTIAL)
fzwd.1 (substantial): real engine unbuilt (no WorkflowRunRecord/DAGRunner; one-step proof only) — gates .2/.3.
fzwd.2 (normal): mind/criome consuming halves. fzwd.3 (substantial, blocked on .1).
fzwd.4 (mechanical): worktree GC transition code (schema variants exist). fzwd.5 (CANNOT-VERIFY runtime).
fzwd.6 (normal): cross-lane push feed. kooj (normal): dynamic-lane cutover decision.

### mind — epic primary-pm7l (2 of 11 open, nearly done)
pm7l.10 (normal, blocked on siblings), pm7l.11 (normal: real caller auth proof — no SO_PEERCRED in transport). 2ne2 (normal): overflow/outbox policy.

### schema-help-daemon — epic primary-80cw (8, SUBSTANTIAL)
80cw + .1-.8 all unbuilt (rkyv catalog, registry, mentci pilot, cutover gate).

### spirit — epics c4dz + nlx5 + ~28 standalone (LARGE cluster)
c4dz: .2 (adopt_head), .4 (Supersede pipeline), .5 (off-host backup), .6 (migration decouple),
  .7 (mechanical: v1-v6 readers already gone, crash-injection tests missing), .8 (mechanical: seal write surface — SchemaHash::for_label back-door remains), .1 (doc reconcile — partial).
nlx5: .1 referents, .2 cache telemetry, .3 rejection glosses, .4 verbatim auth (deferred).
Standalone forward: am9d, a1px, dn1e, uwo0, v1w7, sfn5, fos7, fdd7, mlck, e4o9 (blocks 64s3),
  7wld, ebev, flwg, tiyo, w0v4, pjbp, gxmj, jqkq, vjl5, x178, 4civ, xslx, ydfh.
tcg0 (mechanical, partial: SpiritCliError item fixed; INTENT.md:206/dead concept.schema remain).
64s3 (normal, blocked on e4o9): spirit-manual.md not landed in primary.
1y56 (mechanical): meta-signal-criome [patch] still in spirit flake (patch count 7).
oq0n (mechanical): ~52 stale concept branches still present across engine repos.

### schema stack (schema-next/rust-next/nota-next/sema-engine/horizon-rs) — ~28
o7j2 epic + .1/.2/.3/.4/.5/.7/.8 (RustItem token model, reaction.schema home, structural macro
  routing, RustSurface populator, verdict macro, router Attend/Withdraw). o7j2.7 CANNOT-VERIFY (needs build).
8dcn (mechanical): into_next_step shim still in triad-runtime role.rs; 14-component migration.
w0xf (mechanical): Optional leaves still in domain.schema; inject All not done.
yeom (mechanical): one-line Nix witness grep fix (NotaDecodeTraced breaks adjacency).
n1ao (normal): part1 (chroma off nota-codec) done; part2 (adopt sema-engine) remains.
9x9f (substantial): router M1 landed; M2 on branch, M3/M4 not started.
Forward: 6d5n, 1tdr, 1xor, 2n1r, si42, hhp0, bojw, myku, o2lr, lrf8, 0xn7, npd, wvey, lwc6 (CANNOT-VERIFY),
  lrgj, h1vl, 3rj9 (partial), 54ti (partial), u0by (CANNOT-VERIFY, psyche-gated), s22j (partial).
2wj8 epic + .1/.2/.3 (signal-standard roster; forks still live).

### cloud — ~7
1ubd (Gemma E4B not in inventory), 8jzu (mechanical: no droplet-cap invariant), x8by (partial: CloudNode
  species done; wire cutover/Hetzner-lead/ProviderProjection remain), n98t (goldragon doris CloudNode
  NOT declared — horizon side landed). Operational/CANNOT-VERIFY-from-git: fq9l, ia60, ytdj, y3is, lome.

### CriomOS / CriomOS-home / test-cluster — ~15
Substantial: 0bab (Immich mirror), 5u9 (Ghost node, blocked), ihee (Horizon rewrite — SEE could-not-verify).
Normal: 9wi (mkCriomOSNode/container-host), 8b3 (Ygg key handoff), tpd (overlay-roles decision),
  gfc0 (metal module split), f6cc (model materialization), unig (WebHost node, blocked on n98t),
  1ha/58l/7ay8/nvs8 (test-cluster fixtures), mm0 (clavifaber e2e decision).
Mechanical: 2f7j (worktree track), k9kj (flake-drift check). Operational: yluj (redeploy).
exzf (SEE could-not-verify — candidate close).

### lojix / listener / whisrs / chronos / terminal-cell — ~15
lojix: da7 (blocked on e3c), hpx (blocked on lojix-daemon), srmq (nix-auth crate), 53pz (mechanical worktree track).
listener: c8w0 (blocked on smoke test), gm05 (trust-policy decision), llep (crash durability),
  es8u (MISROUTED — see could-not-verify), 9s3j (STT vocabulary).
whisrs: ipjx (RecordingSession, substantial), oil (feature-gap followups). chronos: fgk (solar engine).
terminal-cell: q4uk (color fidelity).

### process / ?-target / skills — ~20
4ddb epic + .1 (introspect CLI trace query) / .2 (spirit trace-plane engine-id mismatch) / .3 (criome durability).
Blocked proof/shakeout chain: 0bax, 7e7a, tdtl, b99l, xj1y, 57ce, dt1s, 7d8m (SEE contradictions).
Mechanical: nres (18 constraint manifestations), obm (lore audit — AGENTS.md still refs ESSENCE/INTENTION).
Normal/substantial: pl60 (actor-runtime unify + Nix witness), ukzf (per-agent jj workspaces),
  fzwd.6, e3c (registry component choice), 6d5n, dixg (videographer skill), c4dz.1.
ptvb epic + .2/.4/.6 (precious-main-context skill-ladder; W1 human-interaction cut done; intent-log/session-lanes not yet cut).
  ptvb.7 CANNOT-VERIFY (skills.nota not located). 6obv.11/.13/.14 (psyche/conditional).

## COULD NOT CONFIDENTLY VERIFY (need deeper inspection)

- **a6m0** — "query intent records by numeric identifier." RecordIdentifier is
  String-based (From<String>, entry_by_identifier(&str)); no numeric variant found,
  and numeric-id resolution is a known sore spot (ptvb.11, 6obv.13). Generic Lookup
  exists; numeric-specific path unconfirmed. Kept open.
- **u4tl** — persona-spirit branch `spirit-repetition-cleanups` is GONE from the
  remote (main=3701aac); no local checkout. Can't tell merged vs discarded. Kept open.
- **es8u** — repo assignment appears WRONG: describes spirit/triad-runtime Nexus
  runner cutover (NexusRunnerAdapter, NexusEngine::execute) but is filed against the
  STT listener repo (no triad-runtime dep). Likely mis-routed. Kept open; see below.
- **exzf** — criome-auth witness landed on test-cluster main (mkCriomeAuthWitnessTest.nix,
  commits fa449ab/b0b3095) and criome input repointed off criome-auto-approve to
  `github:LiGoldragon/criome`; BUT the original criome-cluster-test branch is unmerged
  and the deliverable diverged (auth-witness vs mkCriomeClusterTest). Candidate close —
  needs the cluster-test owner to confirm the goal is met. Kept open.
- **ihee** — "Horizon rewrite: combine leaner shape with re-engineering." The named
  branches (horizon-leaner-shape, horizon-re-engineering) and worktrees are ALL absent
  from horizon-rs/CriomOS-lib/goldragon/CriomOS-home; unclear if explicitly retired or
  never built. Possibly stale. Kept open, flagged.
- **Operational / live-deploy (not confirmable from source):** yluj, fq9l, ia60,
  ytdj, y3is, lome (physical infra), z2xg (WIP-bookmark disposition — another lane).
- **Runtime/build state:** fzwd.5 (source v3; daemon restart unobservable), o7j2.7,
  lwc6 (byte-identical needs a run).
- **Psyche-gated:** u0by (record 1050 shape decision), 6obv.11 (commit-format call), 6obv.14 (conditional).
- **dw95** — empty description, no acceptance criteria to check.

## NEWLY-SURFACED ISSUES (not closed; for the psyche)

- **om4g.14 is a live blocker, not just forward work:** signal-criome, signal-persona,
  signal-message `schema/lib.schema` still use `FieldName TypeName` name-value syntax;
  schema-next engine.rs now REJECTS this as RetiredStructFieldSyntax. Those contracts
  cannot re-lower until migrated to positional/dot-differentiator syntax. Prioritize.
- **es8u mis-routing:** filed against listener but the work is a spirit/triad-runtime
  Nexus-runner cutover. Re-target before working.
- **7d8m (+.1/.2/.3/.4/.5) is a Spirit-boundary hand-off, not a code close:** the
  INTENT.md file-retirement half is already done across schema-stack repos (commits
  5fbe60b/184516e/04f34d5 dropped per-repo INTENT.md, folded into ARCHITECTURE). The
  remaining half (audit each for intent-not-in-Spirit, capture genuine gaps into
  Spirit per 8rpu) is intent-curator/psyche territory and out of triage scope — I did
  NOT close these. Recommend intent-curator confirm capture, then close.
- **ohpk (reopened) needs a persona-spirit decision:** persona-spirit is Active in the
  manifest but has no local checkout and only May-dated remote branches; spirit is now
  the renamed production daemon. Is persona-spirit still a production target (making
  ohpk's "production marker" real) or effectively dormant (making it moot)?
- No `implement` bead was found to clearly contradict current intent beyond the above;
  the 9 scout-flagged contradiction beads were left untouched for psyche adjudication.

## Follow-up recommendations

- After the psyche confirms, several kept-open beads are cheap spot-closes: exzf,
  7d8m family (via intent-curator), and possibly a6m0/u4tl with a persona-spirit +
  spirit-source deeper check.
- A second confirmatory pass on the spirit cluster (46 beads) may surface 1-3 more
  already-done closes I conservatively kept open.
