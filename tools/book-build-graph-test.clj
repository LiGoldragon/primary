;; Tests for the graph figures of tools/book-build.clj.
;; Run: bb tools/book-build-graph-test.clj
(ns book-build-graph-test
  (:require [clojure.test :refer [deftest is run-tests]]
            [clojure.string :as str]
            [babashka.fs :as fs]))

(def tools-dir (str (fs/parent (fs/absolutize *file*))))
(load-file (str (fs/path tools-dir "book-build.clj")))

(defn sketch [s] (str/split-lines s))
(defn graph [s] (book-build/ascii-graph (sketch s)))
(defn svg [s] (book-build/graph-svg (graph s)))
(defn edges [g] (set (map (juxt :from :to :verb) (:edges g))))
(defn labels [g] (into {} (map (juxt :id :label) (:nodes g))))

(defn texts
  "Every text drawn in an SVG, unescaped, joined by spaces."
  [svg]
  (->> (re-seq #"<text[^>]*>([^<]*)</text>" svg)
       (map second)
       (map #(-> % (str/replace "&lt;" "<") (str/replace "&gt;" ">") (str/replace "&quot;" "\"")
                 (str/replace "&#x27;" "'") (str/replace "&amp;" "&")))
       (str/join " ")))

(defn words [s] (remove #(= "" %) (str/split s #"\s+")))

(defn all-words-drawn?
  "Every word of every label, note and verb is drawn, as often as written; a
  verb shared by the edges of one fork or join counts once."
  [g svg]
  (let [want (frequencies (mapcat words (concat (keep identity (mapcat (juxt :label :note) (:nodes g)))
                                                (distinct (keep :verb (:edges g))))))
        got (frequencies (words (texts svg)))]
    (every? (fn [[w n]] (>= (get got w 0) n)) want)))

(defn width-ok?
  "Drawn at the width it is shown at, at most w, with everything inside."
  ([svg] (width-ok? svg book-build/fig-w))
  ([svg w]
   (let [[_ vw] (re-find #"viewBox=\"0 0 ([\d.]+) " svg)
         [_ sw] (re-find #" width=\"([\d.]+)\"" svg)
         xs (map #(Double/parseDouble %) (re-seq #"(?<= x=\")[\d.-]+" svg))]
     (and (= vw sw) (<= (Double/parseDouble vw) w)
          (every? #(<= 0 % w) xs)))))

(defn font-sizes [svg] (map #(Double/parseDouble (second %)) (re-seq #"font-size=\"([\d.]+)\"" svg)))

(defn rects
  "Verb backdrops (no rx) and boxes (rx), as [x0 y0 x1 y1]."
  [svg]
  (let [r (fn [m] (let [[x y w h] (map #(Double/parseDouble %) (rest m))] [x y (+ x w) (+ y h)]))
        all (re-seq #"<rect x=\"([\d.-]+)\" y=\"([\d.-]+)\" width=\"([\d.]+)\" height=\"([\d.]+)\"([^>]*)>" svg)]
    {:verbs (map #(r (butlast %)) (remove #(str/includes? (last %) "rx=") all))
     :boxes (map #(r (butlast %)) (filter #(str/includes? (last %) "rx=") all))}))

(defn segments [svg]
  (mapcat (fn [[_ d]]
            (let [pts (partition 2 (map #(Double/parseDouble %) (re-seq #"[\d.-]+" d)))]
              (partition 2 1 pts)))
          (re-seq #"<path d=\"([^\"]+)\"" svg)))

(defn under?
  "A segment crossing the inside of a rectangle."
  [[[x1 y1] [x2 y2]] [a b c d]]
  (let [e 0.6]
    (and (< (+ a e) (max x1 x2)) (< (min x1 x2) (- c e))
         (< (+ b e) (max y1 y2)) (< (min y1 y2) (- d e)))))

(defn hidden-lines
  "Segments under a box, or under a verb other than the verb's own line, a
  vertical through its middle."
  [svg]
  (let [{:keys [verbs boxes]} (rects svg)
        own? (fn [[[x1 _] [x2 _]] [a _ c _]] (and (== x1 x2) (< (Math/abs (- x1 (/ (+ a c) 2))) 0.6)))]
    (concat (for [s (segments svg) r boxes :when (under? s r)] [:box s r])
            (for [s (segments svg) r verbs :when (and (under? s r) (not (own? s r)))] [:verb s r]))))

(def chain
  "+-----------+
| asks      |
+-----------+
     | sends to
     v
+-----------+
| answers   |
+-----------+")

(def fork
  "      +-----------+
      | guard     |
      +-----------+
            |
     +------+-------+
     | under        | over
     v              v
+---------+    +---------+
| refuses |    | compacts|
+---------+    +---------+")

(def join
  "+--------+   +--------+
| psyche |   | mind   |
+--------+   +--------+
     |            |
     | reads      | writes
     v            v
   +----------------+
   | field          |
   +----------------+")

(def diamond
  "      +---------+
      | comment |
      +---------+
        |     |
  rules a     asks
        v     v
+--------+  +---------+
| vision |  | inquiry |
+--------+  +---------+
     \\          /
      \\ lands  /
       v      v
     +----------+
     | module   |
     +----------+")

(deftest ascii-to-edn-chain
  (is (= {:nodes [{:id "n1" :label "asks"} {:id "n2" :label "answers"}]
          :edges [{:from "n1" :to "n2" :verb "sends to"}]}
         (graph chain))))

(deftest ascii-to-edn-fork
  (let [g (graph fork) l (labels g)]
    (is (= {"n1" "guard" "n2" "refuses" "n3" "compacts"} l))
    (is (= #{["n1" "n2" "under"] ["n1" "n3" "over"]} (edges g)))))

(deftest ascii-to-edn-join
  (let [g (graph join)]
    (is (= {"n1" "psyche" "n2" "mind" "n3" "field"} (labels g)))
    (is (= #{["n1" "n3" "reads"] ["n2" "n3" "writes"]} (edges g)))))

(deftest ascii-to-edn-diamond
  (let [g (graph diamond)]
    (is (= {"n1" "comment" "n2" "vision" "n3" "inquiry" "n4" "module"} (labels g)))
    (is (= #{["n1" "n2" "rules a"] ["n1" "n3" "asks"] ["n2" "n4" "lands"] ["n3" "n4" "lands"]}
           (edges g))
        "a verb between two lines that meet is the verb of both")))

(deftest ascii-to-edn-bare-text-and-side-arrow
  (is (= {:nodes [{:id "n1" :label "the living speaks" :bare true} {:id "n2" :label "proposal"}]
          :edges [{:from "n1" :to "n2"}]}
         (graph " the living speaks
        |
        v
 +--------------+
 | proposal     |
 +--------------+")))
  (is (= #{["n1" "n2" nil]}
         (edges (graph "+----------+     +----------+
| proposal |---->| you rule |
+----------+     +----------+")))))

(deftest ascii-to-edn-box-drawing-glyphs
  (is (= {:nodes [{:id "n1" :label "Asleep"} {:id "n2" :label "Awake"}]
          :edges [{:from "n1" :to "n2" :verb "is woken"}]}
         (graph "┌────────┐
│ Asleep │
└───┬────┘
    │ is woken
    ▼
┌────────┐
│ Awake  │
└────────┘"))))

(deftest sketch-read-in-part-is-not-drawn
  (is (nil? (graph "+----------+
| outer    |
| +------+ |
| | in   | |
| +------+ |
+----------+
     |
     v
+----------+
| next     |
+----------+")) "a box inside a box")
  (is (nil? (graph "+----------+
| proposal |---->| you rule |
+----------+")) "an arrow to no box"))

(deftest table-is-not-a-figure
  (is (nil? (book-build/figure-svg ["+---+---+" "| a | b |" "+---+---+"]
                                   ["+---+---+" "| a | b |" "+---+---+"]))))

(deftest every-label-drawn-and-width
  (doseq [s [chain fork join diamond]
          :let [g (graph s) out (book-build/graph-svg g)]]
    (is (all-words-drawn? g out) s)
    (is (width-ok? out) s)
    (is (= (count (:nodes g)) (count (re-seq #"<rect [^>]*rx=" out))) "one box per node")
    (is (= (count (:edges g)) (count (re-seq #"<polygon" out))) "one arrowhead per edge")))

(deftest verbs-drawn-once-at-a-join
  (let [out (svg diamond)]
    (is (= 1 (count (re-seq #">lands</text>" out))))
    (is (= 1 (count (re-seq #">rules a</text>" out))))
    (is (= 1 (count (re-seq #">asks</text>" out))))))

(deftest colours-from-page-tokens
  (let [out (svg diamond)]
    (is (str/includes? out "var(--fg"))
    (is (str/includes? out "var(--muted"))
    (is (str/includes? out "var(--sheet"))
    (is (not (re-find #"#[0-9a-fA-F]{3,6}" out)))))

(deftest long-labels-wrap-inside-boxes
  (let [g {:nodes [{:id :a :label "a rather long label that cannot sit on one line in a narrow box"}
                   {:id :b :label "b"} {:id :c :label "c"} {:id :d :label "d"}]
           :edges [{:from :a :to :b :verb "a verb long enough to need wrapping in its column"}
                   {:from :a :to :c} {:from :a :to :d}]}
        out (book-build/graph-svg g)
        rects (map (fn [[_ x w]] [(Double/parseDouble x) (Double/parseDouble w)])
                   (re-seq #"<rect x=\"([\d.]+)\" y=\"[\d.]+\" width=\"([\d.]+)\"[^>]*rx=" out))]
    (is (all-words-drawn? g out))
    (is (width-ok? out))
    (is (< 1 (count (re-seq #"font-size=\"14\"[^>]*>a |font-size=\"14\"[^>]*>[^<]*line" out))))
    (is (every? (fn [[x w]] (<= (+ x w) book-build/fig-w)) rects))))

(deftest edn-figure-fence
  (let [html (book-build/build
              "```figure\n{:nodes [{:id :a :label \"one\"} {:id :b :label \"two\"} {:id :c :label \"three\"}]\n :edges [{:from :a :to :c :verb \"feeds\"} {:from :b :to :c :verb \"feeds\"}]}\n```\n" "")]
    (is (str/starts-with? html "<div class=\"figure\"><svg "))
    (is (= 1 (count (re-seq #">feeds</text>" html))) "a shared verb is drawn once")))

(deftest cycle-and-self-loop
  (let [g {:nodes [{:id 1 :label "x"} {:id 2 :label "y"}]
           :edges [{:from 1 :to 2 :verb "go"} {:from 2 :to 1 :verb "back"} {:from 2 :to 2}]}
        out (book-build/graph-svg g)]
    (is (all-words-drawn? g out))
    (is (width-ok? out))
    (is (= 3 (count (re-seq #"<polygon" out))))))

(deftest branching-text-fence-draws-svg
  (let [html (book-build/build (str "```text\n" join "\n```\n") "")]
    (is (str/starts-with? html "<div class=\"figure\"><svg "))
    (is (not (str/includes? html "textblock")))))

(def nexus-launch
  "Figure 1 of flows/55a2b4/books/15-flow-nexus-whole.md."
  {:nodes [{:id "n1" :label "the CLI"} {:id "n2" :label "Signal"} {:id "n3" :label "Operation"}
           {:id "n4" :label "Memory"} {:id "n5" :label "a new\nflow"} {:id "n6" :label "Refused, answered to the CLI"}]
   :edges [{:from "n1" :to "n2" :verb "sends Launch"} {:from "n2" :to "n6" :verb "refuses OffRoute or NoSecondary"}
           {:from "n2" :to "n3" :verb "intends Compose"} {:from "n3" :to "n4" :verb "reads the Metaflow in"}
           {:from "n3" :to "n5" :verb "Asleep: starts"}
           {:from "n3" :to "n6" :verb "refuses Busy if Awake, ChangedModule if a hash differs"}]})

(def subflows
  "The opening figure of flows/d68c82/books/16-subflows.md."
  "+------------+        +--------------------+
| the living |        |  context modules   |
+------------+        +--------------------+
      |                   |               |
      | speaks to         | shape         | shape
      v                   v               |
+-------------------------------+         |
|           main flow           |         |
+-------------------------------+         |
   |                |        |            |
   | asks           | writes | briefs     |
   v                |        v            v
+----------------+  |      +----------------+
| contextualizer |  |      |    subflow     |
+----------------+  |      +----------------+
   |                |               |
   | names the      |               | judges
   | context for    |               | and does
   v                v               v
+-----------------------+      +----------+
|      psyche log       |      | the work |
+-----------------------+      +----------+")

(deftest no-line-under-a-verb-or-box
  ;; a long edge passing a rank whose fork carries wide verbs
  (doseq [g [nexus-launch (graph subflows) (graph diamond) (graph fork) (graph join)
             {:nodes [{:id 1 :label "Primary, in each aspect"} {:id 2 :label "Secondary, the Primary's secretary"}
                      {:id 3 :label "Tertiary"} {:id 4 :label "Quaternary"}]
              :edges [{:from 1 :to 2 :verb "any layer down, across aspects too"} {:from 2 :to 3} {:from 3 :to 4}
                      {:from 2 :to 1 :verb "one layer up, own aspect"} {:from 3 :to 2 :verb "one layer up, own aspect"}
                      {:from 4 :to 3 :verb "one layer up, own aspect"}]}]
          :let [out (book-build/graph-svg g)]]
    (is (empty? (hidden-lines out)) (pr-str (:edges g)))
    (is (all-words-drawn? g out))
    (is (width-ok? out))))

(deftest text-at-least-12px-on-a-320px-page
  ;; a figure is drawn 1:1 at the width of a proposal on a 320px page, or of
  ;; a ruling inside it, so no text is scaled below its size
  (is (= 254 book-build/fig-w))
  (is (= 181 book-build/ruling-fig-w))
  (doseq [g [nexus-launch (graph subflows) (graph diamond) (graph chain)]
          :let [out (book-build/graph-svg g)]]
    (is (width-ok? out 254))
    (is (every? #(>= % 12) (font-sizes out))))
  (let [html (book-build/build (str "### Proposal 1: x\n\nRuling, one number per line:\n\n```text\n" fork "\n```\n") "")
        svg (re-find #"(?s)<svg .*?</svg>" html)]
    (is (str/includes? html "<li value=\"1\">"))
    (is (width-ok? svg 181) "a figure in a ruling is drawn at the ruling's width")))

(deftest every-figure-in-its-wrapper
  (doseq [html [(book-build/build (str "# T\n\n```text\n" subflows "\n```\n\n## Next\n") "")
                (book-build/build (str "```figure\n" (pr-str nexus-launch) "\n```\n") "")
                (book-build/build (str "```text\n" chain "\n```\n") "")]]
    (is (re-find #"(?s)<div class=\"figure\"><svg [^>]*>.*?</svg></div>" html))
    (is (= (count (re-seq #"<svg " html)) (count (re-seq #"<div class=\"figure\"><svg " html))))))

(deftest words-never-split
  (is (= ["ChangedModule" "if a"] (book-build/wrap "ChangedModule if a" 4)))
  (doseq [g [(graph subflows) nexus-launch
             {:nodes [{:id 1 :label "contextualizer"} {:id 2 :label "a"} {:id 3 :label "subflow"}
                      {:id 4 :label "metaflowcontextualizers"} {:id 5 :label "b"}]
              :edges [{:from 2 :to 1 :verb "writes"} {:from 2 :to 3 :verb "subflowsubflow"}
                      {:from 2 :to 4} {:from 2 :to 5}]}]
          :let [out (book-build/graph-svg g)
                drawn (set (words (texts out)))]]
    (is (every? drawn (mapcat words (keep identity (concat (map :label (:nodes g)) (map :verb (:edges g))))))
        "every word drawn whole")))

(let [{:keys [fail error]} (run-tests 'book-build-graph-test)]
  (System/exit (if (zero? (+ fail error)) 0 1)))
