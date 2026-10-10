# Mirror restore — `signal-repository-ledger` and `repository-ledger`

Subflow of main flow f6db8d, thread `f6db8d14-1dfe-472d-914e-9c441f852834`,
2026-09-11/12. Task: `reports/push-verification.md` discrepancies D1–D3.
Everything below is witnessed by this subflow on this host unless marked
relayed.

## Occasion

`push-verification.md` found three things about these two repositories,
each of which has two git remotes — `origin` (`gitolite@localhost`, a
mirror) and `github` (GitHub):

- **D3**: `nota-pins.md` claimed that a first `jj git push --bookmark main`
  moved `signal-repository-ledger`'s mirror `main` sideways onto the
  local-only divergent commit, and that "it was immediately repointed to
  the intended revision." Witnessed by `push-verification.md`: the mirror's
  `main` was still standing on `9d267c27` (the `f6db8d-nota-pins` branch
  revision), not repointed, and GitHub's `main` (`894335a0`) is not an
  ancestor of it. GitHub itself was untouched.
- **D2**: `repository-ledger`'s `f6db8d-cargo-update` branch
  (`0c9bd81bde7b`, claimed pushed by `cargo-update-tier0.md`) reached only
  the mirror; GitHub's ref list for the repository never carried it.
- **D1**: `nota-pins.md` and `cargo-update-tier0.md` both named
  `repository-ledger`'s `main@origin` (the mirror, `4153fd84`) "the pushed
  authority" and called GitHub's `main` (`0580eff4`) local-only —
  inverted: `origin` there is the mirror, not GitHub.

## Which remote is authoritative

`/home/li/primary/SKILL_VARIABLES.md` was read in full: it defines
`Repository root: /git` and names several GitHub repositories (Curriculum,
standards, CriomOS, CriomOS-home) but has no entry for `gitolite`, a
mirror, or which remote is authoritative between the two.

