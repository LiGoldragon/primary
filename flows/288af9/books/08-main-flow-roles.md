<!-- to-the-living:start -->
Presentation.{ «Flow: main-flow mode and roles» }

# Flow: main-flow mode and roles

## Crystallization

### Proposal 1: what makes a main flow is in its system prompt

An agent script: a subflow declared once, with its own skills and
instructions, that a main flow calls by name with a brief. The agent
file: the file a harness reads to run such a subflow.

Sources: flow 6cc91b, 2026-09-14; flow 48cff7, 2026-09-16; flow
d8df70, 2026-09-24, two records; flow e51411, 2026-09-24, three
records.

File: `psyche-context/skills/intent-main-flow.md`

```text
  Your work is dialogue, coordination, priorities, authority, evidence review, and synthesis. You do not do bounded work yourself. Every inspection, search, test, edit, build, deploy, and probe is delegated to a subflow with a brief, and you receive its concise evidence. A message whose body the main flow wrote itself, it sends itself, in one command. A subflow is a separate process; what it did, you did.
+ You write no code and no script: a small thing to run is a brief to a subflow on a low layer, which writes it, runs it and reports what happened. Your model and your context are the dearest in your aspect; what a subflow can do with the right guidance, a subflow does.
```

«Your model and your context are the dearest in your aspect» is the
machine's rendering of flow 6cc91b, 2026-09-14.

File: `psyche-context/skills/vision-flow.md`

```text
  A Nexus component decides the system prompt and everything about a
  launch, replacing the harness's subagents with specialized harnesses
  launched with specialized system prompts.
+
+ What makes a flow a main flow is in its system prompt, and only there, where it outweighs the harness's own instructions.
```

A Claude agent called by name runs under its own prompt, not the main
flow's; a fork, and a Codex child's base instructions, inherit
(knowledge-subagent-context).

File: `psyche-context/skills/vision-flow.md`

```text
  The harness subagent facility is replaced. It puts two flows into one
  synchronous user interface and locks them both into a single main
  flow. A subflow is instead an independent flow with its own system
  prompt, which can reply to the successor of whoever it was meant to
  answer; that makes the system asynchronous. Subflows run under their
  own system prompts because they need different prompts.
+
+ Each flow is loaded with the skills its role needs. The skill for a bounded job is loaded into the subflow that does it, an agent script: a declared subflow with its skills and its instructions, that a main flow calls by name. For the main flow, the skill is the subflow; for the subflow, the skill is a skill.
+
+ +--------------------------------------+
+ | the main flow: dialogue, judgment    |
+ +--------------------------------------+
+         | calls by name, with a brief
+         v
+ +--------------------------------------+
+ | an agent script: a declared subflow  |
+ | with its own skills and instructions |
+ +--------------------------------------+
+    | writes and runs      | reports what
+    v                      | happened to
+ +-------------------+     |
+ | the little script |     |
+ +-------------------+     v
+                    +--------------------+
+                    | the main flow      |
+                    +--------------------+
```

«skills that only certain subagents can see» (flow e51411,
2026-09-24) stands as the record; «loaded into» is the machine's: an
agent's own definition preloads its skills, a fork inherits its
parent's, and no skill file is hidden from the main flow on a shared
filesystem (knowledge-subagent-context).

Under choice 4, the agent script is a role entry Curriculum generates
into the harness's tree; the entry's positions are `RoleAlias`'s of
`curriculum.ethos`: name, permission, depth, description, surfaces.

File: `Curriculum/roles.datom`

The aliases vector, after its `book` entry; the file is one line, so
the entry is shown in the vertical print. `write`, `trivial` and
`ClaudeAgent` are the file's own permission, depth and surface names.

```datom
+ { scripter write trivial
+   «Writes and runs a little script; reports.»
+   [ ClaudeAgent ] }
```

File: `primary/subagents/scripter.md`

```text
+ # Scripter
+
+ A main flow calls you with a brief naming a
+ small thing to run. Write the script, run it,
+ and return what happened: the command, its
+ output and what you conclude, in a few lines.
```

Under choice 5, the launcher writes the agent file into the harness's
tree, the machine's design; that tree is a generated output of
Curriculum Nexus, whose regeneration removes a file its manifest
(`skills/generated-role-outputs.datom`) does not list.

File: `primary/config/main-flow/shared.edn`

Inside its map; a declared subflow is a file named from its name, and
the agent file is written where each harness reads it. A Codex child
keeps its parent's base instructions and a role replaces only its
developer instructions, so no Codex entry is shown yet
(knowledge-subagent-context).

```clojure
+  :subflows {:dir "subflow" :file "%s.edn"}
+  :agent-file {:claude ".claude/agents/%s.md"}
```

File: `primary/config/main-flow/subflow/scripter.edn`

A new file, the machine's example: the subflow that writes and runs a
little script and reports.

```clojure
+ {:name :scripter :layer :Quaternary
+  :description
+  "Writes and runs a little script; reports."
+  :tools :claude
+  :modules {:system [:spirit-core
+                     :compensation-truth]}}
```

File: `messenger-clj/src/messenger_clj/launch.clj`, builds on «Flow:
launch and lean start» Proposal 10

After `shorthand`; `layer-row` is «Flow: the metaflow» Proposal 2,
`system-prompt` and `tools` are Proposals 1 and 6 of «Flow: launch and
lean start», `model-variant` is Proposal 2 below.

```clojure
+ (defn subflow-file [config sub]
+   (let [{:keys [dir file]} (:subflows config)]
+     (fs/path (:dir config) dir
+              (format file (name sub)))))
+
+ (defn subflow [config sub]
+   (edn/read-string
+    (slurp (str (subflow-file config sub)))))
+
+ ;; The front matter keys are the harness's agent
+ ;; file contract; the body is the subflow's own
+ ;; system prompt, its modules alone: an agent
+ ;; called by name runs under it, not under the
+ ;; main flow's prompt.
+ (defn agent-file [config aspect-config sub]
+   (let [row (layer-row aspect-config (:layer sub))
+         mv (model-variant config row)
+         front {:name (name (:name sub))
+                :description (:description sub)
+                :model (:model mv)
+                :effort (name (:effort mv))
+                :tools (tools config sub)}]
+     (str "---\n"
+          (str/join "\n"
+                    (for [[k v] front]
+                      (str (name k) ": " v)))
+          "\n---\n\n"
+          (system-prompt config {} sub))))
+
+ (defn agent-path [config harness sub]
+   (fs/path (get-in config [:workspace :path])
+            (format (get-in config
+                            [:agent-file harness])
+                    (name (:name sub)))))
+
+ (defn write-agent-file! [config aspect-config sub]
+   (let [path (agent-path config
+                          (:harness aspect-config)
+                          sub)]
+     (fs/create-dirs (fs/parent path))
+     (spit (str path)
+           (agent-file config aspect-config sub))))
```

