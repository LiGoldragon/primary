# People who held the idea: admit the unknowns before designing

Research for flow 33752b, 2026-10-12. Web research authorized by the living.

## The idea being matched

Before designing or proposing, admit what you do not know; list the unknowns
judged against a complete concept (a "golden system", a role model of the
whole); a good idea holds together like a person, consistent and congruent;
the failure mode is forcing puzzle pieces together to make them fit rather
than finding which pieces are missing.

Four parts, so that each candidate can be judged on each:

- A. Admit ignorance first (list the unknowns before building).
- B. Judge the unknowns against a complete concept (a whole, a golden
  model, a reference).
- C. A good idea is whole: consistent, congruent, like a person.
- D. The failure mode is forcing pieces to fit instead of finding the
  missing ones.

Nobody found holds all four as one doctrine. The closest matches are
listed first, then the partial ones. "Verified" means the quoted words
were read in the source text itself (book scan, journal PDF, original
blog post, archive transcript). "Unverified" means the words were only
seen in a secondary source (Wikiquote, a review, a summary).

## Verification method

Quotes were taken from fetched sources: the Harvard copy of Pólya's list,
the Internet Archive text of Brooks's Anniversary Edition, the Caltech
library page of Feynman's address, Darwin Online's manuscript page, the
Gutenberg Jowett text, the Parnas and Clements PDF, the Rittel and Webber
PDF, the Cambridge front matter of Dewar's book, the matthiasn
talk-transcripts copy of Hickey's talk, Bland's Strategyzer article,
Nygard's Cognitect post, Ubl's post, and Merck's UX Strategy Kit page.
PDFs were read with pdftotext. Where a source could not be reached (HBR
full text, the Alexander books themselves, Rumsfeld-era 1968 trade
press), the entry says so.

## The best matches

### 1. George Pólya, mathematics

Work: *How to Solve It*, Princeton University Press, 1945 (2nd ed. 1957).
Copy read: https://legacy-www.math.harvard.edu/~knill/teaching/math22a2018/lit/PolyaHowToSolveIt.pdf

Verbatim (verified, the "How to Solve It" list, phase one):

> What is the unknown? What are the data? What is the condition? Is it
> possible to satisfy the condition? Is the condition sufficient to
> determine the unknown? Or is it insufficient? Or redundant? Or
> contradictory?

Also on the list: "Separate the various parts of the condition. Can you
write them down?" Secondary sources quote "It is foolish to answer a
question that you do not understand" (p. 6; unverified at source).

What he built: a four-phase checklist (understand, plan, carry out, look
back) of heuristic questions, to be asked before any plan is devised. The
first phase is entirely about naming the unknown and the data.

Match: strongest on A. The unknown is literally the first item, and the
condition is checked for sufficiency and contradiction before solving.
"Contradictory?" is a consistency test on the problem statement, which
touches C. Differs: Pólya's "unknown" is the single thing the problem
asks for, not a register of what the solver is ignorant of; there is no
golden whole to judge against (B), and D appears only as "Look at the
unknown!" and "vary the problem".

### 2. Fred Brooks, software engineering

Work: *The Mythical Man-Month*, 1975, ch. 4 "Aristocracy, Democracy, and
System Design"; Anniversary Edition 1995. Text read:
https://archive.org/details/MythicalManMonth (djvu text).

Verbatim (verified):

> I will contend that conceptual integrity is the most important
> consideration in system design.

> It is better to have a system omit certain anomalous features and
> improvements, but to reflect one set of design ideas, than to have one
> that contains many good but independent and uncoordinated ideas.

Also: "The joy that stirs the beholder comes as much from the integrity
of the design as from any particular excellences." (Reims cathedral.)

What he built: a principle and an organizational method: one architect
(or a very few agreeing minds) owns the conceptual integrity; architecture
is separated from implementation. *The Design of Design* (2010) continues
it; Goodreads attributes to it "Sometimes the problem is to discover what
the problem is" (unverified at source).

