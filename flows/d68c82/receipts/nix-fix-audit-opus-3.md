# Re-audit 3: CriomOS-home c20628 (atop 0729dc), first store-literal wave

## What was read and run
- c20628 in /git/github.com/LiGoldragon/CriomOS-home. Its parent is 0729dc
  (`git log`, witnessed).
- `git diff 0729dc c20628` is byte-identical to reaudit-corrections/source.patch
  (witnessed).
- `git archive c20628` was exported to scratchpad/c4. It is identical to the
  extracted source.tar.gz (`diff -r`, witnessed).
- The shared checkout was not touched. Nothing was built.
- Two probes ran on NixBuilder (prometheus):
  - the guard's Python, run against the c4 tree and against mutated copies;
  - `nix-instantiate --eval` of the runCommand body, with interpolations
    replaced by X.
- Home Manager c554d3, modules/home-environment.nix, was fetched from GitHub
  to read how home.path is built.
- The diff touches three files: checks/bird-codex-selection/default.nix,
  checks/codex-next/default.nix and modules/home/codex-endpoints.nix.

Paths are in c4 (c20628).

## 1. bootstrapFromStable defaults false and is asserted: PASS
- The default is false at modules/home/codex-endpoints.nix:37-41. The callee
  agrees: owned-agents/codex/endpoint-tools.nix:8 (`? false`).
- The option reaches the preparation script through one path,
  codex-endpoints.nix:53, which feeds endpoint-tools.nix:39-45.
- checks/codex-next/default.nix:28 asserts that the option is false.
  - That configuration (:12-20) does not set the option, so the assert tests
    the real default and does not confirm itself.
- Limit: no check asserts that the preparation script built from the default
  lacks the bootstrap. checks/bird-codex-selection:132-135 greps only Bird's
  script, and Bird sets the value explicitly (:54).
- Consequence (inference, not run): any user not given an explicit consumer
  selection, li included, now gets no stable-home bootstrap.
  - The consumer that would set li true is 800052. wave-separation.json says
    it is superseded and must be repinned.

## 2. codex-remote verified through a distinct next sentinel: PASS for the instance the check builds; limit below
- checks/bird-codex-selection/default.nix:73-75 selects `codex-remote-tools`
  from Bird's packages. :128-130 runs codex-remote and compares its output
  with the next expectation.
- The output is CODEX_HOME, `--remote`, the Bird next socket, and the
  argument. Only line 1 is replaced, by the isolated CODEX_HOME.
- The bindings behind it:
  - owned-agents/codex/remote.nix:13 runs
    `exec ${codexCliPackage}/bin/codex --remote ${endpoint} "$@"`;
  - modules/home/profiles/min/codex-remote-control.nix:21-24 binds
    codexCliPackage to nextPackage and endpoint to the tools socket.
- The sentinels are distinct (:16-20). If codex-remote bound stablePackage it
  would print `stable-sentinel`. If it bound canonical it would print
  `wrong-canonical-selection`. Either fails the cmp.
- The rendered script (remote probe):
  - passes `bash -n`;
  - places the codex-remote lines at rendered lines 10-12;
  - ends PYGUARD at column 0 (line 63);
  - keeps `touch "$out"` live (line 64);
  - has a guard body that parses as Python.
- Limit (FLAG, pre-existing, not introduced by this wave): the production home
  has a second codex-remote-tools.
  - It is built at modules/home/profiles/min/default.nix:301-304 from
    `config.criomos.corePackages.codex`, with a hand-spelled socket, and
    installed at :331.
  - modules/home/default.nix:39,42 imports both ./profiles/min and
    codex-remote-control.nix.
  - The same instantiation is present at 1517609 and 0729dc (witnessed).
  - The check imports only codex-remote-control.nix and codex-next.nix
    (:40-43), so it never sees that instance.
  - Under the default, nextPackage is the same package as corePackages.codex.
    The socket string has the same value, so both calls should give one
    derivation (inference).
  - Once a consumer overrides nextPackage, the two derivations differ but
    share bin/codex-remote and bin/codex-desktop. Home Manager c554d3 builds
    home.path with a plain pkgs.buildEnv that does not set
    ignoreCollisions (fetched).
  - A collision failure, or a canonical codex-remote, is therefore expected.
    This was not built.

