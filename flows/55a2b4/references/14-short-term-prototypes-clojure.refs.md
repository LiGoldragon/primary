# Refs for «Short-term prototypes: Clojure now?», Version 9 (flow 55a2b4, 2026-10-14)

Not rendered. Never passed to the builder. Archived with the landing when
some or all of a proposal is accepted. Revises Version 7 (this file's
earlier state, in git) on an audit relayed to this seat; Version 7 revised
flows/df159a/books/14-short-term-prototypes-clojure.md (Version 6, its
refs beside it), on Core's order relayed by Psyche Flow Secondary da2038
in flows/df159a/brief-patterns.md «Book A».

## Records drawn from (his words, read whole; provenance as recorded)

- flows/da2038/vision/prototypes.md «Short-term prototypes are written in
  Clojure», 2026-10-13, STT. Carried by the vision-stack proposal below;
  not re-proposed here.
- flows/d4ae97/vision/tools.md «The Clojure stack is vision: Babashka
  first, a Nix-built image when deployed», 2026-10-08, comments: Babashka
  for first use and testing; the image built in Nix when deployed. P3's
  last clause.
- flows/88475f/vision/cljTools.md «Clojure prototypes, then Ethos and
  Rust», 2026-09-25, STT, relayed by e51411: a Clojure call taking a simple
  EDN input; the spec in Malli. P1's line.
- flows/d68c82/vision/tools.md «a repeated use case grows an existing
  tool; EDN in Clojure, datom in Nexus», 2026-10-14, STT: in Clojure an
  EDN payload for everything. P1's line.
- flows/d68c82/vision/flow.md «Flow starting configured in EDN, per
  aspect and per metaflow», 2026-10-13T17:47, STT: the short-term tool for
  starting flows configured wholly in EDN; a shared configuration, a
  per-aspect one, what differs in a per-metaflow one; the tool finds its
  context modules there and whether each is system or user prompt. P2,
  narrowed to that tool.
- flows/df159a/vision/books.md, 2026-10-14, STT, relayed by da2038: no
  proposals of code; an approach, a pattern or standard wrapping code
  instead (a standard entry point, a standard pattern) — named as the kind
  of code to propose, not as a rule. The entry, reader, dispatch and
  launcher are shown as «machine pattern»; no psyche line states the
  entry point, its output schema or its refusal.
- flows/33752b/vision/flow.md, 2026-10-13, STT: «the short-term solution,
  which is [Clojure]». The «Short term:» heading of P2.
- flows/df159a/vision/models.md, 2026-10-14, STT: no model is named on
  the page.
- intent-psyche (psyche-context): a short-term vision is named so.

## Landing home for the stack lines