Match: the strongest statement of C and D found. "Many good but
independent and uncoordinated ideas" is the puzzle-pieces failure named
exactly; omitting a good feature to keep the whole is the opposite of
forcing it in. Differs: Brooks does not start from a list of unknowns (A);
his safeguard is a single mind, not a register.

### 3. Christopher Alexander, architecture and design theory

Work: *Notes on the Synthesis of Form*, Harvard University Press, 1964;
*The Timeless Way of Building*, Oxford University Press, 1979; *The Nature
of Order*, 2002–2005.

Verbatim, *Timeless Way* (verified at a full-text copy,
https://lib.fo.am/the_timeless_way_of_building, section "The Quality"):

> There is a central quality which is the root criterion of life and
> spirit in a man, a town, a building, or a wilderness. This quality is
> objective and precise, but it cannot be named.

Wikiquote gives, as *Timeless Way* p. 31 (unverified at source):

> A thing is whole according to how free it is of inner contradictions.
> When it is at war with itself, and gives rise to forces which act to
> tear it down, it is unwhole.

*Notes on the Synthesis of Form*, as quoted by Richard Gabriel in "Notes
on Notes on the Synthesis of Form"
(https://www.dreamsongs.com/Files/NotesOnNotesPresentation.pdf; unverified
against the 1964 edition):

> We should find it almost impossible to characterize a house which fits
> its context. Yet it is the easiest thing in the world to name the
> specific kinds of misfit which prevent good fit.

What he built: in *Notes*, a method: list the binary "misfit variables"
between form and context, map their interactions, decompose the graph
into nearly independent subsystems, and design to drive all misfits to
zero (the Indian village study had 141 of them). Later, the pattern
language and the fifteen properties of wholeness.

Match: C exactly ("a man, a town, a building": the whole is likened to a
person; wholeness is freedom from inner contradiction). *Notes* is the
nearest thing found to B plus D: good fit can only be approached by
naming the misfits, that is, by naming what is still wrong rather than
asserting what is right. Differs: Alexander's misfits are failures of
fit, not gaps in knowledge (A); Gabriel's critique (same PDF) is that the
mathematical decomposition did not work.

### 4. James A. Dewar and RAND, planning

Work: Dewar, Builder, Hix, Levin, *Assumption-Based Planning: A Planning
Tool for Very Uncertain Times*, RAND MR-114-A, 1993; Dewar,
*Assumption-Based Planning: A Tool for Reducing Avoidable Surprises*,
Cambridge University Press, 2002. Front matter read:
https://assets.cambridge.org/97805218/06534/frontmatter/9780521806534_frontmatter.pdf

Verbatim (verified, the book's own description):

> Assumption-based planning (ABP) is a tool for identifying as many of
> the assumptions underlying the plans of an organization as possible and
> bringing those assumptions explicitly into the planning process.

> ... rooting out those vulnerable, crucial assumptions that, through
> familiarity or other reasons, have gotten buried in one's thinking.

What he built: a five-step method with a vocabulary: list the
assumptions; keep those that are both load-bearing (the plan fails if
they fail) and vulnerable (likely to fail in the horizon); define
signposts (warning signs); shaping actions (to control the assumption);
hedging actions (to survive its failure). Chapter titles verified in the
front matter.

Match: the most developed register of the kind asked for (A). "Buried
in one's thinking" is the admission-of-ignorance move. Differs: ABP is a
post-planning tool applied to an existing plan, not a pre-design step
(Dewar says so in ch. 9, "Why we circumscribed the role of ABP");
nothing on wholeness (B, C).

### 5. The 1960s defense engineers: "known unknowns"

Work: Walter Andrews, "The 'Known Unknowns' And The 'Unknown Unknowns'",
*Armed Forces Journal* 106(15), 7 Dec 1968, reporting Lt. Gen. William B.
Bunker; Hudson Drake (North American Rockwell), 1968 Aerospace Industries
Association study; "unk-unks" in *Fortune*, Aug 1969. All via
https://en.wikipedia.org/wiki/There_are_unknown_unknowns (unverified at
the original 1968 sources).

Verbatim, Bunker 1968 as quoted by Wikipedia (unverified):

> there are two kinds of technical problems: there are the known
> unknowns, and the unknown unknowns.

Rumsfeld, 12 Feb 2002 (verified via the Wikipedia transcript of the
briefing):

> there are known knowns; there are things we know we know. We also know
> there are known unknowns ... But there are also unknown unknowns—the
> ones we don't know we don't know.

What they built: a vocabulary for weapons-system procurement that now
appears as a 2x2 matrix in project and UX practice. One living instance:
Merck KGaA's UX Strategy Kit "Knowns and Unknowns Framework"
(https://strategykit.liquid.merck.design/methods/knowns-and-unknowns-framework/,
verified): "This includes any subject that you are aware exists, but
don't know anything about" and "This is where a team often stands at the
beginning of a new project."

Match: A as a named category. Differs: no whole to judge against (B); the
matrix is a sorting device, not a design discipline.

### 6. Gary Klein, decision research

Work: "Performing a Project Premortem", *Harvard Business Review* 85(9),
Sept 2007, pp. 18–19. https://hbr.org/2007/09/performing-a-project-premortem
(summary and opening read; full text paywalled). Also "The Pre-Mortem
Method", *Psychology Today*, 14 Jan 2021 (verified).

Verbatim (verified, HBR opening):

> too many people are reluctant to speak up about their reservations
> during the all-important planning phase

Verbatim (verified, Psychology Today):

> There is silent pressure in these meetings not to surface doubts that
> might disturb the team's harmony.

What he built: a 20–30 minute exercise. The team is told the plan has
already failed; each member writes the reasons; the list is read out and
the plan revised. Grounded in Mitchell, Russo and Pennington's
"prospective hindsight" (1989), which Klein cites in HBR according to
secondary sources (unverified at source). Veinott, Klein and Wiggins
(2010) found it reduced overconfidence more than critiques or pros-and-cons
lists (verified in the Psychology Today piece).

Match: A, by a trick: imagining the failure licenses people to say what
they do not know. Differs: it is run after a plan exists, and it lists
causes of failure, not unknowns; nothing on wholeness.

### 7. Richard Feynman, physics

Work: "Cargo Cult Science", Caltech commencement address, 1974;
*Engineering and Science* 37(7). https://calteches.library.caltech.edu/51/2/CargoCult.htm

Verbatim (verified):

> The first principle is that you must not fool yourself—and you are the
> easiest person to fool.

> you should report everything that you think might make it invalid

Also: "a kind of utter honesty—a kind of leaning over backwards" and
"bending over backwards to show how you're maybe wrong".

What he proposed: a norm, not a tool: publish what could invalidate the
result; he names the Millikan oil-drop history as the failure of people
discarding results that were "too far off".

Match: D as a moral rule. Discarding the number that does not fit
Millikan's is forcing the piece. Differs: there is no list, no whole, no
design step; the subject is reporting, not designing.

### 8. Charles Darwin, natural science

Work: *Autobiography*, written 1876; manuscript CUL-DAR26 and draft
CUL-DAR53.2.143-146, Darwin Online.
https://darwin-online.org.uk/converted/manuscripts/Darwin_C_R_CUL-DAR53.2.143-146.html

Verbatim (verified, fair copy):

> whenever a published fact, a new observation or thought came across
> me, which was opposed to my general results, to make a memorandum of it
> without fail & at once

Reason given: "such facts & thoughts were far more apt to escape from the
memory than favourable ones."

What he built: a personal rule and a written record, the memorandum of
counter-evidence, so that "very few objections were raised against my
views which I had not at least noticed and attempted to answer."

Match: a running register of the pieces that do not fit the theory,
kept precisely so they are not forced or forgotten (A and D). Differs:
the register is of objections, not unknowns; the "whole" is the theory
itself, not a separate golden model.

### 9. David L. Parnas and Paul C. Clements, software engineering

Work: "A Rational Design Process: How and Why to Fake It", *IEEE
Transactions on Software Engineering* 12(2), 1986, pp. 251–257.
https://userweb.cs.txstate.edu/~rp31/papers/Fake_it.pdf

Verbatim (verified, section II):

> In most cases the people who commission the building of a software
> system do not know exactly what they want and are unable to tell us
> all that they know.

> Many of the details only become known to us as we progress in the
> implementation.

And: "The good news is that we can fake it."

What they proposed: write the documents the ideal process would have
produced (requirements, module guide, interfaces) and keep them current,
so that the record reads as if the rational process had been followed.
The requirements document should list what is not yet known in a
"to be determined" form (the paper's phrase for placeholders; unverified
in this reading, the section was not extracted).

Match: A, stated as a fact about designers and clients. B is the
"rational ideal process" itself, a golden model of the process that the
real one is compared to and documented against. Differs: it concedes the
whole cannot be reached and advises faking the record, which the idea
under study would call forcing the pieces.

### 10. Horst Rittel and Melvin Webber, planning and design theory

Work: "Dilemmas in a General Theory of Planning", *Policy Sciences* 4
(1973), pp. 155–169.
https://urbanpolicy.net/wp-content/uploads/2015/06/Rittel-Webber_1973_DilemmasInAGeneralTheoryOfPlanning.pdf

Verbatim (verified, property 1):

> The information needed to understand the problem depends upon one's
> idea for solving it.

> Problem understanding and problem resolution are concomitant to each
> other.

What they proposed: the ten properties of wicked problems; no method,
but the argument that for such problems a complete list of unknowns
requires "an exhaustive inventory of all conceivable solutions ahead of
time".

Match: the strongest counter-case to B. They deny that a complete concept
can be stated in advance for social problems; the unknowns list depends
on the solution idea. Useful as the objection the idea must answer: a
golden system is available for tame problems (hardware, mathematics) and
contested for wicked ones.

### 11. Rich Hickey, software

Work: "Hammock Driven Development", Clojure Conj, 2010. Transcript:
https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/HammockDrivenDev.md

Verbatim (verified at the transcript):

> most of the big problems we have with software are problems of
> misconception.

> There will be things that right away you know you don't know.

> If there are no question marks, you're missing a step.

What he proposed: a practice: state the problem aloud or in writing;
write down what you know, what you don't know, and the constraints; read
Pólya; look for similar solved problems; then stop and let the mind work
before coding.

Match: A as a direct instruction, with Pólya cited as the source. D is
"misconception". Differs: no golden whole (B); no tool, a personal
discipline.

### 12. David J. Bland, product strategy

Work: Bland and Osterwalder, *Testing Business Ideas*, Wiley, 2019; "How
assumptions mapping can focus your teams on running experiments that
matter", Strategyzer, 4 Aug 2020.
https://strategyzer.com/library/how-assumptions-mapping-can-focus-your-teams-on-running-experiments-that-matter

Verbatim (verified):

> Assumptions Mapping is a team exercise where desirability, viability,
> and feasibility hypotheses are made explicit

> What are all the things that need to be true for this idea to work?

What he built: a workshop and canvas. Write every assumption behind the
idea; plot each on importance against evidence; test the top right
(important, no evidence) first. Descends from Ries's "leap-of-faith
assumptions" (*The Lean Startup*, 2011; unverified at source) and from
Gothelf and Seiden's *Lean UX* (per a secondary source).

Match: A, as a tool, done before building. Differs: the measure is
evidence per assumption, not congruence with a whole; nothing on C.

## Partial matches and tools

- Michael Nygard, "Documenting Architecture Decisions", 15 Nov 2011
  (https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions,
  verified). The ADR records context ("the forces at play"), decision,
  status, consequences ("All consequences should be listed here, not just
  the 'positive' ones"). No open-questions field in the original; later
  templates (MADR, and many teams) add one.

- Malte Ubl, "Design Docs at Google", 6 July 2020
  (https://www.industrialempathy.com/posts/design-docs-at-google/,
  verified). Goals and Non-Goals; trade-offs; "Early identification of
  design issues when making changes is still cheap." The post has no
  "open questions" section; its nearest line is "Are you unsure about the
  right software design, and would it make sense to spend upfront time to
  gain certainty?" Many derivative templates add "Open questions".

- Raphael H. Cohen, IpOp model, 2006 (https://en.wikipedia.org/wiki/IpOp_model,
  secondary): "helps identify and map as many unknowns as possible before
  significant resources (including time) are spent", with unknowns
  categorized (market, technology, process, stakeholders, IP, regulatory).

- Lukasz Lysakowski, "The Unknown Knowns of Design", freeCodeCamp,
  27 Feb 2018 (verified): "Launching a design without answering a Known
  Unknown can potentially jeopardize the project, the company, the end
  user, and possibly yourself."

- smirnowld, agent-practices, PR #3, 27 Sept 2026 (verified at GitHub): an
  "open-questions register" template (question, proposed default, impact,
  date raised, who decides; open items only, answers move to an ADR). A
  recent tool of exactly the kind asked for; small and unknown.

- Gause and Weinberg, *Exploring Requirements: Quality Before Design*,
  Dorset House, 1989, and *Are Your Lights On?*, 1982. "Context-free
  questions" asked before design; "a problem is a difference between
  things as desired and things as perceived" (unverified at source; from
  summaries).

- Golden model, hardware verification: the design under test and a
  trusted reference model receive the same stimulus and are compared;
  a mismatch is a bug in one of them. A 2026 arXiv paper on RISC-V GPGPU
  verification (https://arxiv.org/pdf/2609.13311, read via search summary,
  unverified) argues the golden model itself must be treated as a
  verification target. This is the engineering sense of B: a complete
  reference the design is judged against.

- Reference architecture: Cloutier et al., "The Concept of Reference
  Architectures", *Systems Engineering* 13(1), 2010 (abstract only). A
  reference architecture "captures the accumulated architectural
  knowledge"; the paper finds no consistent definition. Weaker than the
  golden model as a comparison standard.

- John Keats, letter to George and Tom Keats, 21/22 Dec 1817 (via
  Wikipedia, standard transcription, unverified at a manuscript source):
  "capable of being in uncertainties, Mysteries, doubts, without any
  irritable reaching after fact & reason". Coleridge "would let go by a
  fine isolated verisimilitude ... from being incapable of remaining
  content with half-knowledge." The oldest statement of D found: reaching
  after a fact to close the gap is the forcing.

- Socrates, Plato's *Apology* 21d, Jowett (verified at Gutenberg):
  "I am better off than he is,—for he knows nothing, and thinks that he
  knows; I neither know nor think that I know." The root of A.

## What was not found

- No one found names all four parts as one doctrine. The pair "list the
  unknowns" (Pólya, Dewar, Hickey, Bland) and the pair "the whole is
  congruent" (Brooks, Alexander) are held by different people. Only
  Alexander's *Notes* joins a register (of misfits) to a whole (good fit),
  and his register is of failures, not of ignorance.

- "Golden system" as a role model of the whole against which unknowns are
  listed: found only in hardware verification (golden model) and in
  Parnas's "ideal process". No design author found uses a complete
  concept as the ruler against which gaps are measured; Rittel and Webber
  argue it is impossible for wicked problems.

- "Holds together like a person": Alexander's "a man, a town, a building"
  is the nearest. Carl Rogers's "congruence" (self-concept matching
  experience, 1961) was searched but only secondary definitions were
  found; not included as a design source.

- The Pólya "foolish to answer a question that you do not understand"
  line, the Alexander p. 31 wholeness line, the Keats letter, the 1968
  Bunker quote, the Brooks *Design of Design* line, and the Klein
  "prospective hindsight" citation are unverified at source.
