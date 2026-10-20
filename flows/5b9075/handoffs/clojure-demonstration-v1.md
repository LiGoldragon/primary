# Clojure translation demonstration v1

Status: DRAFT FREEZE. This artifact is a complete, prospective
execution handoff. Every expected result below is unwitnessed. No Clojure,
Malli, install, test, probe, or deployment command has been run.

The demonstration selects tagged EDN literals with lowercase field keywords.
The universal representation is explicitly unapproved: this is a bounded
Clojure and Malli demonstration only. It does not implement a Datom adapter,
and it makes no claim that a typed Datom value can be recovered.

## Frozen dependencies

`deps.edn`:

```clojure
{:paths ["src"]
 :deps {org.clojure/clojure {:mvn/version "1.12.6"}
        metosin/malli {:mvn/version "0.18.0"}}}
```

The future Field runner is a JVM Clojure CLI runner. It must use the frozen
`deps.edn` and invoke the namespace below with `clojure -M -m
clojure-demonstration.core`. No Babashka behavior is assumed. This handoff
contains no installation or execution step.

## Complete namespace

`src/clojure_demonstration/core.clj`:

```clojure
(ns clojure-demonstration.core
  (:require [clojure.edn :as edn]
            [malli.core :as m]))

(def known-tags
  #{:person :accepted :refused :pending :some :none})

(defn tagged
  "Construct a recognized tagged literal.

  Tag recognition is the reader boundary. Payload shape is checked by Malli
  after reading so malformed payloads are reported at the schema layer."
  [tag payload]
  (if (contains? known-tags tag)
    {:tag tag :payload payload}
    (throw (ex-info "unknown tag"
                    {:layer :reader :reason :unknown-tag :tag tag}))))

(def readers
  {'person   (fn [payload] (tagged :person payload))
   'accepted (fn [payload] (tagged :accepted payload))
   'refused  (fn [payload] (tagged :refused payload))
   'pending  (fn [payload] (tagged :pending payload))
   'some     (fn [payload] (tagged :some payload))
   'none     (fn [payload] (tagged :none payload))})

(def PersonPayload
  [:map {:closed true}
   [:name :string]
   [:born :int]])

(def PersonLiteral
  [:map {:closed true}
   [:tag [:enum :person]]
   [:payload PersonPayload]])

(def AcceptedLiteral
  [:map {:closed true}
   [:tag [:enum :accepted]]
   [:payload PersonLiteral]])

(def RefusedLiteral
  [:map {:closed true}
   [:tag [:enum :refused]]
   [:payload :string]])

(def PendingLiteral
  [:map {:closed true}
   [:tag [:enum :pending]]
   [:payload [:vector {:min 0 :max 0} :any]]])

(defn person-literal?
  [value]
  (m/validate PersonLiteral value))

(declare option-literal?)

(def OptionLiteral
  [:and
   [:map {:closed true}
    [:tag [:enum :some :none]]
    [:payload :any]]
   [:fn option-literal?]])

(defn option-literal?
  [value]
  (and (map? value)
       (case (:tag value)
         :none (and (= #{:tag :payload} (set (keys value)))
                    (vector? (:payload value))
                    (empty? (:payload value)))
         :some (and (= #{:tag :payload} (set (keys value)))
                    (or (person-literal? (:payload value))
                        (option-literal? (:payload value))))
         false)))

(def PersonVector
  [:vector PersonLiteral])

(def Value
  [:or PersonLiteral
       AcceptedLiteral
       RefusedLiteral
       PendingLiteral
       PersonVector
       OptionLiteral])

(defn schema-valid?
  [value]
  (m/validate Value value))

(defn explain
  [value]
  (m/explain Value value))

(def eof
  (Object.))

(defn read-one
  "Read exactly one EDN form and reject a trailing second form.

  The first read uses an EOF sentinel. The second read proves that no second
  form remains; whitespace and comments after the first form are allowed."
  [text]
  (with-open [reader (java.io.PushbackReader.
                      (java.io.StringReader. text))]
    (let [value (edn/read {:readers readers :eof eof} reader)]
      (when (identical? eof value)
        (throw (ex-info "expected one EDN form"
                        {:layer :boundary :reason :missing-form})))
      (let [trailing (edn/read {:readers readers :eof eof} reader)]
        (when-not (identical? eof trailing)
          (throw (ex-info "multiple EDN forms"
                          {:layer :boundary
                           :reason :multiple-forms
                           :trailing trailing}))))
      value)))

(defn read-and-validate
  "Read one form, then validate its complete representation with Malli."
  [text]
  (let [value (read-one text)]
    (if (schema-valid? value)
      value
      (throw (ex-info "EDN value failed Malli schema"
                      {:layer :schema
                       :reason :invalid-value
                       :value value
                       :explanation (explain value)})))))

(def fixtures
  [{:name :person
    :edn "#person {:name \"Ada\" :born 1990}"
    :expected :accepted
    :expected-value {:tag :person
                     :payload {:name "Ada" :born 1990}}}
   {:name :accepted
    :edn "#accepted #person {:name \"Ada\" :born 1990}"
    :expected :accepted
    :expected-value {:tag :accepted
                     :payload {:tag :person
                               :payload {:name "Ada" :born 1990}}}}
   {:name :refused
    :edn "#refused \"denied\""
    :expected :accepted
    :expected-value {:tag :refused :payload "denied"}}
   {:name :pending
    :edn "#pending []"
    :expected :accepted
    :expected-value {:tag :pending :payload []}}
   {:name :person-vector
    :edn "[#person {:name \"Ada\" :born 1990} #person {:name \"Grace\" :born 1952}]"
    :expected :accepted
    :expected-value [{:tag :person
                      :payload {:name "Ada" :born 1990}}
                     {:tag :person
                      :payload {:name "Grace" :born 1952}}]}
   {:name :none
    :edn "#none []"
    :expected :accepted
    :expected-value {:tag :none :payload []}}
   {:name :some-none
    :edn "#some #none []"
    :expected :accepted
    :expected-value {:tag :some
                     :payload {:tag :none :payload []}}}
   {:name :some-some-person
    :edn "#some #some #person {:name \"Ada\" :born 1990}"
    :expected :accepted
    :expected-value {:tag :some
                     :payload {:tag :some
                               :payload {:tag :person
                                         :payload {:name "Ada" :born 1990}}}}}

   {:name :missing-field
    :edn "#person {:name \"Ada\"}"
    :expected :rejected
    :layer :schema}
   {:name :extra-field
    :edn "#person {:name \"Ada\" :born 1990 :extra true}"
    :expected :rejected
    :layer :schema}
   {:name :wrong-scalar
    :edn "#person {:name 42 :born 1990}"
    :expected :rejected
    :layer :schema}
   {:name :unknown-tag-reader-rejection
    :edn "#mystery {:name \"Ada\" :born 1990}"
    :expected :rejected
    :layer :reader}
   {:name :known-wrong-tag-schema-rejection
    :edn "#accepted \"Ada\""
    :expected :rejected
    :layer :schema}
   {:name :malformed-payload-schema-rejection
    :edn "#pending {:unexpected true}"
    :expected :rejected
    :layer :schema}
   {:name :malformed-edn-reader-rejection
    :edn "#person {:name \"Ada\" :born 1990"
    :expected :rejected
    :layer :reader}
   {:name :multiple-forms-boundary-rejection
    :edn "#none [] #pending []"
    :expected :rejected
    :layer :boundary}])

(defn run-fixture
  "Prospective table-driven runner for the future Field execution.

  This function is defined but is deliberately not invoked in this handoff."
  [{:keys [name edn expected expected-value layer]}]
  (try
    (let [value (read-and-validate edn)]
      {:name name
       :result (if (and (= expected :accepted)
                        (= value expected-value))
                 :pass
                 :fail)
       :observed :accepted
       :value value})
    (catch clojure.lang.ExceptionInfo error
      (let [data (ex-data error)
            observed-layer (:layer data)]
        {:name name
         :result (if (and (= expected :rejected)
                          (= layer observed-layer))
                   :pass
                   :fail)
         :observed :rejected
         :layer observed-layer
         :reason (:reason data)}))))

(defn run-fixtures
  []
  (mapv run-fixture fixtures))

(defn -main
  [& _]
  (doseq [result (run-fixtures)]
    (prn result)))
```

