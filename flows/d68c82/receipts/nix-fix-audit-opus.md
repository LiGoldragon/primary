# Audit: CriomOS-home 91dc62 (first wave, Codex endpoint store literals)

Scope read: candidate 91dc62 and main 1517609 (its parent), exported with
`git archive` into scratchpad/cand and scratchpad/main; the shared working
copy was not touched. `git diff main 91dc62` is byte-identical to the
packet's source.patch (witnessed). The working copy's HEAD 8fa863 is a
separate line, not a descendant of 91dc62, and is out of scope.
Paths below are candidate-tree paths unless marked main:.

## 1. No store literal left in touched files, none relocated — PASS
- Witness: `grep -En '/nix/store/[0-9a-z]{32}-'` over the six touched files
  returns nothing (exit 1). The same grep on main:codex-next.nix:16-17 and
  main:codex-remote-control.nix:24-25 finds the four removed literals.
- No relocation: the diff touches no JSON, hash or manifest file
  (owned-agents/codex/hashes.json is unchanged); the two new files,
  modules/home/codex-endpoints.nix and owned-agents/codex/endpoint-tools.nix,
  hold no literal.

## 2. Each replacement resolves from a declared package/option — PASS, with gaps
- modules/home/codex-endpoints.nix:6-15 declares
  criomosHome.codexEndpoints.{stablePackage,nextPackage}, both defaulting to
  config.criomos.corePackages.codex (core-packages.nix:9-14, which is
  callPackage ../../owned-agents/codex, versioned from hashes.json).
- Consumers interpolate the package, so Nix dependency context is kept:
  codex-next.nix:10,12-16,65; codex-remote-control.nix:21-29,119;
  endpoint-tools.nix:10,21,27-31.
- Overrides propagate: checks/bird-codex-selection/default.nix:36 overrides
  corePackages.codex and :56-70 asserts that every ExecStart equals the
  override and that it carries the override's drvPath in its context.
- Gap a: codex-remote-control.nix:20,49 still selects
  config.criomos.corePackages.codex directly for the plain `codex` of users
  other than li and bird, bypassing the endpoint options.
- Gap b: codex-remote-control.nix:28 repeats the socket path
  `.codex-next/app-server-control/app-server-control.sock` as a string
  instead of using endpoint.socket (endpoint-tools.nix:5).
- Gap c: owned-agents/codex-next is no longer used by any module. Only
  flake.nix:477 references it, as a package output.

## 3. Client/server match; auth, home and socket intent — PASS for match, FLAG for intent
- Next pair: the server (codex-next.nix:65), raw/flow/remote clients
  (:29,35,41), the default `codex` (codex-remote-control.nix:22,25) and
  codex-remote (:26-28) all read nextPackage. They match by construction.
  For li this replaces a frozen 0.158.0-alpha.9 pair with an unfrozen pair
  at the hashes.json version (0.163.0).
- Stable server: codex-remote-control.nix:119 reads stablePackage. No
  CODEX_HOME is set and it listens on unix://, as on main.
- Home and socket: endpoint-tools.nix:4-5 gives
  `${homeDirectory}/.codex-next` and
  `.../app-server-control/app-server-control.sock`, the same as
  main:codex-next.nix:20-21.
- Auth: endpoint-tools.nix:29-35 bootstraps auth.json and config.toml only
  when bootstrapFromStable is set, and codex-next.nix:15 passes !birdTarget.
  I read li's formerly pinned prepare script,
  /nix/store/dxqsqx…-codex-next-prepare, on ouranos. Its behaviour matches
  the new script: mkdir, chmod 700, the same bootstrap loop. Bird's pinned
  prepare (58axnp…) is not in the local store, so it was not witnessed.
  The new Bird prepare has no bootstrap. The check enforces this at
  bird-codex-selection:86-89.
- FLAG (intent change): main:checks/bird-codex-selection:66-69 said "This
  correction does not retire or upgrade Bird's other occupied endpoint". The
  candidate moves Bird's stable server from the frozen 0.153.4 to
  stablePackage (asserted at :65). It also moves li's stable server, which
  main:codex-remote-control.nix:19-21 described as having "an unregistered
  client attached". Whether that unregistered client still matches the new
  server cannot be read from source.

## 4. Occupied-executable transition explicit, cutover left to Field — FAIL
- The candidate deletes the freeze (the `occupied` branches in
  main:codex-next.nix:15-17,94-95 and main:codex-remote-control.nix:19-28,127).
  Nothing replaces it as a transition: there is no option, no hold, and no
  X-SwitchMethod.
