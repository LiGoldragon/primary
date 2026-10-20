# Books to redo (read 2026-10-16)

This list covers books in «Open books» that were published or updated on or after 2026-10-10, are not fully ruled, and have no newer edition. It holds 25 rows, the cap. Where a book has no comments, any rulings shown come from the flow logs.

The current book form: every section is a proposal headed "repo › path" at a location witnessed in the files. Lines removed or added are shown verbatim. There is no technical part. There is no long prose, and no references, hashes or paths outside the headings. A book has an illustration only where the idea has a shape.

All 25 books break the form. Only books 37 and 39 use "repo › path" headings. Every other book puts its location in a "File:" line inside the body.

| Book | URL | Source | Owner | Comments (gist) | What breaks the form | Already ruled (leave out of the redo) |
|---|---|---|---|---|---|---|
| Why your orders get lost | https://claude.ai/artifact/GWSjYgiXpjrr2Gg7S9fJHZ | flows/d68c82/books/39-lost-orders.md | d68c82 | none | All 3 proposals target mind-context › skills/operation-main-flow.md, a machine module and not psyche. A list of causes sits above the proposals. | none |
| How a presentation is worded | https://claude.ai/artifact/HFFBzYJDvZoY4Urukxivg8 | flows/d68c82/books/32-wording.md | d68c82 (index says 33752b) | none | Locations use plain-word names ("the vision of books"), not repo › path. Has a "Technical part" section. P3's Ethos code renders as prose. | none |
| Metaflow roles | https://claude.ai/artifact/1bjt3LCT3JDszJZQZ3SGr8 | flows/da2038/books/6-metaflow-roles.md | da2038 | The first paragraph is noise he won't read. He wants a book on how to do books: one simple view at a time, like children's books. | Opening prose has a path. P2 to P6 are code or data files (role.ethos, .datom, signal.ethos, Curriculum), so they are technical. Has a pinned hash. | none |
| Knowledge: monitoring systems | https://claude.ai/artifact/1BjWNxyDu2BbDRPnJkAvz3 | flows/d68c82/books/31-monitoring-systems.md | d68c82 (index says 33752b) | none | Mostly knowledge tables and prose (memory, stewards). One proposal, in a "File:" line. It is a knowledge review he asked for, not psyche. | none |
| One registry of builds | https://claude.ai/artifact/HfEeNo62s9V6FjUgRa32uV | flows/d68c82/books/30-one-registry.md | d68c82 (index says 33752b) | P1: call it "Nix builds" and say `nix build`, otherwise good. P2 is good. P3 should be a vision proposal and not an implementation. | "File:" lines. Has a context section (the builder's store). P3 and P4 target CriomOS .nix code. | P1 land, amended (name "Nix builds", `nix build`). P2 land. P3 rejected as written (redo as vision). |
| Fable, used with care, 2nd edition | https://claude.ai/artifact/P1Jprnf8QzVuVjSHUSX3AC | flows/d68c82/books/29-fable-care-2.md | d68c82 (index says 33752b) | none | "File:" lines. P2 to P4 target field-context compensation modules, which are machine modules. Long quoted anchor lines. | none |
| What compaction keeps, 2nd edition | https://claude.ai/artifact/5Deg7feWZQYFCGuX97SP77 | flows/d68c82/books/28-compaction-2.md | d68c82 (index says 33752b) | none | Two research sections. All 3 proposals target mind-context knowledge-compaction, not psyche. | none |
| A folder too full to index, 2nd edition | https://claude.ai/artifact/NvqXRaEN6JWZYY4npjEBUg | flows/d68c82/books/26-nix-links-2.md | d68c82 (index says 33752b) | none | Before/after data sections. P1 targets field-context compensation-nix-workflow, a machine module. "File:" lines. | none |
| A module names the role, not the host | https://claude.ai/artifact/X5aaSuYT74t8ZfE1t4oKpU | flows/d68c82/books/24-names-are-data.md | d68c82 (index says 33752b) | none | A table and Nix code sit outside the proposals. Host names appear in the body. "File:" line. | none |
| Watching the cluster | https://claude.ai/artifact/2B6H6S5MLYL1YrJu9w4iM8 | flows/d68c82/books/22-watching-the-cluster.md | d68c82 | Prometheus is cluster data, so name the role that selects it. Write the measures as Ethos. He wants a knowledge book comparing monitoring systems. | Prose plus "Crystallization" and "Choices" sections. Names the host Prometheus. "File:" line. | none (P1 not ruled; 2nd edition ordered) |
| Subflows: kind, role and level | https://claude.ai/artifact/XpPEQD1TFjWA8rQXrTSTNN | flows/d68c82/books/17-subflows-kind.md | d68c82 | none | Has "Knowledge review: the Kind in Clojure" and "Question" sections. P2 is code (Curriculum/kinds.ethos). "File:" lines. | P4 carried into «Context modules: folders, types, placement» and approved there ("good"). |
| Situation, 14 October, evening | https://claude.ai/artifact/3mTpJTTR1q7mwvurCBBFeH | flows/d68c82/books/14-sitrep-2.md | d68c82 | none | Mostly a status report (Zeus, CLIs, Flow; Under way). One proposal, in a "File:" line. | none |
| Chronos, 2nd edition | https://claude.ai/artifact/Fd1jGBnf2dcfkrSRShrE6w | flows/984e88/books/02-chronos.md | 984e88 | No comments on the book. On «Battery drain» he called it glanced and marked for a prototype. | 16 "File:" lines. Ten choices on Ethos anatomy, all technical. | none |
| Compensation core | https://claude.ai/artifact/JqnZvp7RsbdsKycdbjZz8Z | flows/da2038/books/2-compensation-core.md | da2038 | none | Sections explain before the proposals. Most targets are field-context, mind-context or config .edn, not psyche. Several "File:" lines per proposal. | none |
| The Flow Nexus, whole: long term, then short term | https://claude.ai/artifact/SM9kdHvCWXr7A2zw5DDHZg | flows/55a2b4/books/15-flow-nexus-whole.md | 55a2b4 | P1: land, except re-propose the cost-model sentence smaller. The Ethos paragraph is good. The diff tool is wrong (vision-flow is still there). Drop "skill" and "vision-" from file names, since the folder gives the type. | 12 "File:" lines and 19 paths. The short-term Clojure part is technical. Shows a wrong diff. | P1 land, except the "new topic on the cost model" sentence. P2's Ethos paragraph land. |
| Short-term prototypes: Clojure now? | https://claude.ai/artifact/8crUcAX5LKJANvvFsts1hy | flows/55a2b4/books/14-short-term-prototypes-clojure.md | 55a2b4 | P4 is good; make references a standard everyone finds the same way. P3's Terra model example is bad. | Code proposals (Clojure, EDN). 8 "File:" lines. | P4 land (book carries proposals; records in a reference file). |
| Communicating with the living, 3rd edition | https://claude.ai/artifact/R13NaiW5c8C5NGy84MX5cV | flows/17ac8a/books/02-communicating-with-the-living-3.md | 17ac8a / 3960eb | None on this edition. The log says he ruled the name vision-living-communication. | Targets psyche-context/skills/vision-living-communication.md, which does not exist and is not flagged new. "File:" lines. | Module name ruled (vision-living-communication), per the log. |
| Flow: CLI, deployment, long term, 3rd edition | https://claude.ai/artifact/NBDZqnnNptMynwhu6xjrKf | flows/55a2b4/books/12-flow-cli-deployment-long-term-3.md | 55a2b4 / da2038 | none | Locations given by line numbers (L24, L34, L62) in "File:" lines. A figure is placed as a proposal. | none |
| Flow: Nexus, ethos and design | https://claude.ai/artifact/B755eSrUkP5K5Ar73Q9KCi | flows/df159a/books/11-nexus-ethos-design.md | df159a / da2038 | none | 15 proposals, several "File:" lines each, with "under choice N" anchors. Has hashes. | none |
| Flow: messaging between flows | https://claude.ai/artifact/YBBK3jSZuoivFtB25Eg82s | flows/c5f24b/books/10-messaging-between-flows.md | c5f24b / da2038 | none | 33 "File:" lines, 58 paths and hashes in the body. Code proposals. | none |
| Flow: context modules and the prompt | https://claude.ai/artifact/UQiKz4ZHVfgREo6CHHRmkU | flows/c5f24b/books/09-context-modules.md | c5f24b / da2038 | none | 76 "File:" lines, about 100 paths and hashes. Code proposals. | none |
| Flow: main-flow mode and roles | https://claude.ai/artifact/N77pCE2NAc9CuKUBKAuJSj | flows/288af9/books/08-main-flow-roles.md | 288af9 / da2038 | none | 62 "File:" lines, 51 paths and hashes. Agent scripts are proposed, which are technical. | none |
| Flow: launch and lean start | https://claude.ai/artifact/CbCJRpT8sMRsyZWwTtMzVw | flows/563761/books/07-launch.md | 563761 / da2038 | none | 81 "File:" lines, 49 paths and 7 hashes. Code proposals. | none |
| Flow: refresh and handover | https://claude.ai/artifact/GSQSYS6nZDzq7k4YzfoTi9 | flows/563761/books/06-refresh-handover.md | 563761 / da2038 | none | Mixes vision-flow lines with .mjs, .json and .clj code changes in one proposal. 25 "File:" lines. | none |
| Flow: the metaflow | https://claude.ai/artifact/N1tgM3NYPWrgWo61kaTM8j | flows/563761/books/05-metaflow.md | 563761 / da2038 | none | 12 "File:" lines and 23 paths. One location is flows/d4ae97/notion/flow.md, a record and not a module. | none |