## 3. Duplicated allowlisted lines refuse: PASS
The guard (:162-177) now consumes each allowlisted digest once per file.

Remote probe results:

| Case | Result |
|---|---|
| Baseline tree | exit 0; 21 retained; 0 violations |
| An allowed herdr.nix line copied again into herdr.nix | exit 1; violation at the copy |
| The same line copied into codex-endpoints.nix | exit 1 |
| An allowed line changed by a trailing space | exit 1 |

- The 21 retained lines are every allowlist entry: 2+2+1+2+2+12.
- Each entry is consumed exactly once, so no entry is stale.
- Limit: an occurrence is keyed by file and line hash, not by line number.
  Moving an allowed line within its own file passes.

## 4. Nothing new hard-wired: PASS
- In modules, the diff changes only a default (codex-endpoints.nix:39).
- The added check strings (`remote-client-sentinel`, `codex-remote-tools`)
  are fixture values in the check.
- No user name, home path or store literal was added to a module.
- The hashed-store grep over the three touched files finds nothing.

## 5. Prior passes still hold: PASS
- codex-next.nix, codex-remote-control.nix, endpoint-tools.nix and remote.nix
  are unchanged since 0729dc, because the diff does not touch them. These
  findings of nix-fix-audit-opus-2.md therefore stand:
  - 0b: fixture repaired, re-rendered above;
  - 1: keep-old hold, with its limits;
  - 2: tools constructed once.
- Findings in nix-fix-audit-opus-2.md now closed:
  - finding 2's "no check asserts codex-remote's package", for the
    codex-remote-control.nix instance;
  - finding 3's unsafe producer default.
- The keep-old asserts remain at checks/bird-codex-selection:86-91 and
  checks/codex-next:36.

## Stated limits (not failures of this wave)
### Remaining store-literal sites: 21 lines, all allowlisted
- packages/harness-profile/owned-rust-exports.json:2,6,10,14,18,22,26,30,34,38,42,46
- packages/harness-profile/default.nix:4,12 (builtins.storePath)
- modules/home/profiles/min/herdr.nix:53-54 (codex stable/next flow-client)
- checks/herdr-toast-delivery/default.nix:131-132 (the same two)
- checks/bird-home-isolation/default.nix:154-155 (synthetic fixtures)
- lib/primary-committer-hook-trust.nix:7 (nodejs-slim)
- No hashed literal sits in a file other than .nix or .json.
- The pattern-matcher and profile-path lines classified in
  nix-fix-audit-opus.md are unchanged by this diff.

### Lexical guard evasions
forbidden() (:147-150) is unchanged by this diff. Every evasion witnessed in
nix-fix-audit-opus-2.md finding 5 still applies:
- `''/nix/store/'' + h`;
- `builtins.storeDir` concatenation and interpolation;
- `inherit (builtins) storePath`;
- `builtins . storePath`, `builtins."storePath"` and `getAttr`;
- JSON `\/` escapes and `/nix…` escapes;
- `"/nix/${"store"}/"`;
- concatStringsSep;
- a prefix split across lines;
- a literal in a file other than .nix or .json that is read with readFile or
  fromTOML.

evaluated-guard-design.md states the same boundary: the scan is a regression
aid and not proof.

### Recorded later debt
- The li/bird name selection lives in the consumer.
- The Horizon typed endpoint policy is not settled.

## Verdict
PASS on all five criteria for the first wave at c20628. One pre-existing
FLAG: the second, canonical-bound codex-remote-tools at
modules/home/profiles/min/default.nix:301-304,331 is outside the check's
module set. It diverges, with an expected buildEnv collision, once nextPackage
is overridden. That is not built and not introduced by this wave.

# Delta audit: CriomOS-home 4a814f (atop c20628), min-profile dedup

## What was read and run
1. The packet at flow-evidence 0c85a3 min-profile-dedup was read.
2. sha256 was taken of child.patch, source.patch and source.tar.gz. All three
   match artifact_hashes.
3. source.tar.gz was extracted to scratchpad/dedup4a8. All 299 files match
   all_file_hashes. There are no extra and no missing files.
