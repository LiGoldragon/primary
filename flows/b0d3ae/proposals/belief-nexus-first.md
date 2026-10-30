Presentation.{ «The Belief Nexus, first step» }

# The Belief Nexus, first step

Created by the Primary

**Why** A subflow is a composition of belief modules, and the Belief Nexus is the Nexus that holds the modules and composes them. Curriculum is replaced by it whole. This is the first step: what a role is, and the smallest Nexus that composes one. Nothing here says how a module is trained; that is the next step.

### Proposal 1: vision:belief-nexus · psyche-belief › vision/belief-nexus.md — a new module

## What it is

The Belief Nexus holds every belief module as a typed record and composes them into prompts. A role is a named composition: the modules a subflow starts with, and sometimes one small module of its own. A subflow's whole training is its composition; its behavior comes from which modules are composed, and a new behavior is a new composition before it is a new module. The Flow Nexus asks the Belief Nexus for a composition at every launch, and composes nothing itself.

A brief given to a subflow is a question or an order of a line or two, and it is enough because the composition already holds the how.

## Signal

```ethos
Signal
[ belief:[ ModuleId Role Composition ] ]        ; imports
[ Compose.Role                                   ; queries: the prompt for a role
  Read.ModuleId ]                                ;   one module as it stands
[ Composed.Composition                           ; responses
  Module.Text.String
  Refused.[ NoSuchRole NoSuchModule ] ]
[]                                               ; types
```

## Operation

```ethos
Operation
[ belief:[ ModuleId Role Composition Module ] ]  ; imports
[ Gather.Role                                    ; operations: the role's modules, in order
  Render.Vector<Module> ]                        ;   the modules into one prompt
[ Gathered.Vector<Module>                        ; outcomes
  Rendered.Composition
  Failed.[ MissingModule.ModuleId ] ]
[]                                               ; types
```

## Memory

```ethos
Memory
[ belief:[ ModuleId Role ] ]                     ; imports
[ Module.{ ModuleId                              ; record types: one belief module
           Kind.[ Spirit Intent Vision Knowledge Role ]
           Placement.[ System First ]
           Text.String }
  Role.{ Name.String                             ; a named composition
         Vector<ModuleId>
         Option<ModuleId> } ]                    ;   its own small module, when it has one
```

## Meta signal

```ethos
Signal
[ belief:[ ModuleId Module Role ] ]              ; imports
[ Land.Module                                    ; queries: a module as the living approved it
  Define.Role
  Remove.ModuleId ]
[ Landed  Defined  Removed                       ; responses
  Refused.NotOwner ]
[]                                               ; types
```

## The datom

Three roles, each a composition and nothing else; the first has no module of its own:

```datom
; Role
{ reader  [ spirit:core intent:energy knowledge:vocabulary ] None }
{ illustrator  [ spirit:core vision:book ] Some.role:illustrator }
{ lander  [ spirit:core intent:belief-modules vision:belief-modules vision:committing ] Some.role:lander }
```

The Flow Nexus, at a launch, over the ordinary socket:

```datom
Compose.reader
Composed.«…the three modules rendered, spirit first…»
```

The living's landing, over the meta socket:

```datom
Land.{ vision:belief-nexus Vision System «…» }
Landed
```

**What comes next** How a module is trained: what makes a composition well-trained and not over, and how that is witnessed. How a role evolves when it fails. How the Flow Nexus's declaration and a role are one thing.
