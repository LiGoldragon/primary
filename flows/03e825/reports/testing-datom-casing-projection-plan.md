# Scoped testing-datom-messaging projection plan

This is a pre-installation rendered plan for the two generated skill bodies only. Orchestrate lock `4025` reserves exactly `.agents/skills/testing-datom-messaging/SKILL.md` and `.claude/skills/testing-datom-messaging/SKILL.md` for Flow `03e825`. No installed output has been changed at this stage.

## Input and ownership proof

Primary `flake.lock` still pins Curriculum `99409107f4e62d67644612164db069643d4774fe`. Authored Curriculum main and the real remote both resolve to pushed correction `67ca9ab60a56982b28e51eefaccc0a7efbceed61`. Its source diff in `skills/testing-datom-messaging.md` changes one literal transport spelling, `MACHINE.Relay` to `Machine.Relay`, and nothing else in that file.

The supported `curriculum-deploy` runtime at `/nix/store/6ym1xz0xqs3j43kxsilzdvxi0yk6047f-curriculum-deploy-0.6.3/bin/curriculum-deploy` returned `Generated.{ 66 21 }` for each of two initially empty disposable output roots. The old input was a `git archive` of the exact pinned Curriculum commit into `/tmp/03e825-casing-old-source.Ix0W5N`; it generated `/tmp/03e825-casing-old-output.0dbFtM`. The new input was the clean authored Curriculum checkout at pushed `67ca9ab`; it generated `/tmp/03e825-casing-new-output.CfrW3q`. Generation did not target Primary.

Both installed outputs are byte-equal (`cmp`) to their corresponding old-pinned generated files, establishing their current producer preimage. All four old/installed files have SHA-256 `e3460a13934f19440dd1e2a9c456e0db311d3a094c7df81a46afd1bc49d1a7bd`. Both new generated target files are byte-equal to each other, have mode `0600`, and have SHA-256 `53a7d1fb78a56a7e6bb39cfe883b062ee08aa1e03905874a1a1dd8d1024e7e81`. The rendered target diff is the same single literal change as the authored skill diff.

A full old/new generated-root comparison also finds differences in several generated role files from other Curriculum changes. Those files are outside this request. The global Primary source pin remains old, so full `Check` for a mixed-source Primary projection must not be claimed to pass. File presence or byte equality is projection evidence, not a new active native skill receipt.

## Proposed exact installation

1. Immediately before writes under lock `4025`, re-read the Primary `flake.lock` Curriculum revision, both installed file modes/digests, both new rendered modes/digests, and the lock. Refuse if any preimage differs from the values above.
2. Copy only each corresponding new `SKILL.md` byte-for-byte from `/tmp/03e825-casing-new-output.CfrW3q` to its matching installed target, preserving mode `0600`. If either copy/readback fails, restore both from the old generated root and verify old hashes.
3. Compare the two installed files byte-for-byte with their new rendered source, show the exact two-file working diff, and commit/push only those two files plus this proof report. Verify real remote main and release lock `4025`. Do not run Generate into Primary, change `flake.lock`, other skills, role outputs, sidecars, or active sessions.

## Installed two-file receipt

Parent reviewed the pre-installation plan before mutation. Under lock `4025`, the install re-read the pinned Curriculum revision `99409107f4e62d67644612164db069643d4774fe`, both installed preimages at SHA-256 `e3460a13934f19440dd1e2a9c456e0db311d3a094c7df81a46afd1bc49d1a7bd` and mode `0600`, and both new rendered source files at SHA-256 `53a7d1fb78a56a7e6bb39cfe883b062ee08aa1e03905874a1a1dd8d1024e7e81` and mode `0600`. The generator was the existing `curriculum-deploy-0.6.3` binary at the path named above; its old input was exact pinned Curriculum `99409107`, and its new input was authored pushed `67ca9ab6`.

Only `/home/li/primary/.agents/skills/testing-datom-messaging/SKILL.md` and `/home/li/primary/.claude/skills/testing-datom-messaging/SKILL.md` were atomically replaced from the corresponding new disposable Generate output. Each installed postimage had SHA-256 `53a7d1fb78a56a7e6bb39cfe883b062ee08aa1e03905874a1a1dd8d1024e7e81`, mode `0600`, and byte-for-byte `cmp` equality with its render. The exact two-file diff is one literal `MACHINE.Relay` to `Machine.Relay` replacement in each surface. Primary's global Curriculum pin and every other generated output remain unchanged; no full mixed-source `Check` or active-session skill receipt is claimed.

The scoped installation plus initial report landed as Primary commit `e019307038d904c28ebb453aa95d07e28c123b11`. `jj show --summary` listed exactly the two generated skill paths and this report; `git ls-remote https://github.com/LiGoldragon/Primary.git refs/heads/main` returned that same commit after push. Orchestrate then returned `Released.{ 4025 ... }` for precisely the two installed output paths. This report-only receipt addendum records those completed witnesses; the two generated output bytes were not changed again.

## Sources

- `flake.lock` and `flake.nix`: current pinned Curriculum input and supported runtime wrapper declaration.
- Authored Curriculum revisions `99409107f4e62d67644612164db069643d4774fe` and `67ca9ab60a56982b28e51eefaccc0a7efbceed61`, including the single-file Git diff and remote main readback.
- The two installed Primary `testing-datom-messaging/SKILL.md` preimages and the old/new disposable `curriculum-deploy Generate` outputs listed above; `cmp`, `sha256sum`, `stat`, and `diff -u` provide the byte, digest, mode, and exact-line witnesses.
- `orchestrate 'Observe.Locks'` and `Locked.{ 4025 ... }`: exact current two-path ownership for this installation only.
