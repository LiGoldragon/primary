# Over-rectification: viewpoints from the field

Phenomenon: an order against an old way, kept as a standing negative, accumulates as noise. Web research,
2026-10-13, for flow 33752b.

Marks. **Q** means the quote was witnessed in a page fetched in this research. **R** means the quote or
paraphrase was relayed by a search summary, and the primary page was not read. **P** means paraphrase.
"Bearing" lines are this subflow's inference.

## Ranked viewpoints

1. **Simon Willison**, "Highlights from the Claude 4 system prompt", 2025-05-25,
   https://simonwillison.net/2025/May/25/claude-4-system-prompt/ R (the fetched page confirmed the first
   half): "A system prompt can often be interpreted as a detailed list of all of the things the model used to
   do before it was told not to do them." Bearing: this is the phenomenon itself. A prompt becomes a fossil
   record of old faults, and Willison asks whether newer models still need these "system prompt hack[s]" (Q).

2. **Anthropic, Claude Code best practices**, current docs, https://code.claude.com/docs/en/best-practices Q:
   "If Claude keeps doing something you don't want despite having a rule against it, the file is probably too
   long and the rule is getting lost." Q: "For each line, ask: *'Would removing this cause Claude to make
   mistakes?'* If not, cut it." Q: "If Claude already does something correctly without the instruction, delete
   it or convert it to a hook." Q: "A clean session with a better prompt almost always outperforms a long
   session with accumulated corrections." Q: "If you emphasize many lines, none of them stands out." Bearing:
   the vendor's own test for keeping a line is whether it is still needed. A line that forbids a way already
   removed fails that test.

3. **Anthropic Applied AI** (Rajasekaran, Dixon, Ryan, Hadfield), "Effective context engineering for AI
   agents", 2025-09-29, https://anthropic.com/engineering/effective-context-engineering-for-ai-agents Q: teams
   "will often stuff a laundry list of edge cases into a prompt ... We do not recommend this." Q: the right
   altitude sits between "hardcoding complex, brittle logic" and "vague, high-level guidance". Q: the goal is
   "the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome." Q:
   models have an "attention budget". Bearing: every leftover negative spends attention budget.

4. **Anthropic, Claude prompting best practices**, current docs, https://platform.claude.com/docs/en/build-
   with-claude/prompt-engineering/claude-prompting-best-practices Q: "Tell Claude what to do instead of what
   not to do", with "Do not use markdown" replaced by "Your response should be composed of smoothly flowing
   prose paragraphs." Q: "If your prompts were designed to reduce undertriggering on tools or skills, these
   models may now overtrigger. The fix is to dial back any aggressive language." Q: "If your prompts
   previously encouraged the model to be more thorough ... dial back that guidance." Bearing: two points. A
   correction written for one model's fault becomes an over-correction for the next model. A negative names
   the old way without giving the new one.

5. **OpenAI, GPT-5 prompting guide** (Cookbook, archived),
   https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide Q: "poorly-constructed prompts
   containing contradictory or vague instructions can be more damaging to GPT-5 than to other models"; the
   model "expends reasoning tokens searching for a way to reconcile the contradictions" "rather than picking
   one instruction at random." Q (the Cursor case): "Be THOROUGH when gathering information" was
   "counterproductive with GPT-5", because it "often caused the model to overuse tools". Bearing: a stale rule
   that clashes with a new rule is not ignored. The model pays reasoning to reconcile the two. This is the
   shoelace-tripping mechanism.

6. **OpenAI, GPT-4.1 prompting guide**, https://developers.openai.com/api/docs/guides/latest-model/gpt-4.1 Q:
   "trained to follow instructions more closely and more literally than its predecessors". Q: "If there are
   conflicting instructions, GPT-4.1 tends to follow the one closer to the end of the prompt." Q: "It's
   generally not necessary to use all-caps or other incentives like bribes or tips." P: emphasis carried over
   from older prompts can make the model follow those rules too strictly. Bearing: a model that follows
   instructions literally keeps obeying an old negative literally, long after its reason is gone.

7. **Anthropic, Claude's Constitution**, January 2026, https://www.anthropic.com/constitution R: "We generally
   favor cultivating good values and judgment over strict rules and decision procedures, and we try to explain
   any rules we do want Claude to follow." R: training even "quite narrow behavior ... often has broad effects
   on the model's understanding of who Claude is". A rule such as "always recommend professional help" risks
   generalizing to "I am the kind of entity that cares more about covering myself than meeting the needs of
   the person in front of me." Bearing: a rule outlives its case and reshapes the agent's self-model as well
   as its outputs.

