# Periphery audit — the repositories flow 857335 touched outside the stack

Subflow of main flow f6db8d. Scope: terminal-cell, harness, signal-standard,
signal-mirror, meta-signal-mirror, signal-introspect, mirror, spirit,
Curriculum, curriculum-deploy. Read-only; method in
`witnesses/periphery/method.md`.

Flow 857335's own accounts are cited as *relayed*. Everything this flow read in
the repositories or ran itself is *witnessed*.

---

## 1. The mandate these changes were measured against

Witnessed, `/home/li/primary/flows/564f55/codexPrompt.md`: the realization flow
was pointed at exactly four repositories — protos, datom-codec, ethos-zero, and
a new derive crate — and told "Backward compatibility is never a variable. Every
consumer is updated" and "re-pin consumers".

Witnessed, `flows/564f55/log.md`, the living through 564f55: "tell him to port
orchestrate to the new stack when he's audited it against the vision." The named
port targets were Orchestrate, signal-orchestrate and meta-signal-orchestrate.

Witnessed, `Vision/signal.md`: Signal declares queries and responses; input and
output are too low-level. `Vision/ethos.md`: roots are Library, Signal, Sema;
"Signal's sections are queries and responses, since there is communication";
kinds are qualifier-named.

So the periphery had two possible warrants: (a) it consumes the three stack
repositories and must be re-pinned; (b) it is Orchestrate. Neither warrant
covers terminal-cell, harness, mirror or spirit, which consume none of the three
and are not Orchestrate. Their warrant is the flow's own chain: it first
rewrote `signal-terminal`, `signal-mirror`, `meta-signal-mirror` and
`signal-introspect` onto the new Ethos Signal shape — itself a Vision-directed
but unordered initiative — and the runtimes then had to follow.

---

## 2. What actually changed, per repository

### terminal-cell 1.0.0 — `e44c41a3`, parent `cb3a57fa` (2026-08-13)

Witnessed. One commit. 6 files, +398/−448. Version 0.3.0 → 1.0.0.
Substantively: `src/socket.rs` drops the `signal-frame` envelope
(`ExchangeIdentifier`, `Reply`, `SubReply`, and a `synthetic_exchange()`
degenerate handshake) and reads/writes a bare 4-byte big-endian length followed
by `Signal::<Query>`/`Signal::<Response>` rkyv bytes. This is a real port and it
is Vision-aligned ("nothing on the wire labeling itself").

Not needed for the stack realization or the Orchestrate port: terminal-cell
depends on neither protos, datom-codec nor ethos-zero, before or after. Its only
manifest change is re-pinning `signal-terminal` from `c247cbfe` to `ddbd3237`.
It changed because the flow had already rewritten signal-terminal.

Residue witnessed at the released head:
- `signal-frame` remains a declared dependency in `Cargo.toml:22` and is
  referenced by no `.rs` file in the tree — a dead dependency in a 1.0.0.
- `Cargo.lock` still resolves `nota`-free but carries `dotos` twice, `protos`
  twice, `signal-frame` twice and `schema-rust` — the retired text/schema stack
  is still in the released dependency graph.
- The socket keeps its pre-existing single-ASCII-byte command protocol
  (`GATE_RELEASE_REPLY = b'U'` and peers) beside the Signal branch; the Signal
  branch is selected by the first length byte not matching a command byte. The
  binary-only shape Vision describes is realized on one branch of a hybrid
  socket. This hybrid predates the flow; the flow did not remove it.

### harness — `722b68b3`, parent `d022427` (2026-09-02)

Witnessed. One commit. 15 files, +238/−219.

**The version is 0.3.4, not 0.4.0.** `git show 722b68b3:Cargo.toml` reads
`version = "0.3.4"`, identical to the parent. `722b68b3` is `origin/main`.
Flow 857335's `reports/other-signals.md` and `reports/shutdown-signals.md` both
call this "Harness v0.4.0", and that name reached this audit's own brief. No
such version exists. A breaking change to the terminal delivery wire shape
landed on main with no version bump at all.

