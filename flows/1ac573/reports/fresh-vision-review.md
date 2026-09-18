# Fresh Vision Review

A report flow's output. Not advice — this is the thing you review, comment on, and accept. Nothing here has been promoted; every item waits on your word.

Corpus: the operational vision logged 17–18 September in flow 1ac573, read against standing Vision, Intent and the top-level rules. Recency weighted, older records preserved rather than voided.

---

## Ready to become Intent

Two statements have outgrown their topic. They would guide many decisions, not one.

**Better models, not higher effort.** Capability comes from choosing a better model, not from raising a model's effort setting. Effort is not a quality dial: raising it costs a great deal and changes little. Every harness call goes out at medium effort, and that is deliberate rather than an oversight to be corrected.

**Two scales share the words high and medium, and they are not the same scale.** The harness's model-effort setting is one. Your naming of a flow's tier is the other. When you say a flow is high, that names the tier, never the effort setting — a flow that reads it as effort has misread you.

The second exists because the confusion actually happened: flows started Astra and Fable on high effort because the tier was called high.

---

## Ready to become Vision

**Model roles.** Opus is two seats, not one model. The older seat is the wiser one; the newer is faster and blinder but good at getting work done. Thinking, design and psyche interaction run on the older Opus or the newest Fable. The seat is chosen for disposition — resisting the temptation to act, questioning, doubting, asking whether it understood you — not for capability. The default for psyche-medium Claude is Opus 4.6. Its million-token context comes from a Max subscription, not from the model, so the declaration must not assume it for every operator.

**One declaration sets the model everywhere.** The model belongs in Flow as typed configuration, mutated only through the meta wire, with skill variables carrying the value by name into every skill, launcher and brief. Nothing hardcodes a model name. This is the fix for the defect that produced this flow: a launcher wrote `--model opus`, the alias resolved to whatever shipped newest, and the psyche-interaction seat ended up on the one model your vision excludes from psyche interaction.

**Name a session after its ancestor.** A successor cannot be named at creation — nothing is known about it yet. Its ancestor is known exactly. So the ancestor is the only nameable fact available when a session is born.

**A replaced session is reaped by the refresh itself.** Retirement belongs to the refresh event, not to a cleanup that may never run. Live evidence: a dead worker sat in the roster as STALE while still registered and still addressable.

**Messages arrive as datoms, and delivery is harness-specific.** Priority is a head on the datom. Hard abrupt on Claude needs two Escapes — vim mode eats the first — then the prompt, then an explicit Enter. Codex needs one. This is now shipped and witnessed, not proposed.

---

## Blocked on you

**The private layer.** Your top-level rule file charters the private part and marks it NOT ACTIVE until a third, open-source seat runs. Your newest words say to set it up. Recency favours acting; the written precondition forbids it. This one governs what may be asked of a commercial model at all, so it should not be resolved by recency alone.

**Is the soul a new level?** You called it "a private repo for the soul, the core layer." We have four levels — Spirit, Intent, Vision, Notion. I cannot tell whether the soul is Spirit under a truer name, or a level above Spirit that has never been written down. This decides what goes in the repository.

**The open-source stack.** You asked what it is and what your remote access to it would be. Those questions are already in the corpus from 13–14 September — "the best open-source stack with remote control", and a request for a report on the best programmable harness and models. I can find no evidence that report was ever delivered. The questions are still open, and they are yours to answer or ours to investigate.

---

## Less technical, as you asked

Most operational skills read like machine instructions. These are the ones that are really about how work is done, and they would survive being said in plain language to a person:

**Say what you witnessed, and mark what you inferred.** A claim relayed as a fact is the most common failure here, and it has happened repeatedly in one day.

**A message keeps its addressee.** When something is mirrored to everyone, a flow that receives it is a witness, not the subject. Acting on someone else's instruction is not diligence.

**Correct the record, not just the reply.** When something logged turns out wrong, the logged file gets fixed and the correction is visible in it — otherwise the next flow inherits the error.

**Justify in the commit.** The commit message names the epic; thousands of commits share that name. The individual change explains itself once seen in the epic's lens. An operational note is for the flow that later asks why.

**Agents may act on their own judgment in test mode**, with psyche as the base and the justification stated — carried in the message, the log description and the commit, not in a separate document.

---

## Shipped today

Claude hard-abrupt, deployed. Previously refused outright by a hardcoded line saying it was Codex-only. Disproved with a live probe: a 6000-item task interrupted at 4393, the harness printing its own interrupt marker, reproduced twice.

Agent-to-psyche notification, verified working. Earlier it returned `disabled`; it now returns `shown`. This was the one direction we had not built, and it is available to every harness.

One open defect, recorded rather than hidden: the escapes interrupt but do not clear the input box, so residual text concatenates with the delivered message. If the canonical datom rides this path, that corrupts it on the wire.
