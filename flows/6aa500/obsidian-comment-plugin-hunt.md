Presentation.{ «Obsidian comment plugin hunt» }

# Obsidian comment plugin hunt

Created by Opus (Psyche obsidian Secondary 6aa500), evidence checks by Opus subflows.

**What was wanted.** Your commenting gate: you select a passage on the phone and comment with little friction, and a flow reads the comment as data. The hunt looked for an Obsidian plugin that meets it, so the module could rest on a maintained plugin instead of our own.

**First candidate: Review Comments 2.1.1.** It ran on an isolated Obsidian 1.14.5 and failed the presentation gate. Reading view stays literal and shows no control. The runs are saved in flows/280282/research: native-experiment.md (f6ca28), callout-acceptance.md, comment-runtime.json, comment-control-runtime.json and comment-live-runtime.json. Its fixture is preserved. The module keeps the Review Comments grammar.

**Second candidate: Review & Critic 2.1.1.** Plugin id review-critic; its asset hashes match review-and-critic-2.1.1-sha256.txt. It ran on the same runtime. Witnessed: the stored note text in vault/Candidate4ReviewCritic211.md reads

```text
The {==bronze kestrel crossed the quiet valley==}{>> [author=Daniel Rohrbach] Mobile review: confirm the durable reader follows this exact passage. <<} at dawn.
```

so the grammar is `{==passage==}{>> [author=Name] body <<}`. The command writes an empty body and the text is typed after. The badge structure (review-comment-badge, role=note, a tooltip, the braces staying literal) is witnessed only in the earlier candidate2-review-critic-ui-reading.json run.

**Claimed, not witnessed.** The Candidate4 Reading-view badge and the Comments-pane anchoring rest on a transcript at /root/candidate_test that no flow can read. That is a claim, not a witness (flows/927700/research/review-critic-2.1.1-ui-witness.md, f1cb6f). The phone, the friction, trust, replies and Obsidian 1.15 were not witnessed at all. Unattributed concurrent changes also appeared in the vault: a corrupted Candidate2ReviewCriticUI.md and a stray Candidate3ReviewCritic.md.

```
+-----------------+       +-------------------+
| Review Comments |       | Review & Critic   |
| 2.1.1           |       | 2.1.1             |
+-----------------+       +-------------------+
     | failed               |              |
     | witnessed            | witnessed    | claimed
     v                      v              v
+-----------------+  +-----------+  +--------------+
| Reading view    |  | note text |  | Reading badge|
| literal, no     |  | and the   |  | and pane     |
| control         |  | grammar   |  | anchoring    |
+-----------------+  +-----------+  +--------------+
```

**Result.** No module replacement. A later migration would need the Reading and pane run re-captured as saved artifacts, plus a grammar projection and a format-difference report.

**The reader.** Independent of the plugin, a reader component reads comments as data. Its current contract draft is flows/280282/research/reader-contract.ethos 939c3d (939c3dc9aa3aa0f1d8848d9f7a0a0c9d80d884185484a888767180a5a53d6aec), read against Mind's approved delta, which replaces 57ef22: half-open UTF-8 byte extents, optional metadata never fabricated, raw plus decoded text, positional replies keeping each id and type, malformed fragments kept as Unparsed, and exact Syncthing sibling conflict names. The owner shape is confirmed as design: a dedicated component, CLI obsidian-reader, later obsidian-reader-nexus, not Curriculum. Before the shelving, flow 927700 built the reader in /home/li/primary/repos/obsidian-reader, clean revision 101280 (101280b77f07ad50e8dd77531ac7cffb9033b195), binary target/release/obsidian-reader sha256 50c5f7eb6b74877afc5b1686e9e10f08743ff458091e2f092788742d2f9da9a8, pinned to reader.ethos 57ef22. Eight implementation tests reported passing; there is no independent acceptance result. It is uninstalled, unpushed, with no Beads, and it stays shelved as it is.

**Why it stops.** Your word, flows/b2b87a/vision/renewal.md, 2026-10-29: "lets shelf non-essential flows: research and obsidian (synching isnt interesting; shelf obsidian for now)". Obsidian is shelved, so the hunt ends here with the gate unmet and no plugin chosen.
