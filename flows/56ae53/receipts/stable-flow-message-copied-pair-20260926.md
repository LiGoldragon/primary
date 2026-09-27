# Stable Flow and Message copied-pair witness

Captured 2026-09-26 in the `America/Mexico_City` local timezone by Mind Sol 56ae53. The capture only read the live stores and copied their bytes to the isolated receipt directory. It did not stop, restart, quiesce, configure, or otherwise write to either live service, its socket, or its original store.

## Sources and copies

| Store | Live source | Isolated copy | Size (bytes) |
| --- | --- | --- | ---: |
| Flow | `/home/li/.local/state/flow/flow.sema` | `/home/li/.local/state/secondary-56ae53/stable-pair-20260926T1824-0600/flow.sema` | 1056768 |
| Message | `/home/li/.local/state/message/messenger.sema` | `/home/li/.local/state/secondary-56ae53/stable-pair-20260926T1824-0600/message.sema` | 180224 |

The containing copy directory has mode `0700`. The copy files retain their original mode and timestamp but have distinct inodes.

## Pre, copy, and post evidence

| Store | Phase | SHA-256 | Size | Inode | mtime epoch |
| --- | --- | --- | ---: | ---: | ---: |
| Flow | pre | `f03f610a9832378ef0f03fee16383266909d923051ccb5a71980cc9db78c0f03` | 1056768 | 52451029 | 1790468530 |
| Flow | copy | `f03f610a9832378ef0f03fee16383266909d923051ccb5a71980cc9db78c0f03` | 1056768 | 52694455 | 1790468530 |
| Flow | post | `f03f610a9832378ef0f03fee16383266909d923051ccb5a71980cc9db78c0f03` | 1056768 | 52451029 | 1790468530 |
| Message | pre | `4cb4e9ba3544a12afcb2d1771bfd67eb93e74d9aa6b898ba6251036061719457` | 180224 | 54657027 | 1790461893 |
| Message | copy | `4cb4e9ba3544a12afcb2d1771bfd67eb93e74d9aa6b898ba6251036061719457` | 180224 | 52697435 | 1790461893 |
| Message | post | `4cb4e9ba3544a12afcb2d1771bfd67eb93e74d9aa6b898ba6251036061719457` | 180224 | 54657027 | 1790461893 |

Final source and copy reads matched the same hashes, sizes, inodes, and mtimes. `flow-nexus.service` and `message-daemon.service` were both `active` at that final read.

## Registry consistency

A read-only `flow 'List.{}'` answered from the stable live Flow service. It contained 25 top-level flow rows. This is a visual top-level row count: a token-level regular expression is unsuitable because nested predecessor rows share the same identifier shape and overcounts them.

## Result and boundary

Evidence grade: direct copied-pair proof. Both copies equal the respective original before and after their copy operations, and the originals remained live.

No isolated target-binary read was performed. The visible stable Flow client is `0.12.2`; the target Flow 0.14 daemon executable was not resolved locally. The visible Message 0.14 client exposes no demonstrated alternate-store and alternate-socket launch contract. Launching either target therefore could not be proven isolated from live stores and sockets. This witness stops at the copied pair.

Follow-up package inspection established a narrower Message contract: the exact
`message-daemon` 0.14 binary is installed at
`/nix/store/i66j8l0vk6i3bhd0r968dbm7ckllnryf-message-0.14.0/bin/message-daemon`
and requires an external binary configuration file. Its Home source contract
can supply a configuration whose store and sockets are isolated. The matching
Flow target remains unavailable: `flow`, `flow-nexus`, and `flow-meta` all
resolve to the installed 0.12.2 closure. A paired 0.14 target-read therefore
remains unproven. The Message copy was not opened alone.

## Separate read-only process observation

At observation, Astra's existing PID `416817` was still a running `timeout 900 nix flake check --no-build ...`; child PID `416819` was still its running `nix flake check --no-build ...` process. No process was started, stopped, signalled, or retried.

One post-deadline status read at `2026-09-26T22:01:44-0600` found both PIDs
absent. This records terminal absence only; it does not establish the check's
exit status because its stdout and stderr were attached to `/dev/pts/15` and no
file-backed log was available to this witness.
