# Distillation candidates — f38926

Gathering only: quotes and references, no re-articulation, no proposals. Paths are relative to `/home/li/primary`.

**Duplication.** Every 2026-09-19 `flows/b81560/vision/operational-*` record below is the *same living utterance* as its `flows/f38926/vision/*` counterpart, relayed to primary Psyche opus b81560: one record, two logs. All marked *input mode not established*.

---

## 1. Meaning language

**Candidates.** `flows/f38926/vision/meaningLanguage.md`, eight entries, 2026-09-19, spoken directly to PsycheHigh (Fable, f38926):
(a) developed now; unknown proto syntax read as opaque strings; Twitter-style prose now, then a full Sanskrit verb set.
(b) "the logical language, a little bit like Hanzi… specified with structs and enums… ontology in a huge Rust- or ethos-defined but Rust-backed datom graph"; could take a Latin or Greek name.
(c) "in reality, there's going to be a layer after three or four layers of side notes".
(d) "I don't agree with attaching to a path… If a meaning is changed, its identity changes"; checksum links, indexes on demand, append-only locking.
(e) "we need a copy of it by virtue of keeping the link" (Nix retention); statement content-addressed at the root, responses a vector; "Top-level domains, a root of the ontology"; "Go find the best ontology in the world".
(f) "we're going with Vaiśeṣika".
(g) "we don't have to use a single word for translation. We can use a Pascal-case sentence expression to describe one of the gunas".
(h) "Break it up into a structure first, and then specify that in ethos."

Relays: `flows/b81560/vision/operational-{asyncSubflowsAndMeaningLanguage, meaningLanguageLogographic, meaningLanguageAnnotationLayers, meaningContentAddressedAnnotation, meaningGarbageCollectionAndOntology, vaisheshikaRuledAndSyntaxQuestion, meaningDualSanskritEnglishNames}.md`.

