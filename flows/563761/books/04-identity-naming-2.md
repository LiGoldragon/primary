<!-- to-the-living:start -->
Presentation.{ «Flow: identity and naming, second edition» }

# Flow: identity and naming, second edition

## Crystallization

### Proposal 1: a flow id is a hash

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«A topic's name is a camelCase identifier». As it stands:

"A topic's name is a camelCase identifier, uncapitalized. A flow's id is
the hash of the harness's session id, so a transcript is found from the
flow id. Where the harness lets Flow choose the session id, Flow chooses
it before the flow starts and the flow reads it in its prompt; where the
harness assigns it, Flow learns it when the flow binds. No flow declares
its id: every call to Flow is identified by the calling process."

"Binds": the moment Flow ties a flow's record to the live process that
runs it.

Sources: flow 692df8, 2026-09-15; flow edf227, 2026-10-03.

Removed: none.

Added, after «so a transcript is found from the flow id.»:

+ A flow id is a hash, never a string; its written forms are its serialization, made where it leaves Flow, and Flow itself holds only the hash.

Lands in the short-term tools, as Clojure run by Babashka (a program
that runs Clojure scripts at once, without starting a full Java
system). Today a flow id is claimed by `flow-id`, a Rust program in
the harness repository (`src/flow_id.rs`): it takes the harness's
session id, a UUID of 32 hex digits, takes six digits of it as the
flow's id, one digit more at each collision, and creates that flow's
directory. The six and the place where the digits start are written
into its code:

```rust
- const FIRST_CANDIDATE_LENGTH: usize = 6;
- const CODEX_CANDIDATE_START: usize = 23;
```

The whole Rust tool is removed. Both numbers move to
`primary/config/main-flow/shared.edn`, an EDN file (EDN: Clojure's
plain data notation; braces hold a map, brackets a vector, a word with a
leading colon is a keyword). Added inside its map, after `:tools`:

```clojure
+  :flow-id {:first-width 6
+            :session-bits 128
+            :start {:claude 0 :codex 23}}
```

`:start` is where in the 32 digits the short id begins: at the first
for Claude, at the twenty-fourth for Codex, where its id is random.
`:session-bits` is the width of the session id, 128 bits, 32 hex
digits; the code derives from it the width of the hex form and the
longest short id, and Proposal 2 reads the same key. Four bits to a
hex digit is the number base's own shape and stays in the code.

The Clojure rewrite is a new file,
`messenger-clj/src/messenger_clj/flow_id.clj`, beside the messenger
(messenger-clj, the short-term tool that registers flows and types
messages into them). `config` below is `shared.edn` as read, with
`:dir`, the directory it was read from, added by the reader. Under
choice 1, the machine's design (a record: Clojure's named map with
fixed fields):

```clojure
+ (ns messenger-clj.flow-id
+   (:require [babashka.fs :as fs]
+             [clojure.edn :as edn]
+             [clojure.string :as str])
+   (:import
+    [java.nio.file FileAlreadyExistsException]))
+
+ ;; The harness's session id as a number,
+ ;; and where its short written form sits.
+ (defrecord FlowId [session start width])
+
+ (defn session-bits [uuid]
+   (BigInteger. (str/replace uuid "-" "") 16))
+
+ (defn hex-digits [config]
+   (quot (get-in config [:flow-id :session-bits])
+         4))
+
+ (defn session-hex [config session]
+   (format (str "%0" (hex-digits config) "x")
+           session))
+
+ (defn short-hex [config id]
+   (let [{:keys [session start width]} id]
+     (subs (session-hex config session)
+           start (+ start width))))
+
+ (defn claim-lane! [config root id]
+   (let [lane (fs/path root (short-hex config id))
+         mark (str (fs/path lane "flow-id.edn"))
+         seen {:session (:session id)
+               :start (:start id)}]
+     (try (fs/create-dir lane)
+          (spit mark (pr-str seen))
+          id
+          (catch FileAlreadyExistsException _
+            (when (= seen (edn/read-string
+                           (slurp mark)))
+              id)))))
+
+ (defn claim! [config harness root uuid]
+   (let [{:keys [first-width start]}
+         (:flow-id config)
+         from (get start harness)
+         widest (- (hex-digits config) from)
+         id (->FlowId (session-bits uuid)
+                      from first-width)]
+     (or (some #(claim-lane! config root %)
+               (map #(assoc id :width %)
+                    (range first-width
+                           (inc widest))))
+         (throw (ex-info "CandidateExhausted"
+                         {:session uuid})))))
```

