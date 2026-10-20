### Proposal 1: Names say what they name · psyche-context › vision/ethos.md

In Naming. Rule: land, amend or reject.

+ A name says what it names in the system's own words; a word that means something only beside its neighbours, such as First, is not a name.

```ethos
+ Library.{
+ []                                  ; imports
+ [ Prompt.[ SystemPrompt             ; types
+           StartupPrompt ] ]
+ [ Named.[ name.[ String ] ] ]       ; traits
+ [ Named.[ Prompt ] ] }              ; associations
```

### Proposal 2: A capability is named in lowercase · psyche-context › vision/ethos.md

In Trait syntax. Every capability in this book is written so and passes the checker. Rule: land, amend or reject.

+ A capability is named in lowercase camelCase, because it is not a variant: its lowercase first letter tells it from a variant, as a topic's does.

```ethos
+ Library.{
+ []                                  ; imports
+ [ Brief.String ]                    ; types
+ [ Briefing.[ brief.[ String ]       ; traits
+              rewriteBrief!{ [ Named ] [] } ]
+   Named.[ name.[ String ] ] ]
+ [ Brief.[ Briefing Named ] ] }      ; associations
```

### Proposal 3: Library.{ on one line · psyche-context › vision/ethos.md

In Declaration: File. Rule: land, amend or reject.

- An ethos file is written in the sweet form: the root's head, then the sections as siblings, the outer braces omitted.
- The sweet form is kept out of the main logic run: before the text is read as ethos at all, the file is converted mechanically to the canonical form, so the ethos reader sees only proper ethos.
+ A file's usual form is the root's variant, its dot and the brace on one line, then a break, its sections standing unindented one per line, because the root's variant only gives the file its type; this is good form, never a requirement.
+ A file that holds a single thing breaks nowhere.

```ethos
+ Library.{
+ []                                  ; imports
+ [ Sink.{ String Integer } ]         ; types
+ [ Fillable.[ create:[ Self ]        ; traits
+              drain![ Vector<String> ] ] ]
+ [ Fillable.[ Sink ] ] }             ; associations
```

### Proposal 4: One vector per category · psyche-context › vision/ethos.md

In Non-repetition. Rule: land, amend or reject.

+ Where entries share a category, the category holds a vector of them; no entry repeats its category.
+ In associations, a trait borne by several types holds the vector of them: `Prompting.[ SystemPrompt StartupPrompt ]`.
+ An association whose head is a type keeps the vector of traits that type bears.

```ethos
+ Library.{
+ [ flow:[ Key ] ]                    ; imports
+ [ SystemPrompt.⟦ Key ⟧              ; types
+   StartupPrompt.⟦ Key ⟧
+   Placements.⦃ SystemPrompt
+                StartupPrompt ⦄ ]
+ [ Prompting.[ text.[ String ] ] ]   ; traits
+ [ Prompting.[ SystemPrompt          ; associations
+               StartupPrompt
+               Placements ] ] }
```

### Proposal 5: White brackets and white braces · psyche-context › vision/ethos.md

In Shapes and placement. Rule: land, amend or reject.

+ The white square brackets are sugar for a vector, and the white braces for a struct: `⟦ Key ⟧` is `Vector<Key>`, and `⦃ String Integer ⦄` is `{ String Integer }`.
+ Both are read at their own layer and become the plain form before the ethos reader sees the text.

```ethos
+ Library.{
+ []                                  ; imports
+ [ BatchName.String                  ; types
+   Counts.⟦ Integer ⟧
+   Batch.⦃ BatchName Counts ⦄ ]
+ [ Named.[ name.[ String ] ]         ; traits
+   Listed.[ count.[ Integer ] ] ]
+ [ Named.[ BatchName Batch ]         ; associations
+   Listed.[ Counts ] ] }
```

### Proposal 6: The Role and Subagent library · psyche-context › vision/flow.md

Rule: land, amend or reject.

+ A subagent definition names, for each prompt, the vector of modules that goes into it.

```ethos
+ Library.{
+ [ flow:[ Address Layer Key ] ]      ; imports
+ [ RoleName.String                   ; types
+   SubagentName.String
+   Effort.[ Low Medium High ]
+   Modules.⟦ Key ⟧
+   Reach.⟦ Layer ⟧
+   Roles.⟦ RoleName ⟧
+   SystemPrompt.⟦ Key ⟧
+   StartupPrompt.⟦ Key ⟧
+   Role.⦃ RoleName Layer Effort
+          Modules Reach ⦄
+   Definition.⦃ Address Roles ⦄
+   Subagent.⦃ SubagentName
+              SystemPrompt
+              StartupPrompt ⦄ ]
+ [ Named.[ name.[ String ] ]         ; traits
+   Costed.[ cost.[ Integer ] ]
+   Listed.[ count.[ Integer ] ]
+   Prompting.[ text.[ String ] ]
+   Seating.[ roles.[ Roles ] ] ]
+ [ Named.[ RoleName SubagentName     ; associations
+           Role Subagent ]
+   Costed.[ Effort ]
+   Listed.[ Modules Reach Roles ]
+   Prompting.[ SystemPrompt
+               StartupPrompt
+               Role Subagent ]
+   Seating.[ Definition ] ] }
```

```datom
+ { illustrator
+   [ { Intent core } ]
+   [ { Vision book } ] }
```
