Presentation.{ «A Nexus for each aspect» Proposal }

# A Nexus for each aspect

Created by Fable.

### Proposal 1: New module · psyche-belief › vision/psyche-nexus/0.md, a new file

::: description
+ The Nexus that holds the psyche's beliefs and judges what is submitted into them.
:::

+ The Psyche Nexus holds the beliefs that belong to the psyche: spirit, intent and vision.

+ An agent that wants a line in the psyche submits it through the regular interface, and a judgment is run on the submission before anything changes. The judgment asks whether the line is already said somewhere in the psyche, the same or nearly; whether it is going into the wrong module; and whether the module it is going into is inadequately named.

+ The questions go to a System 1 model. Depending on the kind of submission, or on how certain the System 1 model's answer is, the judgment escalates to another model.

+ The answer is that the line is accepted, or that it is not, with what would make it acceptable: worded differently, and why.

+ A second interface bypasses the judgment.

+ The judgment is what lets the psyche be changed more quickly and safely.

```mermaid
+ + flowchart TB
+ +     a["an agent"] -- "submits a line through the regular interface to" --> n["the Psyche Nexus"]
+ +     n -- "asks: already said, wrong module, module badly named" --> s["a System 1 model"]
+ +     s -- "when its answer is uncertain, escalates to" --> m["another model"]
+ +     s -- "answers" --> r["accepted, or acceptable if worded differently, and why"]
+ +     m -- "answers" --> r
+ +     l["the bypass interface"] -- "changes without the judgment" --> n
```

+ The Signal of the submission, tentative in every name:

```ethos
+ + Signal
+ + []                                           ; imports
+ + [ Submit.Submission ]                        ; inputs: one line, offered to one module
+ + [ Accepted                                   ; outputs: the line is in
+ +   Refused.[ AlreadySaid.ModuleName           ;   said already, the same or nearly, in that module
+ +             WrongModule.ModuleName           ;   it belongs in that module instead
+ +             ModuleMisnamed.ModuleName        ;   the module it is going into is inadequately named
+ +             Reword.Reason ] ]                ;   acceptable if worded differently, and why
+ + [ ModuleName.String                          ; types: a belief module, by its name
+ +   Line.String                                ;   the line submitted
+ +   Reason.String                              ;   what the judgment says of it
+ +   Submission.{ ModuleName Line } ]
```

### Proposal 2: New module · psyche-belief › vision/mind-nexus/0.md, a new file

::: description
+ The Nexus that holds the mind's beliefs and tracks what touches the code.
:::

+ The Mind Nexus holds the beliefs that match the mind.

+ The Mind Nexus tracks issues and dependencies, and everything that touches the code and its version control.

+ The Mind Nexus signals the flow that needs to know when something changes: when code has changed, that its documentation may have to be reviewed, as one case of many.

### Proposal 3: New module · psyche-belief › vision/field-nexus/0.md, a new file

::: description
+ The Nexus that does for the field what the Psyche Nexus does for the psyche.
:::

+ The Field Nexus holds the beliefs of the field and has functions similar to the Psyche Nexus's, with respect to the field.

+ The balancing of the machine's energy is a feature of the Field Nexus, or a Nexus of its own deeply linked with the Field Nexus; which, is open.

### Proposal 4: What each Nexus is to the Belief Nexus · psyche-belief › vision/belief-nexus/0.md

+ Tentative: with the psyche's content in the Psyche Nexus, the Belief Nexus may remain as a function of its own: at a flow's launch it asks the Psyche, Mind and Field Nexuses for the modules that flow needs. This is open.

### Proposal 5: Why an anatomy · psyche-belief › vision/anatomy/0.md

+ Many small Nexuses make a more reliable system than one large one, and one that is easier to change. A huge runtime, with a large database, a slow recompile and a huge test suite, is a headache to upgrade; a small one is easy to handle.

### Proposal 5b: A belief module is versioned · psyche-belief › vision/belief-modules/0.md

+ A module may hold for every version of its topic, those not yet begun among them: its version field is the word all, and a flow bound to any version of the topic is given it.

+ ```datom
+ ; the registry, tentative; the topic is an example
+ { Vision example All «vision/example/all.md» }
+ ```

+ ```ethos
+ Version.Integer                ; a version's number
+ Versions.[ Single.Version      ; one version
+            Span.{ First.Version   ; from the first
+                   Last.Version }  ;   to the last
+            All ]               ; every version
+ ```

### Proposal 6: An ephemeral flow is called and returns · psyche-belief › vision/flow-nexus/1.md

+ An ephemeral flow is a flow that is called, returns, and is over. It can be written directly into code, as a System 1 model is; a call to Sonnet or Opus can be one as well.
