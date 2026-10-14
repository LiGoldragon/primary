<!-- to-the-living:start -->
Presentation.{ «The shared Clojure translation pattern» }

# The shared Clojure translation pattern

```
+------------------+     +------------------+
|  Ethos           |     |  typed Datom     |
|  declaration     |     |  value           |
+------------------+     +------------------+
        |  through              |  through
        v                       v
+---------------------------------------+
|        shared construct mapping       |
+---------------------------------------+
        |  gives                |  gives
        v                       v
+--------------+          +-----------+
| Malli schema |--checks->| EDN value |
+--------------+          +-----------+
                                |  recovers
                                v
                      +-------------------+
                      | the typed value   |
                      +-------------------+
```

The shared translation contract is landed in `vision-clojure`.

## Crystallization

### Proposal 2: The mapping and its graph

File: `psyche-context/skills/vision-clojure.md`, after the landed line

```text
+ [graph above]
+
+ The declaration determines the schema and the interpretation of each value. Recovery preserves the typed value, not its textual spelling.
```

The construct mapping:

```clojure
Ethos        Malli schema        EDN value
scalar       named schema        scalar
struct       closed map of       map of the
             required entries    entries
vector       ordered vector      vector
variant      tag plus whole      tagged value
             payload
nesting      recursive           recursive
Option,      keep their variant  Some(None) is
Result       distinctions        not None
```

The worked example. Ethos:

```clojure
Library
[]
[ Person.{ Name.String Age.Integer }
  Reply.[ Accepted.Person
          Refused.String
          Pending ] ]
[]
[]
```

Datom values:

```clojure
{ Ada 36 }
Accepted.{ Ada 36 }
Pending
```

EDN values, the unit variant an empty vector:

```clojure
{:name "Ada" :age 36}
#accepted {:name "Ada" :age 36}
#pending []
```

Clojure, run:

```clojure
(ns translation-example
  (:require [clojure.edn :as edn]
            [malli.core :as m]))

(defn variant [tag schema]
  (let [valid? (m/validator schema)]
    [:fn (fn [value]
           (and (tagged-literal? value)
                (= tag (:tag value))
                (valid? (:form value))))]))

(def Person
  [:map {:closed true}
   [:name :string] [:age :int]])

(def Reply
  [:or (variant 'accepted Person)
       (variant 'refused :string)
       (variant 'pending [:tuple])])

(def readers
  (into {}
        (map (fn [tag]
               [tag #(tagged-literal tag %)])
             '[accepted refused pending
               some none])))

(defn read-example [text]
  (edn/read-string {:readers readers} text))

(def accepted
  (read-example
    "#accepted {:name \"Ada\" :age 36}"))

(m/validate Reply accepted)
;; => true
(m/validate Reply
  (read-example
    "#accepted {:name \"Ada\" :age \"36\"}"))
;; => false

(defn option-schema [payload]
  [:or (variant 'none [:tuple])
       (variant 'some payload)])

(def NestedOption
  (option-schema (option-schema Person)))
(def absent (read-example "#none []"))
(def present-absent
  (read-example "#some #none []"))

(m/validate NestedOption absent)
;; => true
(m/validate NestedOption present-absent)
;; => true
(= absent present-absent)
;; => false
```

Choice A, variant representation:

1. Tagged literals, `#accepted {...}` (recommended).
2. Tagged vectors.
3. Tag and payload maps.

Choice B, keyword casing:

1. Kebab-case, `:flow-id` (recommended; collisions are detected).
2. Ethos spelling, `:FlowId`.

After the choices: a minimal test fixture, then a knowledge module on how it works in practice, for review.

Ruling: land Proposal 2, with choices A and B.
<!-- to-the-living:end -->
