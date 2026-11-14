Presentation.{ «A declaration names the model; the Nexus resolves its version» Proposal }

# A declaration names the model; the Nexus resolves its version

Created by Fable 5.2, on the evidence of Psyche core Opus.

### Proposal 1: The latest version, unless pinned · psyche-belief › vision/model-roles.md

::: comment
You want the latest model always, unless a situation pins one. Today a declaration writes the version literally, so every new version is an edit of every row. With this, a row says fable and stays true through every version.
:::

  ## One declaration sets the model everywhere

  The model is declared once, in the metaflow definition the Flow Nexus
  runs, in datom.

+ A declaration names the model by its name, and the flow runs the latest version of it that its harness offers. A pin is a version written in the declaration, for the one member a situation holds back.

+ ```mermaid
+ flowchart TB
+     d["a member's declaration"] -- "names" --> n["the model, by name: fable"]
+     h["the harness definition"] -- "offers, for each name" --> v["its latest version"]
+     n -- "is resolved at launch to" --> v
+     d -- "may pin" --> p["one version, written whole"]
+     p -- "is launched as written, in place of" --> v
+ ```

### Proposal 2: The types of a model choice · psyche-belief › vision/flow-nexus-v1.md

::: comment
The harness definition is where the versions live, because the harness is what offers them: when a harness is updated, its definition is replaced with the versions it now offers, and that replacement is the event. A running permanent flow takes the new version at its next refresh. Every member row in the module takes the form of the row shown here; thresholds are kept by model name, so a new version inherits its model's threshold.
:::

- A harness is a definition like a metaflow: its name, its features, and each feature's effect on the launch, a flag or a variable;
+ A harness is a definition like a metaflow: its name, its features, each feature's effect on the launch, a flag or a variable, and its offers, the latest version it runs of each model it has;

+ A member names its model by name. At launch the Nexus resolves the name to the version its harness offers, or launches the pinned version as written; a name the harness does not offer refuses the launch, with the harness and the name. A permanent flow's successor is resolved anew, so a flow takes a new version at its refresh.

- ```ethos
-   ModelName.String
-   Harness.{ HarnessName               ; a definition, as a metaflow is
-             Features.Vector<Feature> }
-   Member.{ FlowName HarnessName ModelName Effort
- ```

+ ```ethos
+   ModelName.String                    ; the model, by name: fable
+   ModelVersion.String                 ; the harness's own identifier of one version: claude-fable-5-2
+   Offer.{ ModelName ModelVersion }    ; the latest version a harness runs of that model
+   Version.[ Latest                    ; resolved at launch from the harness's offers
+             Pinned.ModelVersion ]     ;   launched as written
+   Harness.{ HarnessName               ; a definition, as a metaflow is
+             Features.Vector<Feature>
+             Offers.Vector<Offer> }    ; replaced whole when the harness is updated
+   Member.{ FlowName HarnessName ModelName Version Effort
+ ```

- ```ethos
-             Unenforceable.HarnessName     ; Restricted, harness cannot
- ```

+ ```ethos
+             Unenforceable.HarnessName     ; Restricted, harness cannot
+             Unoffered.{ HarnessName ModelName } ; the member's model, absent from its harness's offers
+ ```

- ```ethos
-   Settings.{ HarnessName Tools Model.String } ] ; what the translator writes
-   Threshold.{ Model.String Tokens.Integer
-               Warning.Integer }        ; share left, 20
- ```

+ ```ethos
+   Settings.{ HarnessName Tools ModelVersion } ] ; what the translator writes: the version resolved
+   Threshold.{ ModelName Tokens.Integer  ; kept by name, for every version of the model
+               Warning.Integer }        ; share left, 20
+ ```

- ```datom
- { fable claude claude-fable-5-1 Medium
-   Permanent Path.«/home/li/primary»
- ```

+ ```datom
+ ; the harness, with what it offers now
+ Define.Harness.{
+    claude
+    [ { Bash
+        Flag.«--disallowedTools Bash» } ]
+    [ { fable claude-fable-5-2 }
+      { opus claude-opus-4 }
+      { sonnet claude-sonnet-5-5 }
+      { haiku claude-haiku-4-5 } ] }
+ ; a member on the latest, and one pinned
+ { fable claude fable Latest Medium
+   Permanent Path.«/home/li/primary»
+   … }
+ { opus claude opus Pinned.claude-opus-4 Medium
+   Ephemeral Temporary
+   … }
+ ; the launch, resolved
+ Rehearse.{ designer fable «Read the version one book» }
+ Rehearsed.«herdr --session main agent start … -- --system-prompt-file /…/bundle --model claude-fable-5-2 --effort medium»
+ ; a model the harness does not offer
+ Refused.Unoffered.{ claude terra }
+ ```