- da2038 book 1 «Clojure and data: the rectification»
  (flows/da2038/books/1-clojure-and-data.md, published as
  https://claude.ai/artifact/55knMkm8gem412DzSVZokr, unruled), Proposal 1:
  a new module vision-stack («Short-term code is Clojure»: Clojure;
  Babashka first, Nix builds its image when deployed; long term Ethos and
  Rust from the Malli specs). It names `psyche-skills/skills/vision-stack.md`;
  this page's File: lines read `psyche-context/skills/vision-stack.md` on
  the audit's order. P1 and P3 add lines to that module and build on its
  proposal without restating it; P2 alone lands in vision-flow.md.

## Machine facts and their origin (witnessed by this seat, 2026-10-14)

- vision-flow.md at psyche-context e3823d6: L38 «Who speaks to whom, …»
  and L40 «## Repository and skills» are the P2 context lines, quoted
  byte for byte. No vision-stack.md in psyche-context/skills (ls).
- messenger-clj nix/launcher.sh: a case on basename "$0" mapping each
  hm-* link to a subcommand, then exec "@babashka@/bin/bb" --config
  "@out@/share/messenger-clj/bb.edn" on the uberjar; nix/package.nix
  links each hm-* to the launcher. P3 keeps the link-to-one-launcher shape
  and moves the command table into commands.edn, read by
  prototype.dispatch.
- field-clj: -main takes exactly one argument, prints one EDN value,
  refusals as tagged literals ('refused), exit by variant; malli 0.18.0.
  The entry pattern follows it.
- config/main-flow today: shared.edn, lower-cased aspect files
  (psyche.edn, mind.edn, field.edn) and capitalised metaflow files
  (metaflow/Psyche-Flow-Secondary.edn …). P2's one naming rule lower-cases
  both, so the metaflow files are renamed (psyche-flow-secondary.edn) when
  it lands. tools/main-flow-mode/launch-config.mjs reads them relative to
  the working directory; P2 takes every location from the payload's
  :configuration {:shared :aspects :metaflows}.
- config/main-flow: aspect files carry :modules as a map {:system :user};
  metaflow files carry :modules as a vector. Under P2's default a metaflow
  :modules vector replaces the aspect map; the key names are the owner's
  to align, not proposed here.
- Witness (scratchpad proto8, bb, malli 0.18.0): the page's entry.clj,
  configuration.clj, dispatch.clj, launcher.sh (placeholders filled) and
  commands.edn, with a test launch.seat namespace, against a copy of
  shared.edn, psyche.edn and psyche-flow-secondary.edn: seat-launch with
  the payload printed the merged :modules and 4 voices, exit 0; payload
  «{:x» printed #refused ["invalid type"], exit 2; a link named nope
  printed #refused {:command "nope"}, exit 2.

## Line-by-line grounding of the psyche lines (Version 9)

- P1 «A Clojure call takes a simple EDN input, and its spec is in Malli»:
  flows/88475f/vision/cljTools.md (a Clojure call taking a simple EDN
  input; the spec in Malli). Not carried: «one argument» and the widening
  to every Clojure program; the page's `Machine:` line and the entry
  pattern hold «one argument», the machine's (field-clj's -main).
- P2 «The short-term tool that starts flows reads its whole configuration
  from EDN: a shared file, each aspect's file, and each metaflow's file
  holding what differs. The configuration names every context module a
  flow starts with and whether it goes in the system prompt or the user
  prompt»: flows/d68c82/vision/flow.md, 2026-10-13T17:47. Not carried:
  the merge order «map into map, later wins», the machine's; it stands as
  a `Machine:` line and in P2's choices and the configuration pattern.
- P3 «Babashka in first use and testing, the Nix-built image when
  deployed»: flows/d4ae97/vision/tools.md, 2026-10-08. Not carried: PATH as
  the hm-* commands do, one launcher, links, the EDN file of commands;
  these are the machine's (messenger-clj's launcher shape) and stand in
  the page's `Machine:` line and the launcher pattern.

## Reasons for each choice

- P1 choice 1 (standard input): a large or multiline payload is awkward
  as one argument; hm-send already offers --stdin. The default follows
  the datom interface shape (one inline value, no flags) and field-clj.
- P2 default (map into map): the aspect files nest maps; a metaflow file
  that changes one inner key keeps the rest. Choice 1 is today's shallow
  merge. Choice 2 lets a metaflow add modules to the aspect's list.
- P3 default (names in commands.edn): the hm-* shape with its table moved
  from the shell into data. Choice 1 drops the file by naming convention.
- The refusal is printed as a tagged literal, as field-clj does; how a
  variant is written in EDN is Book B's ruling and the entry follows it.

## Removed from the page in Version 8

- P1's vision-flow line («a prototype is a Clojure program run by
  Babashka, and every prototype starts through one standard entry point
  … or a refusal»): its stack clause is the vision-stack proposal's; the
  entry point, output schema and refusal have no record and are shown as
  machine pattern.
- P1 choice 2 (the standard files in field-clj) and the new-repository
  location note: dropped; where the standard code lives stays unruled.
- P2's line for every prototype: narrowed to the flow-starting tool.
- P2 `(def dir "config/main-flow")`: the locations come from the payload.
- P3's bash case table and its choice 2 (a built jar): no record carries
  the jar; the deployed form is the Nix-built image.
- The figure: redrawn (launcher looks up commands EDN; entry runs its act;
  the reader belongs to the flow starter).

## Removed from the page in Version 7

- The live-path figure (counts by language, which files leave): its
  question was the file migration; Version 7's figure asks how a
  prototype starts and gets its values, and branches.
- V6 P1 file lists and its choices 1–3 (which files leave now) and 4–5
  (field-clj or new repository; 4–5 survive as P1 choice 2 and P1's
  default). The order of removal of the .mjs files is not on this page;
  book 01 P4 («Flow: the first response», held) carries «the Flow starter
  first».
- V6 P2 per-file rewrites (launch-config.mjs, claude-native-seat-
  refresh.py, first_prompt.clj, bb.edn) and its readers choices.
- V6 P3 per-file removals and its choices (prompts as EDN strings or as
  field-context modules; flow ids registered or written; order of moving
  the 58 values). These remain unruled and are not carried here.

### Version 6 crystallization, as it stood (its one example model line elided)

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
- const MODEL = …;   (model elided)
```

File: `config/main-flow/mind.edn` (added)

```clojure
+ :worker {:model … :effort :medium}   (model elided)
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

## Overlaps to coordinate (one module per statement)

- Book 01 «Flow: the first response» (flows/55a2b4/books/01-flow-first-
  response.md, held, unpublished) P4 proposes into vision-flow.md «A
  short-term prototype is written in Clojure with its values in EDN; …»
  and P2 «a prompt, a model, a skill list or a path is never hard-coded».
  Its P4 overlaps the vision-stack proposal and this page's P2; when book
  01 is revised, its P4 defers to them and its P2 keeps only the
  no-hard-coded-value rule, which da2038 book 1 Proposal 2 also carries.
- Book B «Ethos and Datom in Clojure and EDN» decides the EDN variant
  shape the entry's and the dispatch's refusals use.

## Rendering

- The builder (tools/book-build.clj) draws only a single vertical chain
  of boxes as SVG. The branching figure is kept in a `figure` fence and
  renders as monospaced text in the local html; the published page needs
  it drawn by the figure subflow, every box, label and arrow kept.