`Vision/`, `vision-raw/`, and `flows/*/vision/` were searched (`grep -rniE
"gitolite|mirror"`) for any ruling. No hit names `gitolite` or a git
mirror's authority; the four `mirror` hits found are unrelated uses of the
word (ethos type-mirroring, an identity-mirror question to the psyche, an
architecture doc's "mirrored by ethos-monolith"). **No skill variable and
no Vision entry rules on which of `origin` (gitolite mirror) or `github`
(GitHub) is authoritative for these repositories.** This subflow proceeded
on the brief's own instruction — restore the mirror, leave GitHub
untouched, push the f6db8d branches to GitHub as well — without resolving
that open question, which is outside this subflow's scope.

## Orchestrate locks

`orchestrate 'Observe.Locks'` before touching either repository: no lock
held any path under `/git/github.com/LiGoldragon/signal-repository-ledger`,
`/git/github.com/LiGoldragon/repository-ledger`, or
`/git/github.com/LiGoldragon/meta-signal-repository-ledger`.

Acquired:

- `orchestrate 'Lock.{ MirrorRestoreSignalRepositoryLedger f6db8d [ /git/github.com/LiGoldragon/signal-repository-ledger ] "Restore mirror main after sideways move and push nota-pins branches to GitHub" }'` → **Locked 1202**.
- `orchestrate 'Lock.{ MirrorRestoreRepositoryLedger f6db8d [ /git/github.com/LiGoldragon/repository-ledger ] "Push cargo-update branch to GitHub remote" }'` → **Locked 1203**.

Released after all writes: `orchestrate 'Release.1202'` → `Released`;
`orchestrate 'Release.1203'` → `Released`.

`meta-signal-repository-ledger` was not locked: its `origin` remote is
itself `git@github.com:LiGoldragon/meta-signal-repository-ledger.git` (no
gitolite mirror exists for it), and both its remotes already carried
`f6db8d-nota-pins` at `0c2da541` and `main` at `977c9e9b` before this
subflow touched anything — confirmed by `git ls-remote origin` and `git
ls-remote github` both returning identical output. No write was needed or
made there.

## What was read, what was written, in order

1. Read `push-verification.md` and `nota-pins.md` for the claimed and
   actual revisions (relayed above).
2. In `/git/github.com/LiGoldragon/signal-repository-ledger`: read
   `git reflog show refs/remotes/origin/main`. Entry `@{0}` is `9d267c27`
   (the sideways move, `update by push`); entry `@{1}` is `894335a0`
   (`update by push`) — the mirror `main` immediately before tonight's
   move, and identical to GitHub's untouched `main`. This is the local
   checkout's own reflog for its `origin` remote-tracking ref, the
   strongest evidence available (the mirror's own server-side reflog was
   not reached; this subflow has no other access to it).
3. Read `git ls-remote origin` and `git ls-remote github` in each of the
   three repositories — the "before" tables below.
4. Wrote, in `signal-repository-ledger`:
   - `git push origin 894335a074f3dad8b99b540439ba831a8d1f46d1:refs/heads/main --force-with-lease=refs/heads/main:9d267c275df7d2f9db800196465a7dd50ec38623`
     — restored the mirror's `main` to exactly what it was before tonight
     (`894335a0`, "docs: restore Protos estate status"), the same commit
     GitHub's `main` already carries. The lease pinned the expected old
     value so the push would fail rather than clobber an unexpected state;
     it succeeded, forced (non-fast-forward, since the sideways commit is
     not an ancestor of `894335a0`).
   - `git push origin 9d267c275df7d2f9db800196465a7dd50ec38623:refs/heads/f6db8d-nota-pins`
     — new branch on the mirror; GitHub already carried this branch at the
     same revision (`push-verification.md`'s `**EXACT**` row), so this
     write makes both remotes carry it, as the brief asked.
5. Wrote, in `repository-ledger`:
   - `git push github 0c9bd81bde7bdf7628c03c96a46217033620a653:refs/heads/f6db8d-cargo-update`
     — new branch on GitHub; the mirror already carried it (D2). `main` on
     both remotes was left untouched — the pre-existing divergence
     (mirror `4153fd84` vs. GitHub `0580eff4`) was not resolved, per the
     brief.
6. Read `git ls-remote origin` and `git ls-remote github` again in both
   repositories — the "after" tables below.

No repository was fetched into beyond what each checkout already held
(every revision pushed was already present locally, verified with `git
cat-file -e` before pushing).

## Before / after `git ls-remote`

### signal-repository-ledger

**Before**

`origin` (mirror, `gitolite@localhost:signal-repository-ledger`):
```
edabdd4a5f5d4316a807ef195a0d6937ae57c2a5	refs/heads/drop-next
9d267c275df7d2f9db800196465a7dd50ec38623	refs/heads/main
```

`github` (`git@github.com:LiGoldragon/signal-repository-ledger.git`):
```
894335a074f3dad8b99b540439ba831a8d1f46d1	HEAD
9d267c275df7d2f9db800196465a7dd50ec38623	refs/heads/f6db8d-nota-pins
894335a074f3dad8b99b540439ba831a8d1f46d1	refs/heads/main
```

**After**

`origin` (mirror):
```
edabdd4a5f5d4316a807ef195a0d6937ae57c2a5	refs/heads/drop-next
9d267c275df7d2f9db800196465a7dd50ec38623	refs/heads/f6db8d-nota-pins
894335a074f3dad8b99b540439ba831a8d1f46d1	refs/heads/main
```

`github`:
```
894335a074f3dad8b99b540439ba831a8d1f46d1	HEAD
9d267c275df7d2f9db800196465a7dd50ec38623	refs/heads/f6db8d-nota-pins
894335a074f3dad8b99b540439ba831a8d1f46d1	refs/heads/main
```

`main` now agrees between the mirror and GitHub at `894335a0`, and both
remotes carry `f6db8d-nota-pins` at `9d267c27`. `drop-next` (mirror-only,
pre-existing, untouched) is unrelated to tonight's work and was left as
found.

### repository-ledger

**Before**

`origin` (mirror, `gitolite@localhost:repository-ledger`):
```
9bd2a2669f67a7ac7d7f5754c36777480d261326	refs/heads/drop-next
97469580a875a6ba5a088a9b0d8bba0b713bb128	refs/heads/durable-ledger-retention
0c9bd81bde7bdf7628c03c96a46217033620a653	refs/heads/f6db8d-cargo-update
4153fd848c699807822d3f491604828451a1110d	refs/heads/main
33dc91bf53a1c155695802022722a658022d63e8	refs/heads/repository-ledger-os-update-2026-07-08
```

`github` (`git@github.com:LiGoldragon/repository-ledger.git`):
```
0580eff46139aa45a0861b0f03bf3f0d9e6ace2d	HEAD
0580eff46139aa45a0861b0f03bf3f0d9e6ace2d	refs/heads/main
33dc91bf53a1c155695802022722a658022d63e8	refs/heads/repository-ledger-os-update-2026-07-08
```

**After**

`origin` (mirror): unchanged —
```
9bd2a2669f67a7ac7d7f5754c36777480d261326	refs/heads/drop-next
97469580a875a6ba5a088a9b0d8bba0b713bb128	refs/heads/durable-ledger-retention
0c9bd81bde7bdf7628c03c96a46217033620a653	refs/heads/f6db8d-cargo-update
4153fd848c699807822d3f491604828451a1110d	refs/heads/main
33dc91bf53a1c155695802022722a658022d63e8	refs/heads/repository-ledger-os-update-2026-07-08
```

`github`:
```
0580eff46139aa45a0861b0f03bf3f0d9e6ace2d	HEAD
0c9bd81bde7bdf7628c03c96a46217033620a653	refs/heads/f6db8d-cargo-update
0580eff46139aa45a0861b0f03bf3f0d9e6ace2d	refs/heads/main
33dc91bf53a1c155695802022722a658022d63e8	refs/heads/repository-ledger-os-update-2026-07-08
```

`f6db8d-cargo-update` now exists on both remotes at `0c9bd81b`. `main`
divergence between the mirror (`4153fd84`) and GitHub (`0580eff4`) is
**left exactly as found**, per the brief — both heads are recorded above,
neither was repointed, merged, or rebased.

### meta-signal-repository-ledger (unchanged, recorded for completeness)

`origin` and `github` are the same URL
(`git@github.com:LiGoldragon/meta-signal-repository-ledger.git`) — no
gitolite mirror exists for this repository. Both, before and after:
```
977c9e9b8dad0e477316c1a0351dff1242a1e632	HEAD
0c2da541ccb65217cb5b112b85e3790bac0e9293	refs/heads/f6db8d-nota-pins
977c9e9b8dad0e477316c1a0351dff1242a1e632	refs/heads/main
```

## Possible causes, for the record

The sideways move D3 describes (`jj`'s default push target repointing the
mirror's `main` and the report claiming a repoint that did not happen) most
plausibly happened one of two ways: either the repointing `jj git push`
in `nota-pins.md`'s own session targeted the wrong bookmark or remote and
the subflow did not re-verify with `git ls-remote` afterward (its method
note says landed revisions elsewhere in the same flow *were* re-verified
this way, but the mirror-repoint step is not shown being re-verified); or
a second, unlogged push after the repoint moved `main` again, sideways,
without being recorded. Either is consistent with the evidence; this
subflow did not find data to distinguish them, and neither changes the
restore performed here.

## Sources

- `/home/li/primary/flows/f6db8d/reports/push-verification.md` and
  `/home/li/primary/flows/f6db8d/reports/nota-pins.md` — read for the
  claims and discrepancies D1–D3; every claim above attributed to them is
  relayed, not witnessed by this subflow.
- `/home/li/primary/SKILL_VARIABLES.md` — read in full; no `gitolite` or
  mirror-authority entry found.
- `grep -rniE "gitolite|mirror" Vision/ vision-raw/ flows/*/vision/` — run
  by this subflow; no ruling on mirror/GitHub authority found among the
  hits.
- `git reflog show refs/remotes/origin/main`,
  `git ls-remote origin`, `git ls-remote github`, `git cat-file -e`,
  `git log` — run by this subflow in
  `/git/github.com/LiGoldragon/{signal-repository-ledger,repository-ledger,meta-signal-repository-ledger}`,
  read-only except the two `git push` writes recorded above.
- `git push origin 894335a0…:refs/heads/main --force-with-lease=…`,
  `git push origin 9d267c27…:refs/heads/f6db8d-nota-pins`,
  `git push github 0c9bd81b…:refs/heads/f6db8d-cargo-update` — the three
  writes this subflow made, all witnessed by their own command output and
  the "after" `git ls-remote` tables above.
- `orchestrate 'Observe.Locks'`, `orchestrate 'Lock...'` (1202, 1203), and
  `orchestrate 'Release...'` (1202, 1203) — witnessed by this subflow
  against the live Nexus.