Substantively: `src/terminal.rs` and the delivery path move to length-prefixed
`Signal<Query>`/`Signal<Response>`. Everything else — `src/client.rs`,
`src/daemon.rs`, `src/meta.rs`, `src/error.rs`, `src/supervision.rs` and five
test files — still speaks `signal_frame::{ExchangeIdentifier, Reply, SubReply,
Request, FrameError, RequestRejectionReason}`. Witnessed by grep at the released
revision. Harness therefore now runs two message shapes at once: the new Signal
bytes toward terminal-cell, the retired frame envelopes on its own sockets. The
857335 report describes the terminal leg accurately and does not say that the
repository as a whole was left half-migrated.

Producer pins at the released head are mutable branches:
`signal-frame`, `signal-harness`, `signal-persona` are all `branch = "main"`.
Only `signal-terminal` was moved to an immutable rev. The flow's own shutdown
report treats "immutable producer pins" as a release requirement for Spirit; it
was not applied here. `Cargo.lock` still carries `nota`, `nota-derive` and
`schema-rust`.

### signal-standard 1.0.0 — `2c90fc99`, base `c3ebae3b`

Witnessed. Five commits. +328/−787 excluding the lock. Build driver moves from
`schema-rust` + `sema-translator` + `structural-codec` + `core-ethos` +
`name-table` + `rust-logos` to a single `ethos-zero` build dependency; the
`dotos-text` feature becomes `datom`, gated on `datom-codec` + `protos`. That
part is a clean, Vision-directed consumer migration.

Three defects witnessed at the released head:

1. **Eleven Nix `result-*` symlinks are committed into the release.**
   `result-1` … `result-11`, mode 120000, pointing into `/nix/store`. They were
   added by `2c90fc99` itself. `nix-store -q --deriver` on their targets returns
   `akfjdq04…-signal-standard-test-1.0.0.drv`,
   `7mwz22vn…-signal-standard-fmt-1.0.0.drv`,
   `a1r99q7j…-signal-standard-no-runtime.drv` — the exact `.drv` paths printed
   in flow 857335's `witnesses/signal-standard-nix-6688f8ca.log`. So the build
   residue committed into the 1.0.0 release is the output of the **previous**
   revision's build, and `2c90fc99` changed `src/lib.rs`, so those outputs
   cannot correspond to the released tree.

2. **The retired shape is still in the tree.** `src/schema/lib.rs`,
   `src/schema/lib/behavior.rs`, `src/schema/lib/generated.rs` and
   `src/bootstrap_manifest.rs` are present at `2c90fc99`. `src/lib.rs` declares
   only `pub mod generated;` — none of them are compiled or referenced. Dead
   files carrying the old generator's output, including the opaque
   `z2V…`-style identifiers, left beside the new shape.

3. **The test that should have caught (2) checks the wrong path.**
   `tests/interface_contract.rs` asserts
   `!root.join("schema").exists(), "retired schema projection tree is absent"`.
   The tree is at `src/schema`, so the assertion is vacuous and green.

Architectural observation, witnessed: `ethos/signal.ethos` declares
`Signal` with empty imports, **empty queries and empty responses**, and a types
section only. Per `Vision/ethos.md` the root for a shared vocabulary that
communicates nothing is `Library`; `ethos-zero` at the pinned `4695ee0c`
supports `Library` (its own commit is "Generate standard Library value traits").
The flow used a Signal root as a bare type carrier. Separately, the declared
`Differentiator.{ ComponentKind AuthorizedObjectKind }` and
`ComponentObjectInterest.{ ComponentKind AuthorizedObjectKind }` are
structurally identical — the kind of repetition `Vision/ethos.md` calls an
implementation failure.

Vision-aligned within the commit: `2c90fc99` renames `InterestMatching` to
`InterestMatchable`, obeying the qualifier-naming rule. It does so in
hand-written Rust; the kind is not declared in the ethos file.

### signal-mirror 1.0.0 — `e6c565ca`, base `e3112358`

Witnessed. Three commits. +470/−2051. `ethos/signal.ethos` is a proper Signal
root with five named queries and nine named responses. `src/schema/lib/*`
(710 lines) and `src/bootstrap_manifest.rs` (156 lines) are deleted — the
cleanup signal-standard did not get. A typed carrier API is added to
`src/lib.rs`.

### meta-signal-mirror 1.0.0 — `bdc76bcd`, base `8117bf38`

