# References: Nothing is installed by hand

Paths are under /home/li/primary/flows/379e7a/. Base modules read at origin/main: psyche-context 2d9fbb6, mind-context 698ef6d, field-context ed08a8d.

## Proposals

- Proposals 1 and 2: the composed brief, wording kept. Placement checked against psyche-context origin/main vision/criomos.md: both lines enter under "## CriomOS" directly after line 8, "CriomOS is a declarative operating system: nobody edits a file on a host."
- Figure: the composed brief's ASCII, kept as sent; drawn by the Illustrator.
- Case: psyche-context vision/criomos.md, vision/deployment.md, vision/nix-builds.md and mind-context knowledge/lojix.md, each shown whole without front matter. No knowledge module on CriomOS-home exists in mind-context or field-context (grepped for CriomOS-home, local/bin, nix profile, hotfix, runtime mutation, install, systemctl, symlink, shim, workaround). knowledge/lojix.md lines 381-383 (Placement) are a knowledge statement, not compensation, and are left.
- Proposals 3 and 4 (alternatives): compensation/operating-system.md line 12. The audit (audit-undeployed-vision.md, row K3) cites it as line 14 at field-context 785ceb0; at ed08a8d it is line 12. Audit row K15 names line 6 as a restatement of criomos.md:8; at ed08a8d line 6 reads "Before debugging installed software, update it to its latest release.", which is not a restatement, so it is left.
- Proposal 5: compensation/update.md line 14 (audit row K1); only the preserving and no-restart sentences are removed. The audit also names the whole stable/Next procedure; the rest stays because nothing in the vision speaks to the rotation of channels.
- Proposal 6: compensation/agent-harness-packaging.md lines 10 and 16 (the audit lists the module as supporting vision; here the two lines repeat Proposal 1 and are leaned out).
- Proposal 7: compensation/nix-workflow.md line 12. Audit row K15 names line 20 as the duplicate of nix-builds.md; at ed08a8d the module has 18 lines and no such line.

## Examined and left

- compensation/design.md "General repositories keep no setup-specific host value or script.": it says what a general repository contains, not how a program reaches a host; Proposals 1 and 2 do not make it unnecessary.
- compensation/network-temporary.md line 8 (NetworkManager checkpoint rollback; audit K2): a temporary arrangement, which no vision line here speaks to; removing it would be a broader rule than the case gives.
- compensation/temporary.md (K14), messenger-clj.md, main-flow.md, launch.md, primary-commit.md (K4-K13): concern messaging, launching, committing or builders, not installation.
- compensation/orders.md "Deploy means the intended system and user environment now." supports the vision.
- compensation/documentation-placement.md "Put temporary workarounds and their proper fix in NON_IDEAL_AGENTS.md.": records a workaround, does not permit installing one; left.

## Method

- book-check: tools/book-check.mjs.
- Host findings that bear on the case (hand links in ~/.local/bin, imperative nix profile, hand-linked user units) are in audit-undeployed-vision.md section 1; none is shown in the book.