`name`, `description`, `model`, `effort` and `tools` are the agent
file's own fields, read by the installed parser; their effect on a
running child is unwitnessed (knowledge-claude-agent-frontmatter),
the machine's.

Ruling, one number from each group:

The sentences and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

The agent file's place:
4. Generated by Curriculum from the `roles.datom` entry and
   `subagents/scripter.md`, as shown (flow 48cff7, 2026-09-16: «add
   it to the Claude subagents that are generated in curriculum»).
5. Written by the launcher into the harness's tree, as shown, the
   machine's design.

The reminder of «Flow: launch and lean start» Proposal 7 stands as
ruled there; none of his words choose on it here.

### Proposal 2: a flow is a struct with a role

A struct: a record of fixed fields; an enum: a type that is one of
its named variants, a variant carrying data of its own; the datom and
ethos words of the vision-datom skill.

Sources: flow edf227, 2026-10-03; flow d4ae97, 2026-10-07; flow
b7ba00, 2026-09-26; flow e51411, 2026-09-25, two records; flow 48cff7,
2026-09-16; flow 5ac3a3, 2026-09-27; flow d68c82, 2026-10-12.

File: `psyche-context/skills/vision-flow.md`

```text
  Flow is the Nexus that manages flows. A flow is one run of a voice; the component is named for what it manages. A flow the living asks for is launched, properly and surely. Flow holds the lock on flows.
+
+ A flow is a struct of its flow id and its role, and nothing that the role already carries. The role is an enum: a main flow's role is its aspect, carrying its topic and its layer; every other role is a job run on the smallest, most concentrated context that can be assembled for it, a system audit, living interaction, an implementation, a vision audit, and the roles yet to be made, each aspect having variants of its own. What a role needs is the data of its variant; the effort is the data of the model variant, each model having efforts of its own.
```

Long term, the machine's placement: the types go in Flow's ethos,
inside its types vector after `Address`.

File: `flow/crates/flow-ethos/ethos/library.ethos`

```ethos
    Address.{ Aspect Topic Layer }
+   Effort.[ Low Medium High Xhigh Max Ultra ]
+   Model.[ Fable.Effort Opus.Effort Sonnet.Effort
+           Haiku.Effort Astra.Effort Sol.Effort
+           Luna.Effort ]
+   Specialty.[ SystemAudit LivingInteraction
+               Implementation VisionAudit ]
+   Role.[ Psyche.{ Topic Layer Option<Specialty> }
+          Mind.{ Topic Layer Option<Specialty> }
+          Field.{ Topic Layer Option<Specialty> } ]
+   Flow.{ FlowId Role }
```

The specialized roles nested under each aspect's variant are flow
e51411, 2026-09-25; the `Option`, a main flow having no specialty, is
the machine's rendering. Under choice 7 the specialized roles are
variants carrying their aspect, the machine's rendering: one enum
keeps `role!` one lookup.

File: `flow/crates/flow-ethos/ethos/library.ethos`

```ethos
+   Role.[ Psyche.{ Topic Layer }
+          Mind.{ Topic Layer }
+          Field.{ Topic Layer }
+          SystemAudit.{ Aspect Layer }
+          LivingInteraction.{ Aspect Layer }
+          Implementation.{ Aspect Layer }
+          VisionAudit.{ Aspect Layer } ]
```

Short term, the same in the EDN and the Clojure.

File: `primary/config/main-flow/shared.edn`

Inside its map; a model's id is the harness's own name for it, its
efforts the ones its harness advertises for it, which is not their
acceptance at run time (knowledge-harness-effort).

```clojure
+  :models {:fable {:id "claude-fable-5-1"
+                   :efforts [:low :medium :high
+                             :xhigh :max]}
+           :opus {:id "claude-opus-5-5"
+                  :efforts [:low :medium :high
+                            :xhigh :max]}
+           :sonnet {:id "claude-sonnet-5-5"
+                    :efforts [:low :medium :high
+                              :xhigh :max]}
+           :haiku {:id "claude-haiku-5-5"
+                   :efforts [:low :medium :high
+                             :xhigh :max]}
+           :astra {:id "gpt-6-astra"
+                   :efforts [:low :medium :high
+                             :xhigh :max :ultra]}
+           :sol {:id "gpt-6.1-sol"
+                 :efforts [:low :medium :high
+                           :xhigh :max :ultra]}
+           :luna {:id "gpt-6-luna"
+                  :efforts [:low :medium :high
+                            :xhigh :max]}}
+  :roles [:system-audit :living-interaction
+          :implementation :vision-audit]
```

The windows of the OpenAI models move out of the refresh configuration,
which «Flow: refresh and handover» Proposal 1 removes whole.

File: `primary/config/context-refresh.json`

```json
-   "codex": {
-     "models": {
-       "gpt-6.1-sol": 373000,
-       "gpt-6-astra": 272000,
-       "gpt-6-sol": 272000,
-       "gpt-6-luna": 272000
-     }
-   },
```

File: `primary/config/main-flow/psyche.edn`, builds on «Flow: the
metaflow» Proposal 2 and «Flow: refresh and handover» Proposal 1

Each row's model is the variant and its data; the efforts are flow
d68c82, 2026-10-12. The three windows below the Primary's are the
machine's reading: the Claude mark that Proposal 1 moves is one for all
four rows, and that Proposal shows the Primary row alone.

```clojure
-  :layers [{:layer :Primary
-            :model "claude-fable-5-1"
-            :effort :medium
-            :window 1000000}
-           {:layer :Secondary :model "claude-opus-5-5" :effort :medium}
-           {:layer :Tertiary :model "claude-sonnet-5-5" :effort :medium}
-           {:layer :Quaternary :model "claude-haiku-5-5" :effort :medium :source "living correspondence"}]
+  :layers [{:layer :Primary
+            :model [:fable :medium]
+            :window 1000000}
+           {:layer :Secondary
+            :model [:opus :medium]
+            :window 1000000}
+           {:layer :Tertiary
+            :model [:sonnet :medium]
+            :window 1000000}
+           {:layer :Quaternary
+            :model [:haiku :medium]
+            :source "living correspondence"
+            :window 1000000}]
```

File: `primary/config/main-flow/mind.edn`, builds on «Flow: the
metaflow» Proposal 2

