Presentation.{ «Herdr is driven by the Flow Nexus alone» Proposal }
# Herdr is driven by the Flow Nexus alone

Created by Fable 5.1, alone.

### Proposal 1: One driver, one keeper of state · psyche-belief › vision/flow-nexus.md

**Comment** Added under "Herdr holds the panes". Every pane action goes through the Flow Nexus, and the state of a flow is held in one place: the Nexus's Memory.

  Herdr is the third-party terminal workspace every flow runs in, one pane per flow. Herdr is used as it is: a low-level tool that receives finished commands from the translator and holds no logic of ours; every fact about a launch is the Nexus's, decided on the Nexus's types.
+
+ Herdr is driven by the Flow Nexus alone: a pane is made, prompted, pressed and closed by a Nexus operation, and a flow that needs a pane acted on sends the Nexus the request. The state of a flow, awake or asleep, working or idle, which pane and which session, is held in the Nexus's Memory and nowhere else; what herdr shows is read into that Memory, never kept beside it.

### Proposal 2: A permaflow is never without a flow · psyche-belief › vision/flow-nexus.md

**Comment** Added after the refresh paragraph. The rule the refresh paragraph ends on, stated as the invariant it is.

  A flow is refreshed when its context passes its model's threshold: the Flow Nexus keeps the permaflow's next messages for its next flow, and the flow is replaced as it goes idle; while the refresh runs the permaflow is locked, and the predecessor is reaped in the same event. Each model's threshold is configured in the Flow Nexus. A flow still working is not forced to refresh. When the successor cannot start, the Flow Nexus restarts the predecessor and compacts it, so every permaflow keeps a flow.
+
+ A permaflow is never without a flow: from the moment it is started until it is retired, one flow holds its address, and a refresh, a restart or a successor that fails to start leaves that flow standing until the next one holds it.

### Proposal 3: An abrupt delivery leaves the recipient's command running · psyche-belief › vision/flow-nexus.md

**Comment** Added under "A message", after the four observations. A pressing message reaches the model between its tool calls; the tool call in flight runs to its end.

  Inducing an interrupt, placing prompt text, submitting it, and the recipient consuming it are four separate observations. None of them stands for another, and a submission is never a read receipt.
+
+ An abrupt delivery is placed without killing the recipient's command: a HardAbrupt reaches the model at its next turn and a MiddleAbrupt at its next tool boundary, and the command running when either arrives runs to its end, its result kept. A delivery that ends a command is a failed delivery, and the Nexus reports it as one.