## Future Field execution contract

From the directory containing the future project, the runner may execute:

```sh
clojure -M -m clojure-demonstration.core
```

That command is prospective only in this handoff. It has not been run. A
future Field result must report the exact Clojure CLI, JVM, namespace, source,
and dependency files used, and must preserve the distinction between reader,
schema, and boundary rejection. The expected table-driven output is not a
witness until that execution occurs.

## Expected fixture layers

The eight positive fixtures are `person`, `accepted`, `refused`, `pending`,
`person-vector`, `none`, `some-none`, and `some-some-person`; each is expected
to pass and recover the explicit tagged EDN value shown in the namespace.

The negative fixtures are expected to reject as follows:

| Fixture | Expected layer |
|---|---|
| missing field | schema |
| extra field | schema |
| wrong scalar | schema |
| unknown tag | reader |
| known wrong tag | schema |
| malformed payload | schema |
| malformed EDN | reader |
| multiple forms | boundary |

All rows are unwitnessed. This artifact does not claim that any row has
passed, that Malli accepted the schema syntax, or that the pinned dependencies
resolved.

## Explicit exclusions

This demonstration does not implement forward or inverse Datom conversion,
Ethos generation, a universal representation, a transport, a Field tool, or a
runtime installation. It does not recover a typed Datom from EDN. Its scope is
one JVM Clojure namespace, EDN reader behavior, closed Malli maps, tagged
variants, nested options, and the stated prospective fixtures.
