<!-- to-the-living:start -->
Presentation.{ «Subflows: kind, role and level» }

# Subflows: kind, role and level

```
 a task
     |
     v
 +----------------------+
 | Aspect               |
 | Psyche, Mind, Field  |
 +----------------------+
     |  with
     v
 +----------------------+
 | Role                 |
 | Explorer, Worker,    |
 | Tester, Reviewer,    |
 | Publisher, Operator, |
 | Researcher           |
 +----------------------+
     |  at
     v
 +----------------------+
 | Level                |
 | Secondary, Tertiary, |
 | Quaternary           |
 +----------------------+
     |  composes
     v
 +----------------------+
 | the subflow's Kind,  |
 | its context modules  |
 | and its route        |
 +----------------------+
```

Claude names its built-in subflows Explore, Plan and general-purpose. Codex names its own explorer, worker and default. The roles above keep Explorer and Worker, and add the five most frequent tasks in our flows' logs: testing, review, books, deploy and debug, and web research.

## Crystallization

### Proposal 1: A subflow's kind is its use

File: psyche-context/skills/vision-flow.md, at the end

+ A subflow's kind is its use: an aspect, a role and a level, which compose. Secondary is the highest level of a subflow, then Tertiary and Quaternary. Each kind has its default route and its context modules.

Ruling: land, amend, or reject.

### Proposal 2: The Kind in Ethos

File: Curriculum/kinds.ethos, new

```
; The kind of a subflow: aspect, role and level.
Library
[]                    ; imports: intrinsics only
[ Aspect.[ Psyche     ; thinking, psyche records
           Mind       ; documentation, tools,
                      ; code changes, audit review
           Field ]    ; debugging, system audit,
                      ; system search, deploy
  Role.[ Explorer     ; locate and read
         Worker       ; implement or fix
         Tester
         Reviewer
         Publisher    ; books and figures
         Operator     ; deploy, debug, launch
         Researcher ] ; the web
  Level.[ Secondary
          Tertiary
          Quaternary ]
  Kind.{ Aspect
         Role
         Level } ]
[]                    ; kinds
[]                    ; associations
```

Aspect, Role and Level are enums, and Kind is a struct of the three. The Ethos checker accepts the file.

Ruling: land, amend, or reject.

### Proposal 3: A datom is shown with its type

File: psyche-context/skills/vision-datom.md, at the end

+ A datom shown to a reader stands beside its Ethos type, written `type.<Type>` before it:

```
type.Kind { Field Operator Tertiary }
type.Kind { Psyche Explorer Quaternary }
type.Level Secondary
```

The head `type` is lowercase, so it cannot be read as a variant.

Ruling: land, amend, or reject.

### Proposal 4: Context repositories by type

File: psyche-context/skills/vision-context-modules.md, at the end

```
 psyche-context
   spirit/  intent/  vision/
 mind-context
   knowledge/  operation/
 field-context
   compensation/
     |
     v
 +----------------------+
 | Curriculum: every    |
 | file is a context    |
 | module; its folder   |
 | is its type          |
 +----------------------+
     |  harness name
     v
 +----------------------+
 | <type>-<subject>     |
 +----------------------+
```

+ A context repository holds one folder per module type, and a file in it is named by its subject alone. Curriculum makes every file a module of its folder's type; the type and subject join into a name only at the harness.

Ruling: land, amend, or reject.

### Proposal 5: Models by role, numbers out of view

File: psyche-context/skills/vision-model-roles.md, at the end

+ A model is shown by its role and level; its number appears only where a version is pinned, and an alias keeps a version worth keeping.

Ruling: land, amend, or reject.

### Proposal 6: The contextualizer

Carried unchanged from the previous edition, Proposal 3.

## Knowledge review: the Kind in Clojure

```clojure
(defn unit-enum [tags]
  (into [:or]
        (map #(variant % [:tuple]))
        tags))

(def Kind
  [:map {:closed true}
   [:aspect Aspect]
   [:role Role]
   [:level Level]])
```

```
{:aspect #field [] :role #operator []
 :level #tertiary []}            => true
{:aspect #field [] :role #operator []
 :level #primary []}             => false
```

A variant is a tagged literal and a key is kebab-case, following the recommended choices in «Clojure translation», ed. 2. The second value fails because Level has no Primary.

## Question

Does a level set the model's power — Secondary the strongest, Quaternary the lightest — or only the place in the chain of command?
<!-- to-the-living:end -->
