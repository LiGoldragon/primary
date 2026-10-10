# Flow 2e28d8 — disk cleanup planning

Working instruction: Recover the relevant written psyche and current disk state, then form a plan for build-directory cleanup, Nix garbage collection, and removal of old system and user profiles. This prompt creates no psyche record.

Current probe: the root filesystem is 81% used with 171 GiB free; rebuildable repository targets account for about 14 GiB; 36 Home Manager generations and 51 repository result roots may retain substantial Nix closures.

Decision: cleanup is authorized by the living in this flow. Preserve the currently booted system and rollback-capable state, measure before and after each phase, and make any recurring retention policy declarative in CriomOS.
