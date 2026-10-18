<!-- to-the-living:start -->
Presentation.{ «Approved vision into working systems, first edition» }

# Approved vision into working systems

## Proposal 1: Auditing knowledge · mind-context › inquiry/knowledge-auditing.md, a new file

+ Knowledge is checked against current practice at a declared review deadline and when a relevant implementation changes. A deadline requests work once; it does not repeatedly query a system for changes. An unfinished audit remains visible to its owner.
+
+ An audit compares a specific module revision with evidence. Agreement records what was checked. A variation becomes an inquiry linked to the affected statement and evidence; it is not silently promoted to replacement knowledge. The responsible Mind topic resolves the inquiry, and its proposed knowledge returns through the review route.

```figure
+--------------------+
| Review deadline or |
| changed component  |
+--------------------+
          | requests
          v
+--------------------+
| Knowledge audit    |
+--------------------+
          | compares
          v
+--------------------+
| Statement and      |
| current evidence   |
+--------------------+
          | reveal variation in
          v
+--------------------+
| Inquiry            |
+--------------------+
          | asks for resolution from
          v
+--------------------+
| Mind topic         |
+--------------------+
```

Question: should each knowledge module declare its own review interval, or should a shared interval apply until a topic needs another? No interval is selected here.

Question: when a statement is contradicted, should composition mark it as disputed until review, or temporarily omit it? Retaining it without qualification and deleting it automatically have different consequences.

## Proposal 2: Layer and topic roles · mind-context › inquiry/role-sections.md, a new file

+ Role sections describe the responsibility of each layer and the specialization of each topic. The context repositories remain the only authority for their text; Curriculum resolves their module identities. Role descriptions do not become a second model table.
+
+ A launch selects the layer's role and the topic's specialization explicitly. A topic refinement must not silently erase the layer's responsibility. The resulting composition can be inspected before launch.

```figure
+--------------------+
| Layer role         |
+--------------------+
          | supplies responsibility to
          v
+--------------------+
| Role composition   |<-----------------+
+--------------------+                  |
          | guides                      | refines
          v                             |
+--------------------+       +----------------+
| Specialized flow   |       | Topic role     |
+--------------------+       +----------------+
```

Question: does a section mean directories under role for each layer and topic, or named sections within role modules? The choice must preserve one unambiguous module identity and update every consumer together.

Question: may topic roles override a layer instruction, or may they only add narrower responsibilities? The proposal is addition with explicit conflict refusal, rather than an implicit last-writer rule.

## Proposal 3: Judging whether a topic wakes · mind-context › inquiry/topic-wake-judgment.md, a new file

+ A small-model judgment selects a relevant idle topic and suitable layer when new input has no explicit destination. It returns a typed choice, a decision to retain the input, or an uncertainty for the responsible core. It does not choose an arbitrary executable or supply its own identity.
+
+ Flow retains responsibility for launch, queue order and delivery. The model's judgment becomes a request to Flow, not a direct harness action. A failed judgment retains the original input for resolution.

```figure
+--------------------+
| Unaddressed input  |
+--------------------+
          | asks for a topic from
          v
+--------------------+
| Small-model judge  |
+--------------------+
          | proposes an address to
          v
+--------------------+
| Flow              |
+--------------------+
          | queues work for
          v
+--------------------+
| Chosen metaflow    |
+--------------------+
```

Question: should an explicitly addressed order or question continue to wake its target by the existing typed rule, with judgment only for unaddressed input? Or may the small model defer an explicitly addressed request? The first option avoids adding a discretionary veto to a direct order.

Question: which declared model and budget should perform this judgment, and which core receives an uncertain result? Neither is inferred from the unfinished instruction about a Secondary.

## Proposal 4: Vision beside Nexus modules · mind-context › inquiry/nexus-module-vision.md, a new file

+ Shared Nexus principles stay in their common vision. A component's specialized vision is divided along its actual module responsibilities, with links to those modules. A rule belongs in one authoritative place; a module refers to a shared rule rather than copying it.
+
+ The first mapping distinguishes Signal, Operation and Memory, then uses actual code boundaries where their responsibilities are separate. A mismatch between code and vision is recorded as a design question, not concealed by renaming a file.

```figure
+--------------------+
| Shared Nexus       |
| principles         |
+--------------------+
          | constrain
          v
+--------------------+
| Module vision      |
+--------------------+
          | specifies responsibility of
          v
+--------------------+
| Code module        |
+--------------------+
          | provides evidence to
          v
+--------------------+
| Psyche audit       |
+--------------------+
```

Question: should every source module have its own vision module, or should a vision module cover a coherent responsibility that may span several source files? The proposal is the latter, while retaining an explicit mapping to the actual code.

Question: should the first reviewed mapping cover the shared Nexus library or Chronos as the golden example? Doing both independently risks settling incompatible boundaries.

## Proposal 5: Landing the Chronos example · mind-context › inquiry/chronos-implementation.md, a new file

+ The approved fourth edition of Chronos remains the design authority for this work. Its existing Psyche and Mind Prototyping owners retain authorship. Landing the approved vision and demonstrating its implementation are separate milestones.
+
+ The implementation plan follows the declared path from Signal through Operation to Memory and back. Numerical results need independent reference cases; structural compilation alone cannot establish astrological correctness. Coverage includes boundaries of the declared ephemeris range, location selection and derived arcs.

```figure
+--------------------+
| Approved Chronos   |
| fourth edition     |
+--------------------+
          | specifies
          v
+--------------------+
| Existing owners'   |
| implementation     |
+--------------------+
          | answers reference cases for
          v
+--------------------+
| Numerical and      |
| Nexus behavior     |
+--------------------+
          | supplies evidence to
          v
+--------------------+
| Psyche review      |
+--------------------+
```

Question: should the first accepted implementation cover the entire fourth edition, or a named subset while the remaining approved requirements stay open? No narrower completion criterion is assumed.

Question: which independent ephemeris reference and tolerance should decide numerical acceptance? The existing owners should propose these before a result is called correct.

## Proposal 6: Completing the current Ethos contract · mind-context › inquiry/ethos-implementation.md, a new file

+ Separator whitespace and the single-declaration Type variant are reviewed as one coherent parser and generator change, with downstream consumers checked against that same source family. Existing proposal branches are implementation inputs, not evidence of main publication or deployment.
+
+ Parser acceptance is tested across spaces, tabs and line breaks after a separator, while malformed expressions still refuse. The Type form is checked from an authored declaration through generated output and its consuming program.
+
+ Long-term trait design and the short-term executable language are documented separately. A short-term parser must not require a trait feature that its generator cannot yet express unless that requirement is explicitly chosen.

```figure
+--------------------+
| Reviewed Ethos     |
| contract           |
+--------------------+
          | defines
          v
+--------------------+
| Parser and         |
| generator family   |
+--------------------+
          | produces code for
          v
+--------------------+
| Current consumers  |
+--------------------+
          | demonstrate alignment to
          v
+--------------------+
| Psyche review      |
+--------------------+
```

Question: does the short-term instruction to do without traits mean Ethos omits trait declarations while handwritten implementation traits remain, or that implementations also stop requiring traits? The two readings conflict with different current rules and must not be silently combined.

Question: may the whitespace and Type changes land as a separately reviewed complete increment while trait design continues, or must their deployment wait for the trait decision?

<!-- to-the-living:end -->
