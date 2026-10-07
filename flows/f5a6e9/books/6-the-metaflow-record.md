<!-- to-the-living:start -->
Presentation.{ «The metaflow record» }

## 1. The metaflow at the centre

One record in Flow's Memory per metaflow. It is what a message is addressed to, what is woken, refreshed and ended, and what holds its own current flow and its past. The flow record under it holds only what Flow needs to run and reap a session.

```
Memory
[  flow:[ FlowId Aspect Layer Event ] ]
[  Metaflow.{
      Name.[
         Voice.{            ; permanent: never Ended
            Aspect
            Layer }
         Goal.String ]      ; a short camelCase word;
                            ; ends when the goal is met
      State.[
         Awake.FlowId       ; its current flow
         Asleep             ; a request wakes it
         Ended ]
      Past.Vector<FlowId> } ; predecessors, oldest
                            ; first; trimmed by
                            ; forgetting the oldest
   Flow.{                   ; one per run, low-level
      FlowId
      Session.String        ; the harness's own id
      Events.Vector<Event> } ]
```

Written, this seat and one goal:

```
{  Voice.{ Psyche Primary }
   Awake.abandonAbilityAble
   [ zooWrongYouth ] }

{  Goal.flowRefresh
   Asleep
   [ ] }
```

No option anywhere: what exists at each state is carried by that state. A flow that belongs to no metaflow is simply listed by none; which metaflow a flow belongs to is read from the metaflow side, never stored on the flow.

The window, from the earlier book: the number of tokens a model accepts in one call, read from the harness's model catalog; 1,000,000 for the Claude models in use, 258,400 for Codex's. The thresholds are percentages of it.

Feedback you asked for: an Option on a record hides a state inside a field; an enum names the state and carries what that state has, so the record reads as what it is. Holding the current flow and the predecessors in the metaflow's memory is right: the walk back is then the metaflow's own list, and the flow record needs no field for it.

Three spaces of indentation above, in place of two.

## 2. Next books, one each

The lock as a request Message makes of Flow, time-bound, on a metaflow; typed requests to a metaflow and what each does to a new or a full flow; waking an asleep metaflow from a request. Each comes alone, after this one is ruled.

## 3. A line for the skill that holds orders

Added to `compensation-orders`: a later order from the living overrides an earlier hold, whoever relayed the hold.

## Rulings

1. The metaflow record of section 1, with Voice and Goal as its names and Awake, Asleep, Ended as its states: yes, or amend.
2. The flow record reduced to id, session and events: yes, or amend.
3. Three-space indentation in ethos: yes, or amend.
4. The line for `compensation-orders`: yes, or amend.
<!-- to-the-living:end -->
