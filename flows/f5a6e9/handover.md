# Handover: Psyche::Flow Primary f5a6e9 to its successor

## Role and topic
Psyche Fable, Primary, topic flow (title `Psyche.{ flow Primary … }`). Designs the Flow Nexus as books for the living and rules, as current best, what Mind's build and Field's tests ask. Secretary and only route: Psyche::Flow Secondary 9fed42 (Opus); Mind Astra 0c85a3 may be addressed directly. Core relay seat: 445410.

## Governing state
- The buildable design, governing for Mind and the tests: `flows/f5a6e9/reports/flow-buildable-design.md` on main at commit `e1e8d1843107a1f7f01106f1ef3901bd671d3c82` («f5a6e9: the order of checks at Deliver»), design blob `af0f9d565e2bfae86917dc19f76a031a2a1cb012`. It holds one consolidated Flow ethos (Library, Memory, flow-socket Signal, meta-socket Signal), the rules, today versus to build, and section 4's open rulings; every part is marked approved, open before the living, or current best.
- Raw psyche records of this flow: `flows/f5a6e9/vision/{flow,ethos,messaging,books,vision,contextModules}.md`, `flows/f5a6e9/notion/flow.md`.
- The log: `flows/f5a6e9/log.md` (every ruling given, with its reason, in order).

## In flight, not yet published
- The wake-module fold: a wake composes whatever modules the registry holds for the recipient's topic at the moment it wakes (an empty set valid); the forgotten-key case removed; Unknown.Key no longer a refusal of Lock or Deliver (stays for a Launch naming a module and for Forget); NoLayer stays at Lock and Deliver. A subflow of f5a6e9 was folding and publishing it under the lock as «f5a6e9: a wake composes what exists; Unknown.Key leaves Lock and Deliver». If main does not carry that commit, apply and publish it first; Astra and flow-test were told it is coming.

## Open before the living (through 445410's open books), one at a time
1. «The Flow Nexus vision», third edition — https://claude.ai/artifact/7zm4sg5pTx71GRGbBWisW4 — three rulings (the ethos file at `psyche-skills/vision/flow-ethos.md`; the dependency line; where a request lands in an awake flow).
2. «Stored type and datom form», second edition — https://claude.ai/artifact/FadJBFZEhkRFt4Dd3JZuyt — four rulings (Encodable; Bytes<N>; Flow's Library; simple and extended forms). Its proposal 3 is superseded by the design's Blake3 line.
3. «The Nexus starts» — https://claude.ai/artifact/49gSuEYkmo5dWkFmeNKHVb — one ruling (the meta socket's Configure payloads).
Approved and landed: «Speech across aspects» (psyche-skills commit 850fd27). Mind's book «What the new Message does with the old store» decides Flow and Message together; the design's discard of the old store is current best, marked as resting on the living's 2026-09-24 condition.

## Open items and holders
- Mind 0c85a3 (Astra) builds Flow against the design; 73ada7 holds the Message design (main, aligned to the design) and the refusal map; Field 42265e runs flow-test and message-test against pushed revisions on Prometheus. Their questions arrive through 9fed42; answer as rulings marked current best, fold them into the design, publish, send the revision and blob to 9fed42.
- Design points waiting on the living: the flow id as three words or two; the dense title string's type; the address form (Address.{ Aspect Topic Layer }) pending ruling 1 of the Flow Nexus vision; Topic:Name and Bytes<32>, which ethos-zero cannot yet express (the build carries String).
- vision-flow's Today section is knowledge, landed by Mind in knowledge-flow; vision carries only the conceptual account.

## Standing limits
- Books: file-line proposals, one proposal per book, each section opening with the file, lines removed and added, a ruling; a `## Distillation` heading; code lines at most 52 characters; three-space ethos indentation; authored whole by this seat, the publisher only places it; a block written in a turn that incoming messages interrupt does not reach the transcript — write the source file into `books/` and publish from the path.
- The living's words travel only as psyche messages (`hm-send TARGET --psyche CONTEXT VERBATIM`); a message resting on them sends the psyche first.
- Messenger: hm-send and orchestrate on PATH are broken builds; send with `PATH=/nix/store/vsj5mw3jfbwmclzpa4gqlgysvxfip3g2-orchestrate-0.37.0-profile/bin:$PATH FLOW_ID=<self> /nix/store/pqx78mxcdwpbwzhicgiprvfj5qq0lnxs-messenger-clj-0.3.0/bin/hm-send …` until Field's repair ships.
- Publishing: one publisher subflow at a time; a full LOCAL clone of /home/li/primary with origin re-pointed to GitHub (never shallow or filtered, never the slow remote clone); load operation-orchestrate, then the lock in the four-field form `orchestrate 'Lock.{ PrimaryPublish f5a6e9 [ /home/li/primary/.PrimaryPublish.lock ] «Publish f5a6e9 lane» }'` taken only around commit and push and released once; before the push, only the lane's paths may differ and the tree's file count must be at least main's; never push without the lock; never force.
- Heavy builds and tests run on Prometheus through Nix against pushed revisions; never locally.
- A new flow's first response is a presentation of its context in its role, after subflows reinforce it; never READY.
