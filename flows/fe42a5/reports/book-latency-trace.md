# Book latency: exact provenance and missing timing

Primary decision: keep `tools/book-fetch.mjs` unchanged; its duplicate read is an inefficiency, not an established cause of publication delay. No cleanup work, publication or runtime mutation was performed. Production removed0/added0.

## Exact complaint cannot identify one corresponding book

`flows/4a8a28/vision/conversation.md` says communication through books has huge lag and loses the subject before feedback. The originating retained transcript is `/home/li/.claude/projects/-home-li-primary/4a8a2871-af6f-5b71-b4e7-ad8295d7b73f.jsonl`, human/queued record timestamp2026-10-20T19:06:05.552Z. It supplies no book title, URL or publication identity. Therefore selecting a particular book as the complained-of delay would be inference.

## One traceable, unrelated example

“The book modules, slashed,” source `flows/b0d3ae/proposals/book-modules.md`; publication `flows/b0d3ae/publications/eeb888ebf119d1a24f623b771c282ee1aadeb847ae57cb5445f4769db3f0b733/publication`, HTML `book-modules.html` beside it, artifact `https://claude.ai/artifact/4Hg9N2FdyJ2T9x3WWNxbMg`.

Retained transcript `/home/li/.claude/projects/-home-li-primary/b0d3ae3c-95ae-5eb1-969a-1210400d5b22.jsonl` on2026-10-30 (all times UTC):

| Boundary | Time | Source |
|---|---|---|
| Extraction worker launched | 21:05:18.964 | L923 |
| Extraction completion queued | 21:06:15.338 | L1026 |
| Source-writing command issued | 21:06:48.716 | L1030 |
| Publisher launch accepted | 21:06:52.983 | L1048 |
| Artifact frame-link/HTML association | 21:07:07.899 | L1056 |
| Publication marker local mtime | 21:07:09.468 | Filesystem, not transcript receipt |
| Publisher completion queued | 21:07:11.589 | L1057 |
| Flow reports URL | 21:07:12.896 | L1061 |

Measured: extraction-launch→completion-queue56.374s; completion-queue→source-command33.378s; source-command→publisher-launch4.267s; publisher-launch→frame-link14.916s; frame-link→URL-report4.997s. Total extraction-launch→URL-report113.932s. These are observed handoff boundaries, not pure computation times. Render begin/end and Artifact request/response boundaries are not separately timed. No living-visible or read receipt is present. URL/frame-link creation does not establish page visibility.

The unrelated example cannot close the2026-10-20 complaint. It shows where an existing record can bound time and exactly which boundaries remain missing.

## Smallest proposed observation, awaiting judgment

Use one already-requested book, with one shared correlation identifier and UTC timestamp log. Retain existing request time, mark extraction start/end, render start/end and Artifact send/return, then obtain the existing living-facing page path's **page-visible acknowledgment**. A read acknowledgment is distinct and optional if visibility alone answers the timing question. No new telemetry service or replacement publisher is proposed.

This proposal went to Mind core Primary (delivery750 accepted Queued); it is not an observation already performed. The read-only Metaflows snapshot exposed queued Psyche core Secondary order623 asking for one request→visible timing and Primary approval of any code removal; that order was relayed, not treated as an automatic publication command. Without a book identity and visibility witness, the full latency cause remains unknown.
