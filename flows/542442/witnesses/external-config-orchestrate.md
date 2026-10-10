# Orchestrate framed Datom migration witness

Orchestrate main `ac8a92666f4abd8356522c4d52ab23ddcdff4c15` is package 0.30.0.
Its ordinary structural request/reply frames use allocated `(ContractId 1,
revision 4)` and meta frames `(ContractId 2, revision 3)`. The framed socket
witness covers ordinary and meta round trips plus malformed archives, wrong
route, wrong revision, and foreign component bindings before archive decoding.

The persistent representation is schema v2:
`orchestrate_configuration_v2`, `locks_v2`, and `lock_id_allocator_v2`. An
offline genuine v1 fixture with configuration, an active Lock, and allocator 9
migrates atomically. A restart observes the retained configuration and Lock,
the next allocation remains correct, a repeat migration refuses its nonempty
v2 target, and a two-opener witness relies on redb’s native exclusive writable
open. Startup has no runtime v1 compatibility reader.

`orchestrate-store-migrate /absolute/path/to/orchestrate.sema` is the stopped-
daemon offline upgrade command. It preflights input before v2 registration;
existing records remain intact when preflight fails. `UPGRADES.md` distinguishes
this source upgrade from deployment of a running service. The authored
Curriculum Orchestrate skill already has the current inline Datom Lock/Observe
forms, so no skill edit was needed.