4. In /git/github.com/LiGoldragon/CriomOS-home (read-only), 4a814f has
   parent c20628. `git diff c20628 4a814f` is byte-identical to child.patch
   and touches only the two child_paths. Both exported files are identical
   to `git show 4a814f:<path>`.
5. Then: modules/home/profiles/min/default.nix,
   modules/home/profiles/min/codex-remote-control.nix,
   owned-agents/codex/remote.nix, the full checks/bird-codex-selection/default.nix,
   flake.nix:520-547,615, and lib/horizon-user.nix were read, and the tree was
   grepped for remote.nix, codex-remote-tools and bin/codex-remote. Nothing was
   evaluated or built.

## 1. The duplicate is gone and nothing else in the profile changed: PASS
- The min-profile hunks remove only these: the `codexCliPackage` binding, the
  `codexRemote` callPackage with its hand-spelled socket, and the `codexRemote`
  entry in AIPackages. A two-line comment replaces them.
- `codexCliPackage` and `codexRemote` are no longer referenced anywhere in the
  file (grep).
- The tree now has three callers of owned-agents/codex/remote.nix:
  - codex-remote-control.nix:21, the sole production installer;
  - gates/codex-remote;
  - the check.
- No other file provides bin/codex-remote or bin/codex-desktop (grep).
- Coverage is unchanged:
  - The removed entry sat in AIPackages under `mkIf (sizeAtLeast "Min")`
    (min/default.nix:428).
  - The surviving install is `mkIf (sizeAtLeast "Min")`
    (codex-remote-control.nix:111-112).
  - So no size loses codex-remote.
