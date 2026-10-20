<!-- to-the-living:start -->
Presentation.{ «One module name, first edition» }

# One module name

```
+----------------------+
| vision/book.md       |
+----------------------+
          | registers as
          v
+----------------------+
| vision:book          |
+----------------------+
          | resolves through
          v
+----------------------+
| Curriculum registry  |
+----------------------+
          | supplies one body to
          v
+----------------------+
| Startup and roles    |
+----------------------+
```

### Proposal 1: Inquiry 1: One identity throughout composition · mind-context › inquiry/module-naming.md, a new file

+ ### What is settled
+ A module has a type and a subject. Its authored path puts the subject in the type's directory. Its single-string identity is kind:subject, without whitespace. The path vision/book.md therefore names vision:book.
+
+ ### What Mind knows
+ The present Curriculum validator accepts lowercase letters, digits and hyphens, but no colon. Startup checks recognize spirit and intent through hyphen prefixes. Roles and dependency lists still use those old identities. Merely renaming the folders presented by a harness would leave the actual composer on the old contract.
+
+ ### What is proposed for implementation
+ Parse a module identity once into kind and subject. Resolve it only through the existing registry over the three context repositories. Use that parsed kind for placement rules. Keep a separate validator for role names and filename components; they are not module identities and must not acquire a colon accidentally.
+ Rewrite dependency lists, role module references, startup selections and their consumers in one coordinated source revision set. The old identities are replaced, not retained as a second alias vocabulary. Unknown identities, duplicate identities and mixed old/new inputs refuse before a launch or projection.
+
+ ### What is still open
+ Does the approved subject vocabulary retain the current lowercase letters, digits and internal hyphens, or should any other characters be admitted? This first implementation proposes preserving the existing subject vocabulary while changing only the kind separator. It does not infer new casing or escaping rules.

Ruling: land, amend, or reject.

```
+----------------------+
| Parsed module kind   |
+----------------------+
          | determines
          v
+----------------------+
| Placement rule       |
+----------------------+
          | accepts or refuses
          v
+----------------------+
| Requested prompt    |
+----------------------+
```

### Proposal 2: Check the kind, not a spelling prefix · Curriculum › src/startup.rs

The placement rule stays the same: spirit and intent belong in the system prompt. Its implementation would use the parsed identity's kind. The replacement below shows the intended check; the parser and error type must be owned by the registry, rather than implemented again inside startup.

```rust
- let system_only = source.name.starts_with("spirit-")
-     || source.name.starts_with("intent-");
+ let identity =
+     registry.parse_module_identity(&source.name)?;
+ let system_only = matches!(
+     identity.kind(),
+     "spirit" | "intent"
+ );
```

The final presence checks must use the same parsed kind. Tests must show that spirit:core and intent:context remain system-only, that a subject containing the word spirit gains no special placement, and that a malformed or old identity is refused. This code is a proposed interface, not a claim that the parser method already exists.

Ruling: land, amend, or reject.

```
+----------------------+
| Canonical identity   |
+----------------------+
          | is encoded by
          v
+----------------------+
| Target projection    |
+----------------------+
          | checks representation in
          v
+----------------------+
| Native harness      |
+----------------------+
          | supplies evidence to
          v
+----------------------+
| Psyche review        |
+----------------------+
```

### Proposal 3: Inquiry 3: Native names and the colon in Ethos · mind-context › inquiry/module-naming.md, a new file

+ ### What Mind knows
+ Field's isolated proof loaded vision:book in Claude 2.1.294 and Codex 0.158.0-alpha.9, including completion and the exact fixture instruction in native context. That proves those tested routes, not every installed harness. Core reports that OpenCode refuses a colon. Ethos also uses a colon in import notation, so a bare module identity cannot simply be inserted into every syntactic position.
+
+ ### What is proposed for comparison
+ Claude and Codex projections would retain kind:subject. Where OpenCode cannot represent it, a target-specific display or filename encoding could use kind-subject while retaining the canonical identity in the projection record. It must not become a second registry identity. Before generation, the projector must check the actual admitted module inventory for output collisions and refuse any duplicate output path.
+ For fields typed as strings, a quoted Datom string carrying the canonical name is a candidate representation. Whether that is valid in each actual Ethos or Datom consumer must be checked with that parser; import syntax must not be changed by a string replacement.
+
+ ### Open questions
+ Is the OpenCode target encoding acceptable under the approved single-string naming rule, or should that target remain unavailable until it can show the canonical name? If an encoding is accepted, should an unrepresentable collision refuse the whole projection rather than choose another spelling?
+ Does the requested name appear as a string value or as language syntax at each Ethos boundary? Mind will inventory those call sites before proposing a grammar change. No new import grammar is assumed here.
+
+ ### What would settle it
+ The OpenCode ruling and parser-backed examples would settle these questions. Acceptance must show the canonical identity surviving composition and provenance, the correct native completion on each supported target, and explicit refusal where a target cannot represent the name faithfully.

Ruling: land, amend, or reject.

```
+----------------------+
| Reviewed contract    |
+----------------------+
          | guides
          v
+----------------------+
| Coordinated sources  |
+----------------------+
          | produce
          v
+----------------------+
| Checked deployment   |
+----------------------+
          | provides evidence for
          v
+----------------------+
| Psyche audit         |
+----------------------+
          | returns corrections to
          v
+----------------------+
| Implementation       |
+----------------------+
```

### Proposal 4: Inquiry 4: How does the change reach every flow? · mind-context › inquiry/module-naming.md, a new file

+ ### What is being prepared
+ The implementation is divided into authored references, registry and composition, then consumer projections. Each part is checked against the same selected source revisions. Field owns generation and activation; authored bodies and placement must not change merely because their identities change.
+ The old installed cohort stays intact until the replacement can compose every declared startup and callable role. Activation advances the matching registry, sources and consumers together. Rollback restores that complete prior cohort rather than mixing identity formats.
+
+ ### What would settle implementation
+ Compare the old and new inventories by authored source: exactly one new identity for each intended module, no lost or duplicated body, no changed default selection or system/user placement. Exercise all configured startup selections and role definitions, missing and ambiguous identities, malformed names and target collisions. Then witness the supported native names after deployment.
+ Psyche reviews both source behavior and that deployed evidence against the landed naming vision. A published revision or a successful autocomplete alone does not close the implementation cycle.
+
+ ### Remaining boundary
+ Which current consumers still read generated skill folders, and which use the in-memory composer? That inventory must choose the actual existing path for each consumer; the migration must not revive retired file projection just to make an old path look current.

Ruling: land, amend, or reject.

<!-- to-the-living:end -->
