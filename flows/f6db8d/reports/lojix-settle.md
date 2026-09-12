# Settling the Lojix stack on the final producer heads

Subflow thread `f6db8d14-1dfe-472d-914e-9c441f852834` of flow f6db8d,
2026-09-11/12. Four repositories written: `horizon-rs`, `signal-lojix`,
`meta-signal-lojix`, `lojix`. Nothing was deployed. The running Lojix service,
its sockets and its store were not touched. CriomOS and CriomOS-home were not
touched. `goldragon` and `criomos-horizon-config` were read only.

**witnessed** = this subflow ran the command or opened the file and the result
is quoted below. **relayed** = another flow's report or the main flow says so
and is named. Observations, hypotheses and unknowns are kept apart.

## 0. What to look at first

1. **Every repository is repinned, gated and pushed.** The release table is
   §1; the gate table is §5.
2. **Two statements in `reports/lojix-criomos.md` §3.3 are wrong**, and both
   were disproved by direct witness, not by argument. §3 and §4.
3. **The lojix VM fixture no longer restates the Horizon schema.** It is
   composed by the pinned producer while the check builds, and a stale
   fixture now fails at build time with a named error. §4.
4. **The landing note for CriomOS's `f6db8d-lojix-start` is §7.**

## 1. The released revisions

Producers before consumers; each gate green before the next repository pinned
it.

| Repository | Version | Final revision |
|---|---|---|
| `horizon-rs` | `horizon-lib` / `horizon-cli` 0.10.1 | `40d04d2504fee619e9b2b2564b8a769a3a9d6049` |
| `signal-lojix` | 4.1.1 | `5c94485c84d20d5b1496d867a2b40f2d908a02e3` |
| `meta-signal-lojix` | 5.1.1 | `2fdc7742eef200ac3ac3057792f2fa4f4bad9f39` |
| `lojix` | 4.0.1 | see §6 |

Each contract repository carries two commits: the repin with its gate, then
the UPGRADES entry with the final producer head pinned. `lojix` carries two as
well — the beads housekeeping of §5, then the repin. The intermediate revisions
(`horizon-rs` `6942b472`, `signal-lojix` `e3c5a5bb`, `meta-signal-lojix`
`4d43ad61`) are pushed and superseded; nothing should pin them.

The producer heads they settle on, all relayed from
`reports/producer-settle.md` and witnessed here by building against them:

| Producer | Version | Revision |
|---|---|---|
| `protos` | 0.30.1 | `171b21f65337983ab624b7b906397a4f1f92c5a3` |
| `datom-codec` | 0.26.3 | `627db67f2655efd9f786864009955005fd8ab2ad` |
| `ethos-zero` | 8.0.1 | `de3d9928b156f2e1a92d060b7817af201abfdbef` |
| `signal` | 3.0.2 | `8f9a0deb701cebbea518679548df4a795affc918` |
| `nexus` | 0.1.1 | `a84bfa960c0d5c02d30048c4bbbc67dfef79a67c` (already pinned; unchanged) |

Each of those five was confirmed to be its repository's actual remote `main`
at the end of this work, not merely the revision the brief named. Witnessed:
`git ls-remote https://github.com/LiGoldragon/<name>.git refs/heads/main`
returned exactly these five hashes.

### Regeneration from ethos-zero 8.0.1 is byte-identical

All three generating repositories assert this themselves. `build.rs` in
`horizon-rs/lib`, `signal-lojix` and `meta-signal-lojix` each reads the
authored `.ethos`, generates, and `assert_eq!`s the result against the
checked-in `src/generated/*.rs`. Every build under the new ethos-zero
succeeded, so **no generated file changed a byte**, and no generated file was
edited. Witnessed: `cargo build` / `cargo test` green in each repository with
the generated sources untouched in `jj st`.

### The locks

Locks 1111 (`LojixNexusHardening`, `/git/github.com/LiGoldragon/lojix`) and
1112 (`HorizonRsNoFreeFunctions`, `/git/github.com/LiGoldragon/horizon-rs`)
were released on the main flow's authorization before any work began.
Witnessed replies:

```
Released.{ 1111 LojixNexusHardening f6db8d [ /git/github.com/LiGoldragon/lojix ] “W3 W8 W9 W10 failure evidence laws and housekeeping” }
Released.{ 1112 HorizonRsNoFreeFunctions f6db8d [ /git/github.com/LiGoldragon/horizon-rs ] “W9 enforce no-free-functions and no-inherent-methods” }
```

This flow then held lock **1204** `LojixSettle` over the four repositories and
this report for the whole of the work.

## 2. One Cargo.lock revision per crate

