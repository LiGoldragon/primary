# flow-clj typed EDN input

Status: proposed Mind-side input contract for Field Astra to implement. It is
not a transport contract, a claim that these operations are deployed, or a
replacement for the Flow signal/Datom wire.

## Grounding

The current local `signal-flow` contract has only `Start` and `Restart`:
`Start` is `(flow_type, goal, origin)`. The current Flow CLI accepts Datom,
not EDN. The 2026-09-24 ruling adds the basic operations Start, Stop, Send,
and Flow-first raw use; List is included in the dispatched flow-clj brief.
Current source and deployment reports identify standalone Stop, List, and
raw Send as absent. This document therefore proposes only the Clojure CLI
reader and validation boundary.

The living's 2026-09-25 Clojure direction is followed here: EDN tags stand
in for Datom variants and Malli validates the EDN values. The existing
HackyMessenger precedent is a tagged vector, `#msg [sender body]`.

## Four forms

```
#start [aspect exact-model effort power goal skills origin]
#stop  [flow-id]
#list  []
#send  [flow-id body]
```

The forms are closed by tag and fixed arity. Their vectors are positional so
the schema, rather than an open EDN map, owns the meaning of each position.

`#start` positions are:

1. `aspect` — `:psyche`, `:mind`, or `:field`.
2. `exact-model` — the native model identifier selected from the runtime's
   audited catalog, for example `"gpt-6-astra"`; a display name such as
   `"Astra"` is not accepted as an identifier.
3. `effort` — the exact native effort string requested by the caller. Its
   allowed values are owned by the selected model/runtime catalog, not by this
   static EDN grammar.
4. `power` — `:ultra-low`, `:low`, `:medium`, or `:high`.
5. `goal` — one non-empty composed first-prompt goal.
6. `skills` — requested native skill names, in caller order.
7. `origin` — `[parent-flow-id session turn]`, preserving the current
   `signal-flow::Origin` positions.

The Start input deliberately has no requested Flow ID, native title, model
display, Herdr session/pane, or route. Flow creates and records its distinct
Flow identity; its title derives from aspect, observed model-display mapping,
and that identity. Herdr binding, readiness proof, and any availability state
are implementation outputs. This prevents a caller from asserting facts that
belong to Flow or Herdr.

`#stop` and `#send` name a target only by `flow-id`. The implementation must
resolve its current binding immediately before acting and fail closed if the
identity, lifecycle, or route is missing or ambiguous. `#list` has no caller
supplied filter: it asks for the known bindings and their truthful states.
`#send` carries a body only; it must not contain a caller aspect, model, power,
or route. Calling identity is established at the CLI/Flow boundary, as the
existing Flow design requires, rather than trusted from message text.

Aspect, exact model identifier, behavioral power, Flow ID, native title,
native route, and readiness evidence remain distinct facts. In particular,
power is not a model display and is not a title component.

## Reader and Malli representation

The following is the proposed shape, intended for a `flow_clj.edn` namespace.
It is illustrative source, not an implementation commit.

```clojure
(ns flow-clj.edn
  (:require [malli.core :as m]))

(defrecord Form [tag values])
(defn tagged [tag values] (->Form tag values))
(defn read-start [values] (tagged :start values))
(defn read-stop  [values] (tagged :stop values))
(defn read-list  [values] (tagged :list values))
(defn read-send  [values] (tagged :send values))

;; data_readers.clj:
;; {start flow-clj.edn/read-start
;;  stop  flow-clj.edn/read-stop
;;  list  flow-clj.edn/read-list
;;  send  flow-clj.edn/read-send}

(def NonEmpty [:string {:min 1}])
(def FlowId [:and NonEmpty [:re #"^[A-Za-z0-9][A-Za-z0-9_-]*$"]])
(def SkillName [:and NonEmpty [:re #"^[a-z0-9][a-z0-9-]*$"]])
(def Aspect [:enum :psyche :mind :field])
(def Power [:enum :ultra-low :low :medium :high])
(def Origin [:tuple FlowId NonEmpty NonEmpty])
(def StartValues [:tuple Aspect NonEmpty NonEmpty Power NonEmpty [:vector SkillName] Origin])
(def StopValues  [:tuple FlowId])
(def ListValues  [:tuple])
(def SendValues  [:tuple FlowId NonEmpty])

(def Input
  [:or
   [:fn {:error/message "#start needs seven typed positions"}
    #(and (= :start (:tag %)) (m/validate StartValues (:values %)))]
   [:fn {:error/message "#stop needs one Flow ID"}
    #(and (= :stop (:tag %)) (m/validate StopValues (:values %)))]
   [:fn {:error/message "#list takes no positions"}
    #(and (= :list (:tag %)) (m/validate ListValues (:values %)))]
   [:fn {:error/message "#send needs a Flow ID and non-empty body"}
    #(and (= :send (:tag %)) (m/validate SendValues (:values %)))]])

(defn valid-input! [form]
  (if (m/validate Input form)
    form
    (throw (ex-info "invalid flow-clj input"
                    {:explain (m/explain Input form)}))))
```

The second and third Start positions intentionally validate as non-empty
strings here. A live catalog check must then validate the exact
`[exact-model effort]` pair and derive the model display; hard-coding a model
or effort enum in this prototype would duplicate setup-specific configuration.
The `FlowId` regex is anchored because prior HM work found that Malli `:re`
uses partial matching when used alone.

## Valid examples

```edn
#start [:mind "gpt-6-astra" "medium" :high
        "Implement the four Flow operations." ["psyche" "testing"]
        ["38de5b" "messaging-build" "turn-42"]]

#stop ["f5a74e"]
#list []
#send ["f5a74e" "Please read flows/f5a74e/reports/clojure-flow-input.md."]
```

## Rejected at the EDN/Malli boundary

```edn
#start [:mind "Astra" "medium" :high "x" [] ["38de5b" "s" "t"]]
;; model display substituted for exact native model id: rejected by catalog check

#start [:mind "gpt-6-astra" "medium" :astra "x" [] ["38de5b" "s" "t"]]
;; power is not a model: rejected by Power

#start [:mind "gpt-6-astra" "medium" :high "x" [] ["../../etc" "s" "t"]]
;; Flow ID traversal-shaped: rejected by anchored FlowId

#list ["f5a74e"]
;; list is nullary: rejected by tuple arity

#send ["f5a74e" ""]
;; empty body: rejected
```

An unknown but syntactically valid target ID, a stale route, a duplicate Flow
ID, unsupported skill, model/effort mismatch, or unavailable/ambiguous Herdr
binding is not an EDN parsing result. It is a later implementation check and
must yield a truthful refusal or held/pending result; this report does not
specify its transport result variants.

## Verification and handoff

The checked runtime has Babashka and Clojure available. This report does not
add a source namespace or dependency, so it deliberately does not claim a
runnable Malli validator. Field Astra should place the sketch in flow-clj,
load Malli through that tool's declared dependency, and add the four valid and
five rejected examples as boundary tests before transport work.

Sources inspected: `flow/crates/signal-flow/src/lib.rs`,
`flow/crates/flow/src/main.rs`, `Vision/flowNexus.md`, `Vision/modelRoles.md`,
`flows/e51411/vision/{stack,flowAspect}.md`,
`flows/e51411/reports/flow-message-basics.md`,
`flows/e51411/flashbooks/clojure-rust/source.md`,
`flows/e51411/notion/message.md`, and `flows/38de5b/{log.md,receipts/flow-clj.md}`.
