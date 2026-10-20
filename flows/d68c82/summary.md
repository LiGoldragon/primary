# d68c82 — Psyche core Secondary (Opus 5.5), summary for the successor

## Seat
Psyche core Secondary. Logs the living's words in vision/ and notion/, relays with hm-send, publishes books (Artifact tool, interactive session only), lands approved psyche-context lines through subflows. Every comment on a book makes a new edition; nothing is answered in chat alone.

## Specialized topics (the living, 2026-10-19: use specialized Opus topic flows, track them; they may consult a fresh Fable only for design)
- Flow: Psyche flow Secondary aa034f (Opus) — Flow code integration 0.35.19 on branch 6ccb2ed, not deployed.
- Ethos: to be launched as Psyche ethos Secondary (Opus). Books 87/92 (open enum, custom representation), 88/96 (syntax), 90/95 (flow ethos), 81 (memory type traits).
- Books: to be launched as Psyche book Secondary (Opus). Books 83/84/93 (what a book shows), builder support for machine comments and alternatives-as-differences (tools/book-build.clj, uncommitted, for 89fbc1).
- CriomOS: book 82 (third edition) proposals 2–12 open.

## Landed today in psyche-context (origin/main)
d5c7d3d inquiry/context-modules/criomos Services; 12f2558, 1535807 book.md; 4de1d9a criomos P1; a83cbd0, 168d72c, 6c8e266 flow.md/subflows.md/nexus.md/ethos.md; 4ddea6a open enum; d095d0f imports and brackets. field-context bc5fa7c (seven compensation book lines removed).

## Not deployed
Skills flows load are from 2026-10-15; no supported skills generator exists for the current sources (Mind context Secondary 877549 owns it; its queue holds 7 undelivered). Production Flow 0.35.11 does not deliver queued messages to live seats (36 queued for d68c82). Message-side for the new Flow owned by Mind Core Primary 0c85a3.

## Open
- Comment-to-edition register: receipts/comment-edition-register.md from flows/7c89aa/comment-relay-ledger.jsonl; every unaddressed thread gets an edition; a book on the missing-edition failure.
- Flow's vision third edition (P1 front matter, P11, P16/17, P18/19, P21 reworded) after the builder format lands.
- Ethos Set type: Mind ethos Secondary 66f2bb asked to accept; semantics questions to the living in a book.
- Ghost cleanup with Field (receipts/session-inventory-2026-10-19.md); 47d946, 0430eb, 19d9f2 await the living's ruling.
- Vision-implementation audit (receipts/vision-implementation-audit-2026-10-19.md) to be sent to owners.
- Book 97 (topic flows, design Fable, messages from files) in progress.
- Earlier: store-path wave (Sol counter-audit, Field final pin), Sources rule ruling, Sema→Memory proposals.

## Lessons
- Write the living's ruling as ruled; where Ethos lacks a feature (Set), mark it not parseable and report it; never substitute.
- A brief's working words never name a module; Ethos modules are ethos-named.
- An approval anchored inside a proposal covers the whole proposal.
- Subflows wait on completion notices, never on sleep timers.
- Titles are { Aspect Topic Layer FLOW_ID }; the loaded skill still says Aspect.{ Model FLOW_ID }.

## Recovered queue (36 undelivered messages, read 2026-10-19; file /home/li/private-repos/flow-evidence/42265e/session-cleanup-20261019/d68c82-readable-queue.md)
29 superseded or handled. Still open, for one rulings book to the living:
- aa034f #35: two books (joint 76454e, whole-Flow 93a337) are accepted but unpublished. They wait on a ruling on code-line width: generator lines run 88–95 columns, quoted module lines up to 129. Also two book-check.mjs fixes, and who owns the uncommitted book-check edit.
- 804eb9 (Psyche ethos Secondary, earlier holder) #18: books/ethos-v1-3.md is unpublished. It asks for: question E8 to be put to the living; a ruling on dropping the extendable enum, now superseded by the open-enum design; an owner for protos.ethos and datom-codec.ethos.
- aa034f #24: who owns Primary's .claude/agents, since a same-named agent there overrides Flow's role; and Curriculum RoleCallers, which needs the living's approval.
- aa034f #26/#30: Field's illustrator and publisher run Claude, against the layer table; gpt-6-sol or gpt-6.1-sol. The model-differing resume is settled by landed P24, "a woken flow is almost always fresh".
- aa034f #20: may Claude queue delivery keep typing into the pane?
- aa034f #36: the EventTables Mutex finding was handed to 65f93a, now retired, and needs re-handing to Mind.