The brief's item (3) named duplicate `meta-signal-lojix` entries found by
`reports/lojix-criomos.md` §1. That duplication was at lojix `23f09f28`, the
revision CriomOS pins; it is **not** present at lojix `main`. Witnessed at
every repository after the repin, by `grep '^name = ' Cargo.lock | sort |
uniq -d`: the only duplicated package names anywhere are `cpufeatures`,
`getrandom`, `syn` and `windows-sys` — third-party crates at incompatible
semver majors, which cargo cannot collapse and which nothing of ours pins.

One real duplication was found and removed, not previously reported:
**`horizon-rs`'s `Cargo.lock` carried two `datom-codec` 0.25.7 entries** —
the one its manifest pinned (`99a9e8c9cbdb…`) and a second
(`f2cc06858d38…`) reached through `ethos-zero` 6.1.6. Repinning ethos-zero to
8.0.1, which pins datom-codec 0.26.3, collapsed both to the single
`627db67f…`. Witnessed: before the repin `cargo update -p datom-codec` refused
with `specification 'datom-codec' is ambiguous` and listed both; after it,
one entry remains.

## 3. The real cluster proposal — the brief's premise was out of date

**Correction, witnessed.** `reports/lojix-criomos.md` §3.3 names
`/git/github.com/LiGoldragon/goldragon/proposal.datom` as the real cluster
proposal and reports it refused at byte 165 inside "a guillemet string that
itself contains braces", attributing that to a protos writer defect. Three
separate things about that are wrong.

**`proposal.datom` is retired and no longer exists at goldragon `main`.**
Witnessed: `jj file list -r main` in `/git/github.com/LiGoldragon/goldragon`
(main = `199f5eb107d91b9a468cafd09d1b6dc7119df70e`, 2026-09-11) lists
`cluster-definition.datom` and no `proposal.datom`. goldragon's own
`UPGRADES.md` at that revision says "The retired `proposal.datom`
(`Text<ClusterProposal>`) is replaced by" the composed definition. The local
checkout the earlier report read was parked at `2a139455` (2026-09-01), five
commits behind, which is why it still had the file.

**The real proposal today is composed, not authored whole.** goldragon's
`flake.nix` at main composes `./cluster-definition.datom` with
`criomos-horizon-config`'s `horizon-configuration.datom`
(`74a4ad35f7a7`) through `horizon-compose`:

```
horizon-compose "Compose.{ ${configuration} ${cluster} }" > "$out/horizon-definition.datom"
```

**It parses under protos 0.30.1 through lojix's reader.** Witnessed: this
subflow extracted both sources at their `main` revisions, ran the real
producer (`horizon-compose` built from `horizon-rs` at this settle's
revision), and fed the 6060-byte result to `HorizonDefinition::decode` — the
call `lojix` makes at `src/bootstrap.rs:839`, `clients/meta/src/lib.rs:100`
and `tools/src/lojix-write-configuration.rs:141` — inside lojix's own test
harness. Result: `OK: decoded, nodes=8`. **Nothing in lojix needed fixing.**

**The guillemet hypothesis is disproved.** The composed definition carries
seven distinct guillemet strings, none of them containing a brace. To test the
stated cause directly, `«GMKtec EVO-X2»` was rewritten to
`«GMKtec {EVO-X2} [and] braces»` and the definition re-decoded:
`OK: decoded, nodes=8`. A guillemet string containing braces and brackets
round-trips fine under protos 0.30.1.

What the retired file's byte-165 refusal actually was, as far as this flow can
tell: the retired artifact used guillemets as a **map** delimiter
(`«balboa {…} mirror-alpha {…}»`, and nested `«/ {/dev/disk/by-label/NIXOS_SD
Ext4 []}»`) — goldragon's own README still describes that dialect, "maps use
`«key value»`". Current Datom has no map primitive; horizon-rs's
`lib/ethos/horizon.ethos` opens by saying so. That is an observation about a
retired dialect, not a repaired defect, and this flow did not re-run the
retired file against older protos to confirm the byte-165 position has the
same cause it had then.

## 4. The lojix VM fixture

### The stale fixture, and the second correction

`reports/lojix-criomos.md` §3.3's arity finding is **confirmed**. Witnessed
against the composed-out fixture string from `lojix/flake.nix`:

```
REFUSED: Datom(Error { layer: Composition, path: [1, 1, 0], kind: Arity { expected: 11, found: 10 } })
```

Its conclusion is **wrong**. The report says "that check cannot be green at
the revision lojix itself pins". The check was green: the sibling's
`reports/lojix-work.md` gate table records `same-host-test-activation` passing
at exactly that revision. This flow did not re-run the old check — it read why
it could pass, in the sources:

