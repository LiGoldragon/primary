<!-- to-the-living:start -->
Presentation.{ «Flow: the metaflow» }

# Flow: the metaflow

## Crystallization

### Proposal 1: the metaflow is the major abstraction

File: `psyche-context/skills/vision-flow.md`, «What it does», a new
paragraph after the one that begins «Flow manages metaflows».

Sources: flow 8475a9, 2026-10-06; flow f5a6e9, 2026-10-07.

```text
  Flow manages metaflows. A metaflow is one address, { Aspect Topic Layer }, that continues through several flows one after another; the flow is its current run, and what is addressed is always the metaflow, never a flow. The default topic is core: the permanent topic, the thing that keeps the machine going, the last topic to stand.
+
+ The metaflow is the major abstraction, the one mostly thought in; the flow is the lower-level one, and almost never faces the living.
+
  A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.
```

The code that makes the messenger take only metaflows is Proposal 3 of
«Flow: identity and naming», second edition.

Ruling:

1. Land.
2. Land with changes the living names.
3. Drop.

### Proposal 2: a flow, its metaflow, and no voice

File: `psyche-context/skills/vision-flow.md`, the description and the
paragraph that begins «Flow is the Nexus that manages flows».

Sources: flow bad807, 2026-10-04; flow d4ae97, 2026-10-05 and
2026-10-07; flow e5a0bc and flow f5a6e9, 2026-10-07; flow d4ae97,
2026-10-08; flow 445410, 2026-10-09; flow 875960, 2026-10-11; flow
9fb0ad, 2026-10-03, relayed by flow 41fa34.

The description:

```text
  ---
- description: Flow — the Nexus that launches, names, tracks and ends flows — or a voice, a side flow, a hook or the Capsule is being designed or judged against what the living wants.
+ description: Flow — the Nexus that launches, names, tracks and ends flows — or a metaflow, a side flow, a hook or the Capsule is being designed or judged against what the living wants.
  dependencies: [vision-nexus, vision-ethos]
```

The paragraph, under choice 1, with choice 5:

```text
- Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.
+ Flow is the Nexus that manages flows. A flow is one session of a harness, and every flow is one run of a metaflow; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on metaflows: it locks a metaflow while the metaflow rolls over into a new flow, and the lock tells whether a request can reach it.
```

Under choice 2, the second sentence reads instead:

```text
+ A flow is one session of a harness; most flows run a metaflow, and a flow may stand outside every metaflow;
```

Under choice 6, the last sentence stays «Flow holds the lock on flows.»

Under choice 7, a line after the paragraph (a pane: one terminal area
in Herdr, where the living sees a flow):

```text
+ A flow on a topic other than core needs no pane.
```

Proposal 7 of «Flow: identity and naming», second edition, inserts a
clause after «A flow is one run of a voice;»; it follows the new clause.
The short-term form of the lock, the transition mark, is Proposal 2 of
«Flow: short term and long term», third edition.

Lands in the EDN configuration. Each aspect file,
`primary/config/main-flow/psyche.edn`, `mind.edn` and `field.edn`,
names its layers under `:voices`:

```clojure
-  :voices [{:layer :Primary
+  :layers [{:layer :Primary
```

The launcher reads that key in `launch-config.mjs`; its Clojure rewrite
is added to `messenger-clj/src/messenger_clj/launch.clj`, the file
Proposal 5 of «Flow: identity and naming», second edition, creates.
`:layers` and `:layer` are the shape of the EDN, so they stay in code:

```clojure
+ (defn layer-row [aspect-config layer]
+   (or (some #(when (= layer (:layer %)) %)
+             (:layers aspect-config))
+       (throw (ex-info "UnknownLayer"
+                       {:layer layer}))))
```

Ran under Babashka on `psyche.edn` with the key renamed: `:Secondary`
returns its model row; `:Fifth` is refused as `UnknownLayer`.

Ruling, one number from each group:

The flow and its metaflow:
1. Every flow runs a metaflow, the machine's design: since flow d4ae97,
   2026-10-08, every flow has an aspect, a topic and a layer, core by
   default.
2. A flow may stand outside every metaflow (flow d4ae97, 2026-10-07).

The description and the EDN key:
3. Land.
4. Drop.

The lock:
5. Flow holds the lock on metaflows, as shown.
6. The sentence stands.

The pane:
7. Land the pane line (flow d4ae97, 2026-10-07).
8. No line.

### Proposal 3: the registry of metaflows

File: `psyche-context/skills/vision-flow.md`, «What it does», two new
paragraphs and a figure after Proposal 1's paragraph.

