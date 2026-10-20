Evidence for «How Ethos works: the basics», edition 3 (ethos-v1-3.md). Not book text.

Question list and inferences: flows/d68c82/receipts/open-questions-2026-10-18.md, Ethos section, written by d68c82, so they are claims. Quoted words come from the record named on each question. The record headings give 16:41Z for the 10-17 comment; the receipt gives 10:41 local, the same moment. E5–E8 were spoken as chat orders or questions, so no vision record holds them. For those, the source is the receipt's verbatim, checked against d68c82/log.md where the log has it. The 10-18 10:19 transcript was not read here.

The receipt's inference for the whole topic: no book on Ethos itself reached him in the period. His syntax points (category vectors, names, method casing, white brackets) got assurances and more old-form examples, never an Ethos book that answers them.

Two facts weigh on every verdict:
- «Ethos categories and sugar» (SuDGmo) was published on 10-18 after the receipt was written, then republished with figures. Sources: d68c82/log.md, 10-18 entries; flows/804eb9/orders.md item 00.
- Edition 2 (ethos-v1-2.md) still had gaps:
  - The white-bracket rule was missing, though P22's example used the sugar.
  - The category-vector rule was folded into an association alternative (P22).
  - The extendable enum was missing.
  - His own asks sat at P19–P24, behind 500 lines of the module view.

## E1 "First" what?
- His words: "\"First\" is a bit confusing: \"First\" what?" (d68c82/vision/ethos.md:218, 2026-10-17T16:41, on Today 2nd P5). The same comment opens with: "you create a vector in the category instead of repeating the category for every entry". P5's example held `Prompt.[ System First ]` and `Placement.{ Key Prompt }` (flows/39bd0c/books/08-today-as-psyche-2.md:75).
- Inference: supported in part. His words show the Ethos reached him inside another subject's book, in the criticised form. They do not say whether an answer reached him. Edition 2 answered "First" (P23/P24) but buried it at P23. It also dropped the category-vector statement from the same sentence, so the cure for "First" was missing: name each category instead of numbering it.
- Edition 3: Proposal 1 (the category holds a vector of its entries, figure 6, with SystemPrompt and StartupPrompt in place of First); Proposals 2 and 3 (a name says what it names).

## E2 lowercase capabilities: does it compile?
- His words: "I don't know if that actually compiles because, where you have `brief`, `compose`, `name`, and `roles`, these are all lowercase." (d68c82/vision/ethos.md:218). Related: things that are not types or traits are uncapitalized camelCase (d68c82/vision/naming.md:3).
- Inference: supported. He asked for a compile witness. Edition 2 P19 gave only the rule.
- Witnessed for edition 3:
  - Proposal 4's ethos block Checked at d4a630b.
  - Inspect generated `fn brief(&self) -> String;` and `fn setBrief<N: Named>(&mut self, input: N);`.
  - That Rust, with hand-written impls, compiled with `rustc -D warnings` on the remote builder (prometheus): /nix/store/4p50ysv83hbizcyg63s66nz1gy7g1a4k-capability-casing-compiles.
  - The rkyv derive lines were stripped for that compile, because they need the rkyv crate. The datom derive is behind a feature that was off.