- `clients/meta/src/lib.rs` `actualize_horizon` returns `Ok(None)` for
  `DeploymentInputMode::Direct` without opening the file at all.
- `src/schema_runtime.rs` `proposal_source_rejection` admits
  `(Direct, None)` and rejects everything else.

The check's request selects `Direct`. **Its proposal source was never read.**
The fixture was inert: a stale string that looked like a Horizon definition,
sitting in a request that ignores it. That is worse than a stale fixture that
fails, because it reads as coverage.

### What replaced it

The fixture is now produced by the real producer instead of restated:

- `lojix/checks/horizon/horizon-configuration.datom` and
  `lojix/checks/horizon/cluster-definition.datom` are the authored inputs — a
  one-node cluster `fixture-cluster` with node `atlas`. The old string named
  the cluster `alpha` while the deployment request named `fixture-cluster`;
  the authored source uses the name the request already uses.
- `lojix/flake.nix` gains a `horizon` flake input pinned to **the same
  horizon-rs revision every workspace manifest pins**, and builds
  `horizon-definition.datom` with that revision's own `horizon-compose` while
  the check builds.
- The service's `preStart` installs that file instead of `printf`-ing a
  string.
- The test script reads it back **through lojix's own Horizon reader** before
  the deployment runs, with `lojix-write-configuration` and a `TestDefaults`
  naming the path — the tool's `actualize_horizon_definition` calls
  `HorizonDefinition::decode` and exits non-zero on refusal.

Nothing in the check restates the Horizon schema, so it cannot drift from the
revision lojix pins.

### Seen failing once

The new gate was witnessed failing before it was trusted. With the trailing
`Option<FixedLocation>` removed from the authored `ClusterDefinition` — the
exact staleness that was there — `nix build .#checks.x86_64-linux.same-host-test-activation`
fails at build time, named, without booting anything:

```
lojix-fixture-horizon-definition> error: parse ClusterDefinition: datom: Error { layer: Composition, path: [1, 0], kind: Arity { expected: 11, found: 10 } }
error: Cannot build '/nix/store/acyfhpyx57inlvllg64vfmifjc1781sp-lojix-fixture-horizon-definition.drv'.
```

The fixture was then restored and the temporary commit abandoned.

## 5. The gates

Every gate was run locally on this host with `--builders ''` and seen green
before the commit it covers was pushed. `nix flake check` was always run
against a committed tree, because the flake source is the tracked tree — an
uncommitted new file is invisible to it.

| Repository | cargo test | fmt | clippy -D warnings | doc | `nix flake check -L --builders ''` |
|---|---|---|---|---|---|
| `horizon-rs` 0.10.1 | green (10 tests) | green | green | green | all checks passed |
| `signal-lojix` 4.1.1 | green (with and without `datom`) | green | green | green | all checks passed |
| `meta-signal-lojix` 5.1.1 | green (with and without `datom`) | green | green | green | all checks passed |
| `lojix` 4.0.1 | green (32 green test-result lines, 0 failures) | green | green | green | all checks passed, including both NixOS VM tests |

The lojix `nix flake check` covers every declared check, including the two
tests that boot a guest — `retained-transient-semantics` and
`same-host-test-activation`, the latter now carrying the composed fixture and
the reader witness.

One thing to know about `horizon-rs`: its `flake.nix` carries the package
version as a literal (`version = "0.10.1"`, line 45) independently of the
Cargo manifests. A version bump that misses it leaves the derivation named
with the old version while everything else moves. Both were changed here.

### A beads database appeared in the lojix checkout mid-work

Some other flow ran `bd` in `/git/github.com/LiGoldragon/lojix` while this
work was in flight: `.beads/` appeared with a Dolt store, a remote cache and
per-machine state, fifty-odd files, none of it authored here. lojix had no
`.beads/.gitignore`, so all of it was snapshotted. The canonical beads
`.gitignore` (taken from `goldragon`, which carries the same tool) was added
and the runtime paths untracked, leaving only `.gitignore`, `config.yaml` and
`metadata.json` tracked, as in every other repository that carries beads. It
is a separate commit, ordered **before** the repin, so that the revision this
report's landing note names is the tree the gate ran on.

That ordering is not cosmetic. `.beads/` **does** change lojix's flake source
derivation, even though nothing in it is a Cargo source. Witnessed: with
`.beads/` present the `same-host-test-activation` derivation is
`z91mhqylz5k4jzcb5wqbylg15h3hrb54`, with it moved aside
`9zr2s6pncy2h1m0vfj5yycm1kcyivhxd`. The cause, as far as this flow read it, is
`flake.nix`'s source filter: it admits `(type == "directory")`
unconditionally, so directories carrying no admitted file still reach the
store. That is an observation about the filter, not a repair — it was left
alone, because widening or narrowing it is a change to what every check is
built from and nobody asked for it.

