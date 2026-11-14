# Flow release inventory — bounded offline audit

Store: `/home/li/primary/.beads/embeddeddolt`, 518 issues. Reads were sequential. No live Nexus, Memory, socket, service, process, queue, or endpoint was probed. This is a bounded keyword/label and named-bead audit, not a corpus-completeness claim.

## Release 0.48

1. Merge full `origin/version-zero-f35668` 0.47, preserving HarnessFlags and typed socket Invocation. Source commits: sockets `34ad165587c204aaba1a1d042c8b651b8aa0a5b6`, workspace `cfc6b2f1d64ed3119c073789e9fe46abcc67dfb3`, diagnostics `c92128e90781d236dcd4271cf4759abcccea10a1`; reviewed tree `7de8e49`; account `/git/worktrees/flow-versionZero-f35668/witnesses/final-account.md`.
2. Apply `primary-vgvi`: canonical `Send.{ Recipient Message }`; no Delivery or compatibility path. Awake sends submit immediately; Hard alone interrupts. Asleep Soft queues; abrupt priority wakes and gives the whole ordered queue in the first prompt once. Outcomes and replay remain typed and truthful for both harnesses.
3. Build one immutable 0.48 source and hand it to independent validation and the Psyche-owned declarative Home deployment. The first release is not gated on unrelated next-version features. Historical 0.47 work does not itself prove the final 0.48 migration or runtime behavior.

Required release beads: `primary-vgvi` (delivery), `primary-vazt` (migration rehearsal), `primary-k8dm` (declared Home service and rollback), `primary-47co` (independent configured validation), and `primary-42mq` (one compiled release line).

## Next version

- Ruling73 Remembering is preserved on `dirty-main-2026-11-04` commit `263bc8c4dd3173c14208c8e27966dfc59b59f318`; witness `/home/li/primary/flows/70a111/witnesses/primary-vgvi/pre-preservation-working.diff`, SHA-256 `d34ae48b1c616cc9457a76c57e899922903aa533eadf4a33f6cdedb1a949b455`. Flow `6043478` is partial; signal `6c65ef5` v30 and meta `81c46ce` v39 belong to the candidate. Bead: `primary-apqz`, related to `primary-x63r`.
- Ruling76 candidates are `origin/repair/refresh-successor-first` `fecbff9` and `origin/worktree/flow-refresh-c27520` `b59f989`; the latter adds repeated-stop no-rewrite coverage. Bead: `primary-fu40`, related to `primary-bie3.2`, `primary-f6g4`, and `primary-9hnn`.
- Codex Retire archives the named thread and ends its owned process while preserving other seats. Bead: `primary-3sg8`; lifecycle mapping precedes implementation.
- `primary-2gkn`: missing-module resilience beyond the diagnostic child.
- `primary-a8f7`: repin consumers to Ethos Zero newtype generator and regenerate.
- `primary-9hnn`: fresh Refresh flow misses queued s5b in its first prompt; cause remains unknown.

These are semantic rebases against the immutable release line, never blind cherry-picks of stale generated contracts.

## Heartbeat

`primary-mne4` is a next-version semantic rebase, not permanently incompatible. Its ruled evidence is: awake/working-known state, accepted ordinary-message admission count, and ordinary queue length; heartbeat’s own effects are excluded. The baseline advances only after the specified successful admission. One outstanding heartbeat coalesces until an existing native receipt or terminal state; no submission is treated as a read and no acknowledgement is invented. Tests cover awake immediate delivery, asleep Soft queueing, abrupt wake batch, failure/Uncertain, and unchanged quiet behavior.

## Other relevant open work

`primary-x63r`, `primary-bie3.2`, `primary-f6g4`, `primary-18yv`, `primary-ngdd`, `primary-8mee`, `primary-7f3y`, and externally blocked `primary-hbhi` remain open. Older release beads may overlap newer acceptance and are not silently closed.

## Gates and exclusions

- VersionZero historical configured comparisons do not prove the final runtime/state/rollback. Migration proof uses immutable 0.48 source, an isolated synthetic root, configured open plus private startup, typed manifest comparison, completed call-key outcome preservation, and narrowly labelled pre-effect rollback.
- No live access or deployment occurs here. Deployment belongs to Psyche through the declared CriomOS-home `flow-nexus` unit.
- Preserve historical branches and worktrees. No deletion occurs without proof.
- The separate version-one effort runner `8cc6292` is not a Flow release candidate.
