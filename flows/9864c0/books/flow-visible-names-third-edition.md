Presentation.{ «Flow Visible Names» }

# Flow Visible Names

### Proposal 1: mind-context › knowledge/flow-visible-names.md, a new file

+ ---
+ description: What each surface of a flow is named by deployed Flow.
+ dependencies: []
+ ---
+ ## Names a flow shows
+ The title is the datom struct `{ Aspect Topic Layer FlowId }`, a type written with its names capitalized. An instance is `{ Psyche core Secondary 9864c0 }`, its topic value lowercase.
+ Claude session name (`--name`): the title, passed only when a Flow ID is reserved.
+ Herdr pane label: the title, renamed and read back.
+ Codex thread name: the title, set with `thread/name/set` and read back.
+ Herdr workspace label: `claude-<24 hex>`, a hash of the launch request.
+ Herdr agent name: the same hash.
+ Claude Remote Control name, the name in the living's thread list: `flow-<16 hex>`, a hash of the launch request.

### Proposal 2: flow › crates/flow-nexus

```rust
// src/composition.rs: the hash name is deleted
- fn remote_control_name(&self) -> String {
-     format!("flow-{}",
-         self.launch_request_short_form())
- }
```

```rust
// src/title.rs: the topic is shown as written
- topic: self.address.topic.to_lowercase(),
+ topic: self.address.topic.clone(),
```

```rust
// src/herdr/launch.rs: Remote Control = title
- arguments.push(
-     launch.launch_profile.remote_control_name());
+ arguments.push(title.as_str().into());
+ arguments.push(Self::CLAUDE_NAME_FLAG.into());
+ arguments.push(title.as_str().into());
```

```rust
// src/herdr/launch.rs: workspace and agent shown
// before the agent starts
+ if let Some(title) = &claude_title
+     && let Err(error) =
+         self.show_title_before_agent(pane, title)
+ {
+     eprintln!("title not shown early: {error}");
+ }
+
+ // workspace label = title
+ "workspace", "rename",
+     pane.herdr_workspace_id.clone(), title,
+ // pane's displayed agent = title
+ "pane", "report-metadata",
+     pane.herdr_pane_id.clone(),
+     "--display-agent", title,
```

### Proposal 3: field-context › compensation/book-crystallization.md

  A book has no technical part; technical references stay out of the book.
+ A proposed line that names a type writes the type's names capitalized and shows an example value beside it.

Ruling: land, amend, or reject.
