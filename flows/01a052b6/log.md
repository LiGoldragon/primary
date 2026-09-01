# Flow 01a052b6

## About

Remember the earlier work on Codex visual presentation reports, explain and use OpenAI's visual web-report capability, find a practical Android drawing collaboration, and identify an existing proper idea-editing framework where ideas and annotations are structured code rather than DOM- or pixel-anchored review markup.

## Settled

- “Web star presentation report” is current STT drift, not a historical name found in the relevant exchanges. Those exchanges used “visual report,” “web report,” “Claude web report,” and “Codex Reports hub.”
- Codex successfully built and deployed one owner-only Sites report hub in flow 01a04236. A later flow substituted inline ASCII/Markdown for the requested hosted report because the delivery boundary was not durable in Codex's instructions.
- The live owner-only Sites project and its matching local checkout still exist. The current hub is a hardcoded single report, not a reusable report system.
- Codex currently has three distinct visual surfaces: in-conversation Visualize artifacts, PPTX/Google Slides Presentations, and hosted Sites. No Codex-only web-reporting skill currently routes and proves the hosted-report workflow.
- A shared pen-and-machine visual-thought system needs a layered canonical document: preserved raw ink, semantic graph objects, explicit machine proposals/provenance, and durable causal history. Editors and published reports are projections of it.
- No product code, site, deployment, or access policy was changed in this flow.
- OpenAI's present visual stack is split: Visualize makes an interactive visual inside a conversation; Sites builds and publishes a persistent hosted web experience; Presentations makes an editable deck. The installed OpenAI-bundled Sites plugin is the capability that produced the Codex Reports hub.
- OpenAI provides no witnessed ready-made hosted visual-report template. A precise Sites request works now; repeatability would come from a personal template or Codex-only skill built from the existing hub.
- The strongest immediately usable drawing collaboration is Obsidian Android with the Excalidraw community plugin, first-party Obsidian Sync, and Obsidian Headless on the machine. This preserves Android pen input and gives the machine editable Markdown-wrapped Excalidraw JSON through an ordinary local vault.
- Miro's API cannot create or update pen strokes. Excalidraw's standalone collaborative web app lacks a durable machine-readable shared store by itself. Diagrams.net with Google Drive is the strongest fallback for structured diagrams but is a PWA and weaker for freeform drawing.
- The plugin directory search tool was unavailable, so no Miro, Excalidraw, Obsidian, or whiteboard plugin connection was confirmed or changed.
- The living approved the vocabulary addition exactly. Authored Curriculum now defines `Machine: short for thinking machine.` and directs `Use machine, not AI; use flow, not agent, except when reproducing an external name or quotation.` Generated shared skill surfaces were refreshed; a fresh flow produced “A machine started another flow to help the living.”
- The absence of standalone vocabulary copies under `.codex` and `.pi` is intentional: those trees hold role packets, while Codex and Pi consume shared workspace skills from `.agents/skills`. The generator check passed `Checked.{37 27}`.
- Built-in Browser annotations are a desktop/session review surface and are not a match for the living's clarified mobile, asynchronous, batched comment workflow.
- OpenAI currently has no native surface that meets the clarified contract. Sites, Visualize, Work, Canvas, Browser annotations, shared links, and the public API each lack at least one of mobile spatial commenting, asynchronous persistence, a comment inbox, or later target-preserving retrieval by the originating flow.
- Pastel is the strongest ready-made bridge: its phone-accessible review canvas accepts persistent guest comments on report locations, and its documented Codex MCP lets a later flow list canvas comments, retrieve individual comments and screenshots, reply, and resolve. Its OAuth is account-level, and compatibility with an owner-only OpenAI Sites login remains unproved.
- MarkUp.io is the strongest token/API alternative: a `threads:read` scope exposes comment threads with DOM paths, offsets, viewport, messages, and screenshots, but its mobile experience and private OpenAI Sites compatibility are less certain.
- The strongest private/OpenAI-contained fallback is a thin reusable Sites annotation layer: stable report-element IDs, mobile tap-to-comment UI, a D1 comments table, and later bounded comment retrieval through existing Sites database tools. The current hub has no D1 or annotation UI; a proved implementation is estimated at roughly one focused day.
- The living rejects a rendered-web review layer as the underlying idea model. The active target is a structured or projectional idea editor in which ideas, relations, and annotations are first-class data with stable identity; visual pages are projections rather than the canonical structure.
- The established technical category is a semantic collaborative model editor; projectional editor is the model-first subtype, and standoff annotation is the relevant anchor technique. The canonical artifact is a typed graph/store; annotations target stable node, edge, text-range, region, or operation identities rather than rendered HTML.
- The living's earlier work already contains the conceptual core: Meaning as an annotated structured string/graph with typed annotations; stable identity distinct from visible text; and operational edits applied atomically with a change log as VCS. These were recalled from flows a5587095, 0f9d1436, and 5abf3be8.
- tldraw 5.3 plus its commenting and sync packages is the closest genuine visual framework: shapes, bindings, pages, and comments are first-class store records, with comment anchors for shapes, text ranges, regions, points, and pages. It is a framework requiring an application, not a turnkey Android product.
- Tiptap/BlockNote with Yjs are mature text-first structured annotation frameworks; BlockSuite/AFFiNE is the strongest open page-plus-edgeless model, but its anchored-comment and machine-authoring contracts are not yet proved as a turnkey product.
- Figma/FigJam has strong node identity, node-relative comments, REST retrieval, and MCP-native FigJam edits, but Android is view/comment only; full FigJam editing is supported on iPad, not Android.
- Miro plus its official MCP is the strongest immediate Android product for object-centric idea editing: Android can edit shapes, stickies, text, frames, connectors, and comments; Codex can read and update many native objects and list/reply/resolve comments. Its MCP does not provide structural freehand strokes, guaranteed semantic comment-anchor IDs, complete connector fields, or generic deletion, so it is a practical slice rather than the terminal semantic editor.

