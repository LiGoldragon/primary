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
The only live-manager read was `systemctl --user show '*' --state
active,activating`, retained solely as the mock's planning-state input.

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

## Exact offline `sd-switch` dry plan

The initial synthetic mock was insufficient: version 0.6.4 requires the full
property shape of `systemctl --user show '*' --state active,activating` before
it will plan. Under the later, explicit read-only authorization, that exact
property stream was captured once from the user manager and replayed only to
the mock. `sd-switch` itself was run only with `--force-systemctl --dry-run`
against copied unit trees; it never contacted the live manager.

The resulting plan is reproducibly:

```text
Stopping units: flow-configuration-next.service, flow-nexus-next.service
Starting units: criomos-ui-priority.service, flow-configuration-next.service,
flow-nexus-next.service, set-SSH_AUTH_SOCK.service
```

The plan names neither `flow-nexus.service`, `message-daemon.service`, nor
`message-nexus-next.service`. It therefore supplies a plan-level no-action
witness for those units under the captured state and these exact unit trees.
It does stop and start `flow-nexus-next.service`.

The affected Nexus executable is candidate `flow-nexus-next.service`, whose
generated `ExecStart` is Flow 0.17.4. `flow-configuration-next.service` is a
oneshot helper that has `After=` and `Requires=` on Flow-next, so the Flow-next
Nexus must be available before its configuration request runs. Message-next is
already active and unchanged, so it has no plan action. The candidate's stable
0.14.0 generated base has no start action in this plan; Fable's retained
external 0.12.2 drop-in is still required to be captured and verified as the
effective stable command before any switch.

The action plan is a model of the captured manager state. A new live baseline
requires a fresh capture and replay; this receipt does not authorize or perform
a live `sd-switch`, restart, stop, or start.

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