- Cosmetic: the comment at min/default.nix:296-297 ("Codex is the canonical
  pinned upstream CLI; the separately named remote client...") now sits over
  claudeCodePackage. It describes code that is gone.

## 2. The check imports the real profile and fails on a reintroduced duplicate: PASS, with one limit
- checks/bird-codex-selection/default.nix:56 imports
  `../../modules/home/profiles/min/default.nix`, the real file, next to
  core-packages, codex-remote-control and codex-next. The new user, node and
  rustToolchain fixtures (:36-49) supply the inputs the profile reads, for
  example `user.publicKeys` at min:34 and `machine.architecture` at min:243.
- `assert builtins.length (remoteProviders bird) == 1` and the same assert for
  li (:109-110) count the `codex-remote-tools` entries in the merged
  home.packages.
  - On the c20628 profile, the check's `corePackages.codex = canonical` would
    give a second entry, so the assertion would fail at eval (inference from
    the code, not evaluated).
  - The count is by name, not by derivation. A reintroduced instance identical
    to the surviving one is caught too, whereas production's buildEnv would
    accept it silently.
- Limit:
  - `birdRemote` (:88-93) is a buildEnv with `ignoreCollisions = false` over
    `remoteProviders bird`, which the assert has fixed at one element. It
    therefore cannot collide.
  - The "forbid collisions" property adds nothing beyond the count.
  - A collision from a differently named package that ships bin/codex-remote
    would not be seen, because the buildEnv covers only the name-filtered
    entries and not home.path. No such package exists today (grep).
- birdRemote is used by the build script (:160), so the codex-remote sentinel
  cmp now runs through the merged environment.
- Loosened: the service assertion (:143-147) now compares only the services
  prefixed `codex-remote-control`, not all attrNames. This is needed because
  the real profile adds unrelated units. It still catches any extra
  `codex-remote-control*` unit.

## 3. The expected-failing control is not counted as passing: PASS
- `duplicateRemoteNegativeControl` (:98-103) appears only in
  `passthru` of the runCommand (:149).
- passthru is not a build input of that derivation.
- flake.nix:615 exposes only the runCommand as `bird-codex-selection`.
  derivationChecks (:530-540) keeps only top-level derivations, so
  `nix flake check` neither builds nor counts the control.
- Nothing else in the tree references it (grep).
- That the control fails is inference:
  - oldDuplicate binds `canonical`, while the surviving entry binds
    `nextSelected`.
  - Both provide bin/codex-remote and bin/codex-desktop with different
    content.
  - buildEnv with ignoreCollisions=false should therefore stop.
- That failure is not witnessed here. The packet itself lists remote negative
  proof as pending, and Field's c20628 reproduction is a claim in the packet.
- The control is a manual selector. No check asserts its failure, so a future
  change that made it build would pass unnoticed.

## 4. Nothing new hard-wired: PASS
- The removed code took a hand-spelled socket path. The check's oldDuplicate
  takes `bird.criomosHome.codexEndpoints.tools.socket` from the option.
- The new literals are check fixtures:
  - example.invalid identities;
  - "fixture-key";
  - node "endpoint-check";
  - `machine.architecture = "x86_64"`.
- The architecture fixture is constant rather than taken from the check's
  system. It adds i7z to the evaluated package list (min:243), but nothing in
  the check forces that package. This is a fixture choice, not a setup value.
- No new /nix/store literal appears in either diff hunk. The PYGUARD allowlist
  is unchanged.

## Verdict
PASS on all four criteria. The c20628 FLAG (second, canonical-bound
codex-remote-tools at min/default.nix:301-304,331) is closed in source. Open
items:
- The buildEnv collision guard is vacuous once the count is one, so the count
  carries the protection.
- The negative control's failure is unwitnessed and not asserted.
- There is a stale comment at min:296-297.
- Eval, build and negative proof remain for the remote builder.

## Delta audit: 39d266

Verdict: PASS (static; no evaluation or build run, remote evaluation still pending per the packet).

Witnessed from `git diff 12c585 39d266` in /git/github.com/LiGoldragon/CriomOS-home:
- One commit, one file: checks/bird-codex-selection/default.nix (+12/-1); identical to fixture.patch. No production module, owned-agents or license-policy file touched.
- Hunk adds `fixturePkgs = pkgs.extend` replacing only androidenv.androidPkgs.platform-tools with `pkgs.writeShellScriptBin "unrelated-android-tools-fixture" "exit 1"` (built, never run), and `inherit pkgs` becomes `pkgs = fixturePkgs`. The only "license" match is a comment word; no allowUnfree or license attribute set; no assert line added or removed.
- Zero `/nix/store` or `builtins.storePath` in the diff; the sentinel is a derivation, not a literal, so the store-reference ratchet and its allowed-hash list are unchanged.
- Unchanged in the 39d266 file: Min profile imports (core-packages, codex-remote-control, codex-next, profiles/min/default.nix), both `length (remoteProviders ...) == 1` asserts, birdRemote with ignoreCollisions=false and the duplicateRemoteNegativeControl passthru, and the codex-remote next-sentinel `cmp` command checks.
- Inference (mine): `pkgs.extend` with `//` on androidenv/androidPkgs may not reach every path that forces the license gate; only a remote evaluation can show this.

## Delta audit: fe0492 + 628cf7

Verdict: PASS on all six (static plus Field receipts, no build).
1. Factory takes consumer pkgs (CriomOS-home flake.nix:699; gates/bird-codex-selection/default.nix:31,33); no re-import, licence override or package stub added. Sentinels at :16-22 and hexis stub :25-27 predate this delta.
2. Moved checks/ to gates/ outside Blueprint discovery (flake.nix:526-528); run by CriomOS flake.nix:196-198 via projectChecks (:323).
3. Same pkgs as userHomes: CriomOS flake.nix:181 binding feeds factory :197 and nixosSystem :284/:296; userHomes.nix:97-105 useGlobalPkgs + extraSpecialArgs; package-context-qualification.json witnesses match. Check's own pkgs witnessed only through the source binding.
4. Real Min profile imported (:61-64); count one (:118-119); collision-forbidden buildEnv (:97-102); next-sentinel cmp (:164-175); source guard (:186-226); evaluation and build exit 0 on prometheus. Guard JSON output not captured; negative control not built here; override-input directory gone, match rests on post-check-hashes.json.
5. No new store or user/home literal; li/bird keys at userHomes.nix:15-26 are the recorded debt (d8ede2).
6. 6e9e89..fe0492 formatting only (flake.nix:699 joined).
Open: 628cf7 flake.lock pins criomos-home 1517609 without the factory, so committed consumer checks fail until the final Home pin (packet finalHomePin pending). changedPaths lists userHomes.nix, changed in d8ede2 not 628cf7. useGlobalPkgs itself not exercised by the standalone gate.
