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

(defn width-ok? [svg]
  (let [[_ vw] (re-find #"viewBox=\"0 0 ([\d.]+) " svg)
        [_ w] (re-find #" width=\"([\d.]+)\"" svg)
        xs (map #(Double/parseDouble %) (re-seq #"(?<= x=\")[\d.-]+" svg))]
    (and (<= (Double/parseDouble vw) 375) (<= (Double/parseDouble w) 375)
         (every? #(<= 0 % 375) xs))))

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
    (is (every? (fn [[x w]] (<= (+ x w) 375)) rects))))

(deftest edn-figure-fence
  (let [html (book-build/build
              "```figure\n{:nodes [{:id :a :label \"one\"} {:id :b :label \"two\"} {:id :c :label \"three\"}]\n :edges [{:from :a :to :c :verb \"feeds\"} {:from :b :to :c :verb \"feeds\"}]}\n```\n" "")]
    (is (str/starts-with? html "<svg "))
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
    (is (str/starts-with? html "<svg "))
    (is (not (str/includes? html "textblock")))))

(deftest chain-keeps-former-drawing
  (let [content (sketch chain)]
    (is (= (book-build/svg-figure content) (book-build/figure-svg content content)))))

(let [{:keys [fail error]} (run-tests 'book-build-graph-test)]
  (System/exit (if (zero? (+ fail error)) 0 1)))