```clojure
-  :layers [{:layer :Primary :model "gpt-6-astra" :effort :medium}
-           {:layer :Secondary :model "gpt-6.1-sol" :effort :medium}
-           {:layer :Tertiary :model "gpt-6-luna" :effort :medium}
-           {:layer :Quaternary :model "gpt-6-luna" :effort :low}]
+  :layers [{:layer :Primary
+            :model [:astra :medium]
+            :window 272000}
+           {:layer :Secondary
+            :model [:sol :medium]
+            :window 373000}
+           {:layer :Tertiary
+            :model [:luna :medium]
+            :window 272000}
+           {:layer :Quaternary
+            :model [:luna :low]
+            :window 272000}]
```

File: `primary/config/main-flow/field.edn`, builds on «Flow: the
metaflow» Proposal 2

```clojure
-  :layers [{:layer :Primary :model "gpt-6-astra" :effort :medium}
-           {:layer :Secondary :model "gpt-6.1-sol" :effort :medium}
-           {:layer :Tertiary :model "gpt-6-luna" :effort :medium}
-           {:layer :Quaternary :model "gpt-6-luna" :effort :low}]
+  :layers [{:layer :Primary
+            :model [:astra :medium]
+            :window 272000}
+           {:layer :Secondary
+            :model [:sol :medium]
+            :window 373000}
+           {:layer :Tertiary
+            :model [:luna :medium]
+            :window 272000}
+           {:layer :Quaternary
+            :model [:luna :low]
+            :window 272000}]
```

File: `primary/config/main-flow/role/vision-audit.edn`

A new file, the machine's example of a specialized role's shorthand; a
role has an aspect and a layer, which pick its model.

```clojure
+ {:role :vision-audit :aspect :Psyche
+  :layer :Secondary :mode :design
+  :tools :claude
+  :modules {:system [:spirit-core :intent-psyche]
+            :user [:vision-book]}}
```

File: `primary/config/main-flow/shared.edn`

Inside its map, the role shorthands' place.

```clojure
+  :role-shorthands {:dir "role" :file "%s.edn"}
```

File: `messenger-clj/src/messenger_clj/launch.clj`, builds on «Flow:
the metaflow» Proposal 2

After `layer-row`; `ModelUnknown`, `EffortNotOfModel` and
`RoleUnknown` are the refusals' own names.

```clojure
+ ;; A model variant's data is its effort; the
+ ;; model's efforts are the ones it has.
+ (defn model-variant [config row]
+   (let [[model effort] (:model row)
+         known (get-in config [:models model])]
+     (when-not known
+       (throw (ex-info "ModelUnknown"
+                       {:model model})))
+     (when-not (some #{effort} (:efforts known))
+       (throw (ex-info "EffortNotOfModel"
+                       {:model model
+                        :effort effort})))
+     {:model (:id known) :effort effort}))
+
+ (defn role! [config role]
+   (when-not (some #{role} (:roles config))
+     (throw (ex-info "RoleUnknown" {:role role})))
+   role)
+
+ (defn role-shorthand [config role]
+   (let [{:keys [dir file]}
+         (:role-shorthands config)
+         path (fs/path (:dir config) dir
+                       (format file (name role)))]
+     (edn/read-string (slurp (str path)))))
```

File: `messenger-clj/src/messenger_clj/launch.clj`, builds on «Flow:
launch and lean start» Proposal 11

`effort!` reads the variant.

```clojure
- (defn effort! [row effort]
-   (when (and effort (not= effort (:effort row)))
-     (throw (ex-info "EffortNotDeclared"
-                     {:asked effort
-                      :declared (:effort row)})))
-   (:effort row))
+ (defn effort! [mv effort]
+   (when (and effort (not= effort (:effort mv)))
+     (throw (ex-info "EffortNotDeclared"
+                     {:asked effort
+                      :declared (:effort mv)})))
+   (:effort mv))
```

File: `messenger-clj/src/messenger_clj/launch.clj`, builds on «Flow:
launch and lean start» Proposal 10

`start-call` reads the row through the variant.

```clojure
  (defn start-call [config aspect-config mf asked]
    (let [row (layer-row aspect-config (:layer mf))
+         mv (model-variant config row)
          keys (get-in config [:start-call
                               :metaflow-keys])]
      (merge (select-keys mf keys)
             {:harness (:harness aspect-config)
-             :model (:model row)
-             :effort (effort! row (:effort asked))
+             :model (:model mv)
+             :effort (effort! mv (:effort asked))
              :tools (tools config mf)}
             (dissoc asked :effort))))
```

Under choice 5 the harness leaves the aspect file for the model, the
machine's alternative: one harness per model today.

File: `primary/config/main-flow/psyche.edn`

```clojure
  {:aspect :Psyche
-  :harness :claude
```

File: `primary/config/main-flow/mind.edn`

```clojure
  {:aspect :Mind
-  :harness :codex
```

File: `primary/config/main-flow/field.edn`

```clojure
  {:aspect :Field
-  :harness :codex
```

File: `primary/config/main-flow/shared.edn`

Inside its map, in place of the `:models` above.

```clojure
+  :models {:fable {:id "claude-fable-5-1"
+                   :harness :claude
+                   :efforts [:low :medium :high
+                             :xhigh :max]}
+           :opus {:id "claude-opus-5-5"
+                  :harness :claude
+                  :efforts [:low :medium :high
+                            :xhigh :max]}
+           :sonnet {:id "claude-sonnet-5-5"
+                    :harness :claude
+                    :efforts [:low :medium :high
+                              :xhigh :max]}
+           :haiku {:id "claude-haiku-5-5"
+                   :harness :claude
+                   :efforts [:low :medium :high
+                             :xhigh :max]}
+           :astra {:id "gpt-6-astra"
+                   :harness :codex
+                   :efforts [:low :medium :high
+                             :xhigh :max :ultra]}
+           :sol {:id "gpt-6.1-sol"
+                 :harness :codex
+                 :efforts [:low :medium :high
+                           :xhigh :max :ultra]}
+           :luna {:id "gpt-6-luna"
+                  :harness :codex
+                  :efforts [:low :medium :high
+                            :xhigh :max]}}
```

File: `messenger-clj/src/messenger_clj/launch.clj`, builds on this
book's Proposal 2

```clojure
-     {:model (:id known) :effort effort}))
+     {:model (:id known) :effort effort
+      :harness (:harness known)}))
```

```clojure
-            {:harness (:harness aspect-config)
+            {:harness (:harness mv)
```

Ruling, one number from each group:

The paragraph, the types and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

