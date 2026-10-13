<!-- to-the-living:start -->
Presentation.{ «Flow: refresh and handover» }

# Flow: refresh and handover

## Crystallization

### Proposal 1: the three marks of a flow's context

File: `psyche-context/skills/vision-flow.md`, «A replaced session is
reaped by the refresh itself», the second of its two paragraphs.

A mark: a size of the context at which something happens. The hook: a
command the harness runs at the end of each of the flow's turns (its
Stop hook), the only place the context's size is seen today. The runner:
the flow that runs the refresh mechanism (Proposal 3).

Sources: flow d68c82, 2026-10-13; flow d4ae97, 2026-10-07; flow 8475a9,
2026-10-06; flow b80e55, 2026-09-20; flow f55ec8, 2026-09-16; flow
692df8, 2026-09-15; flow 6cc91b, 2026-09-14.

```text
  Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.

- A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+ A flow's context has three marks, set in Flow's configuration for each layer's model: the floor, below which no refresh is asked for; the warning, at which the flow is told that its refresh has begun and writes its handover; and the ceiling, which a flow is never allowed to reach. The flow is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event.
```

The figure, after the paragraph:

```text
+ +----------------------------------+
+ | the floor                        |
+ +----------------------------------+
+         | admits, once passed,
+         v
+ +----------------------------------+
+ | a refresh request                |
+ +----------------------------------+
+         | brings forward
+         v
+ +----------------------------------+
+ | the warning                      |
+ +----------------------------------+
+         | tells
+         v
+ +----------------------------------+
+ | the flow, and its runner         |
+ +----------------------------------+
+         | writes
+         v
+ +----------------------------------+
+ | its handover                     |
+ +----------------------------------+
+         | precedes
+         v
+ +----------------------------------+
+ | the successor, before the ceiling|
+ +----------------------------------+
```

Lands as data and as Clojure. EDN: Clojure's plain data notation, the
form of the launch configuration under `primary/config/main-flow/`;
Babashka (bb): the program that runs Clojure scripts at once. The marks
move out of `primary/config/context-refresh.json`:

```json
-   "warningWindowFraction": 0.5,
-   "claude": {
-     "warningTokens": 200000
-   },
-   "codex": {
-     "models": {
-       "gpt-6.1-sol": 373000,
-       "gpt-6-astra": 272000,
-       "gpt-6-sol": 272000,
-       "gpt-6-luna": 272000
-     }
-   },
```

into `primary/config/main-flow/shared.edn`, inside its map after
`:tools`. A mark is a count of tokens, a fraction of the model's window,
or both (choice 3: `:warn {:tokens 200000 :fraction 0.2}`):

```clojure
+  :refresh {:floor {:fraction 0.15}
+            :warn {:tokens 200000}
+            :ceiling {:tokens 400000}
+            :hook-timeout-s 30}
```

Each model's window goes on its layer's row in the aspect file,
`primary/config/main-flow/psyche.edn` (the key `:voices` is renamed by
Proposal 2 of «Flow: the metaflow»); the first row:

```clojure
-  :voices [{:layer :Primary :model "claude-fable-5-1" :effort :medium}
+  :voices [{:layer :Primary
+            :model "claude-fable-5-1"
+            :effort :medium
+            :window 1000000}
```

The hook, `primary/tools/context-refresh-hook.mjs`, and its JSON file
are removed whole; a new file,
`messenger-clj/src/messenger_clj/refresh.clj`, beside the messenger,
is the machine's design. It reads the flow's transcript, the file the
harness writes for the thread, and finds the flow by the thread the
messenger registered for it:

```clojure
+ (ns messenger-clj.refresh
+   (:require [babashka.fs :as fs]
+             [cheshire.core :as json]
+             [clojure.string :as str]))
+
+ ;; A mark is tokens, a fraction of the window,
+ ;; or both; the lower one binds.
+ (defn mark-tokens [mark window]
+   (let [{:keys [tokens fraction]} mark
+         of-window (when (and fraction window)
+                     (long (* fraction window)))]
+     (reduce min
+             (remove nil? [tokens of-window]))))
+
+ (defn marks [config window]
+   (into {}
+         (for [[k m] (select-keys (:refresh config)
+                                  [:floor :warn
+                                   :ceiling])]
+           [k (mark-tokens m window)])))
+
+ (defn zone [config window used]
+   (let [{:keys [floor warn ceiling]}
+         (marks config window)]
+     (cond (< used floor) :below-floor
+           (>= used ceiling) :ceiling
+           (>= used warn) :warn
+           :else :below)))
+
+ (defn json-lines [path]
+   (->> (str/split-lines (slurp (str path)))
+        (remove str/blank?)
+        (map #(json/parse-string % true))))
+
+ ;; The usage fields are each harness's own
+ ;; transcript contract.
+ (defn claude-used [path]
+   (when-let [u (->> (json-lines path)
+                     (keep #(get-in % [:message
+                                       :usage]))
+                     last)]
+     (+ (:input_tokens u 0)
+        (:cache_creation_input_tokens u 0)
+        (:cache_read_input_tokens u 0))))
+
+ (defn codex-used [path]
+   (->> (json-lines path)
+        (filter #(= "token_count"
+                    (get-in % [:payload :type])))
+        (keep #(get-in % [:payload :info
+                          :last_token_usage
+                          :input_tokens]))
+        last))
+
+ (defn used [harness path]
+   (case harness
+     :claude (claude-used path)
+     :codex (codex-used path)))
+
+ (defn flow-of-thread [routes thread]
+   (some (fn [[flow route]]
+           (when (= thread (:native_thread route))
+             [flow route]))
+         routes))
```

The launcher installs the hook today in
`primary/tools/claude-main-flow-launch.mjs`, `mainFlowMode`, lines 167
and 168, and for Codex in `codex-main-flow-launch.mjs`, line 184:

```js
-   const refresh = [sh(process.execPath), sh(path.join(workspace, 'tools', 'context-refresh-hook.mjs')), '--config', sh(seat.refreshConfigPath ?? path.join(workspace, 'config', 'context-refresh.json'))].join(' ');
-   settings.hooks.Stop = [...(settings.hooks.Stop ?? []), {hooks: [{type: 'command', command: refresh, timeout: 30}]}];
```

Its Clojure rewrite, in `messenger-clj/src/messenger_clj/launch.clj`,
the file Proposal 5 of «Flow: identity and naming», second edition,
creates:

```clojure
+ ;; The hook's settings keys are the harness's
+ ;; contract; the command names the EDN file,
+ ;; the bootstrap pointer to the configuration.
+ (defn stop-hook [config config-file hook-file]
+   (let [timeout (get-in config [:refresh
+                                 :hook-timeout-s])]
+     {:hooks
+      {:Stop [{:hooks
+               [{:type "command"
+                 :command (str "bb " hook-file
+                               " --config "
+                               config-file)
+                 :timeout timeout}]}]}}))
```

Ruling, one number from each group:

The paragraph and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

The warning:
4. A count of tokens for the harness: 200,000 for Claude (flow d68c82,
   2026-10-13).
5. A fraction of the window: 20% (flow d4ae97, 2026-10-07, «20% to
   40%»); dated records: 30%, 300,000 tokens (flow f55ec8, 2026-09-16);
   200,000 to 300,000 after a 100,000 bootstrap (flow b80e55,
   2026-09-20); 20 to 30% for Claude (flow 6cc91b, 2026-09-14).
6. Both, the lower binding, the machine's design: a count fits one
   window, a fraction fits every model's.

The ceiling:
7. 400,000 tokens for Claude (flow d68c82, 2026-10-13); 700,000 was
   unacceptable (flow 8475a9, 2026-10-06).
8. 40% of the window (flow d4ae97, 2026-10-07).
9. 60% (flow 6cc91b, 2026-09-14).

The floor:
10. 15% (flow 692df8, 2026-09-15).
11. 20% (flow 692df8, 2026-09-15).

### Proposal 2: below the floor, a request is refused

File: `psyche-context/skills/vision-flow.md`, «A replaced session is
reaped by the refresh itself», after Proposal 1's paragraph and figure.

Sources: flow d68c82, 2026-10-13; flow 33752b, 2026-10-13; flow 88475f,
2026-09-25; flow e51411, 2026-09-25; flow 692df8, 2026-09-15, two
records; flow 6cc91b, 2026-09-14.

```text
+ Below the floor, a request to refresh a flow, or to compact it, is refused, as is one for a flow younger than a set age, so that a request routed to a flow just started changes nothing. A flow below the floor is still replaced when its direction changes dramatically: a new job starts on a fresh flow, with the training that job needs.
```

The emergency when a successor fails to start is choice 2 of Proposal 1
of «Flow: short term and long term», third edition. The analysis he
asked for on 2026-10-13 (flow d68c82) is a question wanting knowledge:
it lands in mind-context as a knowledge skill, written by a Mind flow.