- Neither the CriomOS-home nor the CriomOS source sets
  systemd.user.startServices, X-SwitchMethod or X-RestartIfChanged
  (grep witnessed). In home-manager at the locked rev c554d344
  (modules/systemd.nix, fetched), startServices defaults to true, which
  means sd-switch restarts changed units. Home activation of this candidate
  would therefore restart codex-remote-control-next and codex-remote-control
  for li and Bird. The cutover happens at Home activation, not as an
  explicit Field step.
- The commit message has no body. The only statement about the transition
  is the packet's runtime_effect, "real cutover required". That is a claim
  outside the source, and the source does not carry it.
- Unblock: the source needs an explicit Field-owned cutover, for example
  X-SwitchMethod = "keep-old" on the occupied units until Field restarts
  them, or a hold option that Field flips. Which mechanism to use is a
  ruling for the main flow or Field.

## 5. Checks and negative guard fail on a reintroduced literal — PARTIAL
- PASS: the guard at bird-codex-selection:94-97 matches every removed
  literal (static grep on main files: exit 0, 4 hits) and passes on the
  candidate (exit 1). The flake wires it at flake.nix:615. A literal
  reintroduced into li's or Bird's ExecStart would also fail the evaluation
  asserts at :63-65.
- FAIL, coverage: the guard reads only four files. It does not reach
  herdr.nix, checks, lib/, packages/, or a JSON or manifest. A literal
  moved into owned-agents/codex/*.json and read with fromJSON evades it.
  So do `builtins.storePath ("/nix/store/" + h + "-codex")` and
  `"/nix/store/${hash}-codex"`. I witnessed all three with a static probe:
  grep exit 1.
- FAIL, discrimination: stablePackage and nextPackage both default to the
  same `selected` (:36), so a consumer that read the wrong option would
  still pass. No check overrides the two options separately.
- Self-confirming: checks/codex-next/default.nix:22 reads the same option
  the module reads, so :35-37 only checks that the module agrees with
  itself. :45 compares `--version` to package.version, which duplicates the
  package's own installCheck (owned-agents/codex/default.nix:36).
- The derivation checks were not run, per the brief: they need builds. The
  packet's own record is "diff --check only; remote formatting/evaluation/
  build pending".

## 6. Structure: bindings in modules and options, not let-blocks of host values — PARTIAL
- PASS: package selection now sits in a declared option module
  (codex-endpoints.nix). The endpoint wrappers and prepare script are one
  shared callPackage file (endpoint-tools.nix).
- FAIL: user and host identity is still hard-coded in let-blocks and
  duplicated across both modules:
  - birdTarget, with "bird" and "/home/bird", at codex-next.nix:11 and
    codex-remote-control.nix:18;
  - usesRemoteDefault, with "li" and "/home/li", at
    codex-remote-control.nix:19;
  - the li and bird lists at :43,73,79.
  These are setup-specific values in a general repository and should be
  options or horizon facts.
- FAIL: endpoint-tools is instantiated twice (codex-next.nix:12,
  codex-remote-control.nix:21) rather than exposed once as a module value.
  The endpoint facts (home, socket) are not options.

## Remaining hashed store literals (main and candidate)
Removed by the candidate: main:codex-next.nix:16,17 and
main:codex-remote-control.nix:24,25.
Present in both:
- modules/home/profiles/min/herdr.nix:53-54 (codex-stable/next-flow-client,
  in the rotation predecessor config)
- checks/herdr-toast-delivery/default.nix:131-132 (the same two)
- lib/primary-committer-hook-trust.nix:7 (nodejs-slim-24.19.0 node)
- packages/harness-profile/default.nix:4,12 (builtins.storePath of
  home-manager-path and chatgpt-26.901.51231)
- packages/harness-profile/owned-rust-exports.json:2,6-46 (12 Rust
  toolchain store targets: literals held in a JSON manifest)
- checks/bird-home-isolation/default.nix:154-155 (synthetic hash-form
  fixture literals)
Pattern matchers or fixtures, not identities:
- modules/home/base.nix:109
- modules/home/profiles/min/pi-models.nix:229,233
- modules/home/profiles/min/migrate-obsolete-spirit-judge-override.sh:38
- modules/home/profiles/min/field-monitoring.nix:175
- checks/spirit-deployment/default.nix:429-453
- checks/codex-next/default.nix:39
- checks/opencode-harness/default.nix:73,76
- packages/messenger-clj-deployment/default.nix:11
- patches/herdr/codex-executable-selection.patch:457 (comment)
Profile-path literals, a separate class (needs a ruling on whether they are
"Nix paths"):
- modules/home/profiles/min/flow.nix:45
- modules/home/profiles/min/spirit.nix:45-46
- modules/home/profiles/med/element.nix:19
- packages/flow-deployment/default.nix:138