The harness:
4. Stays in the aspect file, as it stands (flow b7ba00, 2026-09-26:
   «I guess you can put it in»).
5. Leaves the aspect file for the model, as shown, the machine's
   alternative.

The specialized roles:
6. Variants nested under each aspect's variant, as shown (flow
   e51411, 2026-09-25).
7. Variants carrying their aspect, as shown, the machine's rendering.

### Proposal 3: the delegation ceiling in layers

Sources: flow 445410, 2026-10-09; flow 5ac3a3, 2026-09-27; flow
b7da5d, 2026-09-26.

File: `psyche-context/skills/vision-model-roles.md`

«Delegation ceiling», its two subsections replaced by one paragraph,
the machine's rendering of the same lines in layers through the table
above them.

```text
  Each layer has a ceiling on what subflows it may launch. Conservative by
  default: prefer the lower layer.
  
- ### OpenAI side
- 
- Luna launches only Luna. Sol is not
- launched lightly; it is getting expensive. Astra launches Sol and Luna — try Luna first. Astra is main-flow only: no flow ever
- launches an Astra subflow.
- 
- ### Claude side
- 
- Sonnet launches Sonnet and Haiku. Opus launches
- Sonnet and Haiku, and sometimes Opus, but rarely. Fable launches Opus and
- Sonnet often, and Haiku for small jobs. Fable is main-flow only: no flow
- ever launches a Fable subflow.
+ A Quaternary launches Quaternaries. A Tertiary launches Tertiaries and Quaternaries. A Secondary launches Tertiaries and Quaternaries, and a Secondary rarely, since a Secondary is not launched lightly. A Primary launches Secondaries and Tertiaries often, and Quaternaries for small jobs, the lower layer tried first. A Primary is main-flow only: no flow launches a Primary subflow.
```

The mapping in data is the `:layers` rows and `:models` of
Proposal 2.

Under choice 4 the table of layer and model moves to a skill of its
own, named for the mapping.

File: `psyche-context/skills/vision-layer-to-model.md`

```text
+ ---
+ description: A layer's model is looked up, or a model is named where a layer is meant.
+ dependencies: []
+ ---
+
+ ## Each layer has its model
+
+ | Layer | Claude (Psyche) | OpenAI (Mind, Field) |
+ |---|---|---|
+ | Primary | Fable | Astra |
+ | Secondary | Opus | Sol |
+ | Tertiary | Sonnet | Luna |
+ | Quaternary | Haiku | Luna, low effort |
+
+ Every seat runs at medium effort, except the OpenAI Quaternary.
```

File: `psyche-context/skills/vision-model-roles.md`

```text
  Roles are explained by layer, not by model; one skill maps layer to model.
- 
- | Layer | Claude (Psyche) | OpenAI (Mind, Field) |
- |---|---|---|
- | Primary | Fable | Astra |
- | Secondary | Opus | Sol |
- | Tertiary | Sonnet | Luna |
- | Quaternary | Haiku | Luna, low effort |
- 
- Every seat runs at medium effort, except the OpenAI Quaternary.
```

```text
- The layer selects the configured model through the table above, so the
+ The layer selects the configured model through the vision-layer-to-model skill, so the
  title names the layer, never the model.
```

Ruling, one number from each group:

The paragraph:
1. Land.
2. Land with changes the living names.
3. Drop.

The table of layer and model:
4. Moves to a skill of its own, as shown (flow 445410, 2026-10-09:
   «we should just have a layer-to-model skill»).
5. Stays in this skill, as it stands, the machine's suggestion: this
   skill already says one skill maps layer to model.

### Proposal 4: speech climbs one layer; the Secondary is the secretary

The secretary: the Secondary of a Primary's aspect and topic, the
word of «Flow: launch and lean start» Proposal 12.

Sources: flow d4ae97, 2026-10-07; flow 5578cc, 2026-10-03.

File: `psyche-context/skills/intent-main-flow.md`

```text
  Never block on a subflow. When the living speaks, answer from what is already witnessed; a holding line while a subflow is out is a complete answer.
+
+ You speak across at your own layer, one layer up in your own aspect, or to any layer below, in any aspect. A Secondary is its Primary's secretary: it keeps track of what the Primary works on, and what climbs from below reaches the Primary through it. A Primary designs and implements through its own subflows. Below the Primary, you ask the layer above for authority and a mandate when you are not sure, and you say that you do not know: the layer above infers better than you.
```

File: `psyche-context/skills/vision-model-roles.md`

```text
- Horizontal communication joins aspects at the same layer.
- Vertical communication stays within one aspect and normally advances one layer
- at a time. If the adjacent layer is absent or unavailable, routing advances to
- the next running layer in that direction, so a Tertiary may reach the Primary
- when the Secondary is not running. The missing layer is reported as a gap; it
- does not make the message disappear.
+ Speech climbs one layer at a time, within one aspect, never skipping a layer, and descends to any layer, across aspects too; the Primary layer is spoken to least.
+
+ +--------------------------------------+
+ | Primary, in each aspect              |
+ +--------------------------------------+
+    ^ one layer up,        | any layer down,
+    | own aspect           v across aspects too
+ +--------------------------------------+
+ | Secondary, the Primary's secretary   |
+ +--------------------------------------+
+    ^ one layer up,        |
+    | own aspect           v
+ +--------------------------------------+
+ | Tertiary                             |
+ +--------------------------------------+
+    ^ one layer up,        |
+    | own aspect           v
+ +--------------------------------------+
+ | Quaternary                           |
+ +--------------------------------------+
```

```text
- Horizontal routing selects the unique eligible cell in the target aspect at
- the sender's layer. Vertical routing selects the nearest eligible
- layer in the requested direction within the same aspect. Busy is still
+ Horizontal routing selects the unique eligible cell in the target aspect at
+ the sender's layer. Upward routing selects the layer above, within the same aspect; downward routing selects the layer named. Busy is still
```

Under choice 5 the messenger checks the route, the machine's design.

File: `primary/config/main-flow/shared.edn`

Inside its map; the order of the layers is the machine's addition:
nothing else in the EDN says which layer is above which.

```clojure
+  :layer-order [:Primary :Secondary
+                :Tertiary :Quaternary]
```

File: `primary/config/main-flow/shared.edn`, builds on «Flow: launch
and lean start» Proposal 5

Inside `:environment`; the variable is the machine's addition, the
bootstrap pointer from a flow's commands to the EDN, as `FLOW_ID` is
to the flow.

```clojure
   :environment
   {:flow-id "FLOW_ID"
+   :config "HM_CONFIG"
```

