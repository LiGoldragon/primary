# Chroma corrective proof

The corrective slice keeps the approved D-Bus wire surface intact. Owner loss
now requires `NameOwnerChanged` to remove the registered unique name itself;
releasing a well-known name owned by that client no longer changes its
projection status. Failure reports validate their finite code vocabulary and
byte bound before stale revision handling. Theme revisions reject a real mode
change at `u64::MAX` before persistence, application, or signal publication.

The durable private-bus witness instantiates `ThemeDbusService` and an actual
`ChromaRoot` with a private redb store and fake gamma relay. It covers real
service registration, fixed report shape, validation, sender binding,
second-owner rejection, unrelated-name release, unique-owner disappearance,
full snapshot signal, and service restart. Existing state witnesses reopen
redb and confirm persisted theme revisions.

The witness restarts the exported service, not the complete `chroma-daemon`
process. A full process/service-manager restart is a Home-level integration
responsibility because Home owns service launch and lifecycle; this Chroma
repository proves the protocol and durable store boundary only.

The subsequent Home cross-process witness found startup reconciliation applying
Manual Light over persisted Dark revision 1. Chroma revision
`6a8e4c6a9bb0be0a76baa43b975df91edf6752f9` records whether the theme table
already existed and omits only that initial theme schedule projection. The
private bus test now creates the persisted Dark revision 1 state, starts an
actual root with conflicting Manual Light, invokes the daemon startup schedule,
and observes `RegisterConsumer` return Dark revision 1.

## Sources

- witnesses/chromaCorrectiveProof.md
- flows/01a02b4b/vision/emacsPlugin.md
- flows/01a0238b/vision/emacsPlugin.md
