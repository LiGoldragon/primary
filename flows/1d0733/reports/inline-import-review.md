# Review of «The inline import»

Book: https://claude.ai/artifact/CCFHiycbDtGJFY93SF25UC, version 1791577853-8054, read 2026-10-09 with the Artifact read action.

Verdict: the book cannot go to the living as it stands. P1 targets a file the living has ruled moved. P1 also contradicts the book's own Q1. The context presents as new a form that ethos-zero c2653d already parses with a different meaning. Q3 and Q4 extend the living's Nexus file registry into the ethos import registry, which he never said. The form is sound: there is one distillation section, every code line is 52 characters or fewer, the figure is SVG, and no ASCII is shown.

Origin key: W = witnessed by this review (a probe run or a file read here); R = taken from another report and not re-run; I = this review's own inference.

## Findings

### 1. High: the inline form already parses today, with another meaning (technical truth)
- Section: context, "Two ways to name a type from elsewhere", and the figure.
- At issue: "The inline import, the same key: … `[]  ; imports: none` … `Topic:Name } ]  ;   core's Name`". The figure says "imports section: none / Topic:Name / named where it is declared".
- Conflicts with: ethos-zero c2653d `Conceiving<Reference>` (src/conception.rs, the `Headed`/`Separator::Colon` arm). A colon reference already stands inline in a type position, and its head becomes a Rust source path. W: this review built c2653d (ethos-zero 16.0.0) and generated the book's inline example unchanged. Output: `pub name: Topic::Name`. No `Topic` type is declared, and the field is named after `Name`. `flow:Voice` gives `pub voice: flow::Voice`. Mutex probe a9 shows the same (R: reports/mutex-probe.md).
- Effect: the book frames the inline form as an addition. What it actually proposes is a change of meaning: today the head is a source; under Q1 a capital head would be a declared type name. Neither the context nor P1 says so.

### 2. High: P1 contradicts Q1 and the figure (his words, internal)
- Section: Proposal 1.
- At issue: "A sourced reference, `source:Name`, may also stand where a type is declared … A capitalised source names the core built-ins of the language".
- Conflicts with: Q1's proposed answer "A capital head (`Topic:Name`) declares a type of that name from a core built-in", and with his words "`name` would be one of the built-ins in the core of the language" (flows/d5df1d/vision/ethos.md, 2026-10-09). In his example the built-in is `Name` and `Topic` is the declared type. P1 calls `Topic` a "source" that "names the core built-ins". Separately, P1 asks for a ruling that would settle what Q1, Q2 and Q5 still leave open. This goes against "small, conservative proposals; a proposal is accepted whole" (flows/bad807/vision/distillation.md:16) and "distill one thing at a time" (flows/91ea9f/vision/distillation.md:5), as listed in reports/presentation-psyche-package.md §3.

### 3. Medium: P1's target file is being moved by the living's ruling (book rules, his words)
- Section: Proposal 1, target chip.
- At issue: "`psyche-skills/skills/vision-ethos.md`".
- Conflicts with: his comment in the same thread: "should be psyche-skills/vision/ethos.md" (reports/golden-ethos-comment.md; flows/1d0733/vision/ethos.md). W: the psyche-skills checkout holds this move uncommitted: `D skills/vision-ethos.md` and an untracked `vision/ethos.md`. origin/main 9407b7 still has the old path. The compensation-book-distillation line "a proposal names its authored source under psyche-skills/skills …" now conflicts with his ruling. That conflict is for the main flow to raise, not for the book to settle silently.
- W: the context lines shown around the insertion match main: the "use statements" paragraph, the "What a declaration turns into" heading, and Sources ending `e51411 ethos`, `88475f ethos`.

### 4. Medium: Q3 and Q4 move the Nexus file registry into the ethos import registry (his words)
- Section: Q3 "The anatomy of a registry entry"; Q4 "One registry or two".
- At issue (Q3): "`Entry.{ Key.{ Subaspect.[…] Topic:Name } Location.{ Source:Name Hash.String RelativePath.String } }`", which is offered as the entry of the import registry. At issue (Q4): "held in the Memory of the Nexus that serves it, changed only by payloads on its meta signal. Ethos Zero … receives the environment's registry in its `Generate` request."
- Conflicts with: his words. The `{ Subaspect… Topic:Name }` key, the source hash and the relative path, and "those payloads live on the meta signal (to modify those registries)" all describe how the Nexus locates context files (part (d) of the comment). For imports he said only "We need a whole registry for all this: all of the manifests for where all the different libraries live" and "There's going to be a registry for those as well." Sharing `Location`, "Memory of the Nexus", "only", and the registry travelling in the `Generate` request are the book's own inventions. They are put as proposed answers but never marked as going beyond him.
- Also: `Hash.String` makes a hash a string. The records "identifiers are real types, not strings" (flows/692df8/vision/identifiers.md:7) and "FlowId is a hash" (flows/edf227/vision/identifiers.md:5) point the other way. Low.

### 5. Medium: "Every ethos type name is capitalised" is not true of ethos-zero today (technical truth)
- Section: Q1.
- At issue: "Every ethos type name is capitalised, so the name after the colon is always capitalised; only the head before it can differ."
- Conflicts with: W: c2653d generates `Library [ std:sync ] [ Holder.{ sync<String> } ] [] []` and the inline `Holder.{ std:sync<String> }`. Both emit `pub string_sync: std::sync<String>` (also R: mutex probe a4). `Name::try_from` takes any Rust identifier. vision-ethos (main) has no capitalisation rule. Q1's case argument rests on this sentence. If the sentence is meant as vision, it needs its own ruling.

