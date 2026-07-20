# Psyche-vision context handover — the Protos engine effort (2026-07-20)

## HEALTH WARNING
This carries ONLY the psyche's vision: verbatims, rulings, hedges, open questions, durable pointers. No agent chronology. Verify every factual claim in the named artifact before acting. Quotes marked as his are his; derivations are flagged and are NOT rulings.

## 0. Binding conduct (unchanged laws, plus two new)
- NEVER use the Fable model for subagents; Opus at most. Workflows forbidden — subagents only.
- All-green truthful denominators; no bypasses seated as design; wrong/negative examples forbidden in skills; fabrication barred, disclosure never; the psyche is the human.
- Field-name TOTAL ban everywhere in the Protos family; positional disambiguation; deterministic ordinal Rust names (landed, green).
- NEW — the Codex delta channel: "codex has been working for a while, you cant just edit the document. anything that was added after the first version needs to be passed to him as an additional instruction." Every new ruling goes to Codex as a paste-ready numbered delta (ledger reached line 25 this session), never only a document edit.
- NEW — consult Spirit before raising joints: "retype of course. spirit would have answered that" — questions derivable from accepted intent must not reach the psyche.
- Communication: no first person in Spirit records ("'I' is ambiguous. Ruling psyche is not"); no unexplained agent jargon ("what mirror?" — his rebuke); plain ASCII visuals, multiple layers, no Mermaid ("visuals are best. give me multiple layers").

