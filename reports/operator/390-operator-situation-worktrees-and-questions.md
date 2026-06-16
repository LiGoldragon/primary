# Operator Situation, Worktrees, And Questions

## What I did

I reviewed the new Spirit-adjacent designs, checked the current source state, ran
focused Spirit tests, and cleaned local worktrees that were both clean and already
merged into their repo's `main`.

I did not delete unmerged or dirty worktrees. I also did not reset canonical
`/git` checkouts while producing this report, because several are currently being
used as structural integration staging checkouts.

## Worktrees removed

These were clean local worktrees whose parent commit was already contained in
their repo's `main`. Only local worktree directories were removed; bookmarks and
remote history were not deleted.

| Removed path | Why |
|---|---|
| `/home/li/wt/github.com/LiGoldragon/spirit-resolve-clarification` | merged to `spirit` main at `4fce1c5f` (`spirit: migrate mixed schema ten production stores`) |
| `/home/li/wt/github.com/LiGoldragon/signal-spirit-resolve-clarification` | merged to `signal-spirit` main at `019a1330` (`signal-spirit: publish schema directory metadata`) |
| `/home/li/wt/github.com/LiGoldragon/meta-signal-spirit-resolve-clarification` | merged to `meta-signal-spirit` main at `c917b865` (`meta-signal-spirit: publish schema directory metadata`) |
| `/home/li/wt/github.com/LiGoldragon/schema-next/schema-cc-integration` | schema-cc integration is on `schema-next` main at `caa77971` |
| `/home/li/wt/github.com/LiGoldragon/nota-next/structural-forms-integration` | branch bookmark and main both pointed at `f9155de5` |
| `/home/li/wt/github.com/LiGoldragon/sema-engine/engine-decomposition` | contained in `sema-engine` main |
| `/home/li/wt/github.com/LiGoldragon/sema-engine/rebuild-from-log` | contained in `sema-engine` main |
| `/home/li/wt/github.com/LiGoldragon/sema-engine/record-key-sum` | contained in `sema-engine` main |
| `/home/li/wt/github.com/LiGoldragon/sema-engine/single-writer-internal-lock` | contained in `sema-engine` main |
| `/home/li/wt/github.com/LiGoldragon/spirit/store-decomposition` | contained in `spirit` main |
| `/home/li/wt/github.com/LiGoldragon/spirit/vc-followups` | contained in `spirit` main |
| `/home/li/wt/github.com/LiGoldragon/triad-runtime/generic-reaction-frame` | contained in `triad-runtime` main |
| `/home/li/wt/github.com/LiGoldragon/triad-runtime/structural-forms-integration` | branch bookmark and main both pointed at the same integrated commit |

## Current canonical checkout situation

The canonical `/git` checkouts are not all sitting on `main`:

| Repo | Current checkout parent | Situation |
|---|---|---|
| `spirit` | `1cd4b357` on `main` | clean; includes public intent render client |
| `schema-rust-next` | `9ffa588d` on `main` | clean |
| `nota-next` | `f9155de5` on `main` and `structural-forms-integration` | clean |
| `sema-engine` | `1afcd012` on `main` | clean |
| `schema-next` | `b7af872e` on `structural-forms-integration` | clean but not main |
| `signal-spirit` | `4f024d9f` on `structural-forms-integration` | clean but not main |
| `meta-signal-spirit` | `4484c3a9` on `structural-forms-integration` | clean but not main |

This matters because an operator expecting `/git/.../signal-spirit` to be main
will be looking at the structural branch. My lean is to reset canonical `/git`
checkouts back to main when not actively integrating, and keep branch state under
`/home/li/wt`. I did not do that reset in this pass because the psyche asked for
reports and cleanup, not a checkout-state intervention.

## Remaining Spirit-adjacent worktrees

| Worktree | State | Why it stays |
|---|---|---|
| `schema-next/structural-forms-integration` | clean, unmerged | positional struct-body syntax and retired-syntax rejection; still not on main |
| `schema-next/typeref-structural-generics` | clean, unmerged | older TypeReference/positional line; needs reconciliation or explicit retirement |
| `schema-rust-next/structural-forms-integration` | dirty, unmerged | structural branch working copy has fixture/emitter changes |
| `schema-rust-next/family-identity-newtype` | clean, unmerged | implements the `SchemaHash` newtype emission idea; not on main |
| `signal-spirit/structural-forms-integration` | dirty, unmerged | positional schema migration branch; not safe to delete |
| `meta-signal-spirit/structural-forms-integration` | dirty, unmerged | positional schema migration branch; not safe to delete |
| `spirit/structural-forms-integration` | dirty, unmerged | positional schema migration branch; not safe to delete |
| `nota-next/named-field-structural-derive` | clean, unmerged | universal-positional prototype line; not on main |
| `sema-engine/structural-forms-integration` | clean, unmerged | structural integration branch; not on main |
| `spirit/mirror-shipper` | clean, unmerged | mirror production is blocked by ingress/auth posture, so this stays parked |
| `criome/criome-auth-pilot` | clean, unmerged | criome crypto/auth pilot, relevant to Spirit attestation but not production-ready |

There are also non-Spirit or older branch worktrees still present, including
Horizon, Lojix, pipe-delimiter, and reaction-expand lines. I left them alone
unless they were clearly merged and clean.

## Legacy raw-git-looking directories

Some directories under `/home/li/wt` have `.git` files but are not readable as jj
repos from their root, for example:

- `/home/li/wt/github.com/LiGoldragon/CriomOS-home/next`
- `/home/li/wt/github.com/LiGoldragon/CriomOS/next`
- `/home/li/wt/github.com/LiGoldragon/chroma/next`
- `/home/li/wt/github.com/LiGoldragon/mirror/arc-shipper`

I did not inspect these with raw git because the workspace contract says version
control is `jj` except for named escape hatches. They need a separate cleanup pass
if we want to retire legacy raw-git worktrees.

## Open operator questions

1. Should I reset the canonical `/git` checkouts for `schema-next`,
   `signal-spirit`, and `meta-signal-spirit` back to `main` now, leaving
   structural branch state only in `/home/li/wt`?

2. For `ResolveClarification`, should v0 require explicit target record changes,
   with target auto-discovery only as a CLI/helper suggestion? My recommendation
   is yes.

3. For private capture, is the name `RecordPrivate` acceptable, and should it set
   `Privacy Minimum` by default? My recommendation is `RecordPrivate` plus
   `Minimum` unless the named ritual is intended to mean a stronger privacy rung.

4. Should the structural positional stack land to all mains before the
   family/stream universal positional work (`primary-hhp0`), or should `hhp0` be
   folded into that same final cascade? My recommendation is one cascade: finish
   `hhp0`, then land the structural stack once.

5. Should `spirit-render` be allowed to generate or refresh per-repo `INTENT.md`
   files during the transition, or should it only emit sidecar/generated reports
   until the Spirit-only contract is fully updated?