## Left out

Fully ruled:

- Short hashes: P1 landed in vision-messaging; P2 and P3 cut; P4 in the wrong place.
- Drawing ideas, 3rd edition: P1, P2 and P4 land; P3 rejected.
- Code shown as code: rejected.
- Context modules: folders, types, placement: P1 to P3 good.
- Git servers for the thinking machine: P1 land renamed Git Server; P2 land.
- Battery drain in sleep: P1 not landed; it becomes one hardware skill.
- Only psyche reaches you.
- What you review is psyche.
- Figures that move.
- Short-term and long-term vision.
- What you said today.
- Dense and visual.
- Situation, 14 October.
- The shared Clojure translation pattern.
- Flow: philosophy and artifacts: landed.

Replaced by a newer edition or withdrawn:

- Drawing ideas, 1st and 2nd editions.
- Fable, used with care, 1st edition.
- A folder too full to index, 1st edition.
- What compaction keeps (7nx5nP).
- Flow: identity and naming, 1st edition.
- Books, reviews and the hierarchy, 1st edition.
- Three lines from the chat, 1st and 2nd editions.
- Cleaning up the skills, 1st edition.
- Context modules, 1st edition.
- Where today stands: withdrawn.

Reports with nothing to rule:

- Usage.
- Flow context sizes.
- What a flow sees.

