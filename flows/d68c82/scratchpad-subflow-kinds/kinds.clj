(ns kinds
  (:require [clojure.edn :as edn]
            [malli.core :as m]))

(defn variant [tag schema]
  (let [valid? (m/validator schema)]
    [:fn (fn [value]
           (and (tagged-literal? value)
                (= tag (:tag value))
                (valid? (:form value))))]))

(defn unit-enum [tags]
  (into [:or]
        (map #(variant % [:tuple]))
        tags))

(def aspects '[psyche mind field])

(def roles
  '[explorer worker tester reviewer
    publisher operator researcher])

(def levels '[secondary tertiary quaternary])

(def Aspect (unit-enum aspects))
(def Role (unit-enum roles))
(def Level (unit-enum levels))

(def Kind
  [:map {:closed true}
   [:aspect Aspect]
   [:role Role]
   [:level Level]])

(defn read-value [text]
  (edn/read-string {:default tagged-literal}
                   text))

(def good
  (str "{:aspect #field [] :role #operator []"
       " :level #tertiary []}"))

(def bad
  (str "{:aspect #field [] :role #operator []"
       " :level #primary []}"))

(doseq [text [good bad]]
  (println text "=>"
           (m/validate Kind
                       (read-value text))))
