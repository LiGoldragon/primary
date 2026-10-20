<!-- to-the-living:start -->
Presentation.{ «Ethos: categories, names and sugar» }

# Ethos: categories, names and sugar

### Proposal 1: A category holds a vector of its entries, in Non-repetition · psyche-context › vision/ethos.md

+ Where entries share a category, the category holds a vector of them; no entry repeats its category.

```ethos
Library.{
[ flow:[ Key ] ]                      ; imports
[ SystemPrompt.⟦ Key ⟧                ; types
  StartupPrompt.⟦ Key ⟧
  Placements.⦃ SystemPrompt
               StartupPrompt ⦄ ]
[ Prompting.[ text.[ String ] ] ]     ; traits
[ SystemPrompt.[ Prompting ]          ; associations
  StartupPrompt.[ Prompting ]
  Placements.[ Prompting ] ] }
```

```datom
{ [ { Intent core } ]
  [ { Vision book } ] }
```

Ruling: land, amend, or reject.

### Proposal 2: A name says what it names, in Naming · psyche-context › vision/ethos.md

+ A name says what it names in the system's own words; a word that means something only beside its neighbours, such as First, is not a name.

```ethos
Library.{
[]                                    ; imports
[ Prompt.[ SystemPrompt               ; types
          StartupPrompt ] ]
[ Named.[ name.[ String ] ] ]         ; traits
[ Prompt.[ Named ] ] }                ; associations
```

Ruling: land, amend, or reject.

### Proposal 3: A capability is named in lowercase, in Trait syntax · psyche-context › vision/ethos.md

+ A capability is named in lowercase camelCase, because it is not a variant: its lowercase first letter tells it from a variant, as a topic's does.

```ethos
Library.{
[]                                    ; imports
[ Brief.String ]                      ; types
[ Briefing.[ brief.[ String ]         ; traits
             rewriteBrief!{ [ Named ] [] } ]
  Named.[ name.[ String ] ] ]
[ Brief.[ Briefing Named ] ] }        ; associations
```

Ruling: land, amend, or reject.

### Proposal 4: The root, its dot and the brace on one line, amending Proposal 1 of «The Ethos syntax, 2nd edition» · psyche-context › vision/ethos.md

- A file's usual form is a break after the dot and a break after the brace, its sections standing unindented one per line, because the root's variant only gives the file its type; this is good form, never a requirement. A file that holds a single thing breaks nowhere.
+ A file's usual form is the root's variant, its dot and the brace on one line, then a break, its sections standing unindented one per line, because the root's variant only gives the file its type; this is good form, never a requirement. A file that holds a single thing breaks nowhere.

```ethos
Library.{
[]                                    ; imports
[ Sink.{ String Integer } ]           ; types
[ Fillable.[ create:[ Self ]          ; traits
             drain![ Vector<String> ] ] ]
[ Sink.[ Fillable ] ] }               ; associations
```

Ruling: land, amend, or reject.

### Proposal 5: White brackets for a vector and white braces for a struct, in Shapes and placement · psyche-context › vision/ethos.md

+ The white square brackets are sugar for a vector, and the white braces for a struct: `⟦ Key ⟧` is `Vector<Key>`, and `⦃ String Integer ⦄` is `{ String Integer }`.
+ Both are read at their own layer and become the plain form before the ethos reader sees the text.

```ethos
Library.{
[]                                    ; imports
[ BatchName.String                    ; types
  Counts.⟦ Integer ⟧
  Batch.⦃ BatchName Counts ⦄ ]
[ Named.[ name.[ String ] ]           ; traits
  Listed.[ count.[ Integer ] ] ]
[ BatchName.[ Named ]                 ; associations
  Counts.[ Listed ]
  Batch.[ Named ] ] }
```

Ruling: land, amend, or reject.

### Proposal 6: The Role and Subagent library, amending Proposal 5 of «Today, as psyche, 2nd edition» · psyche-context › vision/flow.md

+ A subagent definition names, for each prompt, the vector of modules that goes into it.

```ethos
Library.{
[ flow:[ Address Layer Key ] ]        ; imports
[ RoleName.String                     ; types
  SubagentName.String
  Effort.[ Low Medium High ]
  Modules.⟦ Key ⟧
  Reach.⟦ Layer ⟧
  Roles.⟦ RoleName ⟧
  SystemPrompt.⟦ Key ⟧
  StartupPrompt.⟦ Key ⟧
  Role.⦃ RoleName Layer Effort
         Modules Reach ⦄
  Definition.⦃ Address Roles ⦄
  Subagent.⦃ SubagentName
             SystemPrompt
             StartupPrompt ⦄ ]
[ Named.[ name.[ String ] ]           ; traits
  Costed.[ cost.[ Integer ] ]
  Listed.[ count.[ Integer ] ]
  Prompting.[ text.[ String ] ]
  Seating.[ roles.[ Roles ] ] ]
[ RoleName.[ Named ]                  ; associations
  SubagentName.[ Named ]
  Effort.[ Costed ]
  Modules.[ Listed ]
  Reach.[ Listed ]
  Roles.[ Listed ]
  SystemPrompt.[ Prompting ]
  StartupPrompt.[ Prompting ]
  Role.[ Named Prompting ]
  Definition.[ Seating ]
  Subagent.[ Named Prompting ] ] }
```

```datom
{ illustrator
  [ { Intent core } ]
  [ { Vision book } ] }
```

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
