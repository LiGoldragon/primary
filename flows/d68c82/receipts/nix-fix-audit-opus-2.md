# Re-audit: CriomOS-home 00b534 -> c8fee5 -> 0729dc, CriomOS consumer 800052

## What was read
- 00b534 and c8fee5 (CriomOS-home), each exported with `git archive` into
  scratchpad/c2 and scratchpad/c3. 800052 (CriomOS) was read with `git show`.
  No shared checkout was edited. Nothing was built.
- The evidence files match the commits (witnessed):
  - audit-correction/source.patch == `git diff 1517609 00b534`
  - audit-child.patch == `git diff f5fab4 00b534`
  - consumer-selections/userHomes.nix == 800052:modules/nixos/userHomes.nix
- Home Manager is locked at c554d3 in both flakes. Its modules/systemd.nix
  was fetched; its sha256 a5df03… matches the packet's copy.
- sd-switch 0.6.4 is the version in the locked nixpkgs 0e251e
  (pkgs/by-name/sd/sd-switch/package.nix). Its source was fetched from sr.ht.
- Two probes ran on NixBuilder (prometheus):
  - `nix-instantiate --eval` of the check's runCommand script, rendered from
    00b534 and from c8fee5, with interpolations replaced by X;
  - a Python probe of the guard's `forbidden()` function.

Paths are c8fee5 paths unless marked otherwise.

## 0. c8fee5 formatting deltas are formatting only — PASS
- Three files changed:
  - checks/bird-codex-selection/default.nix
  - modules/home/codex-endpoints.nix
  - modules/home/profiles/min/codex-remote-control.nix
- With all whitespace stripped, each file is byte-identical to its 00b534
  version.
- The only whitespace change inside a string is the check's runCommand body.
  It was shifted by 2 columns. Rendered remotely, both versions give the same
  string (sha256 b4d26a…).

## 0b. 0729dc fixture delta — PASS: no assertion changes; the runtime script changes, as a repair
- heredoc-fixture-child/fixture.patch == `git diff c8fee5 0729dc` (witnessed).
- One file changed, checks/bird-codex-selection/default.nix:117-121.
  Lines 1-113, which hold every Nix assert, are byte-identical (witnessed).
- The expected fixture has the same four strings, now written with printf.
- Rendered on NixBuilder:
  - the script passes `bash -n`;
  - the PYGUARD block parses as Python;
  - the PYGUARD terminator is at column 0;
  - `touch "$out"` is a live command again.
- The rendered builder script therefore differs from c8fee5. In c8fee5 the
  `<<'EXPECTED'` heredoc never ended and swallowed the cmp, the grep, the
  guard and `touch`. With 0729dc those commands run.
- So it changes no assertion and no expected value. It does change what runs:
  it repairs finding 4's FAIL. The check was not built.

## 1. keep-old hold for stable and next, with a working Field release — PASS (source); native run not witnessed
- The option is typed `enum [ "keep-old" "restart" ]`, default keep-old:
  modules/home/codex-endpoints.nix:24-31.
- Both units set it: modules/home/profiles/min/codex-next.nix:51 and
  modules/home/profiles/min/codex-remote-control.nix:117.
- Home Manager c554d3 accepts Unit.X-SwitchMethod with keep-old
  (modules/systemd.nix:160-173). startServices defaults to true, which means
  sd-switch runs (:335-342, :507).
- sd-switch 0.6.4 takes the method from the NEW unit file (src/lib.rs:267-302,
  `new_unit_file.switch_method()`). For an active unit whose old unit file
  exists, keep-old gives KeepOld. So the first activation of this candidate
  already holds; the old units do not need to carry the key.
- Release works by flipping the option to restart:
  - restart_eq excludes only Description and Documentation
    (src/unit_file.rs:142-147), so a change in X-SwitchMethod alone makes the
    unit differ;
  - the new value, restart, then gives Restart (lib.rs:275).
  - A manual `systemctl --user restart` also releases it.
- The check asserts both states: checks/bird-codex-selection/default.nix:83-88.
  checks/codex-next/default.nix:35 asserts keep-old.
- Limits:
  - After the daemon-reload, a crash restarts the unit on the new
    definition: Restart=on-failure (codex-next.nix) and Restart=always
    (codex-remote-control.nix). The option description states this.
  - keep-old is the standing default, not a one-time hold. Every later change
    to these two units also stays held until a restart.
  - Neither consumer 800052 nor any other source sets switchMethod. The
    release step exists only as the option.
  - New client wrappers (home.packages) are installed while the old servers
    keep running. The source does not prevent that window.
  - The real sd-switch hold was not run.

## 2. Endpoint tools constructed once — PASS
- The one construction is the readOnly `tools` option:
  codex-endpoints.nix:47-56. codex-next.nix:11 and codex-remote-control.nix:19
  read it.
- The socket is spelled once: owned-agents/codex/endpoint-tools.nix:12.
  remote.nix receives it at codex-remote-control.nix:21-24. That file is a
  separate tool (codex-remote and codex-desktop), not a second endpoint-tools.