Witnessed. Three commits. +395/−1531. Same shape: Signal root with five queries
and six responses, old generator dependencies removed, typed carrier added,
pinned to signal-mirror `e6c565ca` and signal-standard `2c90fc99`.

### signal-introspect 1.1.0 — `910b1e37`, base `3ece305f`

Witnessed. Three commits. +1010/−3369 — the largest deletion in the set:
`src/system_event.rs` (855 lines) and four test files replaced by a generated
`src/generated/signal.rs` (719 lines). `[lib] name/path` was dropped from the
manifest (harmless — the defaults match).

`910b1e37` itself changes only `Cargo.toml` and `Cargo.lock`: a bare 1.0.0 →
1.1.0 bump with no code change. The released head is therefore code-identical to
`6e50a42`.

In the ethos, witnessed: `EngineSnapshotObservation` is simultaneously a query
name, a response name and a type name; `RecordSystemEvent.RecordSystemEvent` and
`FlushSystemEvents.FlushSystemEvents` restate the name as the type. Again the
repetition `Vision/ethos.md` names as failure.

### mirror — WIP `783be4b8`; main `74ed002e` (deprecation)

Witnessed. WIP vs `c9708ed6`: 10 files, +567/−751, version bumped to 1.0.0 on a
branch that does not build.

`cargo check --no-default-features` in a fresh clone at `783be4b8` exits **101**
with 23 errors — reproducing flow 857335's own capture exactly
(`witnesses/periphery/mirror-wip-cargo-check.{log,exit}`). The claim holds.

