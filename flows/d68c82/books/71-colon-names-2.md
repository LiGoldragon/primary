<!-- to-the-living:start -->
Presentation.{ «A context module is named kind:name» }

# A context module is named kind:name

### Proposal 1: a module's name shows its kind before a colon · psyche-context › vision/context-modules.md

  A context repository holds one folder per module type; no folder is called skills. A file is named by its subject alone, and its folder gives its type.
+ A module's name is its kind and its name joined by a colon, as vision:book, so the eye sees where the kind ends and the name begins.
+ On disk the kind stays the folder: vision:book is the file vision/book.md.
+ Every flow learns in its basic training to read a name as kind:name.
  A context repository holds one section of role modules per layer, Primary, Secondary, Tertiary and Quaternary, and may hold sections for specialized topics.

```
+-----------------------+
| vision:book           |
+-----------------------+
   |                |
   | kind, before   | name, after
   | the colon      | the colon
   v                v
+-----------+  +-----------+
| vision    |  | book      |
+-----------+  +-----------+
   |                |
   | is the folder  | is the file
   v                v
+-----------------------+
| vision/book.md        |
+-----------------------+
```

Ruling: land, amend, or reject.

### Proposal 2: the module ID becomes kind:name · Curriculum › src/registry.rs

In Ethos a name before a colon already means an import from that source (Topic.custom:Name), so vision:book written in Ethos would read as an import.

```rust
  // after valid_id
  }
+ /// kind:subject, as vision:book.
+ pub fn valid_module_id(value: &str) -> bool {
+     value.split_once(':').is_some_and(|(k, s)| {
+         MODULE_TYPES.contains(&k) && valid_id(s)
+     })
+ }
  #[derive(Clone, Debug, Eq, PartialEq)]
  pub struct SourceConfiguration {
```

```rust
  if !valid_id(subject) {
      return Err(invalid(&path, "invalid subject"));
  }
- let name = format!("{kind}-{subject}");
+ let name = format!("{kind}:{subject}");
```

```rust
  .map(|id| {
-     if !valid_id(id) {
+     if !valid_module_id(id) {
```

```rust
  let (kind, subject) = skill
      .name
-     .split_once('-')
+     .split_once(':')
```

```rust
  let mut seen = BTreeSet::new();
- if ids.iter().any(|id| !valid_id(id) || !seen.insert(id)) {
+ if ids.iter().any(|id| {
+     !valid_module_id(id) || !seen.insert(id)
+ }) {
```

Ruling: land, amend, or reject.

### Proposal 3: Claude and Codex folders are kind:name, OpenCode stays kebab · curriculum-deploy › src/runtime.rs

```rust
              Self::Pi => None,
          }
      }
+     /// The folder a harness finds a skill in:
+     /// kind:name for Claude and Codex; OpenCode
+     /// refuses a colon and keeps kind-name.
+     fn folder(self, name: &str) -> String {
+         match (self, name.split_once('-')) {
+             (Self::OpenCode, _) | (_, None) => {
+                 name.into()
+             }
+             (_, Some((kind, rest))) => {
+                 format!("{kind}:{rest}")
+             }
+         }
+     }
  }
```

```rust
  outputs.push((
-     PathBuf::from(surface).join(&skill.name).join("SKILL.md"),
+     PathBuf::from(surface)
+         .join(target.folder(&skill.name))
+         .join("SKILL.md"),
      target.rendered_skill(skill)?,
  ));
```

```rust
  PathBuf::from(".agents/skills")
-     .join(&skill.name)
+     .join(SkillTarget::Codex.folder(&skill.name))
      .join("agents/openai.yaml"),
```

```rust
  let skill_path = entry.path().join("SKILL.md");
- if skill_path.is_file() && !self.skills.defines(&name) {
+ let stem = name.replacen(':', "-", 1);
+ let defined = self.skills.defines(&stem);
+ if skill_path.is_file() && !defined {
      let retired = entry.path();
```

Ruling: land, amend, or reject.

### Proposal 4: basic training reads kind:name · mind-context › knowledge/vocabulary.md

  Machine: short for thinking machine.
+ Module name: kind:name, the module's kind before the colon and its hyphenated name after it; vision:book is the file vision/book.md, written vision-book only where a colon is refused.
  Use machine, not AI; use flow, not agent, except when reproducing an external name or quotation.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