Sources: flow d4ae97, flow f5a6e9 and flow e5a0bc, 2026-10-07; flow
d4ae97, 2026-10-08; flow d68c82, 2026-10-13.

```text
  The metaflow is the major abstraction, the one mostly thought in; the flow is the lower-level one, and almost never faces the living.
+
+ Flow keeps a registry of metaflows. A metaflow's memory holds its current flow and its predecessor; a flow is found by looking up its metaflow, and a metaflow's history is the metaflow's, never carried in a flow's own record.
+
+ Short term: the registry is a database addressed by metaflow name; the launcher starts a successor by naming its metaflow, whose current flow is the predecessor.
```

Under choice 5, «its current flow and its predecessor» reads «its
current flow»; under choice 6, «its current flow and the flows before
it».

The figure, after the short-term paragraph; under choice 5, without its
last box:

```text
+ +--------------------------------+
+ | the launcher                   |
+ +--------------------------------+
+         | starts a successor by naming
+         v
+ +--------------------------------+
+ | the metaflow                   |
+ | { Psyche flow Primary }        |
+ +--------------------------------+
+         | points to
+         v
+ +--------------------------------+
+ | its current flow               |
+ +--------------------------------+
+         | succeeds
+         v
+ +--------------------------------+
+ | its predecessor                |
+ +--------------------------------+
```

**Destroy**, a vision impurity: the second sentence of «A passable Flow
vision: the metaflow as a chain of ancestors», `flows/d4ae97/vision/flow.md`,
and of the same record in `flows/f5a6e9/vision/flow.md` (2026-10-07):
an order to modify the launch scripts. Its first sentence is drawn into
the lines above.

Lands as data and as Clojure. Datalevin: the database the messenger
keeps all its records in. How much lineage a metaflow keeps is data,
added to `primary/config/main-flow/shared.edn` (`:latest` under choice
4, `:none` under 5, `:all` under 6):

```clojure
+  :metaflow-memory {:lineage :latest}
```

The messenger's store schema,
`messenger-clj/src/messenger_clj/typed_store.clj`, line 58. The
attribute names are the shape of its records, so they stay in code:

```clojure
   {:flow/id {:db/unique :db.unique/identity}
+   :metaflow/name
+   {:db/unique :db.unique/identity}
+   :metaflow/current
+   {:db/valueType :db.type/ref
+    :db/cardinality :db.cardinality/one}
+   :lineage/successor
+   {:db/valueType :db.type/ref
+    :db/unique :db.unique/identity}
+   :lineage/predecessor
+   {:db/valueType :db.type/ref}
```

A new file, `messenger-clj/src/messenger_clj/metaflow.clj`, the
machine's design. `:none`, `:latest` and `:all` are the three values of
the setting, so the code names them:

```clojure
+ (ns messenger-clj.metaflow
+   (:require [messenger-clj.typed-store]
+             [pod.huahaiy.datalevin :as d]))
+
+ (def current-q
+   '[:find ?id :in $ ?name
+     :where [?m :metaflow/name ?name]
+     [?m :metaflow/current ?f]
+     [?f :flow/id ?id]])
+
+ (def lineage-q
+   '[:find ?s :in $ ?id
+     :where [?f :flow/id ?id]
+     [?s :lineage/successor ?f]])
+
+ (defn current [db metaflow]
+   (ffirst (d/q current-q db metaflow)))
+
+ ;; The lineage a metaflow keeps:
+ ;; :none, :latest or :all, from the EDN.
+ (defn forgotten [db kept predecessor]
+   (when (= kept :latest)
+     (for [[s] (d/q lineage-q db predecessor)]
+       [:db/retractEntity s])))
+
+ ;; The flow is already registered, so it
+ ;; is named by its :flow/id.
+ (defn roll-tx [config db metaflow flow]
+   (let [kept (get-in config [:metaflow-memory
+                              :lineage])
+         previous (current db metaflow)]
+     (concat
+      [{:metaflow/name metaflow
+        :metaflow/current [:flow/id flow]}]
+      (when (and previous (not= kept :none))
+        [{:lineage/successor [:flow/id flow]
+          :lineage/predecessor
+          [:flow/id previous]}])
+      (when previous
+        (forgotten db kept previous)))))
+
+ (defn roll! [config conn metaflow flow]
+   (d/transact! conn
+                (roll-tx config (d/db conn)
+                         metaflow flow)))
```

