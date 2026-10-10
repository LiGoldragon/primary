# Handover: Psyche Secondary, from d4ae97

## The seat

Psyche Secondary on Claude Opus 5.5, medium: the secretary of the Psyche
Primary, Fable f5a6e9. It relays every message to and from Fable, logs
the living's words verbatim before acting, has books published through
the book agent (`subagents/book.md`), and builds and tests through
subflows. It is not Fable and does not design in Fable's place.

## Read first

- `flows/d4ae97/log.md`: the seat's record, newest at the bottom. Its
  last line is the open order.
- `flows/d4ae97/vision/`: the living's words, verbatim, by topic.
  `messenger.md` holds his latest order (fresh flow for this seat, then
  topic flows for Ethos and Nexus). `flow.md` holds his words on topic
  flows and the fourth flow type. `notion/` holds his notions.
- `flows/d4ae97/reports/topic-launch.md`: what the launcher can and
  cannot do for a topic flow today.
- `flows/d4ae97/reports/flow-ethos-census/topic-flow-context.md`: the
  proposed 39.5k-token context for the Ethos/Flow topic flow.

## Whom it talks to

- Fable f5a6e9, Psyche Primary. Not to be woken for the Ethos/Flow
  redesign (log, 2026-10-08). No housekeeping, commits, layout or book
  reshaping goes to Fable.
- Spirit Fable ebbe30, Psyche Primary for Spirit. Its next book carries
  the golden-rule spirit line.
- Mind Secondary Sol 41fa34: the only route to Mind Astra 0c85a3. Do not
  message Astra directly.
- Field 42265e: publishes Primary, non-force. Subflows push nothing to
  Primary; they hand work back and Field publishes.
- Psyche 02dda6 holds the living's words it relays; the keeper list of
  flows is in the log, 2026-10-07.

Send with `hm-send` (messenger-clj, on PATH); report receipts as printed.

## Books awaiting his rulings

Relay his comments on each to its author, verbatim.

This seat's books:

- Context modules, into Intent: https://claude.ai/artifact/SqphBp52LVGdDUYNt3XTaS
- Raw records pile up: https://claude.ai/artifact/6QyyEQR6TtBEKzDE6iPUAw
- Curriculum's ethos (commented): https://claude.ai/artifact/117Cd1V9Hsp2UTMKmipHtU
- Spirit, a kind of skill: https://claude.ai/artifact/3wPT8EehoyorHacFuD8hEm
- Flow as it runs today: https://claude.ai/artifact/GE2fmKQNcK9zP9QkBEUnej
- Levels, tests, traits: https://claude.ai/artifact/HuFye2HYkS5bEUnQGy76gp
- Curriculum, a vision in ethos: https://claude.ai/artifact/XJ2gicWJRFcC75CdyP2jyr
- Spirit edit incident: https://claude.ai/artifact/B4XrVYH7m6sMKTopQCBJTQ
- Distillation books: https://claude.ai/artifact/RoMY4hePWH6oGjmXrW6mXT
- The fixed Metaflow record: https://claude.ai/artifact/H8pURfefKzc9WW7HWe6Qa1
- Rust toolchain: https://claude.ai/artifact/P8kqk7Kk8vsofdympMeu2n
- Clojure, the vision: https://claude.ai/artifact/Aua4vB78BmKoE7wjuFVBWc
- Haiku on the Quaternary: https://claude.ai/artifact/YaThKLYQWshyy8UcjKssXq
- Astra's five candidates (author 41fa34): https://claude.ai/artifact/3AXTdcjQjzqka5kFHCoLZw
- Status board: https://claude.ai/artifact/TTJp3YYFxZXBekUSDFEx9k
- Flow/Ethos census: https://claude.ai/artifact/2pjntLdTKkoP38WXe7Eqvp
- Framework study: https://claude.ai/artifact/QRfWqbTEWurQ3UeShDRPzi

Fable f5a6e9's books:

- Context modules: https://claude.ai/artifact/LMehrJfPcSnz5vfNifcF4f
- Flow and the metaflow: https://claude.ai/artifact/3zEZo31LLLBpX1gak6JmoW
- Stored type: https://claude.ai/artifact/6cgk7UGUTyK9gCFULNtfLC
- Metaflow kinds, title, word id: https://claude.ai/artifact/Ns3ddQa9hhWVBdY71QYA1X
- Flow, a passable vision: https://claude.ai/artifact/LFKcRWAPzj1FdG1Em1TbJ4
- The queue and the waking rule (commented): https://claude.ai/artifact/HUA3QJiFyVErW12sgJ79wC
- The metaflow record, 2nd ed: https://claude.ai/artifact/1htsLRsyFMsoxvNV92gHxb
- Compensations for the machine: https://claude.ai/artifact/ULK22PXHWUL7ugdY1cdBLu

Spirit Fable ebbe30's book:

- Spirit, three skills: https://claude.ai/artifact/XUWRutzPLCSzK94kKnFgT5

Book sources are in `flows/d4ae97/books/`.

## Work out with other flows

From d4ae97's own compacted summary and log (claims, not re-witnessed):

- Astra 0c85a3, through Sol 41fa34: Codex atomic upgrade, Clojure under
  Nix, the Clojure Flow prototype, the JSON-datom bridge, the topic
  registry (prototype at
  `private-repos/flow-evidence/0c85a3/topic-registry`, not landed), the
  Curriculum ethos rewrite. Results come back as candidates to publish.
- Spirit Fable ebbe30: the golden-rule spirit line in its next book. The
  unapproved lines in `psyche-skills/skills/spirit` stand until his
  ruling on «Spirit, a kind of skill».
- Topic flows for Ethos design and Nexus design: ordered (vision
  `messenger.md`), not launched. See `reports/topic-launch.md` for what
  blocks them.
- Open, unexplained: full fsck of Primary unclean (jj keeps the malformed
  history); `Vision/` reappeared after the migration; a Pi
  compensation-testing deletion.

## Standing constraints

- Psyche data changes only by an edit the living reviewed and approved;
  the rule is the first paragraph of `compensation-design`.
- Every distillation is a skill writing; books are distillation
  proposals, rendered by the book agent (`compensation-book-distillation`).
- Messages move by level (`compensation-launch`): this seat reaches Mind
  only through Mind Secondary.
- A subflow brief says: push nothing to Primary; never edit spirit,
  vision- or intent- skills.
- Questions his records settle are decided, not asked.

## First work: the Ethos and Nexus topic flows
The living ordered on 2026-10-09 two Psyche Opus topic flows, Ethos (Ethos, Datom, the Proto stack) and Nexus (Nexus, and Message using Flow; message is called message), talking to each other. His words: `flows/d4ae97/vision/messenger.md` (2026-10-09) and the transcript of d4ae97. Their context packs: `flows/d4ae97/reports/topic-ethos/context.md`, `flows/d4ae97/reports/topic-nexus/context.md`. Launch each with `tools/claude-main-flow-launch.mjs --aspect Psyche --layer Secondary --topic <Topic> --root --metaflow <file> --brief <file>`; run with `--check` first. Topics he asked for on 2026-10-08 and not yet started: Jev with an Ethos subset (`reports/jev-ethos/material.md`), Testing, Clojure ("eventually").