`flow-id.edn` stays in the code: the file name is the bootstrap
pointer to the data, and data cannot name its own file.

Under choice 2 the record holds only the claimed digits, and the
short id is printed from them:

```clojure
+ (defrecord FlowId [bits width])
+
+ (defn short-hex [{:keys [bits width]}]
+   (format (str "%0" width "x") bits))
```

The messenger keeps a flow id as text today,
`messenger-clj/src/messenger_clj/core.clj`, line 17:

```clojure
- (def FlowId
-   [:and [:string {:min 1 :max 96}]
-    [:re #"^[A-Za-z0-9][A-Za-z0-9_-]*$"]])
+ (def FlowId
+   [:fn #(instance? messenger_clj.flow_id.FlowId
+                    %)])
```

and its database, Datalevin (the database the messenger keeps all its
records in), keys a flow by that text,
`messenger-clj/src/messenger_clj/typed_store.clj`, line 60:

```clojure
-  {:flow/id {:db/unique :db.unique/identity}
+  {:flow/id {:db/unique :db.unique/identity
+             :db/valueType :db.type/bigint}
+   :flow/start {} :flow/width {}
```

Whether Datalevin keeps a large integer as a unique key is not yet
witnessed.

Ruling:

1. Land the sentence, and the record as the whole session id.
2. Land the sentence, and the record as the claimed digits only; six
   digits carry 24 bits, so the word form of Proposal 2 (33 bits)
   cannot then be written from the id alone.
3. Land the sentence; the code waits.
4. Neither.

### Proposal 2: the word form of a flow id

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«A topic's name is a camelCase identifier». As it stands:

"A topic's name is a camelCase identifier, uncapitalized. A flow's id is
the hash of the harness's session id, so a transcript is found from the
flow id. Where the harness lets Flow choose the session id, Flow chooses
it before the flow starts and the flow reads it in its prompt; where the
harness assigns it, Flow learns it when the flow binds. No flow declares
its id: every call to Flow is identified by the calling process."

Sources: flow 05c604, 2026-09-15; flow dea0ba, 2026-10-03; flow d4ae97
and flow f5a6e9, 2026-10-07; flow 0c85a3 and flow ebbe30, 2026-10-09.

Removed: none.

