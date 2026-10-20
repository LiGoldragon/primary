<!-- to-the-living:start -->
Presentation.{ «Today, as psyche, 2nd edition» }

# Today, as psyche, 2nd edition

What you said since the first edition, written as the lines it lands. Ruled carries your words; open is a default for you to amend. What an open book already carries is left out.

### Proposal 1: A proposal touching code shows the code · psyche-context › vision/book.md

Ruled.

+ A proposal that touches a code component shows the code it changes or adds; a proposal about code with no code in it is not sent.

Ruling: land, amend, or reject.

### Proposal 2: Every comment redoes its book · psyche-context › vision/book.md

Ruled.

+ Every comment of his redoes the book it is on, unless the comment closes the topic; a book his comment affects is redone as well. A comment that opens a topic of its own gets a book of its own.

Ruling: land, amend, or reject.

### Proposal 3: The Nexus is an architecture, and everything made is one · psyche-context › vision/nexus.md

Ruled: the Nexus is a concept, not a particular program. Open: that a Nexus's vision is split by its code modules, which you said could be general.

+ The Nexus is an architecture concept, not one specific Nexus: everything made is a Nexus. A vision for one Nexus is that Nexus's, never the Nexus module's.
+ A Nexus's vision is split by its code modules.

Ruling: land, amend, or reject.

### Proposal 4: Hash checking is long term · psyche-context › vision/flow.md

Ruled. This amends the line «Flow: the design» proposes, where each module is checked against its source.

- Flow has them composed from the three aspect context repositories, each module checked against its source:
+ Flow has them composed from the three aspect context repositories:
+ ## Long term: modules checked by hash
+ Long term, every module composed into a prompt is checked against its source by its hash, once hashes update efficiently as edits are made; short term, no check is made.

Ruling: land, amend, or reject.

### Proposal 5: A role stands on its own; a subagent definition is data saying which module goes where · psyche-context › vision/flow.md

Ruled: a role may serve a flow that is not a metaflow, so a role is not found by its metaflow; a subagent definition is a data object, composed of roles and other modules, that says which modules go where, and is specified in Ethos. This amends the library of «Flow: the design»: a role is named and a definition names its roles.

+ A role stands on its own, named, and may serve any flow; a metaflow's definition names the roles it seats. A subagent definition is data: its name, and each module with the prompt it goes into; its payload is composed from the modules it names.

```ethos
Library.
{
[ flow:[ Address Layer Key
        Brief Prompts ] ]                 ; imports
[ RoleName.String                         ; types
  Effort.[ Low Medium High ]
  LeaveOut.String
  Role.{ RoleName                         ; one seat
         Layer
         Effort
         Vector<Key>                      ; modules
         Vector<Layer>                    ; reach
         Vector<LeaveOut> }
  Definition.{ Address                    ; contact
               Vector<RoleName> }
  Prompt.[ System First ]
  Placement.{ Key Prompt }           ; where it goes
  SubagentName.String
  Subagent.{ SubagentName
             Vector<Placement> } ]
[ Briefing.[ brief.[ String ] ]           ; traits
  Composable.[ compose.{ [ Briefing ]
                         [ Prompts ] } ]
  Named.[ name.[ String ] ]
  Seating.[ roles.[ Vector<RoleName> ] ] ]
[ Brief.[ Briefing ]                  ; associations
  Role.[ Named Composable ]
  Definition.[ Seating ]
  Subagent.[ Named Composable ] ] }
```
```
{ illustrator
  [ { { Vision book } First }
    { { Spirit core } System } ] }
```

Ruling: land, amend, or reject.

<!-- to-the-living:end -->