## 1. Vision settled this session (his words)
- Two-way transform: "the textualform can also be generated from source files, and then it is used to generate a nametree + encodedform" / "So we get a two-way transform". TextualForm is the pivot; one StructureTree drives both directions.
- Rust emission: "rust emissiong must be done through the same textualform machinery that schema/logos/nomos use, only it would have a custom structuraltree which is quite different than protos primitives." (Manager's one-engine/data-not-code reading recorded as derivation, NOT explicitly confirmed.)
- No-strings invariant: "basically, in the nomos transformation (schema to logos), there shall be *no string manipulation/introduction/reading of any kind*"; walkers at the boundary: "that is necessary."; "make the invariant for nomos transformation in its architecture documents." — SEATED: core-nomos ARCHITECTURE main c1c60b38 + protos name-table ARCHITECTURE. Architecture files DO hold invariants (verified convention).
- Typed macros: "note that our macros are on typed data, so its all a bit different".
- Identifier: "actually, I was complicating things; the ID is the variant with its inner u16 (16 bits should be lots for a language)" / "Schema.Id16 Logos.Id16 etc" — enum, variant IS the slice.
- Nametables: "yea, one nametable for each component. nomos uses the schema nametable to populate the logos nametable (and uses its own to read/write from/to its own encodedform)"; slicing lean confirmed as "so the nametree is composable."
- Manifest: "yes, full explicit manifest. dont ignore the types the machine wants - everything is typed data" — family principle, lifted to epic.
- Mouth retype: "retype of course." — composed table retyped at the mouth in the ONE slicing cascade.
- Rename: "full rename green light. It was from the start but agents tend to misunderstand my drastic engineering approach. There might be a good spirit record to flesh out of this." — Core*->Encoded* concrete types, authorized, NOT yet executed.
- Escape: "whatever. $ is pretty standard"; survey delivered; two-primitive recommendation ($ realize + $ splice) — see §5.5.

## 2. Rulings executed this session (settled + done; verify at pointers)
- "I said this several times... a separate repo" + "consolidate into protos." — EXECUTED: github.com/LiGoldragon/protos workspace (5 machinery crates), consumers re-pinned, all flake checks green. Old five repos DEPRECATED.
- "you mean when its merged? then delete of course. codex is merging now" — delete-on-merge authorized; NOT yet met (cascade unmerged); condition beads primary-56d1.50–.54.
- "I dont care about byte-exactness. get rid of that. working programs is what we want." — byte goldens deleted in core-nomos.
- "if we have a generator that works... we'll deprecate and eventually delete them" — schema-language/schema-rust deprecated, never reworked.
- Bootstrap: "We should get codex to adapt components using it, and he can bugfix it on a 'bootstrap' branch/worktree... cross examination once in a while..." — bootstrap workflow live; cross-examinations executed twice (see §7).
- "fix the bug and audit the work that codex is now merging in main" — derive field_meta fixed (protos 7e60f60f, core-schema 26a48077, all green); audit: merged core-nomos internally sound and stringless (27/27), but working-program acceptance BLOCKED until the daemon cascade re-pins (two type universes).
- Hygiene: "yes, clean up the debt" (~349 MB, nothing lost); 11 abandoned worktrees — "get an agent to see that the underlying principle was merged in main, or that it was rejected and why, and if those lights turn green, remove..." — all 11 green, removed; "I think those components should be marked as inactive and those branches removed. nothing I can't recreate" — domain-criome + terminal INACTIVE; "yes, retire the contract repos too" — signal-domain-criome + meta-signal-domain-criome INACTIVE.
- Spirit-port constructs: streaming "yes"; aliases — his q "why do you want aliases?" then NameTree-transparency accepted by delegation; interface variants approved; SEMA: "clarify. you can rework sema layouts if it's a better approach" — redesign-first approved with two gates (up-close review before implementation; migration proof on isolated snapshot only). Snapshot at ~/.local/state/spirit-db-test-copy.sema.

## 3. The delegation and what is OWED
"advance everything by your recommendation; explain later." — advanced: slicing slate 2–6 (LogosStandard own variant; generated constants; type-id mirror separate; eager derived names; slicing cascade AFTER rename), Spirit-port slate, Stream unblock (closed relation REPLACES minted-kind route; kind-vocabulary hook deferred until genuinely needed). EXPLANATIONS ARE STILL OWED to him for this batch.

## 4. Derivations pending his confirmation
- Manager's Rust-emission reading (one shared engine, Rust knowledge as per-type StructureTree data, names at emission boundary) — mirrored, not confirmed.
- Manager's two-way-pivot reading — recorded pending confirmation.

## 5. OPEN questions on his desk (each self-contained)
1. SEQUENCING (asked, unanswered): slicing landed BEFORE the ruled after-the-rename order on Codex's producer branches. Accept the inversion (merge once fixed, rename train immediately after — manager lean) or enforce ruled order?
2. SEMA redesign six-item slate (split actor topology; v14 two-family storage; archive-as-lifecycle-state; backpressure Close vs Loss; generator boundary; frozen-v13->fresh-v14 reject-not-coerce migration) — manager recommends all six (Close on 4). Unruled.
3. Source-surface five-item slate (interface alternatives [Closed Opened.SubscriptionToken]; streaming seventh document slot [{OpenSubscription SubscriptionOpened SubscriptionToken IntentEvent CloseSubscription}]; alias admission mechanism; imports as manifest edges only; actor adapters) — manager recommends all five. Unruled. Both codec outputs above are Codex-claimed verbatim, unverified.
4. Spirit record on the drastic-engineering reading default — HIS to flesh: higher abstraction than the rejected draft, not first person, "ruling psyche" voice.
5. Escape-kind set: $ realize + $ splice as the closed set — recommended; arguably covered by the blanket delegation but NOT explicitly seated; confirm before treating as law. Also core-nomos main dropped << >> citing "we won't use <<>> either".
6. cloud + meta-signal-cloud are LIVE consumers of the retired signal-domain-criome contract — migrate off or retire them too?
7. Orchestrate daemon deploy: deployed 0.14.1 lacks git AND ssh in PATH (ConcludeWorktree Rejected broken), has no conclusion/reap levers (11 tombstone registry rows persist; 0.15.x reaps them), and the edit-coordination packet names admin commands that do not exist on the deployed build. One deploy + PATH fix clears all; he has not said whether this front or the OS front owns it.
8. CriomOS flake.nix/flake.lock mismatch on criomos-home input (lock correct, nix hardcodes stale rev) — regression risk on next flake update.
9. Producer branches HOLD conditions (delta 23): S2 panic->typed error/sealed type; S1 doc drift (README says Encoded over Core* code). Codex has the delta; verify before merge.
10. Deferred-not-forgotten (delta 25): alias end-to-end textual proof, streaming frame generation, interface encode round-trip, working-program acceptance.

## 6. Carried from the previous handover, untouched this session
Review-pile remnants (.9 syntax slate, .10 format-upgrade half, .12 lost bootstrap question — only HE can restate it, .14 reports/logos hygiene, .38 wire header layout); clarification-skill discussion (his words in prior handover); public-repo verbatims question; CommitSequence item-envelope rendering under the total ban (primary-56d1.43).

## 7. Durable pointers (verify here)
- Tracker epic primary-56d1 (captures of every verbatim this session); .48 now OPEN; .50–.54 deletion conditions.
- Design authorities this session: reports/logos/id-namespace-slicing-design-v1.md (revised for the enum ruling, 7be16045d); reports/logos/protos-engine-next-layer-design-v1.md (compiling-sketch layer; rulings seated; SourcePath(String) flagged residual untyped, 53b215d5d); reports/logos/macro-escape-taxonomy-v1.md; reports/logos/protos-engine-codex-prompt-v1.md (launch artifact — superseded by the delta channel for the running Codex).
- Codex delta ledger: lines 11–25 issued in chat this session (consolidation, derive fix pins, two-way pivot, nametable-design warning, identifier ruling, alias route, redesign gates, acceptance confirmations, cross-exam holds). The running Codex has ONLY what was pasted to him.
- Producer branches: protos c7510d35, core-schema 827995c3 — HOLD; cross-exam verdict: shapes match ruled design, 96+25 green, S1/S2 before merge; transparent-alias mechanism exists ONLY there.
- Codex agent artifacts (unverified): agent-outputs/ProtosEngine/SpiritSemaRedesign/spirit-sema-daemon-redesign.md; his claim of two-way manifest foundation "full-Nix-green in protos and core-schema".
- Merged core-nomos: stringless engine at 61acdf22, ARCH invariant at c1c60b38; working-program proof blocked on daemon cascade re-pin (nomos-engine cannot compile against it yet — two type universes).