Lands as data, in `shared.edn`, inside `:refresh`:

```clojure
+            :min-age-ms 600000
```

and in `refresh.clj`. A flow's age is its directory's; the request
names the flow and whether it overrides the floor, under choice 5:

```clojure
+ (defn age-ms [flow-dir now]
+   (- now (.toMillis (fs/creation-time flow-dir))))
+
+ ;; :BelowFloor and :TooYoung are the guard's two
+ ;; outcomes, so the code names them.
+ (defn guard [config zone age]
+   (let [min-age (get-in config
+                         [:refresh :min-age-ms])]
+     (cond (= zone :below-floor) :BelowFloor
+           (< age min-age) :TooYoung)))
+
+ ;; RefreshRefused is typed as the messenger's
+ ;; RetireRefused is today.
+ (defn request [config zone age flow override]
+   (if-let [reason (and (not override)
+                        (guard config zone age))]
+     (str "RefreshRefused.{ " flow " "
+          (name reason) " }")
+     :admitted))
```

`main.clj` gains the command `refresh METAFLOW`, with the `hm-refresh`
shorthand beside the others; the metaflow's current flow is found as
Proposal 3 of «Flow: the metaflow» finds it.

Ruling, one number from each group:

The lines:
1. Land.
2. Land with changes the living names.
3. Drop.

What a dramatic change of direction is:
4. A new job (flow 88475f, 2026-09-25); the one who starts the job
   starts the fresh flow, and no request to the old flow is needed.
5. An override named in the request, by the living or a flow above the
   one refreshed, the machine's design: the change is a judgment, and
   the request carries who made it.
6. Left to be defined (flow 692df8, 2026-09-15); until then, no
   exception below the floor.

### Proposal 3: who runs the refresh

File: `psyche-context/skills/vision-flow.md`: a long-term line in
«Starting flows», after the paragraph Proposal 4 of «Flow: the
metaflow» adds; and a short-term line under «Short term», after the
paragraph of Proposal 1 of «Flow: short term and long term», third
edition.

Sources: flow e51411, 2026-09-24; flow 6cc91b, 2026-09-14; flow 02dda6,
2026-10-07; flow b7da5d, 2026-09-26; flow b860be, 2026-09-26.

```text
+ The refresh is standard at every layer of every aspect, part of every flow's instruction. Any flow can deploy any other: the structure is decentralized and respawns from any point, so one flow left standing redeploys the rest.
```

```text
+ Short term: the Quaternary of each aspect runs the refresh mechanism for its aspect's flows, and the flow above stays aware of what it does.
```

**Destroy**, two vision impurities: an order to refresh, in
`flows/b7da5d/vision/flowRefreshAndArchive.md` (2026-09-26), and an
order to refresh now and take a role, in
`flows/b7da5d/vision/mainFlowRefreshAndRoles.md` (2026-09-26), each
entry whole:

```text
- ## Refresh Field and connect the six upper-tier flows
```

```text
- ## Refresh right now; Flow Master and Luna help
```

Lands as data and as Clojure. The recipient leaves
`context-refresh.json`:

```json
-   "recipients": {
-     "field": "Field Core Secondary"
-   },
```

for `shared.edn`, inside `:refresh`: a layer of the flow's own aspect
and topic (choice 4), or a metaflow named whole (choice 5,
`:runner {:aspect :Field :topic :core :layer :Secondary}`):

```clojure
+            :runner {:layer :Quaternary}
```

In `refresh.clj`:

```clojure
+ ;; The runner is the metaflow warned beside the
+ ;; flow: a layer of the flow's own aspect and
+ ;; topic, or a metaflow named whole.
+ (defn runner [config route]
+   (let [{:keys [aspect topic layer]}
+         (get-in config [:refresh :runner])]
+     (str/join " "
+               (map name
+                    [(or aspect (:aspect route))
+                     (or topic (:topic route))
+                     layer]))))
```

Ruling, one number from each group:

The long-term line:
1. Land.
2. Land with changes the living names.
3. Drop.

The runner, short term:
4. The bottom seat of each aspect (flow 02dda6, 2026-10-07; flow
   b7da5d, 2026-09-26: Luna pumps the CLI, the main flow stays aware).
5. Field (flow b860be, 2026-09-26: whoever is in charge of refreshing
   is told; Proposal 8 of «Flow: the metaflow»: Field starts flows until
   this is automated).

The two records:
6. Destroy both.
7. Keep both.