File: `messenger-clj/src/messenger_clj/launch.clj`, builds on «Flow:
launch and lean start» Proposal 5

```clojure
- (defn env-args [config harness flow-id]
+ (defn env-args [config harness flow-id file]
    (let [env (:environment config)
          unset (get-in env [harness :unset])]
      (concat (mapcat #(list "-u" %) unset)
-             [(str (:flow-id env) "=" flow-id)])))
+             [(str (:flow-id env) "=" flow-id)
+              (str (:config env) "=" file)])))
```

File: `messenger-clj/src/messenger_clj/core.clj`

`sender-origin!` split so the sender's route is kept.

```clojure
- (defn sender-origin! []
+ (defn sender-route! []
```

```clojure
-       (metaflow! route))))
+       route)))
+
+ (defn sender-origin! []
+   (metaflow! (sender-route!)))
```

File: `messenger-clj/src/messenger_clj/core.clj`

Before `send-request!`. The variable's name is the one bootstrap
literal, as `HM_REGISTRY` and `FLOW_ID` are in this file: the pointer
to the EDN cannot be read from the EDN. The refusals are in the
messenger's reply form, `Name.{ … }`, as `Held` and `Uncertain` are.

```clojure
+ (defn config! []
+   (let [file (System/getenv "HM_CONFIG")]
+     (when (str/blank? file)
+       (fail "ConfigUnset.HM_CONFIG"))
+     (edn/read-string (slurp file))))
+
+ (defn rank [order layer]
+   (let [i (.indexOf order (keyword layer))]
+     (when (neg? i)
+       (fail (str "LayerUnknown.«" layer "»")))
+     i))
+
+ ;; Down and across is free; up is one layer, in
+ ;; the sender's own aspect.
+ (defn layer-route! [order from to]
+   (let [a (rank order (:layer from))
+         b (rank order (:layer to))]
+     (when-not (or (>= b a)
+                   (and (= b (dec a))
+                        (= (:aspect from)
+                           (:aspect to))))
+       (fail (str "LayerRouteRefused.{ «"
+                  (metaflow! from) "» «"
+                  (metaflow! to) "» }")))))
```

File: `messenger-clj/src/messenger_clj/core.clj`

In `send-request!`, the sender bound as its route, and the check where
the recipient's stored route is first bound; a missing route is held
below, as it stands.

```clojure
-    (let [sender (sender-origin!)]
+    (let [from (sender-route!)
+          sender (metaflow! from)]
```

```clojure
-          (let [raw-stored (try (load-route (registry) flow) (catch Exception _ nil))
-                stored (try (when raw-stored (route-binding! raw-stored)) (catch Exception _ nil))]
+         (let [raw-stored
+               (try (load-route (registry) flow)
+                    (catch Exception _ nil))
+               stored
+               (try (when raw-stored
+                      (route-binding! raw-stored))
+                    (catch Exception _ nil))
+               _ (when raw-stored
+                   (layer-route!
+                    (:layer-order (config!))
+                    from raw-stored))]
```

Ruling, one number from each group:

The paragraphs and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

The enforcement:
4. The intent paragraph alone, the messenger unchanged (flow d4ae97,
   2026-10-07: «the messaging program is imperfect and it cannot
   actually enforce this»).
5. The messenger's check, as shown, the machine's design, from «I want
   that hard-enforced» of the same record.

### Proposal 5: spirit, intent and vision are Psyche's topics

Sources: flow d4ae97, 2026-10-07; flow d68c82, 2026-10-12.

File: `psyche-context/skills/vision-aspects.md`

```text
  Psyche core keeps track of all the psyche within Psyche; a topic Secondary packages what it observes for its own Primary, which answers its Secondary, which reports to core.
+
+ Within Psyche, spirit, intent and vision are each a topic with its own layers; the three stand in that order, a hierarchy of Psyche's own.
```

Six new shorthands of «Flow: launch and lean start» Proposal 10; the
metaflow and its Secondary are the ones he names in flow d68c82,
2026-10-12. `:mode :design` and the empty module lists are the
machine's: no record names these flows' mode or modules, and the
aspect file's modules load.

File: `primary/config/main-flow/metaflow/Psyche-spirit-Primary.edn`

```clojure
+ {:aspect :Psyche :topic :spirit :layer :Primary
+  :mode :design
+  :modules {:system [] :user []}}
```

File: `primary/config/main-flow/metaflow/Psyche-spirit-Secondary.edn`

```clojure
+ {:aspect :Psyche :topic :spirit :layer :Secondary
+  :mode :design
+  :modules {:system [] :user []}}
```

File: `primary/config/main-flow/metaflow/Psyche-intent-Primary.edn`

```clojure
+ {:aspect :Psyche :topic :intent :layer :Primary
+  :mode :design
+  :modules {:system [] :user []}}
```

File: `primary/config/main-flow/metaflow/Psyche-intent-Secondary.edn`

```clojure
+ {:aspect :Psyche :topic :intent :layer :Secondary
+  :mode :design
+  :modules {:system [] :user []}}
```

File: `primary/config/main-flow/metaflow/Psyche-vision-Primary.edn`

```clojure
+ {:aspect :Psyche :topic :vision :layer :Primary
+  :mode :design
+  :modules {:system [] :user []}}
```

File: `primary/config/main-flow/metaflow/Psyche-vision-Secondary.edn`

```clojure
+ {:aspect :Psyche :topic :vision :layer :Secondary
+  :mode :design
+  :modules {:system [] :user []}}
```

Ruling:

1. Land.
2. Land with changes the living names.
3. Drop.

### Proposal 6: every flow that hears the psyche logs it and relays it

Source: flow e51411, 2026-09-25.

File: `psyche-context/skills/intent-psyche-interaction.md`

```text
- Every main flow interacts with the psyche, so every main flow loads psyche-interraction and relays what it hears to a Psyche flow.
+ Every main flow interacts with the psyche, so every main flow loads psyche-interraction; the Psyche flows are the specialists of the psyche, not the only flows that hear it. Usually, a flow that hears the psyche logs it itself and relays it to a Psyche flow as well.
```

Under choice 5, the machine's stricter line: a relay left out is
psyche the Psyche flows never see.

File: `psyche-context/skills/intent-psyche-interaction.md`

```text
- Every main flow interacts with the psyche, so every main flow loads psyche-interraction and relays what it hears to a Psyche flow.
+ Every main flow interacts with the psyche, so every main flow loads psyche-interraction; the Psyche flows are the specialists of the psyche, not the only flows that hear it. A flow that hears the psyche logs it itself and relays it to a Psyche flow as well.
```

