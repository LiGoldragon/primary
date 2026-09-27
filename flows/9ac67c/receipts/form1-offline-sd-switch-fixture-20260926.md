# Form 1 offline `sd-switch` fixture — 2026-09-26

## Scope and authority

Field Sol's Form 1 route retains the external stable Flow 0.12.2 drop-in. This
receipt is an offline inspection of generated Home unit trees and a disposable
mock attempt. It does not activate Home, contact a user systemd manager, open
Flow or Message stores, contact Herdr, inspect live services or sockets, or
change a profile link.

## Exact inputs

- Home source: `daf026f1e02bcd092f0ecc43b81207c96c6ec1b3`, the remote Home
  main / `flow-0174-stage-56ae53` revision. Its Flow-next source is
  `bc464e5e1b94fcc179af73111f43b69db1f69fc5` (0.17.4).
- Candidate Home generation: `8fx6k2w4q69z61dq3qiqp1rna7g8admb`.
- Reference prior Home generation: `wz9f16mhl9n7r3syc2prjrrh6py5b3w8`.
- The candidate activation script selects `sd-switch` 0.6.4 and passes the
  reference and candidate generated user-unit directories as `--old-units` and
  `--new-units` respectively.

The disposable root was made with `mktemp -d /tmp/form1-sd-switch.XXXXXX`.
The Home source was placed there with `jj -R /git/github.com/LiGoldragon/CriomOS-home workspace add <temporary>/home-src -r daf026f1`.
The fixture copied only both generated `home-files/.config/systemd/user` trees,
then invoked the pinned `sd-switch --force-systemctl --dry-run` with a mock
`systemctl` on PATH. It did not invoke either generation's `activate` script.

## Generated-unit evidence

`cmp` and SHA-256 over the copied trees establish the following:

| Unit | Candidate relation to reference |
| --- | --- |
| `flow-nexus.service` | byte-identical; SHA-256 `8ea9c80d5931aacc5d0421779815c2afb7ab2516c8fa5b64f0da5cd7474a53e8` in both |
| `message-daemon.service` | byte-identical; SHA-256 `72349688a2844c6610ce4eb5f5b3e967dd3c47a96a0cc0e2e93181388e4dc5ac` in both |
| `flow-nexus-next.service` | changed; its `ExecStart` advances from Flow 0.17.1 to Flow 0.17.4 |
| `flow-configuration-next.service` | changed |
| `message-nexus-next.service` | byte-identical |

All three next units already exist in the reference generation. The candidate
therefore does not introduce Message-next as a newly added unit. This receipt
does not infer whether an existing next unit will start or restart.

Neither copied generated tree contains `flow-nexus.service.d`. The fixture's
separate external `flow-nexus.service.d/override.conf` is a regular file at
mode `0640`; its `stat` identity and SHA-256 were equal before and after the
copied-tree exercise. The actual activation's `cleanOldGen` owns only leaves
present in the old generation and `linkNewGen` only leaves present in the new
generation. Static evidence therefore supports that this external path is not
an activation-owned leaf. It is not a runtime precedence witness.

## `sd-switch` limitation

The mock did reach `sd-switch`'s systemctl-based planning probe, but version
0.6.4 requires a fuller `systemctl show` property protocol than the mock
provided. It refused the reply before producing a switch plan. No restart,
stop, start, or no-action claim is made for `flow-nexus.service`,
`message-daemon.service`, or any next unit.

A safe completion needs an isolated user-systemd instance or an independently
validated protocol-complete mock. It must use only copied unit trees and must
record the resulting action plan before a production Home activation is
considered.

## Pending independent Form 1 baseline

Fable directly reports that the unmanaged regular-file stable 0.12.2 drop-in
survived three prior activations over the 0.14.0 generated base, including a
stable restart. Fable also requires capturing and verifying the undeclared
user-profile entry that outranks generated stable 0.14.0 clients. This receipt
did not inspect that live entry; it remains an independent pre-switch baseline
gate.

## Client and socket hard gate

Use only the stable 0.12.2 client for the stable Flow ordinary/meta sockets.
Use Flow 0.17.4 `flow-next` and `flow-next-meta` only for the next Flow
ordinary/meta sockets, and `message-next` / `message-next-meta` only for next
Message sockets. Do not send a 0.17 client to either stable Flow socket:
Fable's reported compatibility witness decodes a 0.17 `List` there as `Stop`.

No production contact occurred during this fixture.