### Proposal 4: the switch-over

File: `psyche-context/skills/vision-flow.md`: a long-term line in «A
replaced session is reaped by the refresh itself», after Proposal 2's
line; a short-term line under «Short term», after Proposal 3's.

Sources: flow 1b8ac0, 2026-09-21; flow b860be, 2026-09-26; flow
9993b5, 2026-09-17; flow e51411, 2026-09-24.

```text
+ A flow warned has a switch-over time to write its handover and go idle; Flow checks that its turn is done, and a flow still turning past that time is sent an interrupt asking it to end its flow now. The living need not notice a refresh.
```

```text
+ Short term: the hook warns once, records when, and at the end of a later turn past the switch-over time types the interrupt.
```

Lands as data, in `shared.edn`, inside `:refresh`; the state file is
the record the hook keeps in the flow's directory between turns, and
its name is the bootstrap pointer to that record:

```clojure
+            :switch-over-ms 900000
+            :state-file "refresh.edn"
+            :warning "Refresh begun; hand over."
+            :interrupt "End your flow now."
```

and in `refresh.clj`; what is sent goes through the messenger's `send!`,
to the flow and to its runner:

```clojure
+ ;; What one turn's end does, from the zone and
+ ;; what earlier turns recorded.
+ (defn step [config zone state now]
+   (let [over (get-in config [:refresh
+                              :switch-over-ms])
+         at (:warned-at state)]
+     (when (#{:warn :ceiling} zone)
+       (cond (nil? at) :warn
+             (> (- now at) over) :interrupt))))
+
+ (defn messages [config route flow action]
+   (let [{:keys [warning interrupt]}
+         (:refresh config)]
+     (case action
+       :warn [[flow warning]
+              [(runner config route) warning]]
+       :interrupt [[flow interrupt]]
+       nil [])))
```

Ruling:

1. Land both lines.
2. Land the long-term line only.
3. Land with changes the living names.
4. Drop.

### Proposal 5: the successor is checked; the predecessor hears only of failure

File: `psyche-context/skills/vision-flow.md`: a long-term paragraph and
figure in «A replaced session is reaped by the refresh itself», after
Proposal 4's line; a short-term line under «Short term», after
Proposal 4's.

Sources: flow fd0f97, 2026-09-15; flow 692df8, 2026-09-15; flow
6cc91b, 2026-09-14.

```text
+ Flow keeps track of a refresh: whether the successor started and is working, judged by a small model and recorded. The predecessor is not woken to be told that it has a successor; it is woken only when the successor fails to start, told that its flow could not be refreshed, and then finds the fault or asks for it to be fixed. A refresh replaces only its own flow in the cluster.
```

```text
+ +----------------------------------+
+ | the launcher                     |
+ +----------------------------------+
+         | starts
+         v
+ +----------------------------------+
+ | the successor                    |
+ +----------------------------------+
+         | registers with
+         v
+ +----------------------------------+
+ | the messenger                    |
+ +----------------------------------+
+     | shows it registered | shows nothing
+     v                     v
+ +----------------+  +--------------------+
+ | the predecessor|  | the predecessor,   |
+ | left idle      |  | told of the failure|
+ +----------------+  +--------------------+
```

```text
+ Short term: the launcher, having started the successor, checks once after a set wait that it registered with the messenger; failing that, it messages the predecessor that its refresh failed.
```

Lands as data, in `shared.edn`, inside `:refresh`:

```clojure
+            :successor-wait-ms 120000
+            :failed "Unable to refresh your flow."
```

and in `launch.clj`; `routes` is the messenger's route records:

```clojure
+ ;; One check after the wait, not a poll.
+ (defn successor-check [config routes successor
+                        predecessor]
+   (if (contains? routes successor)
+     :started
+     [predecessor
+      (get-in config [:refresh :failed])]))
```

Ruling, one number from each group:

The lines and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

The name of the event, a side question he asked for a suggestion on
(flow 6cc91b, 2026-09-14); the word stands wherever these lines say
refresh:
4. Refresh (flow d68c82, 2026-10-13; flow 02dda6, 2026-10-07; flow
   b860be and flow e51411, 2026-09-24 to 26), the machine's suggestion:
   the word of his later records.
5. Recycle (flow fd0f97, 2026-09-15).
6. Re-bootstrap (flow 6cc91b, 2026-09-14).

### Proposal 6: two flows of one metaflow

File: `psyche-context/skills/vision-flow.md`, «What it does», after the
paragraph Proposal 3 of «Flow: the metaflow» adds.