Ruling, one number from each group:

The sentence:
1. Land.
2. Land with changes the living names.
3. Drop.

The relay:
4. «Usually», as shown (flow e51411, 2026-09-25).
5. Always, as shown, the machine's stricter line.

### Proposal 7: the operator's notes

Source: flow 48cff7, 2026-09-16.

Under choice 1 the idea is vision.

File: `psyche-context/skills/vision-flow.md`

```text
  The flow repository holds the machinery of the Flow Nexus and is a
  runtime repository. Every skill lives outside it, the basic skills
  included, so that a change to a skill causes no Nix rebuild. The
  basic skills give our own take on how an agent behaves in a harness,
  replacing the prompt the harnesses build in.
+ Each role has an operator's notes skill, named for the role, that a flow of the role edits itself when it learns a way of operating better, more liberally than a standing skill is edited.
```

File: `primary/config/main-flow/shared.edn`, builds on «Flow: launch
and lean start» Proposal 1

Inside its map and inside `:prompt`. The notes are a workspace file
rather than a skill, the machine's design: the skill trees are
generated and read-only to a flow. The file's name, from the
metaflow's aspect and topic, is the machine's rendering: the role a
main flow has is its metaflow (Proposal 2).

```clojure
+  :notes {:file "notes/%s-%s.md"}
```

```clojure
-  :prompt {:parts [:flow-id :mode :modules :brief]
+  :prompt {:parts [:flow-id :mode :modules
+                   :notes :brief]
```

File: `messenger-clj/src/messenger_clj/launch.clj`, builds on «Flow:
launch and lean start» Proposal 1

Before `prompt-parts`, which gains the part.

```clojure
+ (defn notes-file [config mf]
+   (fs/path (get-in config [:workspace :path])
+            (format (get-in config [:notes :file])
+                    (name (:aspect mf))
+                    (name (:topic mf)))))
+
+ ;; Notes are read from the working tree, since
+ ;; the flow itself writes them.
+ (defn notes-block [config mf]
+   (let [file (notes-file config mf)]
+     (when (fs/exists? file)
+       (str/trim (slurp (str file))))))
```

```clojure
+    :notes (notes-block config mf)
     :brief (:brief launch)})
```

**Destroy**, under choice 2: the entry moves whole, to a notion.

File: `flows/48cff7/vision/flowOperatorNotes.md`

```text
- ## 2026-09-16 — a flow role has an operator's notes skill it can edit itself, more liberally than a standing skill
- 
- Context: after the accumulated-proposal document landed, the living opened a new idea.
- 
- > Oh, I just had a brilliant idea. There is a skill, the Flow, that is named after it and can more liberally edit when it learns a way of doing something, like operational notes. It's like an operator's note skill. You have the psyche's operators' notes skill. He can say, "Oh, I have a suggestion for basically anything that he needs to know to operate better. He should just edit it." I don't know exactly how that's going to work, but that's the idea. That's the vision. Let's see how we would do that.
- 
- -- psyche, typed.
```

File: `flows/48cff7/notion/flowOperatorNotes.md`

```text
+ # flowOperatorNotes
+
+ ## 2026-09-16 — a flow role has an operator's notes skill it can edit itself, more liberally than a standing skill
+ 
+ Context: after the accumulated-proposal document landed, the living opened a new idea.
+ 
+ > Oh, I just had a brilliant idea. There is a skill, the Flow, that is named after it and can more liberally edit when it learns a way of doing something, like operational notes. It's like an operator's note skill. You have the psyche's operators' notes skill. He can say, "Oh, I have a suggestion for basically anything that he needs to know to operate better. He should just edit it." I don't know exactly how that's going to work, but that's the idea. That's the vision. Let's see how we would do that.
+ 
+ -- psyche, typed.
```

**Destroy**, under choice 3: the machine's sections of the two 48cff7
records, written by the flow and not his words.

File: `flows/48cff7/vision/flowOperatorNotes.md`

```text
- 
- ## Flow reading
- 
- Each flow role has an *operator's notes* skill named after itself — a loose, editable-by-the-flow scratchpad of how-to-operate. Unlike the standing skills composed under skill-designing's brutal minimalism, the operator's notes accepts verbose, tentative, iteratively-refined tips. When a session in that role learns a way of doing something better, it edits its own notes so the next session starts with the discovery.
- 
- ## Proposed shape
- 
- A per-role skill file `<flow-role>-notes.md`, or `<role>-<tier>-notes.md` when the tip differs by effort tier. Examples:
- 
- - `psyche-notes.md` — for any psyche flow.
- - `psyche-medium-notes.md` — specific to MEDIUM tier when the tip is tier-specific.
- - `visualization-notes.md` — for visualization subflows.
- - `implementation-notes.md` — for implementation subflows.
- 
- Content is free-form. Sections by topic. Entries dated. Each entry names what was learned and how it applies. A seed demonstration lives at `flows/48cff7/notes/psyche-medium-notes.md`.
- 
- The flow reads its notes file at session start (as part of its role skill's dependencies) and adds to it during the session. Every edit is committed to the flow branch with a short line naming what was learned.
- 
- ## Kind and place in the taxonomy
- 
- Operator's notes fit awkwardly against the source kinds named in `flows/48cff7/vision/skillSourceKinds.md`:
- 
- - Not *vision-derived* — they are not designed; they are discovered.
- - Not *mind-derived* — they are operational habits, not verified world-facts.
- - Not quite *usage* — usage teaches a tool's language; notes teach a role's practice.
- 
- Proposal: a fourth source kind, **Notes**, whose content is editable by the flow itself. Alternatively, a subtype marker under Usage.
- 
- Editing rules for the Notes kind are looser than skill-designing:
- 
- - Verbose is acceptable when brevity would lose signal.
- - Tentative wording is acceptable; iteration is expected.
- - The flow may add, edit, or reorganize its own notes; it may not edit another role's notes.
- - Every edit still commits with a short line naming the incident or the choice being recorded.
- 
- ## Consequences
- 
- - **Accumulation across sessions.** A successor psyche-main-flow session loads the same `psyche-notes.md` and inherits every prior discovery. Refresh becomes cheaper — the successor does not re-learn what the predecessor already learned.
- - **Drift risk.** Free-form editing can accumulate stale or contradicting notes. A periodic pruning pass by a psyche flow keeps the file current.
- - **Ownership boundary.** A flow edits only its own role's notes. Cross-role suggestions become vision proposals for the other role's operator to consider.
- - **Promotion path.** A note that hardens into a standing rule promotes upward — from notes to a vision entry, from vision to a skill body — per the pipeline in `flows/48cff7/vision/highPowerAndUpgradePipeline.md`.
- 
- ## Open questions worth the living's word
- 
- 1. Confirm the file-per-role shape, or prefer file-per-role-per-tier, or file-per-role-per-stack.
- 2. Whether Notes is a fourth source kind or a subtype of Usage.
- 3. Whether a flow may add a note that references or contradicts a standing Vision — if so, does that trigger a promotion path?
- 4. Where the file lives — Curriculum authored surface (alongside other skills), or a separate `notes/` tree beside it.
- 5. Which flow performs the periodic pruning pass, and how often.
```

