<!-- to-the-living:start -->
Presentation.{ «Short-term prototypes: Clojure now?» }

# Short-term prototypes: Clojure now?

## Crystallization

### Proposal 1: the live path today, by language, and which files leave it

```text
+--------------------------------------+
| a seat the living asks for           |
+--------------------------------------+
   | is launched by
   v
+--------------------------------------+
| 19 .mjs and 1 .py under tools/       |
| launchers, hooks, committer, census  |
+--------------------------------------+
   | read
   v
+--------------------------------------+
| config/main-flow/*.edn               |
| shared, aspect, metaflow             |
+--------------------------------------+
   | name modules in
   v
+--------------------------------------+
| psyche-, mind-, field-context        |
+--------------------------------------+
   | are loaded into
   v
+--------------------------------------+
| the running seat                     |
| 2 sh hooks, 1 sh status line         |
+--------------------------------------+
   | sends and commits through
   v
+--------------------------------------+
| hm-* and field: 10 .clj              |
| messenger-clj, field-clj; 1 sh       |
+--------------------------------------+
```

File: `tools/` (the non-Clojure live files; group one removed under choices 1 and 2, group two under choice 1 only)

```paths
- claude-main-flow-launch.mjs
- codex-main-flow-launch.mjs
- opencode-main-flow-launch.mjs
- main-flow-mode/launch-config.mjs
- main-flow-mode/spirit-system-prompt.mjs
- native-main-flow-launch-shared.mjs
- native-voice-profiles.mjs
- native-voice-launch.mjs
- model-display-name.mjs
- standing-skill-selection.mjs
- secondary-first.mjs
- native-worker-launch.mjs
-
- context-refresh-hook.mjs
- main-flow-mode/context-refresh.mjs
- main-flow-mode/reminder-hook.py
- field-census/claude-context.mjs
- field-census/codex-context.mjs
- primary-committer/codex-birth.mjs
- primary-committer/restart.mjs
- primary-committer/turn-end.mjs
```

File: `src/` (in the repository of choice 4 or 5; group one added under choices 1 and 2, group two under choice 1 only; each run by bb)

```paths
+ launch/seat.clj
+ launch/config.clj
+ launch/system_prompt.clj
+ launch/first_prompt.clj
+ launch/voices.clj
+ launch/worker.clj
+ launch/secondary_first.clj
+ launch/values.clj
+
+ hooks/context_refresh.clj
+ hooks/reminder.clj
+ census/context.clj
+ committer/birth.clj
+ committer/restart.clj
+ committer/turn_end.clj
```

Ruling, one number from each group:

Which files leave the live path now:
1. Both groups: all 20 removed, the 14 Clojure files added, each old file removed as its Clojure lands.
2. Group one, the launch chain, now; group two after.
3. Neither: every new prototype is .clj; the 20 stay until the long-term Flow Nexus replaces them.

Where the Clojure lives, outside the main workspace:
4. field-clj, the repository that already holds the Field CLI.
5. A new repository, by a proposal for a new repo.

### Proposal 2: one Clojure reader of the startup prompt

File: `tools/main-flow-mode/launch-config.mjs` (removed under Proposal 1 choices 1 and 2; under choice 3 its callers run the Clojure file)

```javascript
- export function firstPromptFromConfig(…) {
-   …
-   return `${prompt.trim()}\n`;
- }
```

File: `tools/claude-native-seat-refresh.py` (the embedded script removed)

```python
- EDN_FIRST_PROMPT = r"""
- …
- """
```

File: `tools/claude-native-seat-refresh.py` (the call; `first-prompt` is installed on PATH by Nix as the hm-* commands are)

```python
-         ["bb", "-e", EDN_FIRST_PROMPT, str(ROOT / "config/main-flow/shared.edn"),
+         ["first-prompt",
+          str(ROOT /
+              "config/main-flow/shared.edn"),
```

File: `nix/launcher.sh` (in the repository of Proposal 1 choice 4 or 5; the dispatch, as hm-* are dispatched)