Not listed because of the 25-row cap. These are still open or partly ruled, and none are in the current form:

- Why Fable was not refreshed: P1 land; P3 has no target; P4 is compensation and not his to rule; P2 open.
- Flow: identity and naming, 2nd edition.
- Flow: short term and long term, 3rd edition.
- Clojure and data: the rectification.
- A guarded compaction request, 2nd edition.
- Tools instead of scripts.
- Three lines from the chat, 3rd edition.
- Short term and long term (Fable).
- Crystallization.
- Makeshift and goalpost: the P1 spirit line rejected as worded, in favour of short-term and long-term vision.
- Makeshift, from Core.
- Makeshift, from Spirit.
- Cleaning up the skills, 2nd edition: on Ruling 2 he said the model-by-family concept may be reviewed, and that the negatives about versions were past corrections, not standing rules.
- Tripping over the shoelaces.
- Handover and the seat without a shovel.
- Context modules, 2nd edition.
- The 10-10 to 10-12 books from 33752b, 875960, 73ada7, d5df1d, 058f16, 081064 and 9519a1. Among them:
  - The Message forks F1 to F13, with no comments.
  - The caller is witnessed: the process-ancestry approach rejected; he wants the flow id.
  - The commit queue: no fresh clone.
  - Persona's root: the old designs to be rewritten; «What the root does» lands with the triad named only.
  - Sources in the commit message: P1 land.
  - Nuts and bolts, second edition: the spirit-core line rejected as not universal.
  - Two Field lines without a source: the trial-succession proposal removed.
