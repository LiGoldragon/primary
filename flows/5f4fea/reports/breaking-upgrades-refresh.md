# Item29 breaking-upgrades refresh witness

Status: proposal and read-only witness; no deployment or activation occurred.

## Curriculum source

The approved four lines were applied exactly from Curriculum proposal commit
`5f8c389504ff22ea705cf1e3c1c04152b44499a1` onto remote Curriculum main:
`0a622756342a9dc0b6157043b01bd8027aa6c4c7`. The real remote
`refs/heads/main` matched `0a622756342a9dc0b6157043b01bd8027aa6c4c7`.

## Regeneration

Exact command, run from `/git/github.com/LiGoldragon/curriculum-deploy`:

```text
nix run .#default -- 'Generate.{ «/tmp/curriculum-item29b» «/home/li/wt/primary-5f4fea» }'
```

Exact output: `Generated.{ 44 21 }`.

Only these generated projections were staged in Primary:
`.agents/skills/breaking-upgrades/SKILL.md` and
`.claude/skills/breaking-upgrades/SKILL.md`. Primary commit:
`2219d9160798dd59017ae8a953dacc6c0c7d9f1c`; remote
`git@github.com:LiGoldragon/primary.git` `refs/heads/flow/5f4fea` was verified
at that revision. The generator also noticed an unrelated Nexus projection;
it was left unstaged.

## Native read-only witness

Exact command, run with cwd `/home/li/wt/primary-5f4fea`:

```text
timeout 180s codex exec --ephemeral -m gpt-5.6-luna -s read-only -C /home/li/wt/primary-5f4fea -o /tmp/item29-luna.txt '$breaking-upgrades Plan the Zeus CriomOS update. State the countdown rollback target, timeout, cancellation witness, and remote-access condition. Do not deploy or edit files.'
```

Native session: `01a0a6bd-298b-7073-bfdb-5101145e7212`; exit 0; configured
model witness `gpt-5.6-luna`; native skill input was `$breaking-upgrades` and
its generated file was present in this isolated worktree. The response stated:

* rollback target is the exact pre-upgrade Zeus boot generation/stack captured
  before activation;
* the cancellation witness is an independent watch flow on another host;
* cancellation requires network connectivity and an actual remote login/session
  to Zeus on the new stack;
* the countdown remains armed until that witness succeeds.

The response proposed a 15-minute timeout. That duration is model output only;
it is not an approved living value. The native response also reported no local
`UPGRADES.md` and made no edits or deployment.