### 6. Medium: the book introduces names and adds words to his, presented as what he wrote (his words, book rules)
- Section: context.
- At issue: "The example below is the registry key you wrote on 2026-10-09: `Entry` is one key, `Subaspect` an enum of what kind of context module it is (Vision, Knowledge, and more to come), and `Topic` a type over core's `Name`, the camelCase short expression checked at runtime when one is made".
- Conflicts with: what he wrote, an unnamed `{ Subaspect.[Vision Knowledge ...] Topic:Name }`. "Entry", "context module" and "short" are the book's own additions. His camelCase record says "the core:Name type which is "camelCaseExpression" type with runtime checks when creating a new one" (flows/445410/vision/flow.md, 2026-10-09); "short" is not there. Telling him what he wrote also goes against "never tell him what he said; proposals only" (flows/d4ae97/vision/books.md:77) and "A book does not restate the living's words" (compensation-book-distillation).

### 7. Medium: P1 carries undefined terms and an unlisted source (distillation rules)
- Section: Proposal 1.
- At issue: "names the core built-ins of the language; … names a registry of the loaded environment. The colon resolves from the registry or is an error."
- Conflicts with: "A distilled statement carries no undefined term" (vision-distillation, prompt). vision-ethos defines neither "core built-ins", nor "registry", nor "loaded environment". The book itself holds "Core built-ins against intrinsics" and "What the isos environment is" for later. The 2026-08-20 ruling being extended speaks of a manifest: "confirmed, kill the fallback." (flows/2b34fafa/vision/importResolution.md). Putting "registry" in place of the manifest is inference (I). P1 says it is "read with" 2b34fafa, but the Sources addition lists only `d5df1d ethos`, not `2b34fafa importResolution`.

### 8. Low: ethos fragments without their root (book rules)
- Section: Q1, Q2, Q4.
- At issue: "`[ Entry.{ Topic:Name ; types: head Topic,`", "`[ Topic:Name ]`", "`[ Launch.{ Topic:Name …`".
- Conflicts with: "ethos is never uncontextualized" (flows/d4ae97/vision/books.md:7) and "always specify the object type when showing Ethos" (flows/692df8/vision/ethos.md:7), both from reports/ethos-psyche-package.md §M.

### 9. Low: comments sit below their element (book rules, ethos layout)
- Section: P1 code, Q1, Q4.
- At issue: "`flow:Voice } ]`" followed on the next line by "`; Voice, from the flow`" (P1), and "`; head flow, name Voice`" (Q1).
- Conflicts with: "a comment goes above or beside, not below" (flows/e5a0bc/vision/ethos.md:25).

### 10. Low: P1 teaches a code rule without the wrong form (book rules)
- Section: Proposal 1.
- Conflicts with: "Code that teaches a domain-model or code rule explains the Ethos types it uses and their purpose, and shows the wrong and right forms" (compensation-book-distillation). P1 shows only the right form.

### 11. Low: Rust in the prose (book rules)
- Section: Q5.
- At issue: "the generator emits that path, fully qualified as today (`ethos_core::Name` for core)", and the quoted rustc message.
- Conflicts with: "no Rust types; ethos is the language for types" (flows/e5a0bc/vision/books.md:31). `ethos_core` is an invented crate name. W: the claim itself is true; rustc answers "cannot find type `Name` in crate `core`" for `pub type Topic = core::Name;`.

### 12. Low: record paths in the context section (book rules)
- Section: context.
- At issue: "(flows/d5df1d/vision/ethos.md, 2026-10-09; flows/445410/vision/flow.md, 2026-10-09)", "(flows/2b34fafa/vision/importResolution.md, 2026-08-20)".
- Conflicts with: the rule's allowance, "A proposal may cite the record it distils by path and date", which covers proposals and not the context. These are record paths, not runtime paths, so this is borderline.

## Checked and found sound
- W: the "Today" example generates on c2653d. `Topic.Name` with `core:Name` emits `pub type Topic = core::Name;`, an alias. This agrees with Q2 depending on the types book and with Q5's compile-failure claim.
- W: the context's statement that a source is emitted as a Rust path agrees with c2653d.
- W: the import head is a single segment (`Source` from the protos head, which ends at the first `.`, `!` or `:`), as reports/mutex-probe.md says. The book does not claim otherwise.
- W: blake3 appears in 13 LiGoldragon checkouts at their present HEADs, including content-identity and sema-engine, and in none of ethos-zero, protos, datom-codec or Curriculum. This matches Q3. The checkouts' revisions were not pinned.
- The 2026-08-20 citation is correct: colon resolves from the manifest or errors.
- Form: one distillation section (P1) with a target, an insertion point and context. All 8 code blocks have lines of 52 characters or fewer (W, measured). The figure is SVG, with no ASCII shown. There is no history narrative and no version, socket or command in the context. Whether a Sonnet or Haiku subflow drew the figure from an ASCII source cannot be told from the page.

## Sources
- Artifact CCFHiycbDtGJFY93SF25UC, version 1791577853-8054.
- flows/1d0733/reports/golden-ethos-comment.md; flows/1d0733/vision/ethos.md; flows/d5df1d/vision/ethos.md; flows/445410/vision/flow.md; flows/2b34fafa/vision/importResolution.md.
- flows/1d0733/reports/ethos-psyche-package.md; flows/1d0733/reports/presentation-psyche-package.md; flows/1d0733/reports/mutex-probe.md.
- Skills loaded: compensation-book-distillation, vision-book, operation-flow-evidence.
- psyche-skills main 9407b7, skills/vision-ethos.md, and its working tree.
- ethos-zero c2653d src/conception.rs. Probes ran on a local build of c2653d. Fixtures are in this flow's scratchpad, under `inl/`: today, inline, lower, lc, a4, a5, c.rs.
- Provenance receipt: unavailable; no PROVENANCE handoff was given.
