# TypeSafe AI's other tools, and a medium for books

For Astra. What else the people behind Jev make, and which medium suits flows presenting books and proposals to the living. Jev itself, its clients and its gateways are in `flows/bad807/reports/jev-ecosystem.md` and are not repeated here. Web pages were read on 2026-10-04. Nothing was installed or called.

Three kinds of statement are kept apart:
- **Observed**: read on a public page or registry, with its URL.
- **Vendor claim**: what a vendor says about itself.
- **Unknown**: not established.

## 1. What the medium has to do

These requirements come from his own words.

| Need | His words | Record |
|---|---|---|
| Pages like a Google Doc, possibly better than artifacts | "Google Doc could also work maybe better than Claude's artifacts but I don't know" | `flows/aa887c/notion/livingMessenger.md` |
| Comment from the phone, many at once, without waking the session | "put in comments without triggering the session every time … It would be able to see all the comments and what they refer to" | `flows/01a052b6/vision/reportFeedback.md` |
| An Android app, set up in hours, with machine access through his token | "that would have an Android app … a way for the machine to access … even if it needs my like token access" | `flows/01a052b6/vision/visualCollaboration.md` |

Today's path is the book agent (`subagents/book.md`). It publishes a Claude artifact backed by `ArtifactData` collections and reads anchored comments with `ArtifactComments`. A flow then records each comment with the passage it is anchored to (for example, `flows/aa887c/reports/his-comments.md`).

## 2. What TypeSafe AI makes

### Observed

