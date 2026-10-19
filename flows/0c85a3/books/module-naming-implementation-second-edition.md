<!-- to-the-living:start -->
Presentation.{ «One module name, second edition» }

# One module name

I put settled statements in an inquiry by treating the whole naming topic as one unresolved implementation question. The original Mind draft already contained that mistake; publication did not introduce it. Its own reference file says, “The kind:subject rule and no-whitespace requirement are settled; the questions here concern implementation boundaries, not reopening that naming decision.” Yet I put those settled rules, source observations and proposed implementation together under the inquiry destination.

I cannot identify a skill sentence or brief that instructed me to put settled knowledge there. The recorded brief was to prepare an implementation-cycle presentation before source changes. It did not prescribe this classification. My earlier reply that I did it “to give its open questions context” was an inferred explanation, not a traced author record. I withdraw it as a historical explanation. The evidence establishes a classification mistake in my draft, not an instruction requiring it.

The correction separates three things: the living's approved rule stays in vision; verified observations about sources and tests belong in knowledge; only what still needs an answer belongs in inquiry. This edition replaces the three competing proposals for the same inquiry file with one knowledge proposal and one inquiry proposal. Neither file was created by the first edition, so this corrects proposed content rather than claiming to repair an already-landed module.

```figure
+--------------------------+
| Approved naming rule     |
+--------------------------+
             | stays in
             v
+--------------------------+
| Vision                   |
+--------------------------+

+--------------------------+
| Verified observations    |
+--------------------------+
             | belong in
             v
+--------------------------+
| Knowledge                |
+--------------------------+

+--------------------------+
| Questions still open     |
+--------------------------+
             | belong in
             v
+--------------------------+
| Inquiry                  |
+--------------------------+
```

### Proposal 1: Keep verified naming observations in knowledge · mind-context › knowledge/module-naming.md, a new file

+ # Module naming
+
+ The approved naming rule is held in psyche-context vision/context-modules.md. That vision, rather than this knowledge module, is the authority for type directories and the kind:subject identity. The example vision/book.md → vision:book illustrates that approved rule; it is not evidence that every implementation already accepts it.
+
+ At the inspected Curriculum revision 2ec28623, src/registry.rs accepts lowercase ASCII letters, digits and hyphens in valid_id, but not a colon. At that same revision, src/startup.rs identifies spirit and intent through spirit- and intent- prefixes. These are observations of that revision, not a statement that a later implementation has been checked or deployed.
+
+ Field's isolated native experiment on Claude 2.1.294 and Codex 0.158.0-alpha.9 accepted vision:book through the tested completion and invocation routes, and the fixture instruction appeared in native context. This establishes those tested routes and versions; it does not establish compatibility for every harness or the complete composition and deployment chain.
+
+ The first edition of One module name mixed approved rules, implementation observations and unresolved questions in a proposed inquiry/module-naming.md. Its provenance already distinguished the settled rule from implementation questions. No instruction requiring that mixed placement was identified. The proposed inquiry file was not created by that edition.

Ruling: land, amend, or reject.

### Proposal 2: Give the remaining questions one inquiry target · mind-context › inquiry/module-naming.md, a new file

+ # Open module-naming questions
+
+ Does the subject retain the existing lowercase letters, digits and internal hyphens, or must other characters be admitted? An explicit vocabulary ruling would settle which names the parser must accept and refuse.
+
+ Can each supported native target represent the canonical identity directly? In particular, is the reported OpenCode colon restriction present on the intended installed route? If it is, is a target-only encoding acceptable, or must that target wait for canonical-name support? A qualified native example and the living's ruling would settle the representation; any encoding would still need a collision check.
+
+ At each Ethos consumer, is the module identity a string value or part of import syntax? A call-site inventory with parser-backed examples would settle whether the existing string representation suffices or a grammar proposal is needed.
+
+ Which active consumers resolve modules in memory, and which still read projected harness files? An inventory tied to the selected source revisions and installed routes would settle the actual migration boundary without reviving retired consumers.

Ruling: land, amend, or reject.

<!-- to-the-living:end -->
