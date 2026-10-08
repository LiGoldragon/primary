(ns tool.main
  (:require [clojure.edn :as edn] [malli.core :as m])
  (:gen-class))
(def Input [:tuple [:= 'status] [:int {:min 1 :max 50}]])
(def Output [:vector :keyword])
(defn -main [& [arg]]
  (let [in (edn/read-string arg)]
    (if (m/validate Input in)
      (let [out (vec (take (second in) [:ok :ok :ok]))]
        (assert (m/validate Output out))
        (prn out))
      (do (prn [:refused (m/explain Input in)]) (System/exit 1)))))
