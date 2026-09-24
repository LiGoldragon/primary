# Prepared Mind Sol successor packet

This directory is a launch-ready input packet. It does not record a launch.

`profile.json` is the human-readable typed profile. `launch-request.datom` is
the exact one-argument Flow request derived from it. `startup-handoff.md` is
the only source body appended to the composed first prompt; it points the new
seat to the predecessor summary without copying its large identifiers or
implementation history. The launcher resolves and expands the ordered skills
through the native Codex skill interface.

Run the command in `manifest.json` only after every launch gate there passes.
The deployed Flow Nexus must route `gpt-6-sol` through the next Codex client,
home, socket, and transcript root as one coherent endpoint. The first turn is
launcher receipt only. Identity, title, route, handoff, and later retirement
remain distinct witnessed stages.