| Product | What it is | License / open | Packages | Downloadable now | State | Machine API | Nix | Android |
|---|---|---|---|---|---|---|---|---|
| Jev and System One API | typed-decision model | closed weights, hosted | (see jev-ecosystem) | API only | early access ([typesafe.ai](https://typesafe.ai)) | `POST /v1/systemone` | client only | none |
| Console and playground | sign-up, keys, browser playground | proprietary SaaS | none | web only | live ([console](https://console.typesafe.ai)) | none documented | n/a | web only; mobile layout unknown |
| Docs site | docs.typesafe.ai: concepts, cookbooks, one demo (Smart Home) | proprietary | none | web | live ([llms.txt](https://docs.typesafe.ai/llms.txt), [demos](https://docs.typesafe.ai/demos.md)) | `.md` pages readable by machines | n/a | web |
| evals.typesafe.ai and WorkflowEvals | public eval site and its code | Apache-2.0 | GitHub source | yes | no release | none | buildable from source | web |
| Python and JS SDKs, skills, system-one-adapter, n8n node | Jev clients and tooling | MIT | PyPI, npm, Claude plugin | yes | 0.x | — | not in nixpkgs | — |
| daggerverse | Dagger modules | Apache-2.0 | GitHub | yes | no release | — | — | — |
| pulumi-clickhouse | Pulumi provider for ClickHouse Cloud | Apache-2.0 | GitHub | yes | last push 2026-07-08 | — | — | — |
| vllm, LLaDA | forks of upstream research and serving code | Apache-2.0, MIT | GitHub | yes | forks, inactive | — | — | — |

All rows come from the org listing (`gh api orgs/typesafe-ai/repos`, [github.com/typesafe-ai](https://github.com/typesafe-ai)), the homepage ([typesafe.ai](https://typesafe.ai)) and two third-party summaries ([jev-ai.org](https://jev-ai.org/blog/typesafe-ai/), [jevwiki](https://jevwiki.ai/wiki/entities/typesafe-ai.md)).

**No Notion-like pages or docs product from TypeSafe AI was found.** The searches covered:
- the homepage and team page;
- the docs index and demos;
- the GitHub org (eleven repos, all listed above);
- third-party product summaries;
- the awesome-typesafe-jev list;
- HN (Algolia);
- web search for "typesafe" with pages, docs, notebook, Notion and workspace.

The homepage names one product, Jev, "in early access."

Other products of the people themselves ([team](https://typesafe.ai/team)):
- **Erik Gafni (CTO)**: founded Ravel, multimodal AI for DNA sequencing. His GitHub ([egafni](https://github.com/egafni)) holds COSMOS2 (a scientific pipeline manager), ConfigSys and ML playgrounds. None is a document tool.
- **Diogo Almeida (CEO)** and **Sasha Sheng (COO)**: no product of either was found.

A different company shares the name: Typesafe Inc., maker of Scala, Akka and Play, renamed Lightbend ([HN](https://news.ycombinator.com/item?id=32827160)). It makes no Notion-like product either.

### Unknowns

- Where the "Notion-like product" report came from. Nothing public matches it. It may be unannounced, a misremembered name, or another vendor.
- Whether the console has a mobile layout.

## 3. Candidates for the books medium

TypeSafe offers no candidate, so the comparison is between the two media that do exist. Outline is added as the nearest self-hosted, Nix-packaged option. It lies outside the brief and is shown only so that the gap is visible.

| | Claude artifacts (today) | Google Docs | Outline (outside the brief) |
|---|---|---|---|
| What it is | hosted HTML page on claude.ai, with comment threads and a page database | hosted document editor | self-hosted team wiki |
| License | proprietary SaaS | proprietary SaaS | BSL 1.1 (GitHub reports NOASSERTION), source available ([repo](https://github.com/outline/outline)) |
| Packages | none; reached through Claude Code tools | none; clients: crates `google-docs1`, `google-drive3` 7.0.0 ([crates.io](https://crates.io/crates/google-docs1)); nixpkgs `gws` 0.22.5, `gogcli` 0.40.0, `rclone` 1.75.1 | server v1.10.1, 2026-09-09 |
| Self-host | no | no | yes |
| Write a page by machine | yes: `Artifact` publish and `ArtifactData` (observed in `subagents/book.md`) | yes: Docs API `documents.create` and `batchUpdate` | yes: `documents.create` ([API](https://www.getoutline.com/developers)) |
| Read his comments by machine | yes: `ArtifactComments` read, anchored to a passage (observed in `flows/aa887c/reports/his-comments.md`) | yes: Drive `comments.list`; each comment carries `anchor` and `quotedFileContent`, the quoted text ([reference](https://developers.google.com/workspace/drive/api/reference/rest/v3/comments)) | yes: `comments.list`; anchoring to a selection is stated, its API shape unknown |
| Machine reply or resolve | reply through `ArtifactComments` | yes: `replies.create`, `action: resolve` ([guide](https://developers.google.com/workspace/drive/api/guides/manage-comments)) | `comments.create` |
| Machine-made anchored comment | unknown | **no**: "Docs … don't render comments created with the Drive API anchored to content; they treat these comments as unanchored" ([guide](https://developers.google.com/workspace/drive/api/guides/manage-comments)) | unknown |
| Suggestions (proposed edits he accepts) | none | yes, both ways: `documents.get` with `suggestionsViewMode`; `batchUpdate` with `WriteControl.writeMode = SUGGEST`, which cannot suggest format, header or footer changes ([guide](https://developers.google.com/workspace/docs/api/how-tos/suggestions), updated 2026-09-30) | none |
| Rich content | full HTML: SVG figures, live database | text, tables, images; no inline SVG or code highlighting; the Docs API has no Markdown import | Markdown, images, diagrams |
| Comments without waking the session | yes: comments wait until a flow reads them (his reported workflow) | yes | yes |
| Android | used today on the phone for reading and commenting (`flows/01a052b6/vision/reportFeedback.md`, flashbook phone records) | native Docs app; offline create, view and edit: "you can still create, view, and edit files" ([support](https://support.google.com/docs/answer/6388102?co=GENIE.Platform%3DAndroid)); offline commenting not stated | mobile web; no native app found |
| Offline | no (unknown) | yes, per the support page | no (unknown) |
| Nix | Claude Code is our existing seat; nothing new to package | API clients in nixpkgs and on crates.io; no server | nixpkgs `outline` 1.10.1 and NixOS module `services.outline` |
| Identity | his claude.ai account | his Google account; OAuth token held through `secrets` | our own host |
| Private-layer fit | public vendor | public vendor | ours (self-hosted) |

### Reading the table

- **Google Docs** adds three things the artifact lacks:
  - an Android app with offline editing;
  - true suggestions, which let a flow propose an edit he accepts with one tap;
  - a stable public API that any Nexus or CLI can call, not only a Claude seat.
- **Google Docs** costs three things:
  - figures, which must become images;
  - machine-made comments, which lose their anchor;
  - the book's live database, which has no equivalent.
- **Artifacts** stay strongest for drawn, code-heavy books. They are reachable only through a Claude Code seat; a Codex seat has no such tool (his reportFeedback record asks for exactly this).

## 4. Integration with our system

```
flow ──book──▶ medium page ──▶ the living (phone, batched comments)
  ▲                                   │
  └── comments with quoted passage ◀──┘   read on his word "I commented"
```

| Part | Google Docs | Artifacts (today) |
|---|---|---|
| Living messenger | `hm-*` sends the doc link; on his reply, the flow reads `comments.list` since the last mark | same, with the artifact link |
| Books | the book agent renders sections as Docs `batchUpdate` requests; rulings as numbered list items; figures as PNG uploads | unchanged |
| Comment intake | `quotedFileContent.value` plus `content` become "Anchored to / His comment" lines, the format of `his-comments.md` | `ArtifactComments` read |
| Proposals as suggestions | each proposed edit to a Vision file is written in SUGGEST mode; accepted versus rejected is read back from `suggestionsViewMode` | no equivalent |
| Nexus / Flow design | a CLI side (datom in, Docs JSON out at the network edge), consistent with "a Nexus never handles text"; a Rust client from `google-docs1` and `google-drive3` | a Claude-only tool; not callable from a Nexus |
| Nix / NixOS | `gws` or a Rust client in a flake; OAuth refresh token via sops; no service to run | none needed |

## 5. Next concrete step

1. **TypeSafe.** Ask the living where he saw the Notion-like product: a link, a name, or a post. Without that, nothing further can be searched.
2. **Google Docs.** Run a one-afternoon witness. A flow publishes one existing book as a Google Doc through `gws` or the Docs API, using a token he grants. He comments and accepts or rejects one suggestion on his Android phone. The flow then reads the comments with `quotedFileContent` and the suggestion states. Compare the result line by line with the same book's artifact comments.
3. **If self-hosting matters** (the private-layer charter), order a separate survey of Outline, Docmost (AGPL-3.0, v0.96.0, not in nixpkgs) and AFFiNE. The survey should cover their comment APIs and Android use.

## Sources

- TypeSafe: [typesafe.ai](https://typesafe.ai), [team](https://typesafe.ai/team), [docs index](https://docs.typesafe.ai/llms.txt), [demos](https://docs.typesafe.ai/demos.md), [GitHub org](https://github.com/typesafe-ai), [jev-ai.org summary](https://jev-ai.org/blog/typesafe-ai/), [jevwiki](https://jevwiki.ai/wiki/entities/typesafe-ai.md), [awesome-typesafe-jev](https://github.com/AbdelStark/awesome-typesafe-jev), [egafni](https://github.com/egafni), HN Algolia search.
- Google: [Drive comments guide](https://developers.google.com/workspace/drive/api/guides/manage-comments), [Comment resource](https://developers.google.com/workspace/drive/api/reference/rest/v3/comments), [Docs suggestions](https://developers.google.com/workspace/docs/api/how-tos/suggestions), [Android offline](https://support.google.com/docs/answer/6388102?co=GENIE.Platform%3DAndroid).
- Packaging: crates.io API (`google-docs1`, `google-drive3`); nixpkgs `nixos-unstable` package files (`outline`, `gws`, `gogcli`, `rclone`) and `module-list.nix`; GitHub API (outline, docmost).
- Outline: [developers](https://www.getoutline.com/developers).
- Our records: `flows/bad807/reports/jev-ecosystem.md`, `flows/bad807/books/18-jev.md`, `flows/bad807/vision/jev.md`, `flows/aa887c/notion/livingMessenger.md`, `flows/01a052b6/vision/reportFeedback.md`, `flows/01a052b6/vision/visualCollaboration.md`, `subagents/book.md`, `flows/aa887c/reports/his-comments.md`.
- Provenance receipt: unavailable. No PROVENANCE handoff was received.