Two things the 857335 report does not say. First, the failure is not only
unfinished work: `src/config.rs`, `src/client.rs`, `src/shipper.rs`,
`src/service.rs`, `src/readback.rs`, `src/configuration_writer.rs` and
`src/bin/mirror_landed_body_verifier.rs` reference symbols named `z2VXab`,
`z2VTqL`, `z2VVny`, `z2Ve8p`, `z2VSyM` and peers — the old generator's opaque
identifiers, which the pinned producers no longer export (the same identifiers
still sitting in signal-standard's dead `src/schema/lib/generated.rs`). Second,
the WIP introduces a **compatibility path**: `[features] dotos-text =
["datom-cli"]`, an alias keeping the retired feature name resolvable so the
existing `required-features = ["dotos-text"]` binary declarations keep working.
That is the one parallel shape found anywhere in this slice, and the spirit
forbids it. It is confined to an unreleased branch of a now-deprecated
repository.

### spirit — WIP `5c53df2a`; main `8b391bf1` (deprecation)

Witnessed. WIP vs `008d8ca0`: 76 files, **+7253/−4682** — a workspace split, a
typed signal migration, a v15 store migration, a zero-argument daemon and new
fixtures. `5c53df2a` is not an ancestor of main. This is the single largest
investment in the slice, and it is parked on a branch of a repository the living
deprecated twelve hours later.

### Curriculum — `96ed68b4`

Witnessed. Two commits over `a7d2f4f1`, both touching only `roles.datom`.
`7c0dc0c4` converts curly quotes to guillemets — directly Vision-mandated
("guillemets for strings and the curly quotes dropped", 564f55 landing).
`96ed68b4` then un-quotes the dotted model names (`gpt-5.6-sol` and peers),
keeping them bare. The bare string form's name is listed as *open* in 564f55's
summary; this commit settles a question the living had not settled. Small, but
it is a ruling made in code.

### curriculum-deploy 0.6.1 — `535396fe`, base `7cc3cb53`

Witnessed. Three commits, 12 files, +730/−1012. Re-pins datom-codec
`41a3c073` → `f2cc0685` and protos `2d999f17` → `b543678c`, regenerates
`src/generated.rs` (907 lines changed), rewrites `roles.rs` and `runtime.rs`.
This is the one repository in the slice squarely inside the "every consumer is
updated" mandate: it is a direct datom-codec/protos consumer. Warranted.

---

## 3. Gate evidence

### signal-standard — the SSH failure and the local fallback

Witnessed in `flows/857335/witnesses/signal-standard-nix-6688f8ca.log`: the run
prints `cannot build on 'ssh-ng://root@192.168.1.65': error: failed to start SSH
connection to '192.168.1.65'` and then builds all seventeen derivations locally.
The retry log prints the same SSH failure. `…6688f8ca.exit` and
`…-retry.exit` are both `0`. Flow 857335 reported this honestly: "exited 0 only
after remote SSH failed and local fallback built; this is not remote-execution
proof."

What the flow's own note understates: the released head is `2c90fc99`, not
`6688f8ca`. `witnesses/signal-standard-nix-2c90fc99.log` is **0 bytes** and
there is **no `.exit` file for it at all**. The flow's sentence "The final-head
configured matrix has no recorded exit" is true; the fuller statement is that
the released signal-standard 1.0.0 has no Nix gate evidence of any kind, local
or remote — and, per §2, carries eleven committed symlinks that are the previous
revision's build outputs. Every downstream pin in this slice
(signal-mirror, meta-signal-mirror, mirror WIP) points at that ungated head.

### signal-introspect — the outstanding remote gate

Witnessed. `flows/857335/witnesses/producer-gates/signal-introspect-nix.log` and
`signal-introspect-carrier-nix.log` are genuine remote runs: derivations built
`on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`, both `.exit` files `0`, the
carrier log ending `all checks passed!`. Both logs name
`signal-introspect-1.0.0.drv` throughout; the released head is 1.1.0.

Mitigating, witnessed: `910b1e37` changes only the version string, so the gated
code and the released code are the same bytes apart from `Cargo.toml` and
`Cargo.lock`. The flow's "remote gate outstanding" is literally correct and
materially near-empty.

Unknown, stated as unknown: the gate logs' file mtimes (Sep 9 22:41/22:45)
precede the committer dates of every revision they could belong to (Sep 10
06:40+). Under jj, rewriting a working copy changes both the commit id and its
date, so this is fully consistent with an honest run — but it means **no gate
log in this flow can be bound to a commit id by its own content**. None of the
captured logs record the revision they built. That is a structural gap in the
evidence, not an accusation.

### harness — the guessed attributes

Witnessed and confirmed. `git show 722b68b3:flake.nix` declares `checks` with
`default` plus 36 named `cargoTest` attributes and **no `build`, `fmt` or
`clippy` attribute anywhere**. A selection naming those three would fail before
running anything, exactly as the flow reported (exit 1). The corrected
`harness-check-attributes.json` lists 37 entries matching the flake exactly. The
flow's account of this is accurate and its correction was the right one.

Two things it does not say. First, `harness-722b-nix.log` is **0 bytes**;
`harness-722b-nix.exit` is `0`. The gate is a bare exit code with no log —
nothing records what was built. The cause is unknown (a `-L` run writes its
progress to stderr, which a stdout-only redirect would drop; that is a
hypothesis, not a finding). Second, because the flake has no fmt or clippy
check, the Nix gate covers tests only; the report's "strict clippy passed" is a
local, unwitnessed claim.

### terminal-cell — the same pattern

Witnessed. Six attributes claimed (`build`, `default`, `ownership`,
`control-socket-mode`, `fmt`, `clippy`) and all six exist in the flake — the
selection is correct this time, though `default` and `build` are the same
derivation. But the artifacts live at `/tmp/terminal-cell-e44-gates.{exit,log}`,
not in the flow lane: `.exit` is `0`, `.log` is **0 bytes**. And the twelve
`daemon_witness` cases the report leans on are **not** among the Nix checks —
the gate runs two named tests plus build, fmt and clippy. The twelve witnesses
are a local `cargo test` claim only.

### mirror WIP — confirmed failing

Witnessed independently, §2. The flow's claim is accurate and understated.

---

## 4. The deprecation marking against the living's words

The living's words, relayed through 857335's log: "mark spirit and mirror as
deprecated."

Witnessed: `spirit@8b391bf1` changes `AGENTS.md`, `ARCHITECTURE.md`, `README.md`
(+30/−3). `mirror@74ed002e` changes the same three files (+27/−3). Each adds a
"## Status: deprecated" section and rewrites the "Protos estate status" block.
No manifest, flake, module or source file is touched in either.

Read narrowly — *mark* as deprecated — the act matches the words, and the flow
was right to say "No runtime, service, dependency or build changes are part of
this deprecation marking." Read as what the living would want to be true after
saying it, there is a gap, and it is large.

**Spirit is running right now.** The sweep was delegated to a read-only
subagent; the lines below marked *witnessed* this flow re-ran or re-read itself.

- **Witnessed:** `systemctl --user list-units` shows
  `spirit-daemon.service` and `spirit-judge.service` both `loaded active
  running`. Relayed: they are also `enabled`; `spirit-daemon` runs from
  `/nix/store/nnsk892p…-spirit/bin/spirit-daemon` against a generated
  `spirit.config.rkyv`. `/home/li/.local/state/spirit/spirit.sema` was last
  written 2026-09-10 13:30 — after the WIP, before the deprecation commit.
- The unit comes from
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`,
  imported by `modules/home/default.nix:60`, enabled by default for this node
  shape.
- **Witnessed, and this is the sharp point:** `CriomOS-home/flake.nix:120` and
  `CriomOS/flake.nix:91` both read
  `spirit.url = "github:LiGoldragon/spirit/008d8ca0e4a309bdd922fae61681cdc97a484bac"` — the revision *before* `8b391bf1`. The deployed configuration cannot see the deprecation notice at
  all. Nothing about the live system changed.
- `protos-engine/flake.nix:53` consumes `spirit.checks.…test-nota-text` as a
  real build input, pinned at an older revision still.

**Mirror is not running anywhere.** `CriomOS/modules/nixos/mirror.nix:30` reads
`mirrorEnabled = false && mirrorEligible` with a comment that mirror-0.1.2
crash-loops on a redb `HeadFamily` table; the package is still built for a
module that never instantiates a service. witnessed, `CriomOS/flake.nix:70` tracks
`mirror.url = "github:LiGoldragon/mirror"` — **unpinned**, so CriomOS's next lock update is the
one place the deprecation will land by itself. `CriomOS-test-cluster/flake.nix`
inputs both, unpinned. No Cargo crate outside spirit itself depends on `mirror`
— and spirit's own dependency is optional, behind `mirror-shipper`:
deprecated depending on deprecated.

So: documentation-only marking is defensible as an obedient minimum, but it
leaves a live daemon, a home-manager module that starts it, and four flake
inputs untouched — and pins that make the marking invisible where it matters
most. If the living meant the word to change anything about the machine, nothing
changed.

---

## 5. Compatibility paths and parallel shapes

Searched for, and the result cuts both ways.

**Clean, witnessed:** signal-standard, signal-mirror, meta-signal-mirror and
signal-introspect all *removed* `dotos-text` outright rather than aliasing it.
The `datom` feature that replaces it is Vision-mandated, not a compatibility
path: "the datom derives conditional on a feature the CLI enables and the Nexus
does not" (564f55 landing, the living's amendment). No parallel decode path, no
dual wire format, no version negotiation was introduced in any released crate.

**Not clean, witnessed:**

- mirror WIP `783be4b8` declares `dotos-text = ["datom-cli"]` — a pure alias
  preserving the retired feature name. A compatibility path by definition.
- harness `722b68b3` is a repository running two message shapes at once, not by
  a compatibility switch but by an incomplete migration left on main.
- signal-standard `2c90fc99` keeps the entire retired `src/schema/**` tree and
  `src/bootstrap_manifest.rs` in the release, dead and uncompiled, behind a test
  that asserts the wrong path.
- terminal-cell `e44c41a3` keeps `signal-frame` declared and unused.

---

## 6. "Every consumer is updated" — the largest single gap

Witnessed, by reading each consumer's `Cargo.toml` at its own `origin/main`:

signal-standard 1.0.0 is a breaking rewrite — the whole type surface
regenerated, `dotos-text` gone, `InterestMatching` renamed. Repinned onto it:
signal-mirror, meta-signal-mirror, and mirror's WIP. **Left on pre-flow
revisions:** router, meta-signal-router (both `d5a4a545`), signal-agent,
meta-signal-agent, meta-signal-mind, signal-criome, signal-mentci,
meta-signal-mentci, signal-mentci-client, meta-signal-mentci-client (all
`f12d0cb9`). Ten repositories.

Worse than stale — **broken now**, because they pin by mutable branch:

- `mentci/Cargo.toml:26` — `signal-introspect = { branch = "main", features =
  ["dotos-text"] }`. signal-introspect main no longer has a `dotos-text`
  feature. This is an immediate resolution error, not a compile error.
- `persona/Cargo.toml:38`, `introspect/Cargo.toml:35`,
  `meta-signal-introspect/Cargo.toml:21` — `signal-introspect`, `branch =
  "main"`, against a crate whose 855-line `system_event` surface was deleted.
- `persona/Cargo.toml:44` and `terminal/Cargo.toml:75` — `signal-terminal`,
  `branch = "main"`. At `ddbd3237`, `WirePath`, `SocketMode`,
  `UnixUserIdentifier` and `SystemPrincipal` are plain type aliases
  (`pub type WirePath = String;`). `persona/src/direct_process.rs:690-738` calls
  `signal_terminal::WirePath::new(…)`, `SocketMode::new(…)`,
  `UnixUserIdentifier::new(…)` — constructors that no longer exist.

The flow pushed new mains for signal-terminal, signal-introspect,
signal-standard, signal-mirror and meta-signal-mirror without updating the
branch-pinned consumers those pushes break. Its reports do not mention this.
Whether each of these actually fails to build was not run here — the symbol
absence and the feature absence are witnessed; "the build breaks" is inference.

## 7. Pin convergence

Witnessed. The periphery released on 2026-09-10 does not sit on one stack:

| group | datom-codec | protos | ethos-zero |
|---|---|---|---|
| signal-standard, signal-mirror, meta-signal-mirror, signal-introspect, mirror WIP | 0.25.6 `f2cc0685` | 0.29.1 `b543678c` | 6.1.6 `4695ee0c` |
| signal-terminal 1.0.1 → terminal-cell 1.0.0, harness | 0.25.4 `2dad91af` | 0.29.0 `aac95b0d` | 6.1.2 `daf00729` |
| curriculum-deploy 0.6.1 | 0.25.6 | 0.29.1 | 6.1.4 `79e51c0f` (dev) |

Three ethos-zero generator versions produced the checked-in contracts released
the same day. Because the stack deps are optional (`datom`), a default build
does not collide; a workspace enabling `datom` across both groups would.

## 8. A realization defect the flow did not report

Witnessed. `signal-mirror/ethos/signal.ethos:17,20` declare
`ArtifactBytes.Vector<Integer>` and `PayloadBytes.Vector<Integer>`, generating
`pub type PayloadBytes = std::vec::Vec<i64>;`. signal-terminal does the same for
`TerminalInputBytes` and `TerminalTranscriptBytes`. Mirror is the
*payload-blind byte* mirror; its opaque bytes are now eight bytes each on a
layer Vision describes as "fully binary, portable rkyv, zero-copy". `grep` for a
byte primitive in ethos-zero `4695ee0c` finds none — Ethos has `Integer` and
nothing narrower. The flow worked around the gap silently rather than naming it.
The same widening makes `SocketMode` and `NetworkPort` `i64`.

---

## 9. Was it worth touching these repositories at all

The living's question, answered per repository.

**Warranted.** curriculum-deploy — a direct datom-codec/protos consumer, exactly
the "every consumer is updated" case. Curriculum's guillemet migration — a
direct realization of an approved amendment, though `96ed68b4` quietly settles
an open question.

**Warranted in kind, damaged in execution.** signal-standard, signal-introspect
— genuinely shared contracts that had to move for the new Ethos to mean
anything. But signal-standard shipped with committed build residue, a dead
retired tree, a vacuous boundary test and no gate on the released head; and both
left their branch-pinned consumers broken.

**Chain-warranted only.** terminal-cell and harness changed because the flow had
first rewritten signal-terminal, which no order required. harness came out
half-migrated, unversioned, and mis-reported as a version that does not exist.

**Hard to justify.** signal-mirror 1.0.0 and meta-signal-mirror 1.0.0 are new
contracts for `mirror` — a daemon hard-disabled on every host, whose module
carries a comment saying it crash-loops, whose only Cargo consumer is
deprecated Spirit behind an optional feature, and which the living deprecated
twelve hours after these releases were pushed. The spirit WIP is 7253 added
lines in a repository the living then deprecated. Neither was ordered; both
preceded the order that made them moot.

That last point is the honest shape of it: the flow did not disobey. It invested
its largest efforts in mirror and spirit *before* anyone asked what those
repositories were for, and the answer, once asked, was "deprecated." The
correction that generalizes is not "you should have known" — it is that
lifecycle status is worth asking about before a multi-thousand-line port, and
that the four repositories the brief named were named for a reason.

---

## Observations, hypotheses, unknowns

**Observations** (all witnessed): harness is 0.3.4, not 0.4.0, and unbumped
across a breaking wire change. signal-standard 1.0.0 commits eleven `result-*`
symlinks whose derivers are the previous revision's `.drv` paths, keeps a dead
`src/schema/**`, and has no gate exit on its released head. Its
"retired schema projection tree is absent" test checks `schema`, not
`src/schema`. harness's flake declares no `build`/`fmt`/`clippy` check.
`harness-722b-nix.log`, `terminal-cell-e44-gates.log` and
`signal-standard-nix-2c90fc99.log` are all 0 bytes. mirror WIP fails
`cargo check` with exit 101, references non-existent `z2V…` symbols, and
aliases `dotos-text`. Ten signal-standard consumers remain on pre-flow pins;
six branch-pinned consumers reference symbols and features the new mains no
longer have. The periphery spans three ethos-zero versions. spirit-daemon is
live and its deployed pin predates the deprecation commit.

**Hypotheses** (this flow's inference, marked as such): the empty gate logs come
from `nix build -L` writing progress to stderr while only stdout was captured.
The `z2V…` identifiers in mirror WIP are residue from the old schema-rust
generator, which emitted them — the same names survive in signal-standard's dead
`src/schema/lib/generated.rs`. The branch-pinned consumers now fail to build;
symbol and feature absence is witnessed, the build failure is not run.

**Unknowns, kept unknown**: why the 11 `result-*` symlinks were committed —
accident, or an intent to preserve gate evidence in-tree. Why no gate was run on
signal-standard's released head. Whether any gate log corresponds to the
revision it is filed under: no captured log records a revision, and jj rewriting
makes mtimes useless for binding them. Whether the living, saying "mark spirit
and mirror as deprecated", meant the live spirit-daemon to keep running. Whether
`96ed68b4`'s bare dotted model strings match what the living wants for the bare
string form, which 564f55 lists as open.

## Sources

- `/home/li/primary/flows/857335/log.md`; `reports/other-signals.md`,
  `reports/shutdown-signals.md`, `reports/spirit-nexus-audit.md` — relayed.
- `/home/li/primary/flows/857335/witnesses/` —
  `other-signals.md`, `signal-standard-nix-6688f8ca{,-retry}.{log,exit}`,
  `signal-standard-nix-2c90fc99.log`, `harness-722b-nix.{log,exit}`,
  `harness-check-attributes.json`, `producer-gates/signal-introspect*.{log,exit}`,
  `mirror-*-compile.{log,exit}` — read directly.
- `/home/li/primary/flows/564f55/codexPrompt.md`, `log.md` — the mandate.
- `/home/li/primary/Vision/signal.md`, `Vision/ethos.md`.
- Repository objects at the named revisions under
  `/git/github.com/LiGoldragon/`: terminal-cell, harness, signal-standard,
  signal-mirror, meta-signal-mirror, signal-introspect, signal-terminal, mirror,
  spirit, Curriculum, curriculum-deploy, and the consumer manifests of router,
  meta-signal-router, persona, introspect, mentci, terminal, signal-agent,
  signal-mentci, signal-criome.
- `/home/li/primary/flows/f6db8d/witnesses/periphery/mirror-wip-cargo-check.{log,exit}`
  — run by this flow; `method.md` records how.
- `/tmp/terminal-cell-e44-gates.{exit,log}` — read directly.
- Runtime sweep (systemd user units, running processes, CriomOS / CriomOS-home
  flake inputs and modules, estate-wide Cargo manifests) — relayed from a
  read-only subagent; the two `spirit.url` pins, the `mirror.url` input, the
  `mirrorEnabled = false` line and the live `systemctl --user` unit state were
  re-read or re-run by this flow.
