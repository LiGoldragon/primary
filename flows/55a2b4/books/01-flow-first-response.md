# Flow: the first response

```
┌──────────────┐
│ Flow starter │
└──────┬───────┘
       │ reads
       ▼
┌──────────────────────────┐
│ EDN: aspect, metaflow,   │
│ first-prompt template    │
└──────┬───────────────────┘
       │ fills with
       ▼
┌──────────────────────────┐
│ topic · handover · raw   │
│ psyche with its context  │
└──────┬───────────────────┘
       │ starts
       ▼
┌──────────────┐
│ new flow     │
└──────┬───────┘
       │ answers, first turn
       ▼
┌──────────────────────────┐
│ crystallization proposal │
│ or a question            │
└──────────────────────────┘
```

**P1 — The first prompt and the first response**

File: psyche-context/skills/vision-flow.md, section Starting flows, after the launch paragraph

```
  A layer is Primary, Secondary, Tertiary or
  Quaternary, in every aspect; ... checking each
  module's hash against its source.
+
+ A flow is started with something to do. Its
+ first prompt carries its topic, its handover,
+ and the raw psyche on that topic, each record
+ with the context of the flow that heard it.
+ The flow's first response, the whole of its
+ first turn, is a crystallization proposal on
+ that topic, or a question where no proposal
+ stands. No flow is started only to say it is
+ ready.
```

Choice 1.1 — the response shaped by aspect (your earlier, wider wording):
```
+ ... is a presentation in its role: Psyche
+ distils its context for vision, Mind for
+ knowledge and implementation, Field for its
+ own; a question where no proposal stands.
```

**P2 — The startup context is data**

File: psyche-context/skills/vision-flow.md, after P1

```
+ The default startup context is data read by
+ the starter: a prompt, a model, a skill list
+ or a path is never hard-coded in code.
```

The standard entry point that lands it, shown once (the per-file removals live in the refs):

File: config/main-flow/first-prompt.edn
```
+ {:schema "first-prompt/1"
+  :template
+  "Topic: {{topic}}
+
+ Handover: {{handover}}
+
+ Raw psyche records on this topic, each read
+ with the context of its flow:
+ {{records}}
+
+ Your first response is a crystallization
+ proposal on this topic, made from these
+ records, or a question where no proposal
+ stands."}
```

File: tools/first_prompt.clj (run by bb)
```
+ (ns first-prompt
+   (:require [clojure.edn :as edn]
+             [clojure.string :as str]))
+
+ (defn- fill [template values]
+   (reduce-kv
+    (fn [text k v]
+      (str/replace text
+                   (str "{{" (name k) "}}") v))
+    template values))
+
+ (defn first-prompt
+   "The first prompt of a seat, filled from
+   its launch record."
+   [entry-path launch]
+   (let [entry (edn/read-string
+                (slurp entry-path))]
+     (fill (:template entry)
+           {:topic (name (:topic launch))
+            :handover (:handover launch)
+            :records (->> (:records launch)
+                          (map #(str "- " %))
+                          (str/join "\n"))})))
```

**P3 — Flow, Nexus and Ethos together; Flow bootstrapped first**

File: psyche-context/skills/vision-flow.md, section What it does

```
- Flow deploys first and is used raw to send
- messages, until Message sends through Flow's
- socket.
+ Flow, the Nexus architecture and Ethos are
+ developed together: Ethos the language, Nexus
+ the runtime, Flow the component bootstrapped
+ first, since starting clean lean flows,
+ specialized flows and refreshed flows is a
+ cornerstone of the system. Flow deploys first
+ and is used raw to send messages, until
+ Message sends through Flow's socket.
```

Choice 3.1 — the bootstrapped thing is Persona, the meta harness, and the sentence lands in vision-persona.md instead, Flow named as its first component:
```
+ Persona, the meta harness, is bootstrapped
+ first; Flow is its first component, since
+ starting clean lean flows, ...
```

**P4 — Short-term prototypes in Clojure** (builds on book 14 P1–P3, unruled)

File: psyche-context/skills/vision-flow.md, after P2

```
+ A short-term prototype is written in Clojure
+ with its values in EDN; one not in Clojure is
+ rewritten in Clojure, the Flow starter first.
```

Choice 4.1 — the rule lands with book 14's module rather than here, vision-flow keeping only «the Flow starter is rewritten first».