## Handoff addendum (after 5dd7e5 took the seat)
- Naming failure: 5dd7e5, 43efac and 7cd214 were launched through Flow 0.35.11 with claude-<hex> workspaces and flow-<hex> remote names, against the living's standing order. He ruled: rename, don't tear down, fix the tool. A d68c82 subflow is renaming all three now and will report to this log. Mind and Field are asked to ship a narrow production release with only the visible-name fix, aa034f's commit from 0.35.19. Until then, no launch without renaming. Proposed launch-skill line: "A flow is launched only through a route whose result carries the ruled names on its workspace, title and remote session; a route known to break that ruling is not used: the fix comes first, or the launch is held and the blocker named."
- Sends from d68c82 to aa034f, 877549 and "Psyche core Secondary" return MessageRefused Unidentified. Field is asked to repair them. The P8 subflows inquiry is NOT delivered to 877549; Mind Core is asked to carry it with packet /home/li/private-repos/flow-evidence/41fa34/context-owner-landing-20261019/packet.json. aa034f and 877549 still need psyche-context 6c8e266 as their newest source.
- Thresholds: none ruled beyond the ephemeral Claude 300k/250k; they go into Flow's vision third edition as alternatives. The 15%/200k/400k values stay unrestored.
- Published since the summary:
  - 92 «Ethos: the open enum, 2nd ed — a custom representation» (Ji2q15), 23 proposals;
  - 95 «Flow ethos, 2nd ed» (W4AqzG), Set<Model>;
  - 96 «Ethos: imports and definition brackets, 2nd ed» (9i8G7N; published despite a book-check refusal of excerpted context; the Books seat owns that conflict);
  - 97 «Topic flows, a design Fable, and messages from files» (SQRvq4).
  - 93 «What a book shows, 3rd ed» is publishing now.
- The builder now supports **Comment** and **Alternative N** groups. These are uncommitted in tools/ and wait for 89fbc1: book-build.clj, book-check.mjs, book-code.html and their tests.
- mind-context 63f8a0 landed the «One module name» Q4.
- The vision audit summary went to Mind and Field: 28 implemented, 57 partly, 29 not, of 114. Ruling needed: does "a new service lives in CriomOS" include CriomOS-home?
- The living's ruling is needed on 47d946, 0430eb and 19d9f2. Flow test rows and the "--help" Herdr session are unresolved.
- The P8 subflows inquiry is still undelivered: it failed before enqueue. Send it once only after Field qualifies the sender route; packet /home/li/private-repos/flow-evidence/41fa34/context-owner-landing-20261019/packet.json.
- Mind ethos Secondary 66f2bb is asked to accept two Ethos findings, Set and the EventTables Mutex. Both questions go to the living as findings, with no workaround.
- URGENT, from Mind Core Primary for 5dd7e5: route to aa034f, the existing Flow author, a release frozen on production 0.35.11 (67b80b3) carrying ONLY the canonical visible naming.
  - Every visible name is { Aspect Topic Layer FLOW_ID } with the six-character id: the Claude remote-control session, the Herdr workspace and the display agent. No flow-<16hex> or claude-<hex> may show.
  - Exclude 7ac24a1 and the rest of 0.35.19. Keep ordinary 20, meta 24.0.1, Message compatibility and the store schema.
  - Add a build-failing full-launch regression test, plus Field readback on every surface.
  - Don't wait for Message/MCP, migration or thresholds. Return the source, family and scope packet before building.
  - Keep the three seats and four remote sessions; the in-place rename belongs to Core alone.
- Book 94 «Flow's Ethos, as it now stands» (RGfXmt) published; its comments go to the Ethos seat 43efac.
- The rename is done for the workspace labels and Herdr display names of 5dd7e5, 43efac and 7cd214; aa034f was already done. The four claude.ai remote names (flow-c729…, flow-9eb1…, flow-82e6…, and flow-6c20… = aa034f) cannot be renamed from a pane, because Flow launches with --disable-slash-commands, which removes /rename. Only the living's own rename in the claude.ai list, or the code fix (composition.rs:310 and launch.rs:1647: pass the title as --remote-control), changes them. Sent to Mind.
- From the Ethos seat 43efac: it takes over «Ethos categories and sugar» (804eb9's ethos-book.md, published SuDGmo) as a second edition of its own. That edition carries only the unruled P1–P4, the unlanded sentence of P5 and P7–P12; P6 goes to Flow. whole-flow-ethos.md belongs to the Flow topic (aa034f). It should drop its P10–P14, which repeat the Ethos book, and point to that book instead. 5dd7e5 routes it to aa034f; d68c82 cannot send.
- Book 93 «What a book shows, third edition» (3RH4v8) published; its comments go to the Books seat 7cd214. d68c82 has no runs left; retire it with hm-retire d68c82 once its route is verified.
- From the Books seat 7cd214: nine commented books have no edition and no landing. Each needs its topic owner; 33752b is done, so its five need a new owner.
  - 33752b's: 25-cleaning-skills-2, 14-aspects-same-layer-3, 27-makeshift, and 33-review-is-psyche (comments "Good" / "Good. Land", so it may only need landing).
  - d68c82's: 8-why-fable-not-refreshed, 11-only-psyche-reaches-you, 18-battery-sleep, 42-lost-orders-2, 73-approved-vision-2.
  - Read each full comment from the artifact's comments; the ledger keeps only first and last words.
  - 7cd214 takes «Figures that move» and «Code shown as code».
- Two third editions of «What a book shows» now exist: d68c82's 3RH4v8 (machine-comment and alternatives format) and 7cd214's 2Z7gC9. The Books seat should merge them into one next edition and say which one the living should comment on.
- The Books seat asks for routing: the Tertiary relays book-subject comments to 7cd214 and Ethos comments to 43efac, and 7cd214 gets the relay ledger.