File: `flows/48cff7/vision/flowAnatomy.md`

```text
- 
- Flow reading, not the living's words: every named flow type (psyche, visualization, narrator, gatherer, implementation, …) is *shaped* by two things: a shared harness base and a role block that varies. The role block is the anatomy — that is what makes a visualization flow different from a psyche flow. ASCII carries the anatomy readably in the terminal; a renderer can infer the same graph from it that it would from mermaid, so the choice is stylistic when the density is low.
- 
- ## Anatomy (ASCII)
- 
- ```
- flow harness system prompt
- ├── shared across flow types
- │   ├── harness base                tool schemas · tone guidance · doing-tasks guidance
- │   ├── project instructions        CLAUDE.md · NON_MANAGEMENT_AGENTS.md · SKILL_VARIABLES.md
- │   ├── skills index                <name> — <one-line description>
- │   └── environment                 cwd · git status · session id · date
- │
- └── role block                      ← varies per flow type; the anatomy
-     ├── role name                   psyche · visualization · narrator · gatherer · implementation · …
-     ├── effort tier                 LOW · MEDIUM · HIGH
-     ├── stack                       Claude · Codex · open
-     ├── layer                       primary · secondary · core
-     ├── authority scope             what this flow may do; what it must never do
-     ├── peers                       coordinating sessions
-     ├── ad hoc skill body inline    setup-specific behavior not yet in Curriculum
-     └── role skills to load         Curriculum skills the role's work always uses
- ```
- 
- ## Example role blocks
- 
- ```
- role block — psyche · MEDIUM · Claude · primary  (this flow, 48cff7)
- ├── role name          psyche
- ├── effort tier        MEDIUM
- ├── stack              Claude
- ├── layer              primary
- ├── authority          draft locally, respond to living, dispatch subflows
- │                      · NEVER contact HIGH without living word
- │                      · NEVER refresh Codex, change settings, use reset
- │                      · NEVER render (charts, SVG, HTML)
- ├── peers              Codex d9961c (native thread 01a0aacb-ac84-71a1-88a0-05ed9961ca9d)
- ├── ad hoc skill body  psyche-power-protocol
- └── role skills        psyche · spirit · main-flow · transcript-search · datom · nexus
- 
- role block — visualization · [effort] · [stack] · [layer]  (does not yet exist)
- ├── role name          visualization
- ├── effort tier        (low; rendering is cheap)
- ├── stack              (any)
- ├── layer              (primary)
- ├── authority          receive (pointer, anatomy, ethos, intent), fetch block via transcript-nexus,
- │                      produce SVG · NEVER edit source of truth · NEVER speak to living directly
- ├── peers              (whichever main flow dispatched it)
- ├── ad hoc skill body  (per dispatch)
- └── role skills        transcript-search · datom · artifact-diagramming · artifact-design
- ```
- 
- ## Open questions worth the living's word
- 
- 1. Whether "stack" and "layer" belong inside the role block, or in the shared header (all flows in a given deployment carry the same stack and layer).
- 2. Whether "authority scope" is expressed as prose (as today) or as an ethos-typed capability set.
- 3. Which role skills are the fixed floor for each flow type (this is what "we should have started with" would look like made explicit).
- 4. Whether the ad hoc skill body should always be inline in the role block, or referenced by hash from Curriculum once a role stabilises.
- 5. Whether the "environment" bullet belongs above or below the role block in the actual prompt order (I put shared first here; the current Claude Code layout interleaves them).
```

Ruling, one number from each group:

The idea:
1. Vision, as the sentence and code above show (flow 48cff7,
   2026-09-16: «That's the vision»).
2. Notion, moved as shown, the machine's suggestion: «I don't know
   exactly how that's going to work» (flow 48cff7, 2026-09-16).

The machine's sections of the two records:
3. Destroy them, as shown.
4. Keep them.

### Proposal 8: a Primary poses questions; hooks carry them

Sources: flow d68c82, 2026-10-13; flow b7da5d, 2026-09-26.

Under choice 4 the idea is vision.

File: `psyche-context/skills/vision-flow.md`

```text
  Creating a subflow is a routing job: whether there is already a flow
  that should simply get this message or this question. A Field
  Quaternary flow checks every question and every
  request a flow ends with, and, according to the ending flow's
  authority, spawns subflows given those questions and requests to
  answer or fulfill.
+
+ A flow poses a question in its reply and makes no call for it: a hook forwards the question as the turn ends, and the answer comes back queued for the flow's next turn, with whatever else was queued for it, the psyche's new words among them. A Fable Primary so served has hardly any tool access, and its context goes to judging, inferring and summarizing; the shoveling is the lower layers'.
+
+ +--------------------------------------+
+ | the Primary's reply                  |
+ +--------------------------------------+
+         | ends the turn; the hook reads
+         v
+ +--------------------------------------+
+ | Question.{ «…» } blocks in it        |
+ +--------------------------------------+
+         | are sent to
+         v
+ +--------------------------------------+
+ | the Field Quaternary                 |
+ +--------------------------------------+
+         | spawns subflows, which answer into
+         v
+ +--------------------------------------+
+ | the Primary's queue                  |
+ +--------------------------------------+
+         | enters, with the psyche's new words,
+         v
+ +--------------------------------------+
+ | the Primary's next turn              |
+ +--------------------------------------+
```

**Destroy**, under choice 5: the entry moves whole, to a notion.

File: `flows/d68c82/vision/seats.md`

```text
- ## Fable judges; lower layers shovel
- 
- > I'd also like to talk about how we can insulate Fable from the low-level drudgery, the shoveling aspect that should be the concern of lower levels.
- >
- > I see a world where we have Fable Flow, or more than one, which doesn't actually have hardly any tool access. Something like that, where any questions that it brings forth would be researched and answered by other models. Some hooks would automatically forward these questions. The Fable Flow wouldn't have to make the call to a sub-agent to look into stuff. It would just pose the question and the question would be answered. The answer would be given back to it the next time it gets a turn, with all the other things that would be queued for it: whether they're new insights from the psyche, information that a previous turn was asking about, or anything like that. All of its context would revolve around making judgments, inferring, and summarizing instead of actually grabbing the shovel handle and shoveling.
- 
- Context: same comment, 2026-10-13T16:20.
- -- psyche, STT.
```

File: `flows/d68c82/notion/seats.md`

```text
+ ## Fable judges; lower layers shovel
+ 
+ > I'd also like to talk about how we can insulate Fable from the low-level drudgery, the shoveling aspect that should be the concern of lower levels.
+ >
+ > I see a world where we have Fable Flow, or more than one, which doesn't actually have hardly any tool access. Something like that, where any questions that it brings forth would be researched and answered by other models. Some hooks would automatically forward these questions. The Fable Flow wouldn't have to make the call to a sub-agent to look into stuff. It would just pose the question and the question would be answered. The answer would be given back to it the next time it gets a turn, with all the other things that would be queued for it: whether they're new insights from the psyche, information that a previous turn was asking about, or anything like that. All of its context would revolve around making judgments, inferring, and summarizing instead of actually grabbing the shovel handle and shoveling.
+ 
+ Context: same comment, 2026-10-13T16:20.
+ -- psyche, STT.
```

File: `primary/config/main-flow/shared.edn`, builds on «Flow: launch
and lean start» Proposal 6

Under choice 4, inside its map; the mark is the block's head, the
recipient a metaflow in the messenger's name form; and inside
`:tools`, the set a judging Primary carries, the machine's choice of
tools: its own files alone, since what it would look up with Bash or
the web goes out as a question; Write and Edit write its log and its
psyche records without Bash (knowledge-claude-tool-allowance).

```clojure
+  :questions {:mark "Question"
+              :to "Field core Quaternary"}
```

```clojure
+          :judge ["Read" "Write" "Edit"]
```

File: `primary/config/main-flow/shared.edn`, builds on «Flow: launch
and lean start» Proposal 5

Inside `:command`, the `:claude` vector; `--tools` sets the built-in
tools a flow has, where a tool left out of `--allowedTools` is not
removed (knowledge-claude-tool-allowance).

```clojure
-    "--allowedTools" :tools
+    "--tools" :tools
```

File: `messenger-clj/src/messenger_clj/launch.clj`, builds on «Flow:
launch and lean start» Proposal 6

```clojure
- ;; --allowedTools takes its names comma-joined,
- ;; the harness's own form of the flag.
+ ;; --tools takes its names comma-joined, the
+ ;; harness's own form of the flag.
```

File: `primary/config/main-flow/metaflow/Psyche-flow-Primary.edn`,
builds on «Flow: launch and lean start» Proposal 10

Under choice 6; the Psyche flow Primary loses the Artifact tools it
publishes books with.

```clojure
-  :tools :book-publisher
+  :tools :judge
```

File: `messenger-clj/src/messenger_clj/questions.clj`

A new file, under choice 4, the machine's design; `json-lines` and
`flow-of-thread` are «Flow: refresh and handover» Proposal 1 and
`aspect-config` is «Flow: launch and lean start» Proposal 7;
`ReplyUnread` is the refusal's own name. `response_item`, `message`,
`assistant` and `output_text` are the rollout's own markers; the last
such text is the latest assistant text, not always a completed turn's
answer (knowledge-codex-rollout).

```clojure
+ (ns messenger-clj.questions
+   (:require [messenger-clj.core :as hm]
+             [messenger-clj.refresh :as refresh]))
+
+ ;; The transcript's record keys are the harness's
+ ;; own; the last text of the assistant is the
+ ;; reply.
+ (defn claude-reply [path]
+   (->> (refresh/json-lines path)
+        (filter #(= "assistant" (:type %)))
+        (mapcat #(get-in % [:message :content]))
+        (filter #(= "text" (:type %)))
+        (map :text)
+        last))
+
+ ;; The rollout's record keys are the harness's
+ ;; own: a response_item whose payload is an
+ ;; assistant message, its output_text entries.
+ (defn codex-reply [path]
+   (->> (refresh/json-lines path)
+        (filter #(= "response_item" (:type %)))
+        (map :payload)
+        (filter #(and (= "message" (:type %))
+                      (= "assistant" (:role %))))
+        (mapcat :content)
+        (filter #(= "output_text" (:type %)))
+        (map :text)
+        last))
+
+ ;; :claude and :codex are the aspect file's
+ ;; :harness values; a transcript with no
+ ;; assistant text is refused.
+ (defn reply [harness path]
+   (or (case harness
+         :claude (claude-reply path)
+         :codex (codex-reply path))
+       (hm/fail (str "ReplyUnread: "
+                     (name harness)))))
+
+ ;; A marked block is Head.{ «…» }: the head is
+ ;; the mark, the guillemets datom's string form.
+ (defn marked [mark text]
+   (map second
+        (re-seq (re-pattern
+                 (str mark "\\.\\{ «([^»]*)» \\}"))
+                (or text ""))))
+
+ ;; :session_id and :transcript_path are the
+ ;; harness's own fields of the hook event.
+ (defn harness [config event]
+   (let [[_ route] (refresh/flow-of-thread
+                    (hm/route-records)
+                    (:session_id event))]
+     (:harness (refresh/aspect-config
+                config (:aspect route)))))
+
+ ;; send! without waiting, no pane named.
+ (defn forward! [config event]
+   (let [{:keys [mark to]} (:questions config)
+         text (reply (harness config event)
+                     (:transcript_path event))]
+     (doseq [q (marked mark text)]
+       (hm/send! to q false nil))))
```

File: `messenger-clj/src/messenger_clj/main.clj`, builds on «Flow:
launch and lean start» Proposal 7

The `ns` form and the `turn-end` dispatch.

```clojure
+             [messenger-clj.questions :as q]
```

```clojure
            "turn-end"
-           (refresh/turn-end! (hook-config xs)
-                              (hook-event!))
+           (let [config (hook-config xs)
+                 event (hook-event!)]
+             (refresh/turn-end! config event)
+             (q/forward! config event))
```

Ruling, one number from each group:

The paragraph, the figure and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

The idea:
4. Vision, as shown: the hook that reads the transcript is the flow
   wanted (flow b7da5d, 2026-09-26).
5. Notion, moved as shown, the machine's suggestion: «I see a world
   where» (flow d68c82, 2026-10-13).

The judging set:
6. The Psyche flow Primary carries it, as shown.
7. No Primary yet; the set is declared only.
<!-- to-the-living:end -->