- Edition 3: Proposal 4 (the rule, its ethos, the Rust it generates, and figure 7 on what a symbol's first letter names).

## E3 white brackets and braces
- His words: "visually it could help if we use the white. In the same way, when we declare a struct, we could use the white braces" (d68c82/vision/ethos.md:218). Earlier: "a white square bracket. I want to use that as sugar in ethos, as a special syntax at the right layer of interpretation" (d68c82/vision/ethos.md:83, 2026-10-16).
- Inference: supported. Edition 2 had no proposal for the sugar and still used it in an example.
- Witnessed: d4a630b reads both sugars. src/sugaring.rs rewrites them after protos and before conception. `Batch.{ BatchName ⟦ Count ⟧ }` generates `count_vector: Vec<Count>`, and `⦃ BatchName Count ⦄` generates a struct.
- Edition 3: Proposal 6 (white brackets, the layer, figure 8); Proposal 7 (white braces). Proposal 28's example is now plain, so it no longer leans on unruled sugar.

## E4 extendable enum
- His words: "this special syntax for a sort of extendable enum concept, which is differentiated by the user-made entries being uncapitalized" (d68c82/vision/ethos.md:230).
- Inference ("Chat … put 7 questions back to him; no book followed"): his words do not decide it. He asked once ("I also want to talk about"), so nothing shows that it recurs. Edition 2 had no answer.
- Edition 3: Proposal 8 (the definition in his terms, with figure 9). It has no code block, because the checker has no extendable-enum semantics, and a lowercase entry is refused by Conform (books/joint-ethos-audit.md).
- Overlap: books/joint-ethos-extendable-enum.md P1 carries the same definition. Its other proposals (the made entry's type name, declaration marking, generated Rust, promotion, Topic) stay there.

## E5 "Have they been done? I don't even know."
- His words: "I want to review the flow, the whole flow, with all of the ethos and the ethos proposals. Have they been done? I don't even know." (d68c82/log.md:2125, verbatim in the log).
- Inference: supported. He states that he does not know.
- Edition 3 carries every open Ethos syntax proposal (Proposals 1–38). Flow's own Ethos is outside volume 1: it is in books/whole-flow-ethos.md, which is not ready for publication per the 17c364 notices in flows/804eb9/log.md.

## E6 "Did you make the book for the changes I want to make in Ethos?"
- His words: d68c82/log.md:2146 (verbatim in the log).
- Inference: supported. He had not seen it. The book existed but was held, per the d68c82 log, 10-18.
- Edition 3 answers by containing each change he named:
  - category vectors (P1);
  - First (P2, P3);
  - lowercase methods (P4);
  - Library.{ on one line (P5);
  - white brackets (P6) and braces (P7);
  - extendable enum (P8);
  - every file a vector (P9, P10);
  - traits on every root (P12, P13).
- These come first, in the order he raised them.

## E7 "the ethos book that I've been asking for all day yesterday, which I either didn't see or wasn't made"
- His words: the receipt's verbatim. d68c82/log.md, 10-18, "not seen or not made", is consistent.
- Inference: supported, and the record explains it. 804eb9's send to d68c82 stayed Queued (d68c82/log.md, 10-18 "Found:" entry).
- Edition 3 is the book itself: figures 1–4 first, then the module, then his asks as Proposals 1–13.

## E8 "We have an ethos flow, right?"
- His words: the receipt's verbatim only.
- Inference: his words do not decide it. They show he does not see the Ethos flow's output.
- No proposal or figure in a book about Ethos's basics answers this. It is a Flow-topic fact (Psyche ethos Secondary 804eb9). Not answered in volume 1.

## E9 "explained back to me with visuals and show me how ethos works"
- His words: "I want to see all of that explained back to me with visuals and show me how ethos works. We can do it like a three-volume thing but let's just start with the basics" (flows/804eb9/vision/ethos.md:9).
- Inference ("Unanswered. Volume 1 is being written"): supported. Edition 2 had four figures before the module, one of which took T1a's side.
- Edition 3 has nine figures:
  - 1, 3, 4 and 5 kept.
  - Figure 2 made neutral: "a file" holds the roots.
  - New, each inside the proposal it answers: 6 category, 7 casing, 8 the sugar layer, 9 extendable enum.

## Tension found
- vision/protos.md names five delimiter pairs. The checker reads ⟦ ⟧ and ⦃ ⦄ as protos enclosures (src/sugaring.rs). So Proposal 6's sugar layer sits on a protos change that no proposal states. Figure 8 does not say protos reads them. This belongs to the protos topic or volume 2.