```bash
+ exec "@babashka@/bin/bb" \
+   --config "@out@/share/launch/bb.edn" \
+   -m launch.first-prompt "$@"
```

File: `bb.edn` (choice 5's new repository; under choice 4 field-clj's deps.edn already carries malli 0.18.0)

```clojure
+ {:paths ["src"]
+  :deps {metosin/malli {:mvn/version "0.18.0"}}}
```

File: `src/launch/first_prompt.clj` (the embedded script, moved and changed; its first line, elided, against the file's; it takes the JSON and the EDN paths its caller already sends)

```clojure
- (require '[clojure.edn :as edn] …)
+ (ns launch.first-prompt
+   (:require [clojure.string :as str]
+             [cheshire.core :as json]
+             [malli.core :as m]
+             [launch.values :as values]))
+
+ (def fields ["{{modules}}" "{{handover}}"
+              "{{raw-psyche}}"])
+
+ (def Launch
+   [:map
+    [:template
+     [:and :string
+      [:fn #(every? (fn [f] (str/includes? % f))
+                    fields)]]]
+    [:sources [:vector {:min 1}
+               [:string {:min 1}]]]
+    [:handover [:string {:min 1}]]])
+
+ (defn- fill [template values]
+   (str/replace template #"\{\{([^}]+)\}\}"
+     (fn [[_ k]]
+       (let [k (keyword k)]
+         (if (contains? values k)
+           (get values k)
+           (throw (ex-info "unknown field"
+                           {:field k})))))))
+
+ (defn first-prompt [config input]
+   (let [sources (:raw-psyche-paths config)
+         launch {:template
+                 (:first-prompt-template config)
+                 :sources sources
+                 :handover (:handover input)}]
+     (when-not (m/validate Launch launch)
+       (throw (ex-info "first prompt contract"
+                       (m/explain Launch launch))))
+     (fill (:template launch)
+           {:modules (:modules input)
+            :handover (:handover input)
+            :raw-psyche (str/join "\n" sources)
+            :topic-context
+            (:topic-context config "")
+            :metaflow (:metaflow input)})))
+
+ (defn -main [& edn-paths]
+   (print (first-prompt
+           (apply values/config edn-paths)
+           (json/parse-string (slurp *in*) true))))
```

Ruling, one number from each group:

The readers:
1. The one Clojure file; both existing readers removed.
2. The Clojure file; the embedded script stays until its .py is retired.

### Proposal 3: the values leave the code

File: `tools/native-worker-launch.mjs` (removed, kind model)

```javascript
- const MODEL = 'gpt-5.6-terra';
```

File: `config/main-flow/mind.edn` (added)

```clojure
+ :worker {:model "gpt-5.6-terra" :effort :medium}
```

File: `tools/standing-skill-selection.mjs` (removed, kind skill list; the list lands in the `:modules :user` vector each aspect EDN already carries)

```javascript
- export const STANDING_SKILLS = Object.freeze([
-   …
- ]);
```

File: `src/launch/values.clj` (the one reader of the EDN; first_prompt.clj reads through it)

```clojure
+ (ns launch.values
+   (:require [clojure.edn :as edn]))
+
+ (defn- read [path]
+   (edn/read-string (slurp path)))
+
+ (defn config
+   "the EDN files the caller passes; later wins."
+   [& paths]
+   (apply merge (map read paths)))
```

Ruling, one number from each group:

The prompts:
1. EDN strings in `config/main-flow`, as the startup prompt is today.
2. Context modules in field-context, named in the EDN by module name, the prompt body under the living's review like every module.

The flow ids and the native session ids:
3. Not authored at all: registered at launch and resolved at run time, never in EDN.
4. In EDN, written by the launcher as it registers them.

The order:
5. All 58 move as each file is rewritten under Proposal 1.
6. All 58 move now; the line each .mjs reads them with is the owner's, not proposed here.
<!-- to-the-living:end -->