- Gap: remote.nix gets nextPackage directly (codex-remote-control.nix:22), and
  no check asserts codex-remote's package.
- Naming carried over from main: `codexStable` is the next default client
  (codex-remote-control.nix:20), and the next admin client is named
  `codex-stable-remote` (endpoint-tools.nix:26).

## 3. user/home literals gone from let-blocks — PASS producer; FAIL consumer criterion
- Producer: the touched modules have no "li", "bird" or "/home/…" literal
  (grep witnessed).
- Pre-existing, unchanged from main: WorkingDirectory "${home}/primary"
  (codex-next.nix:58, codex-remote-control.nix:13).
- Consumer 800052 hard-wires the user names `li` and `bird` as keys of a
  let-bound map: CriomOS modules/nixos/userHomes.nix:15-27. It applies them by
  horizon user name at :56-58.
  - It holds no home path and no store literal.
  - It does not set switchMethod, so the hold stands.
  - Values: li gets true/true/true. bird gets useNextAsDefault true,
    bootstrapFromStable false, artifactAutoOpenDisabled true. This matches
    main's behaviour for both.
  - The same file already carries hashed store literals that 800052 did not
    add: userHomes.nix:31-32, 36, 41-42, 46 (zeusRecordedHomeAdoption).
- Producer defaults when a user has no selection
  (codex-endpoints.nix:32-45): useNextAsDefault false, bootstrapFromStable
  true, artifactAutoOpenDisabled false. Any user missing from the consumer map
  therefore gets a stable-home auth bootstrap. The safe default for Bird would
  be false.
- Cohort: 800052 still pins criomos-home 1517609 (flake.nix:36 and the lock).
  That revision does not declare criomosHome.codexEndpoints. So 800052 is not
  evaluable without a pin to c8fee5. Its packet says this ("no push or pin
  yet").

## 4. Distinct sentinels catch wrong selection — PASS (assertions); runtime part FAIL at c8fee5, repaired at 0729dc (not built)
- The three sentinels are distinct: nextSelected, stableSelected and
  canonical (checks/bird-codex-selection/default.nix:16-20).
- These evaluation asserts catch the wrong option or the canonical package:
  - stable read as next: :99-100;
  - next read as stable: the liNext and birdNext equality asserts;
  - canonical selected: :81-82;
  - dependency context: :102-107.
- checks/codex-next/default.nix:7,23 builds its expected package
  independently of the option it tests.
- FAIL at c8fee5, repaired by 0729dc (see 0b). The runCommand body is broken in 00b534 and c8fee5 alike (witnessed by
  remote render):
  - The Python block at column 0 drops the indented string's minimum indent.
    The heredoc terminator then renders as "  EXPECTED" (:122), so
    `<<'EXPECTED'` (:117) never ends.
  - The expected lines also keep two leading spaces.
  - Everything after :117 becomes heredoc input: the cmp, the Bird bootstrap
    grep, the li client run, the whole PYGUARD guard, and `touch "$out"`.
  - None of it executes, and the derivation produces no output.
  - In 91dc62 the terminator rendered at column 0.
- Self-confirming: the Bird no-bootstrap grep tests bootstrapFromStable=false,
  which the check itself sets (:54). The production value lives only in
  800052.

## 5. Repo-wide guard — PARTIAL
- Scope: .nix and .json under the whole source tree (:158), with negative
  controls (:140-153). Debt is allowed per file by line sha256 (:137).
- Probe on NixBuilder. CAUGHT:
  - a literal hash;
  - `"/nix/store/" + h`;
  - `"/nix/store/${h}"`;
  - `builtins.storePath`;
  - a JSON literal;
  - `"/nix/store/"+h`.
- EVADES:
  - `''/nix/store/'' + h` (indented-string concat);
  - `builtins.storeDir + "/" + h`;
  - `"${builtins.storeDir}/${h}"`;
  - `inherit (builtins) storePath;`;
  - `builtins . storePath`;
  - `builtins."storePath"`;
  - `builtins.getAttr "storePath" builtins`;
  - JSON `\/nix\/store\/…`;
  - JSON `/nix…`;
  - `"/nix/${"store"}/…"`;
  - `lib.concatStringsSep "/" [ "" "nix" "store" h ]`;
  - a prefix split across lines;
  - any literal in a non-.nix/.json file read with readFile, fromTOML or
    importJSON on another suffix.
- Copying an allowed line within the same file passes, because the allowlist
  is a set of line hashes per file.
- At c8fee5 the guard never runs (finding 4). At 0729dc it runs.
- The allowlisted debt still includes Codex flow-client store identities:
  modules/home/profiles/min/herdr.nix and checks/herdr-toast-delivery.

## 6. New store literal or hard-wired value introduced — PASS (no store literal); see 3
- Hashed-store grep over the touched files in c8fee5: exit 1, no match.
- 800052 adds no store literal.
- The hard-wired values introduced are the li and bird keys in 800052
  (finding 3).
