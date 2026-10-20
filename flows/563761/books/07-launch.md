<!-- to-the-living:start -->
Presentation.{ «Flow: launch and lean start» }

# Flow: launch and lean start

## Crystallization

### Proposal 1: the startup prompt is one lean block

File: `psyche-context/skills/intent-startup-prompt.md`, the paragraph
«One block, with the startup skills in it», as it stands, with two
sentences added at its end.

The launcher: the script that starts a flow,
`tools/claude-main-flow-launch.mjs` and `tools/codex-main-flow-launch.mjs`.
EDN: Clojure's plain data notation, the form of the launch configuration
under `primary/config/main-flow/`. A module: one skill file composed
into a prompt. Babashka (bb): the program that runs Clojure scripts at
once.

Sources: flow d8df70, 2026-09-23 and 2026-09-24; flow e51411,
2026-09-24; flow ebbe30, 2026-10-09; flow d68c82, 2026-10-13.

```text
  A flow starts from one startup prompt: a single block of text. Some skills are startup skills: they are given to particular flows at their start and never to their subflows, and the harness is configured so the model cannot see or load them itself. Each harness has a facility for this, and that facility is what is used. A startup skill enters through the startup prompt; if one was left out, it is put in afterward, as a repair of the startup prompt.
+ The order of the startup skills in the block carries nothing. The block is lean: the flow's id, its mode, its modules and its brief, and nothing else.
```

File: `primary/tools/claude-main-flow-launch.mjs`, the skills sent in
batches of six:

```js
- export const MAX_SKILLS_PER_PROMPT = 6;
- const STARTUP_INSTRUCTION = 'Startup context only: load these skills for the upcoming launch brief. Do not begin that work or write files yet. Reply exactly READY.';
```

```js
-   return `${skillNames.map(n => `/${n}`).join(' ')} # Startup skills\n\n${STARTUP_INSTRUCTION}\n`;
```

```js
-     while (loadedCount < skillNames.length) {
-       const nextSkills = skillNames.slice(loadedCount, loadedCount + MAX_SKILLS_PER_PROMPT);
-       const startupPrompt = composeSkillPrompt({skillNames: nextSkills, exists: liveSkillExists(o.workspace)});
-       submitPrompt(o.herdrSession, paneId, startupPrompt);
```

File: `primary/tools/native-main-flow-launch-shared.mjs`, the order
forced on the skills:

```js
- export function orderSkillsForPrompt(names, leading = 'compensation-main-flow') {
-   if (new Set(names).size !== names.length) throw new Error('resolved skill closure contains duplicates');
-   return names.includes(leading) ? [leading, ...names.filter(name => name !== leading)] : [...names];
- }
```

File: `primary/tools/codex-main-flow-launch.mjs`, the heading and the
skill header written into the block:

```js
- export const skillBlock = (workspace, name, text) =>
-   `Base directory for this skill: ${path.join(workspace, '.agents', 'skills', name)}\n\n${text.trim()}\n`;
```

```js
-   const prompt = `${blocks.join('\n')}\n# Launch brief\n\n${brief.trim()}\n`;
```

File: `primary/tools/main-flow-mode/launch-config.mjs`, the repository
of a module inferred from its name in code:

```js
-     for (const placement of ['system', 'user']) config.modules[placement] = config.modules[placement].map(name => ({name, repository: name === 'compensation-book-crystallization' || name === 'compensation-main-flow' || name.startsWith('compensation-') ? 'field' : (name.startsWith('intent-') || name.startsWith('spirit-') || name === 'vision-book' ? 'psyche' : (name.startsWith('knowledge-') || name.startsWith('operation-') ? 'mind' : config.aspect.toLowerCase())), path: `skills/${name}.md`, placement}));
```

File: `primary/config/main-flow/shared.edn`. The skill path becomes a
pattern filled with the module's name; each kind of module names its
home; the prompt's parts, their order and their separator are data:

```clojure
-                         :skills "skills"}
+                         :skills "skills/%s.md"}
```

```clojure
+  :module-homes {:spirit :psyche :intent :psyche
+                 :vision :psyche
+                 :knowledge :mind :operation :mind
+                 :compensation :field}
+  :prompt {:parts [:flow-id :mode :modules :brief]
+           :separator "\n\n"}
```

File: `primary/config/main-flow/metaflow/Psyche-Flow-Primary.edn`, the
one shape for system and user modules that the aspect files have; the
topic uncapitalized, a camelCase name:

```clojure
- {:aspect :Psyche :topic :Flow :layer :Primary :modules [:spirit-core :intent-main-flow :vision-book :compensation-book-crystallization] :user-modules [:compensation-main-flow] :secondary-native-id "da203818-26b4-4a15-9de8-faeb1e7d23cd"}
+ {:aspect :Psyche :topic :flow :layer :Primary
+  :secondary-native-id
+  "da203818-26b4-4a15-9de8-faeb1e7d23cd"
+  :modules
+  {:system [:spirit-core :intent-main-flow
+            :vision-book
+            :compensation-book-crystallization]
+   :user [:compensation-main-flow]}}
```

File: `primary/config/main-flow/metaflow/Psyche-Flow-Secondary.edn`:

```clojure
- {:aspect :Psyche :topic :Flow :layer :Secondary :modules [:spirit-core :intent-main-flow :vision-book :compensation-book-crystallization] :user-modules [:compensation-main-flow]}
+ {:aspect :Psyche :topic :flow :layer :Secondary
+  :modules
+  {:system [:spirit-core :intent-main-flow
+            :vision-book
+            :compensation-book-crystallization]
+   :user [:compensation-main-flow]}}
```

File: `primary/config/main-flow/metaflow/Psyche-Core-Primary.edn`:

```clojure
- {:aspect :Psyche :topic :Core :layer :Primary :modules [:intent-psyche-interaction]}
+ {:aspect :Psyche :topic :core :layer :Primary
+  :modules {:system [:intent-psyche-interaction]
+            :user []}}
```

File: `primary/config/main-flow/metaflow/Mind-Core-Primary.edn`:

```clojure
- {:aspect :Mind :topic :Core :layer :Primary :modules [:intent-psyche-interaction]}
+ {:aspect :Mind :topic :core :layer :Primary
+  :modules {:system [:intent-psyche-interaction]
+            :user []}}
```

File: `primary/config/main-flow/metaflow/Field-Core-Primary.edn`:

```clojure
- {:aspect :Field :topic :Core :layer :Primary :modules [:intent-psyche-interaction]}
+ {:aspect :Field :topic :core :layer :Primary
+  :modules {:system [:intent-psyche-interaction]
+            :user []}}
```

File: `messenger-clj/src/messenger_clj/launch.clj`, its requires, and
the composition of the block; the machine's design, because a module's
text is read once from its repository at the declared revision and
nothing else is written into the block:

```clojure
  (ns messenger-clj.launch
    (:require [clojure.string :as str]
+             [clojure.java.shell :refer [sh]]
              [malli.core :as m]))