A send finds its target by scanning every route for the same aspect,
topic and layer; `messenger-clj/src/messenger_clj/core.clj`,
`target-flow!`, line 533, reads the registry instead, with
`[messenger-clj.metaflow :as mf]` and `[pod.huahaiy.datalevin :as d]`
added to its requires:

```clojure
-   (let [matches (for [[id route]
-                       (route-records) ...] id)]
-     (when-not (= 1 (count matches)) ...)
-     (first matches))
+   (or (store/with-db (root)
+         #(mf/current (d/db %) target))
+       (fail (str "TargetNotRegistered: "
+                  target)))
```

The launcher, in `messenger-clj/src/messenger_clj/launch.clj`, finds
the predecessor from the metaflow and rolls the metaflow once the
successor is registered, under the messenger's reservation:

```clojure
+ (defn predecessor [metaflow]
+   (store/with-db (core/root)
+     #(mf/current (d/db %) metaflow)))
+
+ (defn roll-metaflow! [config metaflow flow]
+   (core/with-reservation flow
+     #(store/with-db (core/root)
+        (fn [conn]
+          (mf/roll! config conn metaflow flow)))))
```

With Proposal 6 of «Flow: identity and naming», second edition, its
`continuation.edn` then keeps only `:origin`; the predecessor and the
metaflow leave the flow's record.

Ran under Babashka against Datalevin 0.8.25, with the messenger's own
store and the schema above: after `0c9a77` and then `563761` roll
`Psyche flow Primary`, the current flow is `563761`; under `:latest` one
lineage record remains, under `:none` none, under `:all` both; an
unregistered metaflow is refused as `TargetNotRegistered`.

Ruling, one number from each group:

The lines and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

What a metaflow's memory holds:
4. Its current flow and its predecessor, the machine's design (flow
   f5a6e9, 2026-10-07).
5. Its current flow only.
6. Its current flow and every flow before it; flow d4ae97, 2026-10-07,
   doubts the whole history is kept.

Where the registry lives, in the short term:
7. The messenger's Datalevin database, the machine's design: the
   launcher already registers each flow through the messenger.
8. Its own database, in a Clojure flow tool beside the messenger (flow
   d4ae97, 2026-10-08); the code above moves into that tool. Whether
   the launcher and the messenger become one tool is group D of
   Proposal 2 of «Flow: short term and long term», third edition.

### Proposal 4: software starts flows

File: `psyche-context/skills/vision-flow.md`, «Starting flows», a new
paragraph after the first.

Sources: flow 8475a9, 2026-10-06, relayed by flow d4ae97; flow d4ae97,
2026-10-08; flow d68c82, 2026-10-13.

```text
  A Nexus component decides the system prompt and everything about a launch, replacing the harness's subagents with specialized harnesses launched with specialized system prompts.
+
+ Starting and refreshing flows is the software's work; no model spends its context making up for a missing tool. A flow is spawned when its metaflow refreshes, or when a metaflow spawns another for a subject that needs its own. Field starts flows only until this is automated.
+
  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
```

Lands in no code of its own. Lean, specialized flows are Proposal 5 of
«Flow: short term and long term», third edition.

Ruling:

1. Land.
2. Land with changes the living names.
3. Drop.

### Proposal 5: the end of a metaflow

File: `psyche-context/skills/vision-flow.md`, «What it does», after
the paragraph that begins «A topic never dies».

Sources: flow bad807, 2026-10-04; flow d4ae97, 2026-10-07; flow 875960,
2026-10-11.

Under choice 1:

```text
  A topic never dies; it goes idle, its flows turned off. When the living touches on it again, whether to wake a flow for it, and at which layer, is a judgment, made by a small model; a topic is bound to its context modules, so Flow knows what to start it with, together with the new input that warrants it.
+
+ A metaflow on a topic other than core may carry its end: a short description of the goal that closes it; when the goal is reached, its topic goes idle.
```

Under choice 2, the record moves whole, as its own words propose:

**Move to notion**: `flows/d4ae97/vision/flow.md`, the entry «The end of
a metaflow», to `flows/d4ae97/notion/flow.md`.

Lands in no code.

Ruling:

1. Land the line in vision-flow.
2. Move the record to notion; no line.
3. Neither.

### Proposal 6: the metaflow clusters and the Sun

File: `psyche-context/skills/vision-flow.md`, «What it does», after
Proposal 5's place.

Sources: flow bad807, 2026-10-04: three entries of `vision/metaflow.md`,
and the five of `notion/metaflowDimensions.md`, which doubt that the Sun
stays up and say it is woken.

The Sun: the Primary layer.

Line A, the clusters:

```text
+ Metaflows expand and contract by demand and availability, from three to seven, three the fewest; around them, clusters of metaflows rise for a situation or a goal, and contract, change or disappear with it. Their design draws on human knowledge and symbolism, Sanskrit above all.
```

Line B, the Sun:

```text
+ The Sun, the Primary layer, is not always on: it is woken for judgment and unwinds when nothing is in progress. Its next flow receives only what is still undecided; what is decided goes into the context modules.
```

Line B sits beside Proposal 6 of «Flow: short term and long term»,
third edition: a handover carries what needs judgment.

**Move to notion**, under choices 2 and 3: `flows/bad807/vision/metaflow.md`,
the entries «A system that expands and contracts between 3 and 7 roles»
and «The sun is in the basic triad», to
`flows/bad807/notion/metaflowDimensions.md`; under choice 3, also the
entry «The Sun is the primary layer, woken for judgment».

Lands in no code.

Ruling:

1. Land A and B in vision-flow.
2. Land B; A's records move to notion.
3. Land neither; all three records move to notion.

### Proposal 7: what Flow is specified in

File: `psyche-context/skills/vision-flow.md`, «Repository and skills»,
a new paragraph at its end.

Sources: flow d4ae97, 2026-10-08. Against it: Proposal 1 of «Clojure
and data: the rectification», which rewrites the long term from the
prototype's Malli specs (Malli: the library the Clojure code describes
its data shapes with); flow d68c82 and flow da2038, 2026-10-13.

```text
  The flow repository holds the machinery of the Flow Nexus and is a runtime repository. Every skill lives outside it, the basic skills included, so that a change to a skill causes no Nix rebuild. The basic skills give our own take on how an agent behaves in a harness, replacing the prompt the harnesses build in.
+
+ Flow's types, functions and logic are specified in Ethos, and Ethos code creates them; the Clojure prototype follows that specification.
```

Lands in no code here; the Ethos declaration of the registry's records
waits on this ruling.

Ruling:

1. Land: Ethos first, the prototype follows.
2. No line: the prototype's Malli specs come first, and the long term
   is rewritten from them, as the rectification's Proposal 1 stands.
3. Land with changes the living names.

### Proposal 8: what each aspect does

File: `psyche-context/skills/vision-aspects.md`, the description and a
new section at the end.

Source: flow d4ae97, 2026-10-08, relayed also by flow 41fa34.

```text
  ---
- description: Flows of different aspects work on one topic, or Field reaches Psyche.
+ description: Flows of different aspects work on one topic, Field reaches Psyche, or what an aspect does is judged.
  dependencies: []
  ---
```

```text
  Psyche core keeps track of all the psyche within Psyche; a topic Secondary packages what it observes for its own Primary, which answers its Secondary, which reports to core.
+
+ ## What each aspect does
+
+ Psyche sees; its audit asks whether the system conforms to the design of the psyche, a broad audit that may redesign the architecture. Mind implements and documents; it finds optimizations and replaces bad tests with runtime tests that emulate the real world. Field maintains, debugs and deploys, running the mutating system: it starts flows and winds them down where no hook does yet, and automates winding down; it is the glue that keeps the system running, doing what is being automated.
```

Lands in no code.

Ruling:

1. Land.
2. Land with changes the living names.
3. Drop.

### Proposal 9: options and wrapped types

File: `psyche-context/skills/vision-design.md`, the description and two
new sections at the end.

Sources: flow 8475a9, 2026-10-06, relayed by flow d4ae97; flow f5a6e9,
2026-10-07.

```text
  ---
- description: A design is judged for whether its pieces are enough, or a flow meets an unanswered question while designing or building.
+ description: A design is judged for whether its pieces are enough, a flow meets an unanswered question while designing or building, or a type or a field is being shaped.
  dependencies: [intent-design]
  ---
```

```text
  No one can know ahead of time that the pieces are enough to yield the best version that could be come up with at the moment. Everybody contributes to the judgment, without limit. Judging that an idea is complete is the hardest part of a thinking machine to get.
+
+ ## Options are a last resort
+
+ An optional field is a last resort, taken only when no design without it works.
+
+ ## No double-wrapped types
+
+ A type is never wrapped in another new type: what is a flow id is called a flow id.
```

Lands in Proposal 3's code: the predecessor is a lineage record of its
own, so no field of a metaflow is optional, and a metaflow names its
flow by flow id.

Ruling:

1. Land both.
2. Land options only.
3. Land double-wrapped types only.
4. Neither.
<!-- to-the-living:end -->