## 6. The mid-flight rebase

This is recorded because the ordering matters to anyone reading the history.

This subflow was told the `lojix-work` subflow had finished and that lojix
`main` stood at 3.0.0 `48f637e8`. It had not finished. Work started on
`48f637e8`: the repin, the fixture replacement, a 3.0.0 → 3.0.1 bump, and a
full local `cargo` gate, all green. The main flow then corrected the premise:
`lojix-work` had released **4.0.0 `8cb12b8d9c3864813cf54619597ea8e734b2e99f`**
onto `main` (the content that had been on the `lojix-trait-laws` bookmark,
which is now gone from the remote), with `signal-lojix` 4.1.0,
`meta-signal-lojix` 5.1.0 and `horizon-rs` 0.10.0 unchanged.

The 3.0.0-based work was discarded rather than merged: `jj new main` onto
`8cb12b8d`, then every edit re-applied from scratch against the 4.0.0 tree —
the same manifest repins, the same `flake.nix` changes (whose anchors had
moved by eighteen lines), the same `checks/horizon/` sources — and the version
bumped **from 4.0.0 to 4.0.1**. The full gate in §5 is the one run on that
rebased tree; nothing from the 3.0.0 run is being relied on.

The three contract repositories were untouched by the correction: their
repins already sat on the heads the correction named unchanged.

## 7. Landing note for CriomOS's `f6db8d-lojix-start`

`reports/lojix-criomos.md` §1.4 records that the branch could not carry its
own repin: the lojix revision CriomOS pins (`23f09f28`) does not compile,
because its `Cargo.lock` carries two `meta-signal-lojix` 2.3.0 entries at
incompatible `datom-codec` revisions, and the branch could not rewrite
`CriomOS/flake.lock` while another f6db8d subflow held it.

**The revision `f6db8d-lojix-start` should pin is `lojix`**

```
<FINAL-LOJIX-REVISION>
```

— version **4.0.1**, `main`, the revision whose gate is §5.

Three things about it that the branch's module depends on, all unchanged from
what §1.2 of that report verified field by field: the binary is `lojix-nexus`,
it takes zero arguments, and it opens `/run/lojix/ordinary.sock`,
`/run/lojix/meta.sock` and `/var/lib/lojix/lojix.sema` by its own built-in
defaults. Nothing in this settle touched any of them.

Its `Cargo.lock` carries one revision of every crate of ours (§2), so the
build failure §1.4 witnessed at `23f09f28` cannot recur at this revision —
witnessed here by `nix flake check` building the package.

## 8. Unknowns

- Whether the retired `goldragon/proposal.datom`'s byte-165 refusal under the
  older protos had the same cause it has now. The file is gone from goldragon
  `main`; this flow read it from a stale local checkout, established that the
  live artifact is a different file, and did not pursue the dead one further.
- Whether any consumer outside these four repositories still pins the
  superseded intermediate revisions listed in §1. This flow touched no
  consumer.
- `reports/lojix-work.md` records 26 unmerged lojix bookmarks awaiting the
  living's ruling. This settle neither added to nor resolved that list.

## Sources

- Direct action: this subflow ran every command quoted above on primary under
  `FLOW_ID` f6db8d, holding Orchestrate lock 1204. Every `cargo`, `nix`,
  `jj`, `git ls-remote` and `orchestrate` result is its own tool output in
  this session.
- `flows/f6db8d/reports/producer-settle.md` — the four producer heads
  (`protos`, `datom-codec`, `ethos-zero`, `signal`) and their gates; relayed,
  and witnessed here by building against them.
- `flows/f6db8d/reports/lojix-criomos.md` §1.4, §3.3 — the pinned-lojix build
  failure, the fixture arity finding and the proposal-parse finding. §3.3's
  arity finding is confirmed here; its two conclusions are corrected in §3
  and §4.
- `flows/f6db8d/reports/lojix-work.md` — the 0.10.0/4.1.0/5.1.0/3.0.0
  releases this settle repins, and the lojix bookmark ruling still owed.
- The main flow's mid-task correction, quoted in substance in §6 — the source
  for lojix `main` having moved to 4.0.0 `8cb12b8d` while this work was in
  flight.
- `/git/github.com/LiGoldragon/goldragon` at `main`
  `199f5eb107d91b9a468cafd09d1b6dc7119df70e` and
  `/git/github.com/LiGoldragon/criomos-horizon-config` at `main`
  `74a4ad35f7a7` — read only, for §3.
- The `nexus`, `testing`, `versioning`, `file-editing` and `flow-evidence`
  skills.