Source: flow e51411, 2026-09-24.

```text
+ Two flows of one metaflow share everything with each other, and one cedes.
```

Lands in the messenger's registration. Under choice 4 the later
registration displaces the earlier: Proposal 3 of «Flow: the metaflow»
makes it current and choice 8 of Proposal 2 of «Flow: short term and
long term», third edition, retires the earlier. Under choice 5, in
`messenger-clj/src/messenger_clj/core.clj`, `register!`, line 547, a
registration for a metaflow already current is refused unless it names
the flow it succeeds:

```clojure
+ (defn same-seat [routes route]
+   (let [seat #(select-keys % [:aspect :topic
+                               :layer])]
+     (for [[flow r] routes
+           :when (= (seat r) (seat route))]
+       flow)))
+
+ ;; DuplicateSeat is the registration's own
+ ;; refusal.
+ (defn duplicate-seat! [routes route successor-of]
+   (doseq [flow (same-seat routes route)
+           :when (not= flow successor-of)]
+     (fail (str "DuplicateSeat: " flow))))
```

`main.clj`'s `register` gains the option `--successor-of FLOW`, which
the launcher passes.

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

Which cedes:
4. The earlier, the machine's design: the metaflow has one current
   flow, and the later is the one started on purpose.
5. The later, refused at registration unless the launcher names the
   flow it succeeds: a second flow of one metaflow is an accident
   until declared.

### Proposal 7: what the successor receives, and does first

File: `psyche-context/skills/vision-flow.md`, «A replaced session is
reaped by the refresh itself», after the line Proposal 6 of «Flow: short
term and long term», third edition, adds (the handover carries
judgment).

Sources: flow 48cff7, 2026-09-16; flow f55ec8, 2026-09-16 and
2026-09-17; flow 1b8ac0, 2026-09-21; flow e51411, 2026-09-24 and
2026-09-25; flow 88475f, 2026-09-25; flow b80e55, 2026-09-20; flow
6cc91b, 2026-09-14.

```text
+ A refresh is made so that the successor is smarter and better equipped than its predecessor, for the problem at hand and in general. Besides the handover, the successor receives the flow's presentations, the raw psyche it was given, the basic skills, and the best of the layers below it, gathered on refresh. What has been merged into files since the last refresh is carried by the files, never again by a handover, so a lineage does not accumulate. The successor's first goal is a presentation of the current state, its open questions and undecided design, and of the design as it understands it, with figures and examples.
```

Under choice 7, one more sentence:

```text
+ The bootstrap is the same for every flow of one layer, so its cache is shared among them.
```

The figure, after the paragraph:

```text
+ +----------------+  +----------------------+
+ | the handover   |  | the layers below     |
+ +----------------+  +----------------------+
+     | carries judgment    | give their best to
+     v                     v
+ +------------------------------------------+
+ | the successor                            |
+ +------------------------------------------+
+     | reads from files    | presents first
+     v                     v
+ +----------------+  +----------------------+
+ | what was merged|  | the current state    |
+ | since the last |  | and design           |
+ | refresh        |  +----------------------+
+ +----------------+
```

What is decided goes into the context modules and only the undecided
reaches the next flow: line B of Proposal 6 of «Flow: the metaflow».

Lands as data: the handover's file name in `shared.edn`, inside
`:refresh`, and the modules a successor starts with in the aspect file,
`psyche.edn`, after `:modules`:

```clojure
+            :handover-file "handover.md"
```

```clojure
+ :successor-modules [:spirit-core :vision-book]
```

and in `launch.clj`:

```clojure
+ (defn successor-prompt [config aspect-config
+                         predecessor-dir]
+   (let [file (get-in config [:refresh
+                              :handover-file])]
+     {:modules (:successor-modules aspect-config)
+      :handover (slurp (str (fs/path
+                             predecessor-dir
+                             file)))}))
```

Ruling, one number from each group:

The paragraph and the figure:
1. Land.
2. Land with changes the living names.
3. Drop.

Who gathers the best of the layers below:
4. A subflow of the refreshing flow, on an older model (flow f55ec8,
   2026-09-17).
5. The runner of Proposal 3 (flow 02dda6, 2026-10-07).
6. No one gathers, the machine's design: each lower flow's own handover
   is its best, and the successor reads them.

The shared bootstrap:
7. Land the sentence (flow b80e55, 2026-09-20).
8. No sentence.
<!-- to-the-living:end -->
