## Removed

File: tools/claude-main-flow-launch.mjs (lines as at HEAD; the
working tree already carries other edits to this file)

```diff
- 47: const STARTUP_INSTRUCTION = 'Startup context only: load these skills for the upcoming launch brief. Do not begin that work or write files yet. Reply exactly READY.';
- 132:   return `${skillNames.map(n => `/${n}`).join(' ')} # Startup skills\n\n${STARTUP_INSTRUCTION}\n`;
```

## Added, data

File: config/main-flow/first-prompt.edn

```clojure
{:schema "first-prompt/1"
 :template
 "Topic: {{topic}}

Handover: {{handover}}

Raw psyche records on this topic, each read
with the context of its flow:
{{records}}

Your first response is a crystallization
proposal on this topic, made from these
records."}
```

## Added, code

File: tools/first_prompt.clj (run by bb)

```clojure
(ns first-prompt
  (:require [clojure.edn :as edn]
            [clojure.string :as str]))

(defn- fill [template values]
  (reduce-kv
   (fn [text k v]
     (str/replace text (str "{{" (name k) "}}") v))
   template
   values))

(defn first-prompt
  "The first prompt of a seat, filled from its
  launch record."
  [entry-path launch]
  (let [entry (edn/read-string
               (slurp entry-path))]
    (fill (:template entry)
          {:topic (name (:topic launch))
           :handover (:handover launch)
           :records (->> (:records launch)
                         (map #(str "- " %))
                         (str/join "\n"))})))
```