Correction: The first research round pursued a terminal homegrown architecture after the parent instructed its research subflow, “This is not yet an implementation recommendation: map the best possible end-shape.” That contradicted the living's request for a workflow “possible right now.” The active target is an existing Android-capable drawing product plus the smallest access/sync/skill integration needed for living-and-machine editing now.

Correction: The flow later called Sites plus built-in Browser annotations a full match for Claude Artifact comments. The sentence “That satisfies the essential Claude interaction” omitted the living's actual boundary: comments must be placed from a phone, accumulated asynchronously without triggering Codex, remain anchored to report elements, and become readable together by the originating flow only when the living returns and asks. The active report-feedback target is this mobile, persistent, batched contract.

Remembered: 01a04236, 01a0428b, db97561c, 01a04e75 — depth 2 — the successful one-off Codex Sites hub, the later missed web-report boundary and recovered procedure, the Claude Artifact quality reference, and the unfinished reusable skill/QA/navigation/version/access contract.

Remembered: a5587095, 0f9d1436, 5abf3be8 — depth 2 — Meaning as annotated structured graph, operational editing with atomic changes and VCS, and stable identity separated from textual projection.

## Open

- Whether hosted reports, slide decks, or both should be first-class named deliverables and how Codex should disambiguate them.
- The access default for published reports: owner-only, explicitly shared, or another policy.
- The hub's canonical report schema, routes/navigation, version/checkpoint model, collision behavior, rollback, and browser/screenshot QA contract.
- Whether machine changes to the shared visual are direct edits or durable proposals requiring the living's acceptance.
- Which existing Android-capable drawing product gives the best immediate combination of pen input, structurally editable storage/API, machine access, and setup within hours.
- The smallest sync/authentication and Codex skill needed to make that product a shared living-and-machine surface now.
- Whether this visual collaboration pattern should graduate from Vision to Intent.
- Whether the living chooses the recommended Obsidian + Excalidraw + first-party Sync path, including any required Obsidian Sync subscription.
- A real-device round trip proving Android pen capture, headless synchronization, machine rendering, one structural proposal edit, living acceptance, and history recovery.
- Whether OpenAI Sites has a native mobile persistent comment surface, an existing visual-review service can provide it with machine-readable access, or the Sites report needs a small reusable persistent annotation layer.
- Whether the living accepts Pastel processing report pages, screenshots, comment text, and metadata through its servers, or requires the private D1-backed Sites layer.
- A harmless phone-to-Codex Pastel proof against an OpenAI Sites report, because Pastel compatibility with OpenAI's owner-only sign-in has not been witnessed.
- Whether an existing structured/projectional editor combines visual thinking, stable node/span/edge identity, first-class annotations, mobile input, machine-readable APIs or files, and practical setup now.
- How this desired idea-editing framework relates to the living's prior Protos, datom, Notae, graph, and visual-expression work without prematurely folding it into a homegrown architecture.
- Whether freehand strokes themselves must be canonical, identified, annotatable ideas, or whether drawing may serve as input from which canonical idea nodes, relations, and annotations are formed. This determines whether Miro is an adequate immediate slice or a tldraw-class model is required.