Added, after «so a transcript is found from the flow id.» (after
Proposal 1's sentence, if it lands), under choices 1 to 3:

+ A flow id is also written as words: the first 33 bits of the harness's session id, as words from a published word list, and read back into those bits so the transcript is found from the words. When two flows' words match, the collision is brought to the living.

A published word list: BIP-39 is one, 2048 words, each carrying 11
bits, so three words carry 33 bits; two words need a denser list.

Lands as data and as Clojure. The list is a new file,
`primary/config/main-flow/flow-words.edn`, the BIP-39 English list
copied whole as one vector; its first and last words:

```clojure
+ ["abandon" "ability" "able" "about"
+  ...
+  "zebra" "zero" "zone" "zoo"]
```

How many words, and how they are joined, is data in
`primary/config/main-flow/shared.edn`, added inside its map:

```clojure
+  :flow-words {:file "flow-words.edn"
+               :length 3
+               :join {:separator ""
+                      :capitalize-rest true}}
```

`:join` is the written form: the separator between the words, and
whether every word after the first is capitalized.

The conversion, both ways, is added to
`messenger-clj/src/messenger_clj/flow_id.clj` (Proposal 1), the
machine's design. It reads the bits from the record of Proposal 1,
choice 1, starting where the short id starts (`:start`): the first
bits for Claude; for Codex the bits from the twenty-fourth digit, as
its first digits are not random (choice 5; choice 6 takes `:start` 0
for both):

```clojure
+ (defn read-config [config file]
+   (edn/read-string
+    (slurp (str (fs/path (:dir config)
+                         file)))))
+
+ (defn mask [n]
+   (.subtract
+    (.shiftLeft BigInteger/ONE (int n))
+    BigInteger/ONE))
+
+ (defn bit-width [n]
+   (dec (.bitLength (biginteger n))))
+
+ (defn leading-bits [config id n]
+   (let [{:keys [session start]} id
+         width (get-in config
+                       [:flow-id :session-bits])]
+     (.and (.shiftRight
+            session
+            (int (- width (* 4 start) n)))
+           (mask n))))
+
+ (defn words [config id]
+   (let [{:keys [file length]}
+         (:flow-words config)
+         vocab (read-config config file)
+         per (bit-width (count vocab))
+         bits (leading-bits config id
+                            (* per length))]
+     (for [i (range (dec length) -1 -1)]
+       (nth vocab
+            (-> bits
+                (.shiftRight (int (* per i)))
+                (.and (mask per))
+                long)))))
+
+ (defn word-form [config id]
+   (let [ws (words config id)
+         {:keys [separator capitalize-rest]}
+         (:join (:flow-words config))
+         rest-form (if capitalize-rest
+                     str/capitalize
+                     identity)]
+     (str/join separator
+               (cons (first ws)
+                     (map rest-form (rest ws))))))
```

Back from the words, the pattern that finds the transcript: it matches
a session id written without its dashes, at each harness's start:

```clojure
+ (defn split-words [text]
+   (map str/lower-case
+        (re-seq #"[A-Z]?[a-z]+" text)))
+
+ (defn session-pattern [config text]
+   (let [{:keys [file]} (:flow-words config)
+         vocab (read-config config file)
+         index (zipmap vocab (range))
+         ws (split-words text)
+         n (* (bit-width (count vocab))
+              (count ws))
+         bits (reduce #(+ (* %1 (count vocab))
+                          (index %2))
+                      0 ws)
+         r (mod n 4)
+         hex (format (str "%0" (quot n 4) "x")
+                     (bit-shift-right bits r))
+         lo (bit-shift-left
+             (bit-and bits
+                      (dec (bit-shift-left 1 r)))
+             (- 4 r))
+         hi (+ lo (dec (bit-shift-left
+                        1 (- 4 r))))
+         starts (vals (get-in config
+                              [:flow-id :start]))]
+     (re-pattern
+      (str "^(?:"
+           (str/join "|"
+                     (map #(str ".{" % "}")
+                          starts))
+           ")" hex
+           (when (pos? r)
+             (format "[%x-%x]" lo hi))))))
```

A search that finds more than one transcript for one pattern has found
a collision, which is brought to the living.

Ruling:

1. Land now; three words joined as one uncapitalized camelCase word,
   like `wordWordWord`, as shown (flow 05c604, 2026-09-15; flow
   d4ae97, 2026-10-07; flow 0c85a3, 2026-10-09).
2. Land now; three words apart, with a separator of their own (flow
   05c604, 2026-09-15); `:separator` names it and `:capitalize-rest`
   is false.
3. Land now; two words from a denser published list (flow 05c604,
   2026-09-15; flow d4ae97, 2026-10-07); `:file` names that list and
   `:length` is 2.
4. Wait until after a minimum viable product; no line now (flow dea0ba,
   2026-10-03).
5. With choice 1, 2 or 3, the machine's design: the 33 bits are taken
   from `:start` (digit 24 for Codex), because the Codex id's leading
   digits are not random.
6. With choice 1, 2 or 3, his phrase literally: `:start` is 0 for both
   harnesses, so the first 33 bits are the first digits; Codex's hex
   short id then differs in origin from its words.

### Proposal 3: flow ids are for the ledger

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«Flow manages metaflows». As it stands:

"Flow manages metaflows. A metaflow is one address, { Aspect Topic
Layer }, that continues through several flows one after another; the
flow is its current run, and what is addressed is always the metaflow,
never a flow. The default topic is core: the permanent topic, the thing
that keeps the machine going, the last topic to stand."

