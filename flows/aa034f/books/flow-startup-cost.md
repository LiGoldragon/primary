<!-- to-the-living:start -->
Presentation.{ «Flow Startup Cost» }

# Flow Startup Cost

### Proposal 1: signal-flow › ethos/signal.ethos

**Comment** Four tools a flow never needs have no leave-out name. Each gets one; the generated Rust is regenerated from this file.

```
+----------------------------------------------+
| flow start                                   |
+----------------------------------------------+
        | sends
        v
+----------------------------------------------+
| first turn  ~50k tokens                      |
+----------------------------------------------+
   | carries   | carries   | carries  | carries
   v           v           v          v
+--------+ +----------+ +--------+ +-----------+
| tools  | | modules  | | system | | reminders |
| 22.8k  | | 20.3k    | | 4.6k   | | 2k        |
+--------+ +----------+ +--------+ +-----------+
```

```
+----------------------------------------------+
| first turn now  ~50k                         |
+----------------------------------------------+
        | leaves out 3 tools  -4.2k
        v
+----------------------------------------------+
| ~46k                                         |
+----------------------------------------------+
        | leaves out protos, datom  -3.5k
        v
+----------------------------------------------+
| ~42k  seat that publishes                    |
+----------------------------------------------+
        | leaves out Artifact  -15.3k
        v
+----------------------------------------------+
| ~27k  seat that never publishes              |
+----------------------------------------------+
```

- LeaveOut.[ ClaudeAiConnectors ConfiguredMcpServers AgentTool ExplorePlanAgents FileTools WorkflowTool ScheduleWakeupTool ReportFindingsTool ListAgentsTool CronTools WebTools DeferredTools SkillTool BundledSkills ClaudeMd GitInstructions AttributionReminder UserSettings ToolSearch BashTool CodexSkillListing CodexAgentsMd CodexCollaborationMode CodexEnvironmentContext CodexPermissions CodexDeveloperInstructions ]
+ LeaveOut.[ ClaudeAiConnectors ConfiguredMcpServers
+    AgentTool ExplorePlanAgents FileTools
+    WorkflowTool ScheduleWakeupTool
+    ReportFindingsTool ListAgentsTool CronTools
+    WebTools DeferredTools SkillTool
+    BundledSkills ClaudeMd GitInstructions
+    AttributionReminder UserSettings ToolSearch
+    BashTool ArtifactTool FeedbackTool AskTool
+    NoticeTool CodexSkillListing CodexAgentsMd
+    CodexCollaborationMode
+    CodexEnvironmentContext CodexPermissions
+    CodexDeveloperInstructions ]

Ruling: land, amend, or reject.

### Proposal 2: flow › crates/flow-nexus/src/lean.rs

**Comment** Each new leave-out turns into the tool it names in `--disallowedTools`; the variants belong to Claude by the existing default.

+ const LEFT_OUT: [(LeaveOut, &[&str]); 4] = [
+     (LeaveOut::ArtifactTool, &["Artifact"]),
+     (LeaveOut::FeedbackTool, &["SendFeedback"]),
+     (LeaveOut::AskTool, &["AskUserQuestion"]),
+     (LeaveOut::NoticeTool, &["ReadNotifications"]),
+ ];
+
+ fn table_tools(out: &LeaveOut) -> &'static [&'static str] {
+     LEFT_OUT
+         .iter()
+         .find(|(known, _)| known == out)
+         .map_or(&[], |(_, names)| *names)
+ }
+
                  LeaveOut::SkillTool => &["Skill"],
-                 _ => &[],
+                 other => table_tools(other),

Ruling: land, amend, or reject.

### Proposal 3: primary › config/main-flow/shared.edn

**Comment** Every Claude seat goes without the three tools no flow uses. Artifact stays out of this default; a seat that never publishes names it in its own row.