8. **Jason Fried and David Heinemeier Hansson**, *Rework* (2010), first on Signal v. Noise. John D. Cook
   quoted it on 2009-07-30: https://www.johndcook.com/blog/2009/07/30/organizational-scar-tissue/ R: "Policies
   are organizational scar tissue. They're codified overreactions to situations that are unlikely to happen
   again. They're collective punishment for the misdeeds of an individual." Bearing: this is the human-
   organization name for the phenomenon. Cook adds (P) that a foolish-looking policy was often sensible when
   it was written.

9. **Kelly Hong, Anton Troynikov and Jeff Huber (Chroma)**, "Context Rot", 2025-07-14,
   https://research.trychroma.com/context-rot R: across 18 models, performance grows "increasingly unreliable
   as input length grows", even on simple tasks, and is worse when distractors are close in topic to the
   target. Bearing: a negative about the old way is the most on-topic distractor possible, because it names
   the very thing being worked on.

10. **Drew Breunig**, "How Long Contexts Fail" and "How to Fix Your Context", 2025-06,
    https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html R: four failure modes, namely context
    poisoning, distraction, confusion, and clash ("new information ... that conflicts with other information
    in the prompt"). Bearing: an accumulated negative is a standing case of clash and confusion.

11. **Jaroslawicz et al. (Distyl AI)**, "How Many Instructions Can LLMs Follow at Once?" (IFScale), arXiv
    2507.11538, 2025-07, NeurIPS 2025. R: the best frontier models reach about 68% accuracy at 500
    simultaneous instructions. Decay comes in threshold, linear and exponential patterns, with a bias toward
    earlier instructions. Bearing: instruction count is a measurable load, and every retained negative adds to
    it.

12. **Castricato, Lile, Anand, Schoelkopf, Verma and Biderman**, "Suppressing Pink Elephants with Direct
    Principle Feedback", arXiv 2402.07896, 2024-02-12. Q: the paper frames the "Pink Elephant Problem", which
    is to stop discussing one entity and discuss a preferred one. R: "mentioning that topic in the LLM's
    prompt makes the model more likely to mention it even when instructed not to". Bearing: this is the
    machine analogue of ironic process. A negative primes the very thing it forbids.

13. **Daniel Wegner**, "Ironic processes of mental control", *Psychological Review*, 1994; white-bear studies
    1987 (JPSP 53:5-13). https://dtg.sites.fas.harvard.edu/DANWEGNER/html/ironic_control.html R/P: intentional
    suppression runs a monitoring process that searches for the forbidden thought, and under load that monitor
    makes the thought more likely. One critic (R) says the popular framing goes beyond the original paradigm.
    Bearing: this is the human root of "don't think of an elephant".

14. **G. K. Chesterton**, *The Thing*, 1929, "The Drift from Domesticity". https://www.chesterton.org/taking-
    a-fence-down/ P: a reformer may remove a fence only after learning why it was put up. Bearing: this cuts
    the other way. A remover must know a rule's reason, which argues for every rule carrying its reason so
    that its expiry can be judged.

15. **Hyrum Wright**, "Deprecation", *Software Engineering at Google*, ch. 15, 2020.
    https://abseil.io/resources/swe-book/html/ch15.html Q: advisory deprecations "don't have a deadline".
    Compulsory deprecation "usually comes with a deadline for removal". Q: "Deprecation warnings can help
    prevent new uses, but rarely lead to migration of existing systems." Q: the warnings "can soon overwhelm
    users of a system to the point where they ignore them altogether", which medicine calls "alert fatigue".
    The same author's law (R, from secondary sites): "With a sufficient number of users of an API, it does not
    matter what you promise in the contract: all observable behaviors of your system will be depended on by
    somebody." Bearing: a standing negative works like an advisory deprecation warning, and it produces alert
    fatigue. Hyrum's law explains why remnants of the old way persist.

16. **Andrej Karpathy**, X post, 2025-05 (status 1921368644069765486; returned 402, not read). R/P: he
    proposes "system prompt learning", in which humans learn by writing explicit notes for next time, and he
    was prompted by Claude's system prompt rule on counting the r's in "strawberry". He followed this with
    "context engineering" on 2025-06-25: R: "the delicate art and science of filling the context window with
    just the right information for the next step." Bearing: this is the case for accumulating lessons. He does
    not address pruning them, so the phenomenon is the unsolved half of his paradigm.

17. **Zhang, Zou, Olukotun et al.**, "Agentic Context Engineering" (ACE), arXiv 2510.04618, 2025-10, ICLR
    2026. R: an evolving "playbook" of strategies, built by incremental curated updates. Wholesale rewrites
    cause "context collapse", and optimizers drift toward a "brevity bias". Bearing: this is the strongest
    counterweight. Accumulated lessons help when they are curated item by item, and blind compression loses
    them.

18. **Arditi, Obeso, Syed, Paleka, Panickssery, Gurnee and Nanda**, "Refusal in Language Models Is Mediated by
    a Single Direction", NeurIPS 2024, arXiv 2406.11717. R: adding the refusal direction "elicits refusal on
    even harmless instructions". Alongside it is **Paul Röttger et al.**, XSTest, arXiv 2308.01263, 2023-08,
    NAACL 2024. R: well-calibrated models should not refuse safe prompts that "use similar language to unsafe
    prompts". Bearing: over-refusal is over-rectification learned into the weights. A negative trained against
    one case fires on the surface features of that case.

19. **Betley et al.**, "Emergent Misalignment", ICML 2025. https://proceedings.mlr.press/v267/betley25a.html
    R: narrow finetuning on insecure code produced broadly misaligned behaviour, and a benign stated motive
    prevented it. Bearing: a narrow correction generalizes beyond its case, and the reason stated with it
    changes what generalizes.

20. **Lynch et al. 2024; Siddiqui et al. 2025** on unlearning (arXiv 2505.22310). R: unlearned knowledge
    returns with a few related examples, or even with retain-set finetuning alone, so unlearning often
    suppresses rather than removes. Bearing: suppression is not removal, in weights as in prompts. A standing
    "don't" keeps the old way alive and only gates it.

Also relevant, one line each. **Marilyn Strathern**, "'Improving ratings'", *European Review*, 1997, p. 308
(R): "when a measure becomes a target, it ceases to be a good measure". The bearing is that a negative rule
becomes the target in place of the outcome. **Cognition (Walden Yan)**, "Don't Build Multi-Agents", 2025-06
(R/P): implicit decisions that conflict make systems fragile, which bears on stale rules across seats.

## Candidate terms for a removal order that is not a standing rule

- **Tombstone, with a grace period.** Origin: Apache Cassandra.
  https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/tombstones.html (R) A
  tombstone is a deletion marker that exists only until every replica has applied the delete. After
  `gc_grace_seconds` (default 864000, ten days) it is purged in compaction. If it is purged too early, the
  deleted data is resurrected ("zombie data"). This is the closest fit: a delete propagates, then the marker
  itself expires. - **Compulsory deprecation, as against advisory deprecation.** Origin: Hyrum Wright,
  *Software Engineering at Google*, ch. 15 (Q above). The compulsory kind has a removal deadline and ends. The
  advisory kind is a standing warning that people learn to ignore. - **Sunset clause.** Rationale relayed from
  Thomas Jefferson to Madison, 1789-09-06. R, via Jeff Jacoby's commentary (the primary page was not
  retrieved): "every constitution, then, and every law, naturally expires at the end of 19 years". The sunset
  idea itself: "a law of limited duration is much more manageable than one which needs a repeal." The search
  did not establish this letter as the origin of the legislative term. - **Repeal, as against prohibition**
  (common legal usage). A repeal removes the old law and leaves no standing counter-law. - **Migration**
  (Wright, ch. 15). This is the finite work that removes the old way's uses, after which no rule is needed. -
  **Pruning** (Anthropic Claude Code docs, Q above). The rule test is "Would removing this cause Claude to
  make mistakes?"

Flow inference, not found in any source: a removal order could carry a tombstone's shape, holding until a
named witness shows that no remnant remains and then deleting itself.

## Not found

- No primary source was found for "every rule has a body count" or "rules are written in blood". The search
  returned only noise. - No statement by Ethan Mollick, Chip Huyen, Lilian Weng or Harrison Chase was found on
  negative-rule accumulation specifically. Chase's LangMem ("procedural memory" as optimized system prompts,
  https://www.langchain.com/blog/langmem-sdk-launch) covers updating prompts, not pruning negatives. - No
  Google (Gemini) vendor guidance on negative instructions was retrieved. - No established term was found for
  "a removal order that is not a standing rule" in prompt or agent engineering. The terms above all come from
  databases, software deprecation and law. - The full text of Karpathy's post (HTTP 402), the original Signal
  v. Noise post, and the primary text of Jefferson's letter were not read. - No controlled study was found
  that measures accumulated stale negatives specifically, as distinct from instruction count or context
  length.
