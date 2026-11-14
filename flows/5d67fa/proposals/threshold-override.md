Presentation.{ «A flow's own threshold, and a warning it cannot miss» Proposal }

# A flow's own threshold, and a warning it cannot miss

Created by Fable 5.2, on the living's words of 2026-11-09.

### Proposal 1: The threshold and its warning · psyche-belief › vision/flow-nexus-v1.md

::: comment
Two changes. A member may carry its own threshold, the model's being the default. And the warning to write the handover arrives at the flow's next tool boundary, so a flow in a long working cycle receives it while it works; a model does not know the size of its own context, so the Flow Nexus, which learns it from the harness's hooks, is what tells it.
:::

- It is warned when its context reaches the Warning share of its model's threshold, configured per model in the Flow Nexus: a HardAbrupt Notice naming its handover path, `flows/<id>/handover.md`.
+ Its threshold is its model's, configured per model in the Flow Nexus, unless its own definition names one. A flow does not know the size of its context: the Flow Nexus learns it from each hook, while the flow works as well as when it rests, and warns the flow when it reaches the Warning share: a MiddleAbrupt Notice naming its handover path, `flows/<id>/handover.md`, which reaches a working flow at its next tool boundary.

- ```ethos
-   Intake.Integer                       ; the most characters a message to this member carries
-   Member.{ FlowName HarnessName ModelName Effort
-            Continuity Workspace Beliefs Tools
-            Features.Vector<FeatureName>  ; of its harness, composed into its launch beside its complex's
-            Intake
-            Vector<Route> }
-   Threshold.{ Model.String Tokens.Integer
-               Warning.Integer }        ; share left, 20
- ```

+ ```ethos
+   Intake.Integer                       ; the most characters a message to this member carries
+   Mark.{ Tokens.Integer                ; the context size at which the flow is refreshed
+          Warning.Integer }             ;   the share left at which it is warned, 20
+   Member.{ FlowName HarnessName ModelName Effort
+            Continuity Workspace Beliefs Tools
+            Features.Vector<FeatureName>  ; of its harness, composed into its launch beside its complex's
+            Intake
+            Option<Mark>                  ; its own threshold; None takes its model's
+            Vector<Route> }
+   Threshold.{ Model.String Mark }      ; the default for every flow of that model
+ ```

+ ```datom
+ ; the model's default, set over the meta surface
+ Configure.Threshold.{ claude-fable-5-2 { 300000 20 } }
+ ; a member that takes it, and one with its own
+ { fable claude claude-fable-5-2 Medium Permanent Path.«/home/li/primary» … 1200 None [ Living ] }
+ { bookmaker claude claude-sonnet-5-5 Medium Permanent Temporary … 40000 Some.{ 120000 30 } [] }
+ ; the warning, as the flow receives it at its next tool boundary
+ MiddleAbrupt.Notice.«Write your handover at flows/f54886/handover.md»
+ ```
