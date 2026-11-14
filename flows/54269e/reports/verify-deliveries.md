# Verification of the smaller deliveries (ouranos, 2026-11-14)

Nothing was switched, configured or committed. The only side effect is that `apksigner` and a JRE were fetched into the Nix store (claim 6). Scratch: /tmp/tmp.TMUrWUhX4C.

## 1. Claude Desktop 5.11492.5 is installed and launches: verified
- `readlink -f $(readlink -f ~/.local/state/nix/profiles/home-manager)/home-path/bin/claude-desktop`
  -> `/nix/store/c5qpvyf4r6sbfsilm2z15zks9fk660x1-claude-desktop-5.11492.5/bin/claude-desktop`
- The active generation is home-manager-1159 (the `home-manager` profile link, 2026-11-14 05:43). The desktop entry `Exec=claude-desktop %U` resolves to that same store path through `~/.nix-profile/bin`.
- `ps -eo pid,args | grep claude-desktop` -> a running process `/nix/store/c5qpvyf4r6sbfsilm2z15zks9fk660x1-claude-desktop-5.11492.5/lib/claude-desktop/claude-desktop`.

## 2. intent:scratch:0 in every permaflow's system modules and every role packet: verified for the declarations, with one stale find
- Flow Nexus: `flow-nexus-meta 'Configuration'` is a read. It answered `Configuration.{ ... }`, 33675 bytes. The running daemon is `flow-configured-0.56.2`, the same store path as the client.
  Parsing the 40 `ConfigureMetaflow` entries: 40 of 40 hold `intent:scratch:0` in SystemModules (40 occurrences in total, none in PromptModules).
- Curriculum: the running `curriculum-nexus` (pid 513076) has `CURRICULUM_ROLES_FILE=/nix/store/0q6d4lbn28skhwqsixhdns7r7gy659nf-source/roles.datom`.
  `awk` over its 31 role lines -> all 31 contain `intent:scratch:0`.
- Differences from the brief: there is no roles.datom in psyche-belief. The roles are in the Curriculum repository, `/git/github.com/LiGoldragon/Curriculum/roles.datom` (HEAD 4695835). That file has 0 occurrences of `scratch`, so it does not match the file the running Curriculum reads. Whatever landed the scratch module in the running roles file is not in the repository checkout I read.
- Stale, probably unrelated: `~/.claude/agents/general-purpose.md` and `book-author.md` (both dated Nov 3) hold 0 occurrences of `scratch`. I did not find where Curriculum writes composed packets now, so the per-packet composed text is unverified; only the roles source is verified.

## 3. AskUserQuestion left out on the five living-interaction permaflows: verified
- The same Configuration read, `ConfiguredHarnessFlags`, has 20 entries. `--disallowedTools ...AskUserQuestion` appears on exactly 5:
  Psyche beliefReview Fable, Psyche beliefReview Opus, Psyche nexusVariations Fable, Psyche core Fable, Psyche core Opus.
- Those are exactly the 5 permaflows whose modules include `intent:living-interaction:0`.
- My own process (Psyche core Opus 54269e) carries `--disallowedTools Artifact,ArtifactComments,ArtifactData,SendMessage,ListAgents,AskUserQuestion`, matching the configuration.
- Caveat: the five are the 5 permaflows that carry the module living-interaction, and no other permaflow carries the flag. The flag is a harness flag, not a `LeaveOut`; the leave-outs hold only ClaudeMd, GitInstructions and Codex names.

## 4. Amend exists in the live meta contract: verified (not called)
- Version: `flow-nexus-meta` and the daemon are both `flow-configured-0.56.2`. The tool takes no help argument (`--help` is refused as an invalid Input), so I read the contract text embedded in the binary: `strings .../flow-configured-0.56.2/bin/flow-nexus-meta`.
- Decisive lines: `Amend.{ Address Change } ]          ; one value of one permaflow` in `ConfigurationChange`, and `; Configure.Amend changes one value of one permaflow alone: it names the permaflow's Address and the Change.`
- `Change.[ Workspace.Option<Root> Purpose Kind.FlowKind Continuity Add.Element Remove.Element ]`.
- The knowledge module flow-messaging:0 names Flow 0.54.3; the installed version is 0.56.2.

## 5. The primary repository is clean: failed (the ignore rules are verified)
- `git -C /home/li/primary status --short | wc -l` -> 13 lines, not clean:
  ` M .beads/config.yaml`, ` m flow`, ` M flows/374411/0mlh-release/report.md`, and 10 untracked: `.beads.gate.lock`, `.cloudflare/`, `flows/1203fb/`, `flows/2e404d/release/`, `flows/565bc8/release-0562/`, `flows/565bc8/release/`, `flows/896bac/handover.md`, `flows/896bac/reports/`, `flows/896bac/rmmd/`, `flows/e3a7d1/`.
  Some of this may be other flows' work in progress; the claim as stated ("clean") does not hold at this moment.
- Ignore rules, tested with `git check-ignore -v`:
  - `flows/abc/x.txt` -> ignored (`/flows/*/**`)
  - `flows/abc/handover.md` -> re-included (`!/flows/*/handover.md`)
  - `flows/abc/reports/a.md` and `flows/abc/reports/sub/z.md` -> re-included (`!/flows/*/reports/**/*.md`)
  - `flows/abc/reports/z.txt` -> ignored
  - `flows/abc/proposals/x.md` and `proposals/sub/y.txt` -> re-included (`!/flows/*/proposals/**`)
  - Verified.

## 6. The Dictate APK exists and is signed: verified
- `/home/li/android/dictate/dictate-6.4.0-release.apk`, 146145148 bytes; `sha256sum` -> `38e1720bb9b2b5fa84e7e4f92494695faeb1964d8fb6ca0dc7d999867940cae7`, equal to the sha in report.md.
- `nix shell nixpkgs#apksigner -c apksigner verify --verbose --print-certs <apk>` -> `Verifies`, `Verified using v2 scheme (APK Signature Scheme v2): true` (v1, v3, v3.1 and v4 false), `Number of signers: 1`, `Signer #1 certificate DN: CN=Dictate local build`.
- No secret was read. Note the v2-only signature: acceptable for a sideload, but the APK has no META-INF .RSA file, so a v1-only tool (`jarsigner`) would report it unsigned.

## 7. Three pages listed in the open-books record: verified
- `/home/li/primary/flows/book/open-books.datom` exists (11675 bytes). Lines 58-60:
  - EhCN4AbiAbSwKaYDdd5BQZ -> «Ethos says everything of a Nexus but its bodies», `{ Psyche core Opus } Watched`
  - 4euFErf1xs8TyzKVVfi9P9 -> «A Nexus's clients are named for its component», Watched
  - Ez36ykLEoTQFPoScKkQtWr -> «Scratch goes to a temporary directory, for every flow», Watched
- The record file itself is ignored by git (`.gitignore:73 /flows/*/**`), so it is not part of the repository history.