The ledger: the record of every flow that has run.

Sources: flow 01e496, 2026-10-02; flow 4ddfe1, 2026-10-07; flow 7c89aa,
2026-10-13.

Removed: none.

Added, after «never a flow.»:

+ A flow id is for the ledger: it finds a flow's transcript and its place among its metaflow's past flows. Flows name one another, and the living, by metaflow.

Lands in `messenger-clj/src/messenger_clj/core.clj`. A send names its
target either by flow id or by metaflow, `target-flow!`, line 533, as
it stands (`m/validate` checks a value against a shape written in
Malli, the library the messenger describes its data shapes with):

```clojure
(defn target-flow! [target]
  (if (m/validate FlowId target)
    target
    (do
      (valid! Metaflow target
        "TARGET metaflow (aspect topic layer)")
      (let [matches ...]
        ...
        (first matches)))))
```

Under choices 1 and 2, a target is a metaflow only:

```clojure
- (defn target-flow! [target]
-   (if (m/validate FlowId target)
-     target
-     (do
-       (valid! Metaflow target
-         "TARGET metaflow (aspect topic layer)")
-       (let [matches ...] ...))))
+ (defn target-flow! [target]
+   (valid! Metaflow target
+     "TARGET metaflow (aspect topic layer)")
+   (let [matches ...] ...))
```

The receipt a send prints names the flow id, `record-sent!`, line 939:

```clojure
(str (name grade) ".{ " flow " "
     (or (:agent_status live) "unknown")
     " }")
```

Under choice 1, the machine's proposal, it names the metaflow:

```clojure
- (str (name grade) ".{ " flow " "
+ (str (name grade) ".{ "
+      (metaflow! (load-route (registry) flow))
+      " "
       (or (:agent_status live) "unknown")
       " }")
```

Ruling:

1. Land the sentence, the target change and the receipt change.
2. Land the sentence and the target change; receipts keep the flow id.
3. Land the sentence; the code keeps taking flow ids.
4. Neither.

### Proposal 4: the caller is found, never declared

File: `messenger-clj/src/messenger_clj/core.clj`. The sentence it
carries already stands in `psyche-context/skills/vision-flow.md`, at the
end of the paragraph that begins «A topic's name is a camelCase
identifier»:

"No flow declares its id: every call to Flow is identified by the
calling process."

Source: flow 875960, 2026-10-11.

The messenger takes a sender from the id the flow declares in its
environment, `sender-origin!`, line 524, as it stands:

```clojure
(defn sender-origin! []
  (let [sender (flow-id!
                (or *flow-id*
                    (System/getenv "FLOW_ID")
                    (fail "Set FLOW_ID ...")))]
    (assert-not-retired! sender)
    (let [route (load-route (registry) sender)]
      ...
      (metaflow! route))))
```

A route is the messenger's record of where a flow is reached: its pane
in herdr (herdr: the third-party terminal program the flows run in; a
pane: one terminal area in it) and its aspect, topic and layer. Herdr
marks every process it starts with the pane it runs in, in the
variable `HERDR_PANE_ID`. Removed and added:

```clojure
- (let [sender (flow-id!
-                (or *flow-id*
-                    (System/getenv "FLOW_ID")
-                    (fail "Set FLOW_ID ...")))]
+ (let [sender (or *flow-id* (pane-flow!))]
```

`pane-flow!` is new, above it, the machine's design:

```clojure
+ (defn pane-flow! []
+   (let [pane (or (System/getenv "HERDR_PANE_ID")
+                  (fail "CallerUnknown"))
+         hits (for [[id route] (route-records)
+                    :when (= pane
+                             (:pane_id route))]
+                id)]
+     (if (= 1 (count hits))
+       (first hits)
+       (fail (str "CallerUnknown: " pane)))))
```

`HERDR_PANE_ID` stays in the code: the variable name is the contract
with herdr, read as the bootstrap of the pane.

The same replacement in three more places that read the declared id.
`reserve!`, line 451:

```clojure
- (or *flow-id* (System/getenv "FLOW_ID") flow)
+ (or *flow-id* (pane-flow!))
```

and the `:retired_by` of a retirement record, in `import-retirement!`,
line 705, and `retire!`, line 760:

```clojure
- (or *flow-id* (System/getenv "FLOW_ID") "")
+ (or *flow-id* (pane-flow!))
```

A pane id is unique within one herdr session; two sessions can hold the
same one, and `pane-flow!` then refuses as unknown. A subflow running in
its main flow's pane is found as that main flow, as it is today through
the inherited declared id. The launchers keep setting `FLOW_ID`, which a
flow reads to find its own directory; the messenger no longer reads it.

Ruling:

1. Land all four changes.
2. Land `sender-origin!` and `pane-flow!`; the other three keep the
   declared id.
3. Neither.

### Proposal 5: the title names aspect, topic, layer and id

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«Every flow has a topic». As it stands:

"Every flow has a topic; a flow with no special topic has the topic core,
the heart of its aspect. A topic is a core:Name, a camelCaseExpression
checked when created. A flow's title names its aspect, topic, layer and
flow id: { Psyche core Secondary <id> }."

Sources: flow 5578cc, 2026-10-03; flow d4ae97 and flow f5a6e9,
2026-10-07; flow 445410, 2026-10-09; flow ebbe30, 2026-10-09.

Under choice 1 the paragraph stands, and the data and code below land.

Under choice 2:

Removed:

- flow id: { Psyche core Secondary <id> }.

Added:

+ flow id in its word form: { Psyche core Secondary <words> }.

Lands as data and as Clojure, the machine's design. The order of the
title's parts is data, added to `primary/config/main-flow/shared.edn`
with the default topic and the topic's pattern (EDN has no regex
literal, so it is a string the code compiles):

```clojure
+  :title [:aspect :topic :layer :flow]
+  :default-topic :core
+  :topic "^[a-z][A-Za-z0-9]*$"
```

Under choice 2 the last part is `:words`, the word form of Proposal 2:

```clojure
+  :title [:aspect :topic :layer :words]
```

The metaflow files in `primary/config/main-flow/metaflow/` write the
topic capitalized; in each of the five:

```clojure
- {:aspect :Psyche :topic :Core :layer :Primary
+ {:aspect :Psyche :topic :core :layer :Primary
```

and `:Flow` becomes `:flow` in the two Psyche Flow files. The same in
`primary/config/context-refresh.json`, `"topic": "Core"` and the
recipient `"Field Core Secondary"`. Every metaflow's address then reads
`Psyche core Secondary`; the skills and routes that write `Core` follow.

The launchers' shared code builds the title today,
`primary/tools/native-main-flow-launch-shared.mjs`, lines 10 to 27,
capitalizing the topic and leaving core out:

```js
- // A topic is a dense PascalCase short name:
- // letters only, leading capital.
- export const TOPIC = /^[A-Z][A-Za-z]*$/;
- export const CORE_TOPIC = 'Core';
- ...
- return topic === CORE_TOPIC
-   ? `{ ${aspect} ${layer} ${flowId} }`
-   : `{ ${aspect} ${topic} ${layer} ${flowId} }`;
```