-  :leave-outs {:claude [:ClaudeAiConnectors :ExplorePlanAgents :WorkflowTool :SkillTool :BundledSkills :ScheduleWakeupTool :ReportFindingsTool :ListAgentsTool :CronTools :DeferredTools :ClaudeMd :GitInstructions]
+  :leave-outs {:claude [:ClaudeAiConnectors
+                        :ExplorePlanAgents :WorkflowTool
+                        :SkillTool :BundledSkills
+                        :ScheduleWakeupTool
+                        :ReportFindingsTool
+                        :ListAgentsTool :CronTools
+                        :DeferredTools :ClaudeMd
+                        :GitInstructions
+                        :FeedbackTool :AskTool
+                        :NoticeTool]
               :codex [...]

Ruling: land, amend, or reject.

### Proposal 4: primary › tools/main-flow-mode/launch-config.mjs

**Comment** The shared leave-outs are read by no launcher today; a metaflow without its own row sends none, and Flow's store keeps defaults only for the Addresses it lists. The shared list becomes the fallback for the harness the seat runs.

  const metaflow = {metaflows: [...]};
+ const harnessOf = row => row.voice?.harness ??
+   aspects.find(a => a.aspect === row.aspect).harness;
+ for (const row of metaflow.metaflows) {
+   row['leave-outs'] ??=
+     shared['leave-outs'][harnessOf(row)];
+ }
  validateLaunchConfig({shared, aspects, metaflow});

Ruling: land, amend, or reject.

### Proposal 5: primary › tools/flow-start-adapter.mjs

**Comment** The adapter refuses any leave-out name it does not list; the four new names are listed.

  const LEAVE_OUTS = new Set('...'.split(' '));
+ for (const name of ['ArtifactTool', 'FeedbackTool',
+                     'AskTool', 'NoticeTool'])
+   LEAVE_OUTS.add(name);

Ruling: land, amend, or reject.

### Proposal 6: primary › config/main-flow/psyche.edn

**Comment** The data-format and prototype knowledge goes to the roles that write ethos (Proposals 8 and 9).

- :user [:compensation-book :compensation-behavior :compensation-correction :knowledge-vocabulary :knowledge-psyche :inquiry-psyche-crystallization :vision-crystallization :compensation-psyche-interraction :knowledge-orchestrate :compensation-edit-coordination :compensation-main-flow :compensation-truth :compensation-orders :compensation-prose :compensation-understanding :vision-aspects :vision-model-roles :compensation-launch :compensation-design :compensation-default-effort :knowledge-protos :knowledge-datom :vision-messaging :compensation-messenger-clj :compensation-network-temporary :compensation-temporary]
+ :user [:compensation-book :compensation-behavior
+        :compensation-correction
+        :knowledge-vocabulary :knowledge-psyche
+        :inquiry-psyche-crystallization
+        :vision-crystallization
+        :compensation-psyche-interraction
+        :knowledge-orchestrate
+        :compensation-edit-coordination
+        :compensation-main-flow :compensation-truth
+        :compensation-orders :compensation-prose
+        :compensation-understanding :vision-aspects
+        :vision-model-roles :compensation-launch
+        :compensation-design
+        :compensation-default-effort
+        :vision-messaging :compensation-messenger-clj
+        :compensation-network-temporary
+        :compensation-temporary]

Ruling: land, amend, or reject.

### Proposal 7: primary › config/main-flow/mind.edn

- :user [:compensation-behavior :compensation-correction :knowledge-vocabulary :knowledge-psyche :inquiry-psyche-crystallization :vision-crystallization :compensation-psyche-interraction :knowledge-orchestrate :compensation-edit-coordination :compensation-main-flow :compensation-truth :compensation-orders :compensation-prose :compensation-understanding :vision-aspects :vision-model-roles :compensation-launch :compensation-design :compensation-default-effort :knowledge-protos :knowledge-datom :vision-messaging :compensation-messenger-clj :compensation-network-temporary :compensation-temporary]
+ :user [:compensation-behavior
+        :compensation-correction
+        :knowledge-vocabulary :knowledge-psyche
+        :inquiry-psyche-crystallization
+        :vision-crystallization
+        :compensation-psyche-interraction
+        :knowledge-orchestrate
+        :compensation-edit-coordination
+        :compensation-main-flow :compensation-truth
+        :compensation-orders :compensation-prose
+        :compensation-understanding :vision-aspects
+        :vision-model-roles :compensation-launch
+        :compensation-design
+        :compensation-default-effort
+        :vision-messaging :compensation-messenger-clj
+        :compensation-network-temporary
+        :compensation-temporary]

Ruling: land, amend, or reject.

### Proposal 8: primary › config/main-flow/metaflow/Psyche-Ethos-Secondary.edn

  :raw-psyche-paths ["flows/081064/vision/ethos.md" "flows/23824a/vision/"]
+ :user-modules [:knowledge-protos :knowledge-datom]

Ruling: land, amend, or reject.

### Proposal 9: primary › config/main-flow/metaflow/Psyche-Ethos-Primary.edn

  :raw-psyche-paths ["flows/081064/vision/ethos.md" "flows/23824a/vision/"]
+ :user-modules [:knowledge-protos :knowledge-datom]

Ruling: land, amend, or reject.

### Proposal 10: primary › config/main-flow/metaflow/Mind-ethos-Secondary.edn

**Comment** The topic vision is read by path when its question arises; the launch brief names the path. The ethos role keeps the two knowledge modules.

- :modules [] :user-modules [:vision-ethos]
+ :modules [] :user-modules [:knowledge-protos :knowledge-datom]

Ruling: land, amend, or reject.

### Proposal 11: primary › config/main-flow/metaflow/Mind-nexus-Secondary.edn

- :modules [] :user-modules [:vision-nexus]
+ :modules []

Ruling: land, amend, or reject.

### Proposal 12: primary › config/main-flow/metaflow/Mind-flow-Secondary.edn

- :modules [] :user-modules [:vision-flow]
+ :modules []

Ruling: land, amend, or reject.

### Proposal 13: primary › config/main-flow/metaflow/Field-Illustrator-Tertiary.edn

**Comment** The illustrator returns an SVG and never publishes; its row replaces the shared list with the same list and Artifact added.

  :layer :Tertiary
+ :leave-outs [:ClaudeAiConnectors :ExplorePlanAgents
+              :WorkflowTool :SkillTool :BundledSkills
+              :ScheduleWakeupTool :ReportFindingsTool
+              :ListAgentsTool :CronTools :DeferredTools
+              :ClaudeMd :GitInstructions
+              :FeedbackTool :AskTool :NoticeTool
+              :ArtifactTool]

Ruling: land, amend, or reject.

### Proposal 14: primary › config/main-flow/metaflow/Psyche-Flow-Secondary.edn

**Comment** The same Artifact leave-out for a Psyche main flow, which publishes today through a book subagent. With it the book goes through Field Publisher Quaternary. Whether `--disallowedTools` also reaches a subagent is not witnessed.

  :aspect :Psyche :topic :Flow :layer :Secondary
+ :leave-outs [:ClaudeAiConnectors :ExplorePlanAgents
+              :WorkflowTool :SkillTool :BundledSkills
+              :ScheduleWakeupTool :ReportFindingsTool
+              :ListAgentsTool :CronTools :DeferredTools
+              :ClaudeMd :GitInstructions
+              :FeedbackTool :AskTool :NoticeTool
+              :ArtifactTool]

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