**Earlier records, same subject.** `flows/5851f4/vision/ashtadhyayiKnowledgeBase.md` (STT) — an Ashtadhyayi knowledge base "for thinking, language, communication, and ontology… the base for everything"; `flows/5851f4/vision/anatomyOfCommunicatingThinkingAndReacting.md` (Pāṇini's grammar); `flows/9993b5/vision/typedString.md` (2026-09-17) — "it is just all going to be types"; `vision-raw/structuredStringType.md` — "an annotated string"; `flows/6cc91b/vision/typedPrompts.md` — typed messages specified in Ethos as Datom.

**Existing Vision touched.** `Vision/datom.md` § Meaning: "its shape is still open… Meaning is postponed so that a working syntax lands as soon as possible"; "The name Meaning smells of a verb; it stands provisionally."

**Tensions.** Postponed vs. current: Vision, "Meaning is postponed"; f38926, "this is what we're doing now, a meaning language." Roots: the Ashtadhyayi record claims the base for Pāṇini — "the base for everything" — against the later "we're going with Vaiśeṣika"; the living does not say whether Pāṇini is supplanted or divides with it (verbs vs. roots). Record (d) closes on the living thinking aloud and a question — "I'm just trying to optimize it here. Can you make a link to a piece of data in a certain position in a database, in an absolute way?" — not a settled clause.

**Impurities.** In (f), "let's map all of this with the mind and create a base meaning"; in (h), the sequencing directive to Mind — dispatch and order of work, flagged as such in the records' own context notes. `flows/b81560/vision/operational-ontologySurveyReady.md` is a flow report, not psyche ("provenance: Psyche Fable f38926 report, not living-origin").

**Vision topic.** `Vision/datom.md` § Meaning, or a new `Vision/meaning.md` — the records place the language both as datom's Meaning grown up and as a layer above it.

---

## 2. Subflows as independent asynchronous flows

**Candidates.** `flows/f38926/vision/subflows.md`, three entries, 2026-09-19, direct:
(a) "we're going to get rid of the subagents facility and the harnesses because it puts them in a synchronous user interface… if the subflow is independent and can reply to a successor… we have an asynchronous system"; own system prompts; "it's going to be a routing job".
(b) "a special field agent running on ultra-low power that checks every question or request… based on its authority, we spawn some subflows".
(c) "The requester doesn't hold anything. He gets a request ID… If he's still the flow in charge when that flow is done, he'll get a message."

Relays: `flows/b81560/vision/operational-{asyncSubflowsAndMeaningLanguage, fieldUltraLowRoutesSubflowRequests, subflowRequestIdAndAsync}.md`.

**Earlier records.** `flows/162eb3/vision/subflows.md` (typed, 2026-09-10/12): "we need better training on how to launch subflows. Codex doesn't need another Codex to run ChatGPT models"; "yes, its still a subflow"; "no sandbox. all permissions"; a different harness "shouldn't be invoked with the main flow training, but with the subflow training"; "the main flow should not be available for agents to load by themselves." `flows/9e7c9f/vision/subflows.md` (2026-09-13) — the main-flow skill hidden by code. `flows/9993b5/vision/subflowIdentity.md` (2026-09-17) — the job name is the subflow's identity and report spot. `flows/b49251/vision/subflowDispatch.md` (2026-09-16) — answer low-effort first, then launch. `flows/b05237/vision/operational-mainFlowUsesSubflows.md` (2026-09-18, relayed from Field Sol 33ba2b) — "You're a main flow. You don't do stuff. You use subflows to do it." `flows/b05237/vision/operational-fieldEnergyLevels.md`, `-fieldTestingAndUltraLow.md` (2026-09-18, relayed by Codex Astra 893603) — "Luna will be ultra low"; ultra-low field flows for testing. `flows/4a2502/vision/operational-delegationTierRules.md` — tier ceilings.

**Existing Vision touched.** `Vision/flowNexus.md` § Starting flows — "A Nexus component decides the system prompt and everything about a launch, replacing the harness's subagents with specialized harnesses"; § A replaced session is reaped by the refresh itself. `Vision/modelRoles.md` § Delegation ceiling. `Vision/messaging.md` § A message is a datom.

**Tensions.** The 162eb3 rules govern the harness subagent facility; f38926 removes it — "we're going to get rid of the subagents facility and the harnesses" — and does not say whether those rules survive. Who routes: flowNexus gives launch decisions to "a Nexus component"; f38926 gives the check to "a special field agent running on ultra-low power", a field flow. Successor delivery ("if he's still the flow in charge") sits beside flowNexus's reaping statement, neither contradicted nor covered.

**Impurities.** None evident.

**Vision topic.** `Vision/flowNexus.md` (launch, routing, request ID); the ultra-low checker also touches `Vision/modelRoles.md`, the request-ID handle `Vision/messaging.md`.

---

## 3. Horizon as a Nexus; sandbox VM as a node feature

**Candidate.** `flows/f38926/vision/horizon.md`, 2026-09-19, direct, correcting this flow's proposed wording "tested in a sandbox virtual machine on the host the flow is running on": "No, the virtual machine is running on the node… Prometheus is mostly the workhorse, so it should be a feature on a node. People should be able to know by querying the Horizon… We need to make the Horizon a proper nexus, so the current state of the cluster can be queried from that." Relay: `flows/b81560/vision/operational-horizonNexusAndNodeResources.md`.

**Earlier records.** `flows/0062e8/vision/horizon.md` (STT) — "a separate general definition for nodes that all clusters could call on"; "this CriomOS Horizon settings repo is a perfect place to specify a new generic node setting"; node type as a "high-level, mutually exclusive kind of variant separation." `flows/01a02b4b/vision/homeEquivalence.md` (2026-08-23, typed) — "directly from lojix-emitted horizon output". `vision-raw/setupIndependentInterfaces.md` — host configuration sourced from horizon/cluster data. `flows/024bc7/vision/sandbox.md` (2026-09-13, STT) — "Just start a full sandbox. You can use Prometheus… it's a powerful machine that's used to test these virtual machines" (notion duplicate `flows/bcd02a/notion/sandbox.md`). Other senses of *sandbox*: `flows/6cc91b/vision/sandbox.md` — "a reserved branch of a tree"; "a light sandbox… of my home environment"; `flows/01a02a34/vision/sandboxedTest.md` (2026-08-22, typed) — not interfering with production.

**Existing Vision touched.** `Vision/nexus.md` § Why everything is a Nexus — "Everything built from now on is a Nexus, and what was built in another shape is rewritten as one"; § A Nexus is the whole. `Vision/datom.md` § Repository — "Everything moves to Datom: all of the stack, Horizon, Lojix, everything." `Intent/testing.md` already carries "which node is found by querying Horizon."

**Tensions.** What Horizon is: earlier records treat it as emitted Nix/Lojix configuration data ("lojix-emitted horizon output", "Horizon settings repo") against the new "the current state of the cluster can be queried from that." Which node: 024bc7 names a host ("You can use Prometheus") against "it should be a feature on a node" found by query. Three unreconciled senses of *sandbox* (VM on a node, reserved branch of a tree, light home container).

**Impurities.** None evident.

**Vision topic.** A new `Vision/horizon.md` — none exists; the "everything is a Nexus" consequence lands against `Vision/nexus.md`, the node-feature half supports `Intent/testing.md`.

---

## 4. Committing with explicit paths

**Candidate.** `flows/f38926/vision/committing.md`, 2026-09-19, direct, after this flow raised that `jj commit` snapshots the whole shared working copy: "You can pass a path to the commit command, so you usually really only work in your own flow ID directory… You just commit the files that you edited, right? The call has to be explicit with file paths. Unless the whole repo is locked, in which case nobody else should be editing it." Relay: `flows/b81560/vision/operational-explicitFilePathCommits.md`. Approval: `flows/b81560/vision/operational-pocSandboxIntent.md` — "Your wording for the commit rule is good. You can land that."

**Earlier records.** `flows/aa4c7747/vision/uncommittedChanges.md` (2026-08-25, approved entry-file wording) — "When a tree you are about to write in already holds changes, commit those first, as their own commit, described as found in the tree." `flows/9993b5/vision/{sharedWorkspace, autoCommitOnWrite, orchestrateCommitBinding, noMoreBranches}.md` (2026-09-17) — coordination on shared repos; "a file write event that automatically creates a commit"; commit "by selecting the files or selecting the directory, at least just matching the directory from the lock"; "I want everything merged on main". `flows/c7128c/vision/commitSubflowScript.md` (2026-09-18) — a commit subflow script needing no description.

**Existing Vision touched.** None — `Vision/` has no committing or version-control topic. The rule lives in `CLAUDE.md` § Committing and the Curriculum `file-editing` skill, which the record's own context says it corrects ("Corrects the file-editing skill's landing sequence, which commits without paths").

**Tensions.** "You just commit the files that you edited" against the approved "commit those first, as their own commit" — reconcilable in sequence, but the newer rule read alone forbids touching another flow's dirty files. Path source: explicit paths named by the editor against paths matched from the lock's directory. The whole-repo-lock exception is new; no earlier record covers it.

**Impurities.** None evident.

**Vision topic.** A new `Vision/committing.md`, or `Vision/orchestrate.md`, which already holds the lock protocol the commit binding runs through.

---

## 5. Proof-of-concept deploys on the flow's host; sandbox first

**Candidates.** `flows/f38926/vision/operational-openCodeRemoteAccess.md`, 2026-09-19, direct:
(a) "There's no reason to make this about Zeus. If anything, Zeus is a stable node. We shouldn't be testing stuff."
(b) "We're on Uranus. Uranus is your host. We're working on the host that we're on. This is where we're going to deploy".
(c) "a proof of concept should be tested in a sandbox in a virtual machine. But because we need to log in in the browser with my credentials, and you can't really run this in a virtual machine" (ends mid-sentence as received).
(d) "Maybe I should start. We should have Open Code installed, and I should log in to my Codex subscription there."
Relays: `flows/b81560/vision/operational-pocSandboxVmFirst.md`, `-pocSandboxIntent.md` ("Yes, the intent is good. A proof of concept is tested in a sandbox first."). Also `flows/f38926/vision/nightWork.md` — "Move everything, all the vision, forward into proof of concept, with testing and all the testing that passes into production and testing in the field."

**Earlier records.** `flows/05c604/vision/deployment.md` — "We can go from proof of concept to testing in a sandbox to deploying on anything that has enough vision right now." `flows/6cc91b/vision/pairHierarchy.md` (2026-09-14) — "Once things have been tested in one place, in the primary, in the sandbox, then they try to release that and fix it." `flows/024bc7/vision/sandbox.md` (2026-09-13) — "Can we copy the token into another host so that my codex and Claude log in?… so that we can use the models in the virtual machine." `flows/162eb3/vision/subflows.md` (2026-09-12) — "no sandbox. all permissions", a different sense (harness launch flags, not a test VM).

**Existing psyche touched.** `Intent/testing.md` § A proof of concept is tested in a sandbox first — already distilled from these records; `Intent/sources/testing.md` lists `f38926 operational-openCodeRemoteAccess` and `f38926 horizon`.

**Conflicts checked.** None with the landed Intent statement: it carries both the node/Horizon clause and the credential exception. Residual gap: the host rule is absent from Intent — "We're working on the host that we're on" and "Zeus is a stable node. We shouldn't be testing stuff" are unrepresented, so a flow reading only `Intent/testing.md` learns to query Horizon, not that its own host is the deploy target and stable nodes are off limits. Counter-pointing record: 024bc7 asks whether credentials can be carried into the VM where (c) states they cannot — a question against a ruling, six days apart.

**Impurities.** `nightWork.md` is mostly working instruction by its own context note: "Make everybody work for a few hours, especially the codex guys", "get me some flashbooks I can look at in the morning", "Let's cash in those quotas", the bulleted report contents, "start fresh flows for everything". Not instruction: the ordering proof of concept → testing → production → field, and agent-written testing skills. In the OpenCode record, "you can have Mind implement it, and let's test it" is dispatch, and (d) is hedged ("Maybe I should start").

**Vision topic.** `Intent/testing.md` for the sandbox-first rule (landed). The host rule and the stable-node rule land in a new `Vision/deployment.md`, or in `Vision/horizon.md` if node selection stays with Horizon. The OpenCode provider line is operational and belongs with the remote-access work, not with testing.

## Sources

Every record named inline above was read for this report, plus `Vision/datom.md`, `Vision/nexus.md`, `Vision/flowNexus.md`, `Vision/modelRoles.md`, `Vision/messaging.md`, `Intent/testing.md`, `Intent/sources/testing.md`, `CLAUDE.md` § Committing.

Method: grep over `flows/*/vision/`, `flows/*/notion/`, `vision-raw/`, `Vision/`, `Intent/` for each subject's terms, then reading the matched records. Nothing is witnessed beyond file contents; the `ouranos` hostname witness is quoted from `flows/f38926/vision/operational-openCodeRemoteAccess.md`, not re-run here.
