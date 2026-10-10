# Flow-next shadow repair — 2026-09-27

## Authority and lock

- Bounded Field operation authorized by Flow `9ac67c`: move aside only stale,
  unmanaged `~/.local/bin` Flow-next client shadows. No service, Home, stable
  Flow, or model action was requested or taken.
- Fresh `orchestrate 'Observe.Locks'` found no lock claiming either exact path.
  Lock `8419` was then granted as
  `FlowNextShadowRepair`, owner `9ac67c`, for exactly the two paths.

## Pre-mutation witness

| Path | Kind and provenance | Inode | SHA-256 | Finding |
| --- | --- | ---: | --- | --- |
| `/home/li/.local/bin/flow-next` | `li:users`, regular, `0755`, 170-byte wrapper to `/nix/store/9gf2j799wgxbp0vw6fidg9898mbxpz1p-flow-0.17.0/bin/flow` and the next socket | 53346421 | `89a9540c9c27316a0ef1da4931e3d824c3f1d03acd73e8ebe27fa23ae079f5ca` | unmanaged stale shadow |
| `/home/li/.local/bin/flow-next-meta` | `li:users`, regular, `0755`, 185-byte wrapper to `/nix/store/9gf2j799wgxbp0vw6fidg9898mbxpz1p-flow-0.17.0/bin/flow-meta` and the next meta socket | 53346425 | `435e51023a87525cb1193a2d3e305f8b4ae86236b6926517d1ef8cb14429239e` | unmanaged stale shadow |

The managed `/home/li/.nix-profile/bin/flow-next` and
`/home/li/.nix-profile/bin/flow-next-meta` are `root:root`, regular `0555`
Home Manager wrappers to Flow `0.17.1`. Before repair, `~/.local/bin` appeared
first in `PATH`, so both stale wrappers masked those managed clients.

The running next service was already `flow-nexus-next.service`, active/running,
PID `90750`, executable Flow `0.17.1`; its next Flow and meta sockets existed.
Stable `flow-nexus.service` was active/running, PID `1937`, executable Flow
`0.12.2`.

## Reversible mutation

After rechecking each source inode and hash immediately before the operation,
each exact source path was renamed in place with `mv --no-clobber` at
`20260927T085436Z`. The original paths are absent and no file was deleted or
overwritten.

| Original | Backup | Preserved inode and SHA-256 |
| --- | --- | --- |
| `/home/li/.local/bin/flow-next` | `/home/li/.local/bin/flow-next.flow-0170-shadow-9ac67c-20260927T085436Z.bak` | `53346421`; `89a9540c9c27316a0ef1da4931e3d824c3f1d03acd73e8ebe27fa23ae079f5ca` |
| `/home/li/.local/bin/flow-next-meta` | `/home/li/.local/bin/flow-next-meta.flow-0170-shadow-9ac67c-20260927T085436Z.bak` | `53346425`; `435e51023a87525cb1193a2d3e305f8b4ae86236b6926517d1ef8cb14429239e` |

Rollback, if later authorized:

```sh
mv -- /home/li/.local/bin/flow-next.flow-0170-shadow-9ac67c-20260927T085436Z.bak /home/li/.local/bin/flow-next
mv -- /home/li/.local/bin/flow-next-meta.flow-0170-shadow-9ac67c-20260927T085436Z.bak /home/li/.local/bin/flow-next-meta
```

## Post-mutation verification

- A fresh clean interactive `zsh` resolved both names to
  `/home/li/.nix-profile/bin/{flow-next,flow-next-meta}`.
- `flow-next --version` and the explicit managed client both reported
  `flow 0.17.1`.
- `flow-next-meta --version` is not implemented by the managed Flow `0.17.1`
  binary: it returned its usage and exit `2`. No alternative meta invocation
  was used, honoring the version-only constraint. Its managed wrapper target
  was already directly witnessed as Flow `0.17.1`.
- The explicit managed Flow-next client, with only
  `FLOW_SOCKET=/run/user/1001/flow-next/flow/flow.sock`, completed `List.{}`
  successfully (exit `0`) and listed five next records: `93ba9f`, `b7ba00`,
  `c56100`, `dc53b4`, and `e167d8`. Stable Flow was never queried.
- Stable `flow-nexus.service` remains PID `1937`, Flow `0.12.2`, with stable
  socket inode `68`, mode `0600`, mtime `2026-09-26 16:19:37 -0600`.
  Next remains PID `90750`, Flow `0.17.1`, next socket inode `3382`, mode
  `0600`, mtime `2026-09-26 17:38:33 -0600`.
- No Home activation was invoked. `/home/li/.nix-profile` still points through
  `.nix-profile-8-link` to `/nix/store/f4dpffqhkpiai6f3gcj5szszy869raa4-profile`
  (link mtime `2026-09-23 09:48 -0600`).