```

```clojure
+ ;; A skill's name is words joined by hyphens, its
+ ;; own form; the first word is its kind.
+ (defn module-home [config module]
+   (let [words (str/split (name module) #"-" 2)
+         kind (keyword (first words))]
+     (or (get-in config [:module-homes kind])
+         (throw (ex-info "ModuleHomeUnknown"
+                         {:module module})))))
+
+ ;; git's own words read the file at the declared
+ ;; revision, in its revision:path form.
+ (defn module-text [config module]
+   (let [home (module-home config module)
+         repo (get-in config [:repositories home])
+         file (format (:skills repo) (name module))
+         out (sh "git" "-C" (:path repo) "show"
+                 (str (:ref repo) ":" file))]
+     (when-not (zero? (:exit out))
+       (throw (ex-info "ModuleUnavailable"
+                {:module module :file file})))
+     (:out out)))
+
+ ;; The front matter fence is the skill file's own
+ ;; format; the body is what enters a prompt.
+ (defn module-body [text]
+   (str/trim (str/replace-first
+              text #"(?s)\A---\n.*?\n---\n" "")))
+
+ (defn module-block [config module]
+   (module-body (module-text config module)))
+
+ (defn modules [aspect mf placement]
+   (concat (get-in aspect [:modules placement])
+           (get-in mf [:modules placement])))
+
+ (defn join-parts [config parts]
+   (str/join (get-in config [:prompt :separator])
+             parts))
+
+ (defn system-prompt [config aspect mf]
+   (join-parts config
+               (map #(module-block config %)
+                    (modules aspect mf :system))))
+
+ (defn prompt-parts [config aspect mf launch]
+   {:flow-id (:flow-id launch)
+    :mode (format (get-in config [:prompt :mode])
+                  (name (:mode mf)))
+    :modules (join-parts
+              config
+              (map #(module-block config %)
+                   (modules aspect mf :user)))
+    :brief (:brief launch)})
+
+ (defn first-prompt [config parts]
+   (let [order (get-in config [:prompt :parts])]
+     (join-parts config (map parts order))))
```

`ModuleHomeUnknown` and `ModuleUnavailable` are the two refusals' own
names. `:mode` is Proposal 4.

File: `primary/CLAUDE.md`, under choice 6; `knowledge-psyche` is a user
module of `psyche.edn` already, so the line asks a second load:

```text
- Load the `knowledge-psyche` skill. If your work touches a topic the psyche may
- have spoken on, search the vision- and intent- skills, `vision-raw/`, and `flows/*/vision/` before assuming.
+ If your work touches a topic the psyche may have spoken on, search the vision- and intent- skills, `vision-raw/`, and `flows/*/vision/` before assuming.
```

Ruling, one number from each group:

The sentences and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

What «no hashes» in the block means (flow e51411, 2026-09-24):
4. Markdown headings, the `#` lines; removed as shown.
5. Hex identifiers, the machine's reading; the flow's id then enters
   the block in its word form, `word-form` of `flow_id.clj`:

File: `primary/config/main-flow/shared.edn`:

```clojure
-  :prompt {:parts [:flow-id :mode :modules :brief]
+  :prompt {:parts [:words :mode :modules :brief]
```

File: `messenger-clj/src/messenger_clj/launch.clj`, its requires and
`prompt-parts`:

```clojure
+             [messenger-clj.flow-id :as fid]
```

```clojure
-   {:flow-id (:flow-id launch)
+   {:words (fid/word-form config (:id launch))
```

The `CLAUDE.md` line:
6. Remove the load, as shown.
7. Keep it.

### Proposal 2: the id is claimed for the flow, never by it

File: `psyche-context/skills/vision-flow.md`, «What it does», the
paragraph that begins «A topic's name is a camelCase identifier», one
sentence added at its end; and
`psyche-context/skills/intent-main-flow.md`, the paragraph that begins
«You run a shell command».

Sources: flow f55ec8, 2026-09-16; flow e51411, 2026-09-24.

```text
  A topic's name is a camelCase identifier, uncapitalized. A flow's id is the hash of the harness's session id, so a transcript is found from the flow id. Where the harness lets Flow choose the session id, Flow chooses it before the flow starts and the flow reads it in its prompt; where the harness assigns it, Flow learns it when the flow binds. No flow declares its id: every call to Flow is identified by the calling process.
+ The process that starts a flow claims its id and makes its directory before the flow starts; the id stands in the startup prompt and in a file the flow cannot write, where its subflows find it. No flow or subflow claims an id.
```

```text
- You run a shell command for two things only: claiming your Flow ID, and the writes you own: your log, your psyche records, and your summary. Leave Primary edits for the sole standing committer; never stage, commit, push or take PrimaryPublish yourself. In other repositories, commit and push your own changes. Everything else that reaches into the harness, the cluster, or the code goes through a subflow.
+ You run a shell command for the writes you own only: your log, your psyche records, and your summary; your Flow ID was claimed for you as you started and stands in your startup prompt. Leave Primary edits for the sole standing committer; never stage, commit, push or take PrimaryPublish yourself. In other repositories, commit and push your own changes. Everything else that reaches into the harness, the cluster, or the code goes through a subflow.
```

File: `primary/tools/main-flow-mode/system-prompt.md`, the same
sentence:

```text
- You run a shell command for two things only: claiming your Flow ID, and the writes you own: your log, your psyche records, and your summary. Leave Primary edits for the sole standing committer; never stage, commit, push or take PrimaryPublish yourself. In other repositories, commit and push your own changes. Everything else that reaches into the harness, the cluster, or the code goes through a subflow.
+ You run a shell command for the writes you own only: your log, your psyche records, and your summary; your Flow ID was claimed for you as you started and stands in your startup prompt. Leave Primary edits for the sole standing committer; never stage, commit, push or take PrimaryPublish yourself. In other repositories, commit and push your own changes. Everything else that reaches into the harness, the cluster, or the code goes through a subflow.
```

The id enters the block as `:flow-id` of Proposal 1. The file the flow
cannot write is `flow-id.edn`, the mark the claim writes, fenced after
it is written. Its mode is data, `primary/config/main-flow/shared.edn`,
inside `:flow-id`:

```clojure
+            :mark-mode "r--r--r--"
```

File: `messenger-clj/src/messenger_clj/flow_id.clj`, before
`claim-lane!`:

```clojure
+ (defn fence-mark! [config mark]
+   (fs/set-posix-file-permissions
+    mark (get-in config [:flow-id :mark-mode])))
```

and in `claim-lane!`, once the mark is written:

```clojure
  (defn claim-lane! [config root id]
    (let [lane (fs/path root (short-hex config id))
          mark (str (fs/path lane "flow-id.edn"))
          seen {:session (:session id)
                :start (:start id)}]
      (try (fs/create-dir lane)
           (spit mark (pr-str seen))
+          (fence-mark! config mark)
           id
```

Ruling, one number from each group:

The sentences and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

Where the fenced file sits:
4. In the harness's own starting directory, each flow started in a
   place of its own (flow f55ec8, 2026-09-16).
5. In the flow's directory under `flows/`, reached through the
   `FLOW_ID` environment variable the launcher sets, the machine's
   design: every flow runs in the one shared workspace (Proposal 13),
   so the harness's own directory cannot carry one flow's id.

### Proposal 3: the first response is a presentation

File: `psyche-context/skills/intent-startup-prompt.md`, a new section
after «One block, with the startup skills in it».

Sources: flow 445410, 2026-10-09; flow 73ada7, 2026-10-09.

```text
+ ## The first response is a presentation
+
+ A new flow's first response is a presentation of its context: having loaded it, the flow has subflows question and reinforce it, then distills it for its role, as a proposal for how to make things better. Psyche distills into vision, intent and spirit; Mind into knowledge, questions and implementation; Field into its own roles. No flow is told to answer that it is ready.
```

File: `primary/tools/claude-main-flow-launch.mjs`, the instruction
removed in Proposal 1 (`Reply exactly READY`). File:
`primary/tools/secondary-first.mjs`, the brief written in code:

```js
-         fs.writeFileSync(brief, `You are the ${options.aspect} ${topic} Secondary. Give only your normal startup presentation. No additional task is assigned.\n`, {mode: 0o600});
```

It is data, `primary/config/main-flow/shared.edn`, read by
Proposal 12:

```clojure
+  :secretary
+  {:brief
+   "Give your startup presentation; no task."}
```

Ruling:

1. Land.
2. Land with changes the living names.
3. Drop.

### Proposal 4: a flow is given its mode at start

File: `psyche-context/skills/vision-design.md`, a new section at the
end. The two modes, design and prototype, are the living's words of the
same day in `flows/33752b/vision/design.md`.

Source: flow 33752b, 2026-10-12.

```text
  No one can know ahead of time that the pieces are enough to yield the best version that could be come up with at the moment. Everybody contributes to the judgment, without limit. Judging that an idea is complete is the hardest part of a thinking machine to get.
+
+ ## A flow is given its mode at start
+
+ A flow is told at start whether it designs or builds a prototype; it does not find out.
```

File: `primary/config/main-flow/metaflow/Psyche-Flow-Primary.edn`,
inside its map:

```clojure
  {:aspect :Psyche :topic :flow :layer :Primary
+  :mode :design
```

File: `primary/config/main-flow/metaflow/Psyche-Flow-Secondary.edn`:

```clojure
  {:aspect :Psyche :topic :flow :layer :Secondary
+  :mode :design
```

File: `primary/config/main-flow/metaflow/Psyche-Core-Primary.edn`:

```clojure
  {:aspect :Psyche :topic :core :layer :Primary
+  :mode :design
```

File: `primary/config/main-flow/metaflow/Mind-Core-Primary.edn`, under
choice 4:

```clojure
  {:aspect :Mind :topic :core :layer :Primary
+  :mode :design
```

File: `primary/config/main-flow/metaflow/Field-Core-Primary.edn`, under
choice 4:

```clojure
  {:aspect :Field :topic :core :layer :Primary
+  :mode :design
```

File: `primary/config/main-flow/shared.edn`, inside `:prompt`, the
line that carries it:

```clojure
+           :mode "Mode: %s"
```

The part `:mode` of `prompt-parts`, Proposal 1, reads both.

Ruling, one number from each group:

The section and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

The Mind and Field Core Primaries:
4. `:design`, as shown, the machine's choice.
5. `:prototype`, the machine's alternative.

### Proposal 5: the harness command

File: `psyche-context/skills/vision-flow.md`, «Starting flows», after
the paragraph that begins «A layer is Primary».

Herdr: the third-party terminal program the flows run in; a pane: one
terminal area in it. Remote control: the harness's own way of reaching
a session from another device.

Sources: flow fd0f97, 2026-09-15, four records; flow e51411,
2026-09-24; flow d68c82, 2026-10-13.

```text
  A layer is Primary, Secondary, Tertiary or Quaternary, in every aspect; the layer decides the model, declared once in Flow as configuration and changed only over its meta socket. A launch names the metaflow, the context modules composed into its prompts, and a brief of a small paragraph; the Nexus composes the prompt from its module registry, checking each module's hash against its source.
+
+ A main flow is reachable remotely from the moment it starts, and is seen on the desktop in a normally coloured terminal. Every flow is started with the harness's permission prompts off; a flow that was not is relaunched.
```

Under choice 4, one more sentence:

```text
+ Flow launches it under Herdr.
```

File: `psyche-context/skills/vision-flow.md`, the heading «Short
term», Proposal 1 of «Flow: short term and long term», third edition,
after «A replaced session is reaped by the refresh itself»; every
short-term line of this book sits under it:

```text
  A flow is refreshed when its context passes the layer's threshold: it is told, writes its handover, and is replaced as it goes idle; while the refresh runs the metaflow is locked, and the predecessor is reaped in the same event. Every harness event reaches Flow through its hooks calling the Flow CLI, which identifies the calling process.
+
+ ## Short term

  ## Subflows replace the harness subagent facility
```

Under choice 5, the sentence is a line under «Short term» (flow
d68c82, 2026-10-13: the short-term system for starting flows):

```text
+ Short term: the launcher starts every flow under Herdr.
```

**Destroy**, under choice 9: the record in
`flows/fd0f97/vision/launch.md` (2026-09-15), whole, a working
instruction whose words on the first prompt are drawn into Proposal 1:

```text
- ## Once the Flow component works with a cheap test model, the primary relaunches itself properly in a new Flow with a properly loaded first prompt and context; a good anatomy, judgment, implement; simple syntax
```

File: `primary/tools/claude-main-flow-launch.mjs`, the command and the
environment written in code:

```js
- export const UNSET_ENV = ['CLAUDE_CODE_CHILD_SESSION', 'CLAUDE_JOB_DIR', 'CLAUDE_CODE_SESSION_KIND', 'CLAUDE_CODE_SESSION_ID', 'CLISESSIONID'];
```

```js
-     const command = `cd ${sh(o.workspace)} && exec env ${claudeFlowEnvironment(flowId)} claude --session-id ${sessionId} --model ${sh(o.model)} --effort ${sh(o.effort)} --name ${sh(title)} --remote-control --dangerously-skip-permissions --system-prompt-file ${sh(mode.promptFile)} --settings ${sh(mode.settingsFile)} "$(cat ${sh(promptFile)})"`;
```

File: `primary/tools/codex-main-flow-launch.mjs`, the identities, the
command, and the thread started with its permissions off in code:

```js
-   const identities = ['CODEX_THREAD_ID', 'CODEX_SESSION_ID', 'CLAUDE_CODE_SESSION_ID', 'CLAUDE_SESSION_ID', 'THREAD_ID', 'FLOW_ID', 'FLOW_DIRECTORY'];
```

```js
-   return `exec env ${identities.map(name => `-u ${name}`).join(' ')} ${sh(client.expectedPath)} -m ${sh(o.model)} -c ${sh(`model_instructions_file=${JSON.stringify(systemPromptFile)}`)} -c ${sh(`model_reasoning_effort="${o.effort}"`)} --dangerously-bypass-approvals-and-sandbox -C ${sh(o.workspace)} ${threadId ? `resume ${sh(threadId)} ` : ''}"$(cat ${sh(promptFile)})"`;
```

```js
-       threadStart: ({hooks}) => withRpc(client.endpoint, call => call('thread/start', {
-         model: o.model, cwd: o.workspace, approvalPolicy: 'never', sandbox: 'danger-full-access',
-         baseInstructions: fs.readFileSync(systemPromptFile, 'utf8'), ephemeral: false,
```

File: `primary/config/main-flow/shared.edn`, inside its map. A keyword
in a command template is a field of the launch record; the variable
that carries the flow's id is named once; the colour variable goes with
the identities a parent leaves behind (the context of flow fd0f97's
record, 2026-09-15: `NO_COLOR` came from the launch's environment):

```clojure
+  :command
+  {:claude
+   ["claude" "--session-id" :session
+    "--model" :model "--effort" :effort
+    "--name" :title "--remote-control"
+    "--dangerously-skip-permissions"
+    "--allowedTools" :tools
+    "--system-prompt-file" :system-prompt
+    "--settings" :settings :prompt]
+   :codex
+   ["codex" "-m" :model
+    "-c" :instructions "-c" :reasoning
+    "--dangerously-bypass-approvals-and-sandbox"
+    "-C" :workspace :prompt]}
+  :environment
+  {:flow-id "FLOW_ID"
+   :claude
+   {:unset ["CLAUDE_CODE_CHILD_SESSION"
+            "CLAUDE_JOB_DIR"
+            "CLAUDE_CODE_SESSION_KIND"
+            "CLAUDE_CODE_SESSION_ID"
+            "CLISESSIONID" "NO_COLOR"]}
+   :codex
+   {:unset ["CODEX_THREAD_ID" "CODEX_SESSION_ID"
+            "CLAUDE_CODE_SESSION_ID"
+            "CLAUDE_SESSION_ID" "THREAD_ID"
+            "FLOW_ID" "FLOW_DIRECTORY"
+            "NO_COLOR"]}}
```

File: `messenger-clj/src/messenger_clj/launch.clj`:

```clojure
+ ;; A keyword in the template is a field of the
+ ;; launch record; a vector field is spliced.
+ (defn command-line [config harness launch]
+   (mapcat (fn [part]
+             (if (keyword? part)
+               (let [v (get launch part)
+                     one #(if (keyword? %) (name %)
+                              (str %))]
+                 (if (coll? v)
+                   (map one v)
+                   [(one v)]))
+               [part]))
+           (get-in config [:command harness])))
+
+ ;; -u and NAME=value are env's own forms; the
+ ;; variable is the pointer a flow reads to find
+ ;; its directory.
+ (defn env-args [config harness flow-id]
+   (let [env (:environment config)
+         unset (get-in env [harness :unset])]
+     (concat (mapcat #(list "-u" %) unset)
+             [(str (:flow-id env) "=" flow-id)])))
```

Ruling, one number from each group:

The paragraph and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

Herdr:
4. Flow launches under Herdr, long term as well (flow fd0f97,
   2026-09-15: «maybe under Herder if it works better»).
5. Short term only, the machine's suggestion: «maybe under Herder if
   it works better» (flow fd0f97, 2026-09-15) settles nothing long
   term, and the launcher is the short-term system for starting flows
   (flow d68c82, 2026-10-13).
6. No Herdr sentence.

The permissions sentence:
7. Stands as written, unmarked.
8. Short term only; the Capsule sandboxes long term: the machine's
   design.

The record:
9. Destroy it, as above.
10. Keep it.

### Proposal 6: the tools a flow carries

The tool sets a flow may carry are data, named with the harness's own
tool names; a metaflow names its set.

Source: flow d68c82, 2026-10-13.

File: `primary/config/main-flow/shared.edn`:

```clojure
-  :tools {:claude [:read :edit :write :bash :web]
-          :codex [:read :edit :write :bash :web]
-          :book-publisher [:read :edit :write :bash :web :artifact :artifact-comments :artifact-data]}}
+  :tools {:claude ["Read" "Edit" "Write" "Bash"
+                   "WebFetch" "WebSearch"]
+          :book-publisher ["Read" "Edit" "Write"
+                           "Bash" "WebFetch"
+                           "WebSearch" "Artifact"
+                           "ArtifactComments"
+                           "ArtifactData"]}}
```

File: `primary/config/main-flow/metaflow/Psyche-Flow-Primary.edn`,
inside its map, the set it carries:

```clojure
  {:aspect :Psyche :topic :flow :layer :Primary
+  :tools :book-publisher
```

File: `messenger-clj/src/messenger_clj/launch.clj`; `start-call`,
Proposal 10, fills the launch record's `:tools` from it, and
`command-line`, Proposal 5, places it after `--allowedTools`:

```clojure
+ ;; --allowedTools takes its names comma-joined,
+ ;; the harness's own form of the flag.
+ (defn tools [config mf]
+   (str/join ","
+             (get-in config [:tools (:tools mf)])))
```

Ruling:

1. Land.
2. Land with changes the living names.
3. Drop.

### Proposal 7: every hook, as a notification

File: `psyche-context/skills/vision-flow.md`, «A replaced session is
reaped by the refresh itself», the first long-term paragraph as it
stands; a line under «Short term» (Proposal 5).

A hook: a command the harness runs at one of its events, such as the
end of a turn or the submission of a prompt. The messenger:
messenger-clj, the short-term tool that registers flows and types
messages into them.

Sources: flow 840e42, 2026-09-15; flow d68c82, 2026-10-13.

```text
  Every harness event reaches Flow through the harness's hooks calling the Flow CLI, so Flow knows each flow's state without polling; a marked block landing in a transcript becomes an action, a book among them, with no tool call by the flow; a flow nearing its context limit is told, writes its handover, and is refreshed as it goes idle. Polling is forbidden; a poller that must exist is registered and reported.
```

```text
+ Short term: the launcher installs, from the EDN configuration, a hook on every event the harness offers, each calling the messenger with the flow's configuration; what is done with the event is the messenger's.
```

File: `primary/tools/claude-main-flow-launch.mjs`, `mainFlowMode`, the
hooks written in code:

```js
-   const hook = ['python3', sh(path.join(modeDir, 'reminder-hook.py')), '--prompt-file', sh(promptFile),
-     '--state-dir', sh(path.join(jobDir, 'main-flow-reminder')), '--every', '20'].join(' ');
-   const settings = {hooks: {UserPromptSubmit: [{hooks: [{type: 'command', command: hook, timeout: 10}]}]}};
```

File: `primary/tools/codex-main-flow-launch.mjs`, the hook's shape and
its hash, and the hooks given to `thread/start`:

```js
- export function codexBirthHookSpec({command}) {
-   if (!command) throw new Error('Codex hook command is required before thread/start');
-   const hook = {type: 'command', command, timeout: 30, async: false};
-   const hash = `sha256:${crypto.createHash('sha256').update(JSON.stringify(canonical({event_name: 'stop', hooks: [hook]}))).digest('hex')}`;
-   return {hook, hookKey: '/<session-flags>/config.toml:stop:0:0', hash};
- }
```

```js
-         config: {model_reasoning_effort: o.effort, 'features.hooks': true,
-           'hooks.Stop': [{hooks: [hooks.hook]}],
-           'hooks.state': {[hooks.hookKey]: {enabled: true, trusted_hash: hooks.hash}}}
```

File: `primary/config/main-flow/shared.edn`, inside its map; the event
names are each harness's own, and a command is the messenger's:

```clojure
+  :hooks {:claude [{:event "Stop"
+                    :command "turn-end"
+                    :timeout-s 30}
+                   {:event "UserPromptSubmit"
+                    :command "remind"
+                    :timeout-s 10}]
+          :codex [{:event "Stop"
+                   :command "turn-end"
+                   :timeout-s 30}]}
```

File: `messenger-clj/src/messenger_clj/launch.clj`, the one Stop hook
replaced by every hook of the harness:

```clojure
- ;; The hook's settings keys are the harness's
- ;; contract; bb runs the hook; the command names
- ;; the EDN file, the bootstrap pointer to the
- ;; configuration, under --config, the flag the
- ;; hook reads: its own contract with the command.
- (defn stop-hook [config config-file hook-file]
-   (let [timeout (get-in config [:refresh
-                                 :hook-timeout-s])]
-     {:hooks
-      {:Stop [{:hooks
-               [{:type "command"
-                 :command (str "bb " hook-file
-                               " --config "
-                               config-file)
-                 :timeout timeout}]}]}}))
+ ;; "command" is the harness's hook type; the
+ ;; messenger's own name runs its command; --config
+ ;; is the flag the commands read.
+ (defn hook-entry [config-file hook]
+   {:type "command"
+    :command (str "messenger-clj " (:command hook)
+                  " --config " config-file)
+    :timeout (:timeout-s hook)})
+
+ (defn hook-settings [config harness config-file]
+   (let [hooks (get-in config [:hooks harness])
+         entry #(hook-entry config-file %)]
+     {:hooks
+      (into {}
+            (for [[event group]
+                  (group-by :event hooks)]
+              [(keyword event)
+               [{:hooks (mapv entry group)}]]))}))
+
+ ;; Codex takes its hooks as thread-start config,
+ ;; one key per event; the key form is its own.
+ (defn codex-hook-config [settings]
+   (into {}
+         (for [[event hooks] (:hooks settings)]
+           [(str "hooks." (name event)) hooks])))
```

File: `primary/tools/main-flow-mode/reminder-hook.py`, removed whole:

```python
- #!/usr/bin/env python3
- """UserPromptSubmit hook: re-inject the main-flow-mode core every Nth prompt.
- 
- The core is the first five paragraphs of the replacing system prompt.  The
- prompt count is kept per native session, in the session's state directory:
- ``--state-dir`` when given, else ``$CLAUDE_JOB_DIR`` (the per-seat job
- directory the seat launcher exports).  A failure exits 1, which Claude Code
- treats as a non-blocking hook error: the living's prompt still goes through.
- """
- 
- import argparse
- import fcntl
- import json
- import os
- import pathlib
- import re
- import sys
- 
- PROMPT = pathlib.Path(__file__).resolve().with_name("system-prompt.md")
- SESSION = re.compile(r"^[A-Za-z0-9-]{8,128}$")
- PARAGRAPHS = 5
- 
- 
- def core(prompt_file: pathlib.Path) -> str:
-     paragraphs = [part.strip() for part in re.split(r"\n\s*\n", prompt_file.read_text()) if part.strip()]
-     if len(paragraphs) < PARAGRAPHS:
-         raise ValueError(f"main-flow prompt has fewer than {PARAGRAPHS} paragraphs: {prompt_file}")
-     return "\n\n".join(paragraphs[:PARAGRAPHS])
- 
- 
- def state_directory(given):
-     if given is not None:
-         return given
-     job = os.environ.get("CLAUDE_JOB_DIR")
-     if not job:
-         raise ValueError("no session state directory: pass --state-dir or export CLAUDE_JOB_DIR")
-     return pathlib.Path(job) / "main-flow-reminder"
- 
- 
- def count_prompt(state_dir: pathlib.Path, session_id: str) -> int:
-     if not SESSION.fullmatch(session_id or ""):
-         raise ValueError("hook input has an invalid native session_id")
-     state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
-     with (state_dir / f"{session_id}.count").open("a+", encoding="utf-8") as handle:
-         fcntl.flock(handle, fcntl.LOCK_EX)
-         handle.seek(0)
-         previous = handle.read().strip()
-         value = int(previous) + 1 if previous else 1
-         handle.seek(0)
-         handle.truncate()
-         handle.write(f"{value}\n")
-         handle.flush()
-         os.fsync(handle.fileno())
-         return value
- 
- 
- def main() -> int:
-     parser = argparse.ArgumentParser()
-     parser.add_argument("--prompt-file", type=pathlib.Path, default=PROMPT)
-     parser.add_argument("--state-dir", type=pathlib.Path)
-     parser.add_argument("--every", type=int, default=20)
-     args = parser.parse_args()
-     if args.every < 1:
-         raise ValueError("--every must be positive")
-     event = json.load(sys.stdin)
-     if event.get("hook_event_name") != "UserPromptSubmit":
-         raise ValueError("main-flow reminder only accepts UserPromptSubmit")
-     count = count_prompt(state_directory(args.state_dir), event.get("session_id", ""))
-     if count % args.every == 0:
-         print(json.dumps({"hookSpecificOutput": {
-             "hookEventName": "UserPromptSubmit",
-             "additionalContext": core(args.prompt_file),
-         }}))
-     return 0
- 
- 
- if __name__ == "__main__":
-     try:
-         raise SystemExit(main())
-     except Exception as error:
-         print(f"main-flow reminder failed: {error}", file=sys.stderr)
-         raise SystemExit(1)
```

File: `messenger-clj/src/messenger_clj/reminder.clj`, a new file, its
Clojure rewrite; the machine's design: every Nth prompt re-enters the
first paragraphs of one module, counted per session in the flow's
directory. Its data, `primary/config/main-flow/shared.edn`, inside its
map:

```clojure
+  :reminder {:every 20 :paragraphs 5
+             :module :intent-main-flow
+             :state "reminder"}
```

```clojure
+ (ns messenger-clj.reminder
+   (:require [babashka.fs :as fs]
+             [clojure.string :as str]
+             [messenger-clj.launch :as launch]))
+
+ ;; The event's keys and the reply's are the
+ ;; harness's hook contract.
+ (defn prompt-event? [event]
+   (= "UserPromptSubmit"
+      (:hook_event_name event)))
+
+ (defn count-file [config flow-dir session]
+   (fs/path flow-dir
+            (get-in config [:reminder :state])
+            session))
+
+ (defn read-count [file]
+   (if (fs/exists? file)
+     (parse-long (str/trim (slurp (str file))))
+     0))
+
+ (defn count-prompt! [file]
+   (let [n (inc (read-count file))]
+     (fs/create-dirs (fs/parent file))
+     (spit (str file) (str n))
+     n))
+
+ (defn due? [config n]
+   (zero? (mod n (get-in config
+                         [:reminder :every]))))
+
+ ;; A blank line is Markdown's own paragraph break.
+ (defn core [config]
+   (let [{:keys [module paragraphs]}
+         (:reminder config)
+         body (launch/module-block config module)]
+     (str/join "\n\n"
+               (take paragraphs
+                     (str/split body
+                                #"\n\s*\n")))))
+
+ (defn reply [text]
+   {:hookSpecificOutput
+    {:hookEventName "UserPromptSubmit"
+     :additionalContext text}})
+
+ (defn remind [config flow-dir event]
+   (when (prompt-event? event)
+     (let [file (count-file config flow-dir
+                            (:session_id event))]
+       (when (due? config (count-prompt! file))
+         (reply (core config))))))
```

File: `primary/config/main-flow/shared.edn`, inside its map, the
aspect file named from its aspect:

```clojure
+  :aspects {:file "%s.edn"}
```

File: `messenger-clj/src/messenger_clj/refresh.clj`, its requires and
the Stop command's entry; `:zone` and `:warned-at` are the state
record's own keys; `flow-of-thread`, `zone` and `used` are Proposal 1,
`flow-dir` and `state-file` Proposal 2, `step` and `messages`
Proposal 4 of «Flow: refresh and handover»:

```clojure
  (ns messenger-clj.refresh
    (:require [babashka.fs :as fs]
              [cheshire.core :as json]
              [clojure.edn :as edn]
              [clojure.string :as str]
+             [messenger-clj.launch :as launch]
              [messenger-clj.core :as hm]))
```

```clojure
+ (defn aspect-config [config aspect]
+   (let [file (format (get-in config
+                              [:aspects :file])
+                      (str/lower-case
+                       (name aspect)))]
+     (edn/read-string
+      (slurp (str (fs/path (:dir config) file))))))
+
+ ;; The event's keys are the harness's hook
+ ;; contract; the flow is the one registered on
+ ;; the thread; the window is its layer's row.
+ (defn turn-end! [config event]
+   (let [[flow route] (flow-of-thread
+                       (hm/route-records)
+                       (:session_id event))
+         ac (aspect-config config (:aspect route))
+         row (launch/layer-row
+              ac (keyword (:layer route)))
+         z (zone config (:window row)
+                 (used (:harness ac)
+                       (:transcript_path event)))
+         file (str (state-file
+                    config (flow-dir config flow)))
+         state (when (fs/exists? file)
+                 (edn/read-string (slurp file)))
+         now (System/currentTimeMillis)
+         action (step config z state now)]
+     (spit file
+           (pr-str (cond-> (assoc state :zone z)
+                     (= action :warn)
+                     (assoc :warned-at now))))
+     ;; send! without waiting, no pane named.
+     (doseq [[to text]
+             (messages config route flow action)]
+       (hm/send! to text false nil))))
```

File: `messenger-clj/src/messenger_clj/main.clj`, the `ns` form:

```clojure
  (ns messenger-clj.main
    (:require [messenger-clj.core :as hm]
              [messenger-clj.refresh :as refresh]
+             [messenger-clj.reminder :as reminder]
+             [babashka.fs :as fs]
+             [cheshire.core :as json]
+             [clojure.edn :as edn]
```

before `-main`:

```clojure
+ ;; A hook reads its event as JSON on stdin and
+ ;; answers as JSON on stdout: the harness's hook
+ ;; contract. --config names the EDN file, whose
+ ;; directory is the configuration's.
+ (defn hook-event! []
+   (json/parse-string (stdin-text!) true))
+
+ (defn hook-config [xs]
+   (unknown-flags! xs #{"--config"})
+   (extra-values! xs #{"--config"})
+   (let [file (arg xs "--config")]
+     (assoc (edn/read-string (slurp file))
+            :dir (str (fs/parent file)))))
+
+ ;; The flow's directory is found through the
+ ;; variable the launcher set.
+ (defn hook-flow-dir [config]
+   (refresh/flow-dir
+    config
+    (System/getenv
+     (get-in config [:environment :flow-id]))))
+
  (defn -main [& argv]
```

The dispatch, before `retire`:

```clojure
+           "remind"
+           (let [config (hook-config xs)]
+             (some-> (reminder/remind
+                      config
+                      (hook-flow-dir config)
+                      (hook-event!))
+                     json/generate-string
+                     println))
+           "turn-end"
+           (refresh/turn-end! (hook-config xs)
+                              (hook-event!))
            "retire" (let [[flow & rest] xs]
```

Ruling, one number from each group:

The line and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

The line's mark:
4. Short term, as shown: the launcher is the short-term tool (flow
   d68c82, 2026-10-13).
5. Unmarked.

### Proposal 8: spawning adapts to the harness

File: `psyche-context/skills/vision-flow.md`, «Starting flows», the
first paragraph as it stands, one sentence added after it.

Source: flow 6852f4, 2026-09-17.

```text
  A Nexus component decides the system prompt and everything about a
  launch, replacing the harness's subagents with specialized harnesses
  launched with specialized system prompts.
+
+ Flow knows which harness a flow runs in and what that harness can do; how a flow is spawned and spoken to takes the harness's own form.
```

The EDN of Proposals 5 and 7 is keyed by harness; `(:harness
aspect-config)` of `start-call`, Proposal 10, picks the key.

Ruling:

1. Land.
2. Land with changes the living names.
3. Drop.

### Proposal 9: the pane is bound before messaging is trusted

File: `psyche-context/skills/vision-flow.md`, under «Short term»
(Proposal 5), after Proposal 7's line.

Sources: flow f38926, 2026-09-20, relayed by Field, the wording the
relay's, not established as his; flow d68c82, 2026-10-13.

```text
+ Short term: every new or refreshed flow starts in a Herdr pane, and the launcher registers it with the messenger only once the pane's agent is seen bound to the flow's session.
```

File: `primary/tools/claude-main-flow-launch.mjs`, the wait written as
a poll:

```js
-     await poll('an agent bound to the session', 180, () => {
-       const a = herdr(o.herdrSession, 'agent', 'get', name).agent;
-       return hasExactRegistrationBinding(a, paneId, sessionId);
-     });
```

File: `primary/config/main-flow/shared.edn`, inside its map:

```clojure
+  :binding-wait-ms 5000
```

File: `messenger-clj/src/messenger_clj/launch.clj`; `read-agent` reads
the pane's agent from Herdr, `register!` is the messenger's
registration; the record's keys are Herdr's own; `PaneUnbound` is the
refusal's own name:

```clojure
+ (defn bound? [agent pane thread]
+   (and (= pane (:pane_id agent))
+        (= thread (get-in agent [:agent_session
+                                 :value]))))
+
+ (defn register-when-bound! [config read-agent pane
+                             thread register!]
+   (Thread/sleep (:binding-wait-ms config))
+   (if (bound? (read-agent) pane thread)
+     (register!)
+     (throw (ex-info "PaneUnbound"
+              {:pane pane :thread thread}))))
```

Ruling, one number from each group:

The line:
1. Land.
2. Land with changes the living names.
3. Drop.

The wait:
4. One check after a set wait, as shown, the machine's design: polling
   is forbidden by the paragraph above.
5. The poll stays, registered and reported as a poller.

The line's mark:
6. Short term, as shown: the launcher is the short-term tool (flow
   d68c82, 2026-10-13).
7. Unmarked.

### Proposal 10: one central Start call and its shorthands

File: `psyche-context/skills/vision-flow.md`, «Starting flows», after
Proposal 5's paragraph.

A shorthand: a preconfigured call that fills most of the central call's
settings, so a launch names little.

Sources: flow e51411, 2026-09-25; flow fd0f97, 2026-09-15; flow
ebbe30, 2026-10-09; flow d68c82, 2026-10-13.

```text
+ Flow's start is one central call carrying every setting of a launch; a shorthand fills most of it from a declared flow, so that a launch asks little of whoever starts it, and the simple command the living remembers is a shorthand. Every main feature has this shape: one central call and its shorthands.
```

Under choice 4 the last sentence goes instead to
`psyche-context/skills/vision-design.md`, a new section at the end:

```text
+ ## One central call and its shorthands
+
+ Every main feature has one central call carrying every setting, and shorthands: preconfigured minimal calls that fill most of it.
```

File: `primary/tools/claude-main-flow-launch.mjs`, the arguments a
launch names:

```js
-   const known = new Set(['--model', '--brief', '--aspect', '--layer', '--workspace', '--herdr-session', '--herdr-workspace-label', '--system-prompt-file', '--effort', '--predecessor', '--metaflow', '--topic']);
```

File: `primary/config/main-flow/shared.edn`, inside its map; a
shorthand is a metaflow file, named from its address; the keys a launch
takes from its metaflow are data:

```clojure
+  :metaflows {:dir "metaflow"
+              :file "%s-%s-%s.edn"}
+  :start-call {:metaflow-keys
+               [:aspect :topic :layer :mode]}
```

File: `messenger-clj/src/messenger_clj/launch.clj`, its requires:

```clojure
  (ns messenger-clj.launch
-   (:require [clojure.string :as str]
+   (:require [babashka.fs :as fs]
+             [clojure.edn :as edn]
+             [clojure.string :as str]
              [clojure.java.shell :refer [sh]]
              [malli.core :as m]))
```

and after `layer-row`; `effort!` is Proposal 11, `tools` is
Proposal 6; `asked` is what the call itself names:

```clojure
  (defn layer-row [aspect-config layer]
    (or (some #(when (= layer (:layer %)) %)
              (:layers aspect-config))
        (throw (ex-info "UnknownLayer"
                        {:layer layer}))))
+
+ (defn start-call [config aspect-config mf asked]
+   (let [row (layer-row aspect-config (:layer mf))
+         keys (get-in config [:start-call
+                              :metaflow-keys])]
+     (merge (select-keys mf keys)
+            {:harness (:harness aspect-config)
+             :model (:model row)
+             :effort (effort! row (:effort asked))
+             :tools (tools config mf)}
+            (dissoc asked :effort))))
+
+ (defn metaflow-file [config address]
+   (let [{:keys [dir file]} (:metaflows config)
+         {:keys [aspect topic layer]} address
+         parts (map name [aspect topic layer])]
+     (fs/path (:dir config) dir
+              (apply format file parts))))
+
+ (defn shorthand [config address]
+   (edn/read-string
+    (slurp (str (metaflow-file config address)))))
```

A metaflow file is named from its address, the topic uncapitalized
(Proposal 1), so the five files are renamed, each as it stands after
Proposals 1, 4 and 6.

File: `primary/config/main-flow/metaflow/Psyche-Flow-Primary.edn`:

```clojure
- {:aspect :Psyche :topic :flow :layer :Primary
-  :mode :design
-  :tools :book-publisher
-  :secondary-native-id
-  "da203818-26b4-4a15-9de8-faeb1e7d23cd"
-  :modules
-  {:system [:spirit-core :intent-main-flow
-            :vision-book
-            :compensation-book-crystallization]
-   :user [:compensation-main-flow]}}
```

File: `primary/config/main-flow/metaflow/Psyche-flow-Primary.edn`:

```clojure
+ {:aspect :Psyche :topic :flow :layer :Primary
+  :mode :design
+  :tools :book-publisher
+  :secondary-native-id
+  "da203818-26b4-4a15-9de8-faeb1e7d23cd"
+  :modules
+  {:system [:spirit-core :intent-main-flow
+            :vision-book
+            :compensation-book-crystallization]
+   :user [:compensation-main-flow]}}
```

File: `primary/config/main-flow/metaflow/Psyche-Flow-Secondary.edn`:

```clojure
- {:aspect :Psyche :topic :flow :layer :Secondary
-  :mode :design
-  :modules
-  {:system [:spirit-core :intent-main-flow
-            :vision-book
-            :compensation-book-crystallization]
-   :user [:compensation-main-flow]}}
```

File: `primary/config/main-flow/metaflow/Psyche-flow-Secondary.edn`:

```clojure
+ {:aspect :Psyche :topic :flow :layer :Secondary
+  :mode :design
+  :modules
+  {:system [:spirit-core :intent-main-flow
+            :vision-book
+            :compensation-book-crystallization]
+   :user [:compensation-main-flow]}}
```

File: `primary/config/main-flow/metaflow/Psyche-Core-Primary.edn`:

```clojure
- {:aspect :Psyche :topic :core :layer :Primary
-  :mode :design
-  :modules {:system [:intent-psyche-interaction]
-            :user []}}
```

File: `primary/config/main-flow/metaflow/Psyche-core-Primary.edn`:

```clojure
+ {:aspect :Psyche :topic :core :layer :Primary
+  :mode :design
+  :modules {:system [:intent-psyche-interaction]
+            :user []}}
```

File: `primary/config/main-flow/metaflow/Mind-Core-Primary.edn`:

```clojure
- {:aspect :Mind :topic :core :layer :Primary
-  :mode :design
-  :modules {:system [:intent-psyche-interaction]
-            :user []}}
```

File: `primary/config/main-flow/metaflow/Mind-core-Primary.edn`:

```clojure
+ {:aspect :Mind :topic :core :layer :Primary
+  :mode :design
+  :modules {:system [:intent-psyche-interaction]
+            :user []}}
```

File: `primary/config/main-flow/metaflow/Field-Core-Primary.edn`:

```clojure
- {:aspect :Field :topic :core :layer :Primary
-  :mode :design
-  :modules {:system [:intent-psyche-interaction]
-            :user []}}
```

File: `primary/config/main-flow/metaflow/Field-core-Primary.edn`:

```clojure
+ {:aspect :Field :topic :core :layer :Primary
+  :mode :design
+  :modules {:system [:intent-psyche-interaction]
+            :user []}}
```

File: `psyche-context/skills/vision-flow.md`, the figure, under
«Short term» (Proposal 5), after Proposal 9's line:

```text
+ +--------------------------------------+
+ | the EDN: shared, per aspect,         |
+ | per metaflow                         |
+ +--------------------------------------+
+         | fills
+         v
+ +--------------------------------------+
+ | the Start call, or its shorthand     |
+ +--------------------------------------+
+         | claims
+         v
+ +--------------------------------------+
+ | the flow id and its directory        |
+ +--------------------------------------+
+         | precedes
+         v
+ +--------------------------------------+
+ | the secretary, if a Primary starts   |
+ +--------------------------------------+
+         | precedes
+         v
+ +--------------------------------------+
+ | a Herdr pane, on main                |
+ +--------------------------------------+
+         | runs
+         v
+ +--------------------------------------+
+ | the harness, remote control on,      |
+ | permissions off, hooks installed     |
+ +--------------------------------------+
+         | receives
+         v
+ +--------------------------------------+
+ | one block: id, mode, modules, brief  |
+ +--------------------------------------+
+         | is bound, then registered with
+         v
+ +--------------------------------------+
+ | the messenger                        |
+ +--------------------------------------+
+         | precedes
+         v
+ +--------------------------------------+
+ | the first response: a presentation   |
+ +--------------------------------------+
```

Ruling, one number from each group:

The paragraph, the figure and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

The general sentence:
4. In vision-design, as a shape of every feature, the machine's
   suggestion: he asked for the pattern to be got out into a vision
   (flow e51411, 2026-09-25).
5. In vision-flow only, as shown, the machine's design: the pattern
   was spoken of the Flow tool.

### Proposal 11: a launch takes what is declared

File: `psyche-context/skills/vision-flow.md`, «Starting flows», after
Proposal 10's paragraph.

Source: flow e71dab, 2026-09-26.

```text
+ Every flow that may be started is declared in Flow's configuration with its model and effort, and a launch takes what is declared: an effort no declared flow uses is refused, as is a second flow on one role. What is added to a flow's prompt comes from files, named in that declaration.
```

File: `primary/tools/native-voice-profiles.mjs`, the check in code:

```js
-   if (effort !== undefined && effort !== profile.effort) throw new Error(`voice effort differs for ${key}: required ${profile.effort}, received ${effort}`);
```

File: `messenger-clj/src/messenger_clj/launch.clj`, before
`start-call`; `EffortNotDeclared` is the refusal's own name:

```clojure
+ ;; A declared effort is the only one; a differing
+ ;; request is refused, never taken.
+ (defn effort! [row effort]
+   (when (and effort (not= effort (:effort row)))
+     (throw (ex-info "EffortNotDeclared"
+                     {:asked effort
+                      :declared (:effort row)})))
+   (:effort row))
```

Ruling:

1. Land.
2. Land with changes the living names.
3. Drop.

### Proposal 12: every boss its secretary

File: `psyche-context/skills/vision-flow.md`, «Starting flows», after
Proposal 11's paragraph.

The secretary: the Secondary of the same aspect and topic as a Primary.

Source: flow ee57fb, 2026-10-12.

```text
+ A Primary is never without its Secondary: starting a Primary first starts the Secondary of its metaflow, and a Primary found running without one has it started.
```

File: `primary/tools/secondary-first.mjs`, the running Secondaries
written in code:

```js
- export const DECLARED_SECONDARIES = Object.freeze([
-   {aspect: 'Mind', topic: 'Core', layer: 'Secondary', flowId: '41fa34', name: 'mind_sol_41fa34', nativeId: '01a0fdcc-c1a1-7f43-8c23-06d41fa34438'},
-   {aspect: 'Field', topic: 'Core', layer: 'Secondary', flowId: '42265e', name: 'field_sol_42265e', nativeId: '01a0fdcc-4e82-7353-af14-d6c42265e940'}
- ]);
```

File: `primary/config/main-flow/metaflow/Psyche-flow-Primary.edn`, the
Secondary's native id written in the metaflow file:

```clojure
  {:aspect :Psyche :topic :flow :layer :Primary
   :mode :design
   :tools :book-publisher
-  :secondary-native-id
-  "da203818-26b4-4a15-9de8-faeb1e7d23cd"
   :modules
```

File: `messenger-clj/src/messenger_clj/launch.clj`, its requires:

```clojure
+             [messenger-clj.core :as core]
+             [messenger-clj.metaflow :as mf]
+             [messenger-clj.typed-store :as store]
+             [pod.huahaiy.datalevin :as d]
```

and after `shorthand`; `start!` is the start of Proposal 10, given the
brief of Proposal 3; a metaflow's name in the registry is the
messenger's own, aspect, topic and layer joined by spaces:

```clojure
+ (defn metaflow-name [address]
+   (str/join " " (map #(name (get address %))
+                      [:aspect :topic :layer])))
+
+ (defn current [address]
+   (store/with-db (core/root)
+     #(mf/current (d/db %)
+                  (metaflow-name address))))
+
+ ;; :Primary and :Secondary are the layers' own
+ ;; names.
+ (defn secretary [address]
+   (assoc address :layer :Secondary))
+
+ (defn ensure-secretary! [config address start!]
+   (when (= :Primary (:layer address))
+     (let [sec (secretary address)
+           path [:secretary :brief]]
+       (or (current sec)
+           (start! sec (get-in config path))))))
```

Ruling, one number from each group:

The sentence and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

Who finds a Primary left without its Secondary later:
4. No one yet; the launcher checks at the Primary's start only, as
   shown, the machine's design: the record speaks of the start.
5. The hook of Proposal 7, at the end of each of the Primary's turns,
   the machine's suggestion: a Primary found running without one is
   found at a turn's end.

### Proposal 13: a Primary is launched on main

File: `psyche-context/skills/vision-flow.md`, «Starting flows», after
Proposal 12's sentence.

Source: flow 9993b5, 2026-09-17.

```text
+ A Primary is launched in the shared workspace on main, not in a worktree or on a branch, unless the launch names another place.
```

Under choice 5 the sentence begins «Every flow is launched».

File: `primary/tools/claude-main-flow-launch.mjs`, `parseArgs`, the
place written in code:

```js
-   const o = {aspect: 'Psyche', effort: undefined, model: undefined, workspace: '/home/li/primary', herdrSession: 'default', herdrWorkspaceLabel: undefined, composeOnly: false, systemPromptFile: undefined, root: false, predecessor: undefined, metaflow: undefined, topic: undefined};
```

File: `primary/tools/codex-main-flow-launch.mjs`, `parseArgs`:

```js
-   const o = {aspect: 'Mind', effort: undefined, model: undefined, workspace: '/home/li/primary', herdrSession: 'default', herdrWorkspaceLabel: undefined, composeOnly: false, root: false, predecessor: undefined, metaflow: undefined, topic: undefined};
```

File: `primary/config/main-flow/shared.edn`, inside its map:

```clojure
+  :workspace {:path "/home/li/primary"
+              :branch "main"}
```

File: `messenger-clj/src/messenger_clj/launch.clj`;
`WorkspaceOffBranch` is the refusal's own name:

```clojure
+ ;; git's own words for the current branch.
+ (defn branch [path]
+   (str/trim (:out (sh "git" "-C" path "rev-parse"
+                       "--abbrev-ref" "HEAD"))))
+
+ (defn workspace! [config layer]
+   (let [{:keys [path] wanted :branch}
+         (:workspace config)
+         on (branch path)]
+     (when (and (= layer :Primary)
+                (not= wanted on))
+       (throw (ex-info "WorkspaceOffBranch"
+                       {:path path :branch on})))
+     path))
```

Ruling, one number from each group:

The sentence and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

Whom it binds:
4. Primaries (flow 9993b5, 2026-09-17), as shown.
5. Every flow, the machine's design: the workspace is one, and a lower
   flow on a branch would edit what its Primary does not see.

### Proposal 14: who may restart a flow

File: `psyche-context/skills/vision-flow.md`, «Starting flows», after
Proposal 13's sentence.

Provenance: the flows a flow came from, the one that asked for it among
them, the `:origin` of its `continuation.edn`.

Source: flow 9993b5, 2026-09-17.

```text
+ A flow is restarted by a command to Flow; a request whose flow id matches the flow's provenance carries all the authority needed. A harness that locks itself out of relaunching its own flow is a design defect.
```

File: `messenger-clj/src/messenger_clj/core.clj`, `pane-flow!`, the
caller found from the pane the command is typed in, never declared:

```clojure
  (defn pane-flow! []
    (let [pane (or (System/getenv "HERDR_PANE_ID")
                   (fail "CallerUnknown"))
          hits (for [[id route] (route-records)
                     :when (= pane
                              (:pane_id route))]
                 id)]
      (if (= 1 (count hits))
        (first hits)
        (fail (str "CallerUnknown: " pane)))))
```

File: `messenger-clj/src/messenger_clj/launch.clj`; `continuation.edn`
is the name of the file that holds a flow's origin, the pointer to that
data, so it stays in the code; `RestartRefused` is the refusal's own
name:

```clojure
+ (defn continuation [root flow]
+   (edn/read-string
+    (slurp (str (fs/path root flow
+                         "continuation.edn")))))
+
+ (defn provenance [root flow]
+   #{flow (get-in (continuation root flow)
+                  [:origin :flow])})
+
+ (defn restart! [root flow caller start!]
+   (if (contains? (provenance root flow) caller)
+     (start! flow)
+     (throw (ex-info "RestartRefused"
+              {:flow flow :caller caller}))))
+
+ (defn restart-from-pane! [root flow start!]
+   (restart! root flow (core/pane-flow!) start!))
```

Ruling, one number from each group:

The sentences and the code:
1. Land.
2. Land with changes the living names.
3. Drop.

What matches a flow's provenance:
4. The flow itself and the flow that asked for it, as shown, the
   machine's design: both are in the flow's own record.
5. The flow itself only, the machine's suggestion: the record names
   one id.
6. Any flow of the same metaflow, the machine's suggestion: the
   metaflow's lineage is one line.
<!-- to-the-living:end -->
