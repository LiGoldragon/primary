<!-- to-the-living:start -->
Presentation.{ «Short-term prototypes: Clojure now?» }

# Short-term prototypes: Clojure now?

```figure
        ┌──────────────────────────┐
        │ a command on PATH        │
        └────────────┬─────────────┘
                     │ is a link to
                     ▼
        ┌──────────────────────────┐
        │ the repository launcher  │
        └──┬────────────────────┬──┘
           │ looks up its       │ runs
           │ name in            │
           ▼                    ▼
   ┌────────────────┐ ┌────────────────┐
   │ the commands   │ │ the command's  │
   │ EDN file       │ │ -main          │
   └────────────────┘ └───────┬────────┘
                              │ calls
                              ▼
        ┌──────────────────────────┐
        │ the standard entry       │
        └──┬──────────┬─────────┬──┘
     takes │     runs │  prints │
           ▼          ▼         ▼
     ┌─────────┐ ┌──────────┐ ┌─────────┐
     │ one EDN │ │ its act  │ │ one EDN │
     │ payload │ │          │ │ answer  │
     └─────────┘ └───┬──────┘ └─────────┘
                     │ in the flow starter,
                     │ reads through
                     ▼
        ┌──────────────────────────┐
        │ the configuration reader │
        └────────────┬─────────────┘
                     │ merges, later wins
          ┌──────────┼──────────┐
          ▼          ▼          ▼
     ┌────────┐ ┌────────┐ ┌──────────┐
     │ shared │ │ aspect │ │ metaflow │
     │ file   │ │ file   │ │ file     │
     └────────┘ └────────┘ └──────────┘
```

## Crystallization

### Proposal 1: one EDN payload, and the standard entry

File: `psyche-context/skills/vision-stack.md` (builds on the rectification book's proposal, unruled)

```text
+ ## A Clojure call takes a simple EDN input
+
+ A Clojure call takes a simple EDN input, and its spec is in Malli.
+
+ Machine: the pattern takes one EDN payload as its one argument.
```

File: `src/prototype/entry.clj` (machine pattern)

```clojure
+ (ns prototype.entry
+   (:require [clojure.edn :as edn]
+             [malli.core :as m]
+             [malli.error :as me]))
+
+ ;; every prototype's -main:
+ ;; (defn -main [& args]
+ ;;   (entry/run {:input In :output Out
+ ;;               :act act}
+ ;;              args))
+
+ (defn- payload [args]
+   (when (= 1 (count args))
+     (try (edn/read-string
+           {:default tagged-literal}
+           (first args))
+          (catch Exception _ nil))))
+
+ (defn- refused [schema value]
+   (tagged-literal 'refused
+                   (me/humanize
+                    (m/explain schema value))))
+
+ (defn- answer [value code]
+   (prn value)
+   (System/exit code))
+
+ (defn run
+   "One EDN payload in, one EDN value out."
+   [{:keys [input output act]} args]
+   (let [p (payload args)]
+     (if-not (m/validate input p)
+       (answer (refused input p) 2)
+       (let [result (act p)]
+         (if (m/validate output result)
+           (answer result 0)
+           (answer (refused output result) 1))))))
```

1. The payload arrives on standard input:

```text
- one EDN payload as its one argument
+ one EDN payload on its standard input
```

### Proposal 2: the configuration of starting flows

File: `psyche-context/skills/vision-flow.md` (a new section after «Starting flows»)

```text
  Who speaks to whom, within an aspect and across aspects at the same layer in a shared topic, is the vision-aspects skill's. Flow refuses a request that leaves those routes.
+
+ ## Short term: the configuration of starting flows
+
+ The short-term tool that starts flows reads its whole configuration from EDN: a shared file, each aspect's file, and each metaflow's file holding what differs. The configuration names every context module a flow starts with and whether it goes in the system prompt or the user prompt.
+
+ Machine: it merges the files in that order, map into map, so a later file's value wins at each key.
+
  ## Repository and skills
```

File: `src/launch/configuration.clj` (machine pattern)

```clojure
+ (ns launch.configuration
+   (:require [clojure.edn :as edn]
+             [clojure.java.io :as io]
+             [clojure.string :as str]))
+
+ (defn- file-name
+   "One rule for every file: its parts,
+   lower-cased, joined by hyphens."
+   [& parts]
+   (str (str/lower-case
+         (str/join "-" (map name parts)))
+        ".edn"))
+
+ (defn- read-edn [file]
+   (edn/read-string (slurp file)))
+
+ (defn- deep-merge [& maps]
+   (apply merge-with
+          (fn [a b]
+            (if (and (map? a) (map? b))
+              (deep-merge a b)
+              b))
+          maps))
+
+ (defn configuration
+   "Shared, then aspect, then metaflow;
+   every location from the payload."
+   [{{:keys [shared aspects metaflows]}
+     :configuration
+     {:keys [aspect topic layer]}
+     :metaflow}]
+   (deep-merge
+    (read-edn shared)
+    (read-edn (io/file aspects
+                       (file-name aspect)))
+    (read-edn (io/file metaflows
+                       (file-name aspect topic
+                                  layer)))))
```

1. A later file replaces a whole top-level key:

```text
- map into map, so a later file's value wins at each key.
+ key by key at the top, so a later file's value replaces the whole key.
```

2. A later file's vectors extend the earlier ones:

```text
- map into map, so a later file's value wins at each key.
+ map into map, so a later file's value wins at each key and a later vector extends the earlier one.
```

### Proposal 3: the launcher, as the hm-* commands

File: `psyche-context/skills/vision-stack.md` (builds on the rectification book's proposal, unruled)

```text
+ ## Babashka first, the Nix-built image when deployed
+
+ Babashka in first use and testing, the Nix-built image when deployed.
+
+ Machine: a repository of Clojure programs reaches PATH as the hm-* commands do: every command is a link to one launcher, and the launcher finds the command's namespace by its name in the repository's EDN file of commands, then runs that namespace's `-main`.
```

File: `nix/launcher.sh` (machine pattern, the Babashka form)

```bash
+ #!/usr/bin/env bash
+ set -euo pipefail
+
+ exec "@babashka@/bin/bb" \
+   --config "@out@/share/@pname@/bb.edn" \
+   -m prototype.dispatch \
+   "@out@/share/@pname@/commands.edn" \
+   "$(basename "$0")" "$@"
```

File: `src/prototype/dispatch.clj` (machine pattern)

```clojure
+ (ns prototype.dispatch
+   (:require [clojure.edn :as edn]))
+
+ (defn -main
+   "The commands file, the name the launcher
+   was called by, then that command's own
+   arguments."
+   [commands command & args]
+   (if-let [target (get (edn/read-string
+                         (slurp commands))
+                        command)]
+     (do (require target)
+         (apply (ns-resolve target '-main)
+                args))
+     (do (prn (tagged-literal 'refused
+                              {:command command}))
+         (System/exit 2))))
```

File: `commands.edn` (the repository's data)

```clojure
+ {"first-prompt" launch.first-prompt
+  "seat-launch" launch.seat}
```

1. The command's name spells its namespace:

```text
- finds the command's namespace by its name in the repository's EDN file of commands, then runs that namespace's `-main`
+ runs the `-main` of the namespace its command's name spells
```
<!-- to-the-living:end -->
