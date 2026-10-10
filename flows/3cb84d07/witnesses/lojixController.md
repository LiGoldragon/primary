# Lojix controller

Method: probe local `systemctl show lojix-daemon`; `systemctl cat lojix-daemon`;
`ls -l /run/lojix`; `LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix
'Query.ByNode.(goldragon zeus None)'`; the same query for `ouranos`; and
`Query.ByEventLog.(1 40)`.

Observed:

- The Ouranos daemon is Lojix 0.17.5, active since 2026-08-19, with daemon
  host `ouranos`, ordinary socket `/run/lojix/ordinary.sock`, owner socket
  `/run/lojix/owner.sock`, state `/var/lib/lojix`, 2700-second effect timeout,
  and production `NoTestDefaults`.
- `Query.ByNode.(goldragon zeus None)` returns `Queried.([] [] (625 625))`.
- `Query.ByNode.(goldragon ouranos None)` returns current CompleteHost
  generation 7 and current UserEnvironment generation 27; its event log is
  at commit sequence 625.
- The event-log page contains only Ouranos deployment events. It includes
  earlier failed stages such as `FlakeAuth`, `Build`, `CopyClosure`, and
  `Activate`, and successful terminal records, but no Zeus event.
- `CheckHostKeyMaterial.(goldragon zeus /git/github.com/LiGoldragon/goldragon/datom.dotos)`
  returns `KeyMaterialChecked.(zeus [] (625 625))`.

Inference: this daemon's durable state has no committed Zeus generation or
deployment. The successful empty key-material report is not a live Zeus key
proof: the checked source's `check_key_material` implementation returns an
empty vector and the current marker without inspecting a target.