Its Clojure rewrite, a new file,
`messenger-clj/src/messenger_clj/launch.clj`. `flow` is a map of the
flow's parts, `{:aspect :Psyche :topic :core :layer :Secondary :flow
"38de5b"}`, with `:words` under choice 2:

```clojure
+ (ns messenger-clj.launch
+   (:require [clojure.string :as str]
+             [malli.core :as m]))
+
+ ;; A topic is a camelCase name, uncapitalized;
+ ;; its pattern is :topic in shared.edn.
+ (defn topic-shape [config]
+   [:re (re-pattern (:topic config))])
+
+ (defn topic! [config topic]
+   (let [topic (or topic (:default-topic config))]
+     (when-not (m/validate (topic-shape config)
+                           (name topic))
+       (throw (ex-info "InvalidTopic"
+                       {:topic topic})))
+     topic))
+
+ (defn title [config flow]
+   (str "{ "
+        (str/join " "
+                  (map #(name (get flow %))
+                       (:title config)))
+        " }"))
```

Ruling:

1. The title carries the hex id (flow dea0ba, 2026-10-03: the word id
   after a minimum viable product); land the data and code with
   `:flow`.
2. The title carries the word id (flow 5578cc, 2026-10-03; flow
   d4ae97, 2026-10-07; flow ebbe30, 2026-10-09); land the sentence,
   and the data and code with `:words`.
3. Neither.

### Proposal 6: a flow knows where it was asked for

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«A layer is Primary, Secondary, Tertiary or Quaternary». As it stands:

"A layer is Primary, Secondary, Tertiary or Quaternary, in every
aspect; the layer decides the model, declared once in Flow as
configuration and changed only over its meta socket. A launch names the
metaflow, the context modules composed into its prompts, and a brief of
a small paragraph; the Nexus composes the prompt from its module
registry, checking each module's hash against its source."

Source: flow 9993b5, 2026-09-17.

Removed: none.

Added, at the end:

+ Every flow carries where it was asked for: the flow, session and turn that requested it, found by Flow, so why it was started is read in that transcript.

Lands in the launchers' continuation record: the small file in each
flow's directory that names its predecessor, topic and metaflow, so a
successor inherits them. It is written today by
`primary/tools/native-main-flow-launch-shared.mjs`,
`writeContinuationRecord`, line 74, as JSON:

```js
- const record = {flowId,
-   predecessor: continuation.predecessor,
-   topic: continuation.topic,
-   metaflow: continuation.metaflow};
```

Its Clojure rewrite, the machine's design, added to
`messenger-clj/src/messenger_clj/launch.clj` (Proposal 5), writes it as
EDN, `continuation.edn`, with the origin found from the launching
process (`pane-flow!`, Proposal 4):

```clojure
+ (defn caller-origin []
+   (let [flow (core/pane-flow!)
+         route (core/load-route
+                (core/registry) flow)]
+     {:flow flow
+      :thread (:native_thread route)}))
+
+ (defn write-continuation! [root flow lineage]
+   (spit (str (fs/path root flow
+                       "continuation.edn"))
+         (pr-str (assoc lineage
+                        :flow flow
+                        :origin (caller-origin)))))
```

with `[messenger-clj.core :as core]` and `[babashka.fs :as fs]` added to
its requires, and the reader of a predecessor's record reading
`continuation.edn`. The file name stays in the code: it is the
bootstrap pointer to the record, and data cannot name its own file.
The turn that asked is not visible to a launcher; the record carries
the flow and its session (`:thread`) only.

Ruling:

1. Land the sentence and the code; the turn waits.
2. Land the sentence only.
3. Neither.

### Proposal 7: why the word flow

File: `psyche-context/skills/vision-flow.md`, the paragraph that begins
«Flow is the Nexus that manages flows». As it stands:

"Flow is the Nexus that manages flows. A flow is one run of a voice; the
component is named for what it manages. A flow the living asks for is
launched, properly and surely. Flow holds the lock on flows."

Source: flow 4ddc321d, 2026-08-26.

Removed: none.

Added, after «A flow is one run of a voice;»:

+ a flow is a flow of thought, and an intelligence is many of them, so agent, a word that carries one subject, names none of them;

Lands in no code.

Ruling:

1. Land it.
2. Not in vision-flow.
<!-- to-the-living:end -->
