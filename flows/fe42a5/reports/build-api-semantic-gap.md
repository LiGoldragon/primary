# Flow build centralization: pre-edit gate fails

2026-10-31. Mind core Primary authorized centralization conditionally, then explicitly held editing until existing API coverage preserved exact toolchain, source and archive semantics. An implementation-reader and an independent tester compared the files read-only. No Flow source path was reserved because editing never became eligible.

## Source identities

| Repository | HEAD | State |
|---|---|---|
| `/git/github.com/LiGoldragon/flow` | `60434783b3ed292e3f0b8f4efe3a3c5561a76b96` | Foreign working-tree changes present; untouched. `flake.nix` read as found. |
| `/git/github.com/LiGoldragon/rust-build` | `1bcdafd4590952f73fada56b0507c64192fd6327` | No source change made. Local `AGENTS.md` read. |

Input locks also differ: Flow Crane `eb35abda9f232cc6610b1d1e3200d15c49b7ac54` / Fenix `f8ac2cd5626cc565f546e1053ab4591cfe0b3ea9`; rust-build Crane `59a82a1222dd3b2080b5cc52a1a2e8d5f1b77f37` / Fenix `6914a98b7864cb3ef33cb0a2581f8aed3d354e48`. Equivalent configuration would retain Flow's pins, not silently take shared defaults.

## Existing mapping, where available

Flow `flake.nix:25–31` has exactly `[ "cargo" "rustc" "rustfmt" "clippy" "rust-src" ]`. Shared defaults add `rust-analyzer`; `fromPkgsWithToolchain` at `lib/default.nix:30–35` accepts the exact caller-created toolchain. Its returned Crane operations cover current consumer calls and feature arguments.

The following is a partial configuration mapping, not a patch or a claim of whole-build equivalence. `rustBuildApi` denotes the shared library configured with the same Crane input; `fenix`, `system` and `pkgs` retain Flow's existing inputs:

```nix
toolchain = fenix.packages.${system}.complete.withComponents [
  "cargo" "rustc" "rustfmt" "clippy" "rust-src"
];
rust = rustBuildApi.fromPkgsWithToolchain pkgs toolchain;
src = rust.cleanSource {
  root = ./.;
  name = "source";
  pruneDirectories = [];
  extraFilters = [ (path: type: pkgs.lib.hasSuffix ".ethos" path) ];
};
```

`pruneDirectories = []` is required for the exact main filter rather than accepting shared pruning defaults (`lib/default.nix:65–95`). This mapping was checked by source inspection, not evaluated against Nix derivations.

Flow's `flowEthosSource` and `lawSource` (`flake.nix:48–55,81–88`) admit directories and selected suffixes only. Shared `cleanSource` always also admits Crane Cargo sources, with no switch to disable that arm. Those special filters must remain consumer-owned and unchanged in a narrow centralization; replacing them through this API would alter inclusion.

## Decisive missing capability

Flow currently constructs raw `(crane.mkLib pkgs).overrideToolchain toolchain` (`flake.nix:32`). Shared `fromPkgsWithToolchain` instead overrides every `mkCargoDerivation` (`lib/default.nix:42–62`):

- `doCompressAndInstallFullArchive` defaults to true. A caller can set the flag explicitly, but Flow's inherited Crane behavior must be established first; false was not assumed equivalent.
- `preInstall` always gains `normalize-cargo-artifacts`. Caller `preInstall` is concatenated with the normalizer. There is no configuration capability to omit this added mutation.

An explicit toolchain and source filter cannot remove that mandatory artifact normalization. Exact current archive/artifact semantics therefore fail the authorized gate. No override workaround or API extension was introduced. Output definitions and feature calls can remain consumer-owned, but their preserved derivations have not been established while this gap stands.

## Witness and disposition

Both readers identified the mandatory normalization gap independently; coordinator read the implementation and lock pins directly. Primary result delivery402 was accepted Queued, not a consumption receipt. The change remains read-only pending Primary judgment.

**Production lines removed 0 / added 0. Patch: none. Full build evaluation: not run. Build: not run.** No lockfile/source edit, heavy build, runtime action, cutover change, Flow v1 work or crate2nix rewrite occurred. Source inspection is not successful build evidence.

Field successor separately reported that the historical Home hand is absent and no reachable current speech hand is held; it forwarded the speech deployment-gap witness to Field Primary. Thus the earlier account's Field/Home route is an evidence handoff, not direct owner acceptance or a completed repair. `primary-swaf.1` and `primary-bie3.6.3` remain open.
