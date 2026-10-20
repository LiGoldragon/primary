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

(println (m/validate Reply accepted))

(println (m/validate Reply
  (read-example
    "#accepted {:name \"Ada\" :age \"36\"}")))


(defn option-schema [payload]
  [:or (variant 'none [:tuple])
       (variant 'some payload)])

(def NestedOption
  (option-schema (option-schema Person)))
(def absent (read-example "#none []"))
(def present-absent
  (read-example "#some #none []"))

(println (m/validate NestedOption absent))

(println (m/validate NestedOption present-absent))

(println (= absent present-absent))
