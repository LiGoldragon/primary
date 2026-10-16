#!/usr/bin/env bb
;; Build a book page from its Markdown source.
;;
;; usage: bb tools/book-build.clj SOURCE.md OUT.html [--code tools/book-code.html] [--figures DIR]
;;
;; The source is a book in the to-the-living form: a title, a
;; Crystallization heading, proposals (### Proposal N: title), File:
;; lines, fenced text as red/green/context panels, fenced code as code
;; blocks, and numbered rulings. An ASCII box-and-arrow diagram in an unlabelled
;; fence, and every unlabelled fence outside a proposal, boxed or not, is a
;; diagram; it is never drawn: the n-th diagram needs fig-n.svg in the --figures
;; directory, else the build refuses with a one-line error and exit 1. A paragraph opening with
;; **Destroy** or **Archive** wraps the record that follows in a
;; record panel of that class. The page code (tools/book-code.html) is
;; appended whole.
(ns book-build
  (:require [clojure.string :as str]
            [clojure.edn]
            [babashka.fs :as fs]))

(def box-font "IBM Plex Sans Condensed, Arial Narrow, system-ui, sans-serif")
(def label-font "JetBrains Mono, ui-monospace, DejaVu Sans Mono, monospace")
(def langs {"js" "javascript"})
(def script-dir (str (fs/parent (fs/absolutize *file*))))

;; ------------------------------------------------------------- text helpers

(def ^:private ws "(?U)[\\s\\x1c-\\x1f]")
(def ^:private ws-left (re-pattern (str "^" ws "+")))
(def ^:private ws-right (re-pattern (str ws "+$")))

(defn rstrip [s] (str/replace s ws-right ""))
(defn strip-left [s] (str/replace s ws-left ""))
(defn strip [s] (-> s (str/replace ws-left "") rstrip))
(defn blank? [s] (= "" (strip s)))

(defn cp-count [^String s] (.codePointCount s 0 (.length s)))

(defn esc [s]
  (-> s (str/replace "&" "&amp;") (str/replace "<" "&lt;") (str/replace ">" "&gt;")))

(defn esc-attr [s]
  (-> (esc s) (str/replace "\"" "&quot;") (str/replace "'" "&#x27;")))

(defn num [x]
  (let [x (/ (Math/rint (* 100 (double x))) 100)]
    (if (== x (Math/floor x)) (str (long x)) (str x))))

(defn inline
  "Escape text; turn `code` into <code> and **bold** into <strong>."
  [text]
  (let [m (re-matcher #"`([^`]+)`" text)
        sb (StringBuilder.)
        esc (fn [t] (str/replace (esc t) #"\*\*(?=\S)(.+?)(?<=\S)\*\*" "<strong>$1</strong>"))]
    (loop [pos 0]
      (if (.find m)
        (do (.append sb (esc (subs text pos (.start m))))
            (.append sb (str "<code>" (esc (.group m 1)) "</code>"))
            (recur (.end m)))
        (do (.append sb (esc (subs text pos)))
            (str sb))))))

(defn join-lines [lines]
  (str/join " " (keep #(let [t (strip %)] (when (not= "" t) t)) lines)))

;; ------------------------------------------------------------ graph figures
;;
;; Any box-and-arrow sketch is read cell by cell into an EDN graph,
;;   {:nodes [{:id "n1" :label "his comment"} ...]
;;    :edges [{:from "n1" :to "n2" :verb "rules a line"} ...]}
;; a node may also carry :note (free text beside its box) or :bare true (an
;; unboxed text that a line starts or ends at). A ```figure fence may give the
;; graph directly as EDN. The graph is only read, to tell a
;; diagram from code; the build never draws it. A diagram's figure is the
;; illustrator's fig-N.svg.

(def ^:private box-drawing
  (merge (zipmap (map str "┌┐└┘├┤┬┴┼╭╮╰╯") (repeat "+"))
         {"─" "-" "│" "|" "▼" "v" "▲" "^" "▶" ">" "◀" "<" "►" ">" "◄" "<"}))

(defn char-grid
  "Lines as rows of code points; box-drawing glyphs read as their ASCII."
  [lines]
  (mapv #(mapv (fn [ch] (box-drawing ch ch)) (re-seq #"(?s)." (rstrip %))) lines))

(defn at [g r c] (or (get-in g [r c]) " "))

(def ^:private edge-chars #{"-" "+" "v" "^"})

(defn- box-at
  "The box whose top-left corner is at r c, or nil."
  [g r c]
  (when (and (= "+" (at g r c)) (#{"|" "+"} (at g (inc r) c)))
    (some (fn [c2]
            (when (and (= "+" (at g r c2)) (#{"|" "+"} (at g (inc r) c2))
                       (not= "+" (at g (inc r) c) (at g (inc r) c2)))
              (loop [r2 (+ r 2)]
                (let [a (at g r2 c) b (at g r2 c2)]
                  (cond
                    (and (= "+" a) (= "+" b) (every? #(edge-chars (at g r2 %)) (range c (inc c2))))
                    {:r0 r :c0 c :r1 r2 :c1 c2}
                    (and (#{"|" "+"} a) (#{"|" "+"} b)) (recur (inc r2))
                    :else nil)))))
          (take-while #(edge-chars (at g r %)) (range (inc c) (count (get g r)))))))

(defn- find-boxes [g]
  (reduce (fn [boxes [r c]]
            (if (some #(and (<= (:r0 %) r (:r1 %)) (<= (:c0 %) c (:c1 %))) boxes)
              boxes
              (if-let [b (box-at g r c)] (conj boxes b) boxes)))
          [] (for [r (range (count g)) c (range (count (g r)))] [r c])))

(defn- box-text [g {:keys [r0 c0 r1 c1]}]
  (->> (range (inc r0) r1)
       (map (fn [r] (strip (apply str (map #(at g r %) (range (inc c0) c1))))))
       (remove #(= "" %))
       (str/join "\n")))

(defn- owned-cells
  "Cell -> box index; an arrowhead in a box border stays a connector."
  [g boxes]
  (into {}
        (for [[i {:keys [r0 c0 r1 c1]}] (map-indexed vector boxes)
              r (range r0 (inc r1)) c (range c0 (inc c1))
              :let [ch (at g r c)]
              :when (not (or (and (= r r0) (< c0 c c1) (= ch "v"))
                             (and (= r r1) (< c0 c c1) (= ch "^"))
                             (and (= c c0) (< r0 r r1) (= ch ">"))
                             (and (= c c1) (< r0 r r1) (= ch "<"))))]
          [[r c] i])))

(defn- letter? [s] (boolean (re-matches #"(?U)[\p{L}\p{N}]" s)))

(def ^:private horizontal #{"-" "+" "<" ">"})

(defn- conn-char
  "The connector at r c, or nil. A dash ending its run over or under a
  vertical line is a corner."
  [g owned r c]
  (when-not (owned [r c])
    (let [ch (at g r c) l (at g r (dec c)) rt (at g r (inc c))
          side? #(or (horizontal (at g r %)) (owned [r %]))]
      (case ch
        ("|" "+") ch
        "-" (when (or (horizontal l) (horizontal rt) (owned [r (dec c)]) (owned [r (inc c)]))
              (if (and (not (and (horizontal l) (horizontal rt)))
                       (not (and (side? (dec c)) (side? (inc c))))
                       (or (#{"|" "v" "^"} (at g (dec r) c)) (#{"|" "v" "^"} (at g (inc r) c))))
                "+" "-"))
        ("v" "^" "\\" "/") (when-not (or (letter? l) (letter? rt)) ch)
        "<" (when (= "-" rt) ch)
        ">" (when (= "-" l) ch)
        nil))))

(def ^:private dirs
  {"|" [[-1 0] [1 0]] "-" [[0 -1] [0 1]] "+" [[-1 0] [1 0] [0 -1] [0 1]]
   "v" [[-1 0] [1 0]] "^" [[-1 0] [1 0]] ">" [[0 -1] [0 1]] "<" [[0 -1] [0 1]]
   "\\" [[-1 -1] [1 1]] "/" [[-1 1] [1 -1]]})

(def ^:private points {"v" [1 0] "^" [-1 0] ">" [0 1] "<" [0 -1]})

(defn- step [[r c] [dr dc] k] [(+ r (* k dr)) (+ c (* k dc))])
(defn- neg [[dr dc]] [(- dr) (- dc)])
(defn- diag? [[dr dc]] (and (not= 0 dr) (not= 0 dc)))
(defn- has? [ch d] (some #(= d %) (dirs ch)))

(defn- metric [[r1 c1] [r2 c2]]
  (let [dr (* 2 (- r1 r2)) dc (- c1 c2)] (+ (* dr dr) (* dc dc))))

(defn- min-metric [as bs]
  (reduce min Long/MAX_VALUE (for [a as b bs] (metric a b))))

(defn- label-blocks
  "Runs of text outside boxes and connectors, two spaces apart, gathered
  into blocks of runs starting in one column on consecutive rows."
  [g owned conn]
  (let [text? (fn [r c] (and (not (owned [r c])) (not (conn [r c])) (not= " " (at g r c))))
        runs (for [r (range (count g))
                   run (loop [c 0 runs [] cur nil]
                         (if (>= c (count (g r)))
                           (cond-> runs cur (conj cur))
                           (cond
                             (text? r c) (recur (inc c) runs (if cur (assoc cur 1 c) [c c]))
                             (and cur (= " " (at g r c)) (text? r (inc c)) (not (conn [r c])))
                             (recur (inc c) runs cur)
                             :else (recur (inc c) (cond-> runs cur (conj cur)) nil))))]
               {:r r :c0 (first run) :c1 (second run)
                :text (apply str (map #(at g r %) (range (first run) (inc (second run)))))})]
    (mapv (fn [rs] {:runs rs
                    :text (str/join "\n" (map :text rs))
                    :cells (set (for [{:keys [r c0 c1]} rs c (range c0 (inc c1))] [r c]))})
          (reduce (fn [blocks run]
                    (if-let [k (first (keep-indexed
                                       (fn [k rs]
                                         (let [p (peek rs)]
                                           (when (and (= (:r p) (dec (:r run)))
                                                      (<= (Math/abs (- (:c0 p) (:c0 run))) 1))
                                             k)))
                                       blocks))]
                      (update blocks k conj run)
                      (conj blocks [run])))
                  [] runs))))

(defn ascii-graph
  "The EDN graph of an ASCII sketch; nil when it holds no box, nests a box,
  or has a line joining no two nodes."
  [lines]
  (let [g (char-grid lines)
        boxes (find-boxes g)]
    (when (seq boxes)
      (let [owned (owned-cells g boxes)
            conn (into {} (for [r (range (count g)) c (range (count (g r)))
                                :let [ch (conn-char g owned r c)] :when ch]
                            [[r c] ch]))
            blocks (label-blocks g owned conn)
            block-of (into {} (for [[i b] (map-indexed vector blocks) p (:cells b)] [p i]))
            ;; links, attachments to boxes, and loose ends of every connector
            scan (for [[p ch] conn d (dirs ch)
                       :let [q (step p d 1)]]
                   (cond
                     (owned q) [:attach p {:node [:box (owned q)] :cell p :arrow? (= d (points ch))}]
                     (and (conn q) (or (has? (conn q) (neg d)) (diag? d))) [:link p q]
                     (conn q) nil
                     :else
                     (let [far (when (#{"|" "v" "^" "\\" "/"} ch)
                                 (some (fn [k]
                                         (let [s (step p d k)]
                                           (cond
                                             (owned s) [:attach p {:node [:box (owned s)] :cell p
                                                                   :arrow? (= d (points ch))}]
                                             (and (conn s) (has? (conn s) (neg d))) [:link p s]
                                             :else nil)))
                                       [2 3]))]
                       (or far
                           (let [b (when-not (or (diag? d) (= ch "+"))
                                     (some #(block-of (step p d %)) [1 2]))]
                             (if b
                               [:attach p {:node [:text b] :cell p :arrow? (= d (points ch))}]
                               [:loose p d]))))))
            scan (remove nil? scan)
            adj (reduce (fn [m [kind p q]]
                          (if (= kind :link) (-> m (update p (fnil conj #{}) q) (update q (fnil conj #{}) p)) m))
                        {} scan)
            comp-of (reduce (fn [m p]
                              (if (m p)
                                m
                                (loop [m (assoc m p p) todo [p]]
                                  (if-let [x (peek todo)]
                                    (let [nx (remove m (adj x))]
                                      (recur (reduce #(assoc %1 %2 p) m nx) (into (pop todo) nx)))
                                    m))))
                            {} (sort (keys conn)))
            attaches (group-by (comp comp-of :cell) (keep (fn [[k _ a]] (when (= k :attach) a)) scan))
            loose (group-by (comp comp-of second) (filter #(= :loose (first %)) scan))
            cells-of (group-by comp-of (keys conn))
            targeted? (fn [k] (some :arrow? (attaches k)))
            ;; a line that starts at a box and stops short of any joins the
            ;; nearest arrowed line it runs toward
            merged (reduce
                    (fn [m k]
                      (if (or (targeted? k) (empty? (attaches k)) (< 1 (count (distinct (map :node (attaches k))))))
                        m
                        (let [ends (loose k)
                              cands (for [[_ p d] ends
                                          j (keys cells-of) :when (and (not= j k) (targeted? j))
                                          q (cells-of j)
                                          :let [[dr dc] (map - q p)]
                                          :when (and (>= (* dr (first d)) 0) (>= (* dc (second d)) 0))]
                                      [(metric p q) j])]
                          (if (seq cands) (assoc m k (second (apply min-key first cands))) m))))
                    {} (keys cells-of))
            root (fn [k] (get merged k k))
            comps (group-by root (keys cells-of))
            text-nodes (set (keep (fn [[k _ a]] (when (and (= k :attach) (= :text (first (:node a))))
                                                  (second (:node a))))
                                  scan))
            edges-of
            (into {}
                  (for [[k ks] comps
                        :let [ats (mapcat attaches ks)
                              tg (distinct (map :node (filter :arrow? ats)))
                              src (remove (set tg) (distinct (map :node ats)))
                              [src tg] (if (seq tg)
                                         [src tg]
                                         (let [ordered (distinct (map :node (sort-by :cell ats)))]
                                           [(take 1 ordered) (rest ordered)]))
                              cells-for (fn [n] (set (map :cell (filter #(= n (:node %)) ats))))]
                        :when (and (seq tg) (seq src))]
                    [k (vec (for [s src t tg]
                              {:from s :to t
                               :keys (into (if (< 1 (count src)) (cells-for s) #{})
                                           (when (< 1 (count tg)) (cells-for t)))}))]))
            conn-cells (keys conn)
            near? (fn near?
                    ([b] (near? b conn-cells))
                    ([b cells] (some (fn [[r c]] (some (fn [[r2 c2]] (and (<= (Math/abs (- r r2)) 1)
                                                                          (<= (Math/abs (- c c2)) 3)))
                                                       cells))
                                     (:cells b))))
            labels (for [[i b] (map-indexed vector blocks) :when (not (text-nodes i))] [i b])
            ;; a verb is on the line just left of it, else its nearest line,
            ;; or on every line it touches when those lines join at one node
            verb-blocks (for [[i b] labels
                              :when (near? b)
                              :let [left (some (fn [{:keys [r c0]}]
                                                 (some #(when (conn [r %]) [r %]) [(dec c0) (- c0 2)]))
                                               (:runs b))
                                    k (root (comp-of (or left (apply min-key #(min-metric (:cells b) [%]) conn-cells))))
                                    touching (distinct (filter edges-of (map (comp root comp-of) (filter #(near? b [%]) conn-cells))))
                                    es (mapcat edges-of touching)
                                    meet? (and (< 1 (count touching)) (apply = (map :to es)))]
                              k (if meet? touching (when (edges-of k) [k]))]
                          [k i (cond-> b left (assoc :left left))])
            note-blocks (remove (set (map second verb-blocks)) (map first labels))
            ;; verbs: one label on a line is the verb of all its edges
            verbs (reduce
                   (fn [m [k bs]]
                     (let [es (edges-of k)]
                       (if (or (= 1 (count es)) (= 1 (count bs)))
                         (reduce (fn [m e] (assoc m [k e] (str/join " " (map #(str/replace (:text (nth % 2)) "\n" " ") bs))))
                                 m es)
                         (reduce (fn [m [_ _ b]]
                                   (let [e (apply min-key #(min-metric (if-let [l (:left b)] [l] (:cells b)) (:keys %)) es)
                                         t (str/replace (:text b) "\n" " ")]
                                     (update m [k e] #(if % (str % " " t) t))))
                                 m (sort-by (fn [[_ _ b]] (first (sort (:cells b)))) bs)))))
                   {} (group-by first verb-blocks))
            node-keys (concat (map #(vector :box %) (range (count boxes)))
                              (map #(vector :text %) (sort text-nodes)))
            pos (fn [[kind i]] (if (= kind :box)
                                 [(:r0 (boxes i)) (:c0 (boxes i))]
                                 (first (sort (:cells (blocks i))))))
            node-keys (sort-by pos node-keys)
            ids (zipmap node-keys (map #(str "n" (inc %)) (range)))
            box-cells (fn [i] (let [{:keys [r0 c0 r1 c1]} (boxes i)]
                                (for [r [r0 r1] c (range c0 (inc c1))] [r c])))
            notes (group-by (fn [i] (apply min-key
                                           #(min-metric (:cells (blocks i)) (box-cells %))
                                           (range (count boxes))))
                            note-blocks)
            ;; a note standing wholly above its box's top row titles the box
            above? (fn [bi i] (< (apply max (map first (:cells (blocks i)))) (:r0 (boxes bi))))]
        ;; a sketch read only in part is not drawn: a box inside a box, or
        ;; a line that joins no two nodes
        (when-not (or (some #(re-find #"[+|]-{3,}|-{3,}[+|]" (box-text g %)) boxes)
                      (some (fn [[k ks]] (and (not (edges-of k)) (< 1 (count (mapcat cells-of ks)))))
                            comps))
        {:nodes (vec (for [[kind i :as nk] node-keys]
                       (cond-> {:id (ids nk)
                                :label (if (= kind :box) (box-text g (boxes i)) (:text (blocks i)))}
                         (= kind :text) (assoc :bare true)
                         (and (= kind :box) (seq (filter #(above? i %) (notes i))))
                         (assoc :title (str/join "\n" (map #(:text (blocks %)) (sort-by #(pos [:text %]) (filter #(above? i %) (notes i))))))
                         (and (= kind :box) (seq (remove #(above? i %) (notes i))))
                         (assoc :note (str/join "\n" (map #(:text (blocks %)) (sort-by #(pos [:text %]) (remove #(above? i %) (notes i)))))))))
         :edges (vec (for [[k es] (sort-by key edges-of) e es
                           :let [v (verbs [k e])]]
                       (cond-> {:from (ids (:from e)) :to (ids (:to e))}
                         v (assoc :verb v))))})))))

(defn read-figure
  "A ```figure fence: an EDN graph, or an ASCII sketch."
  [lines]
  (let [src (str/join "\n" lines)
        g (if (str/starts-with? (strip src) "{")
            (clojure.edn/read-string src)
            (ascii-graph lines))
        ids (set (map :id (:nodes g)))]
    (when-not (seq (:nodes g))
      (throw (ex-info (str "figure has no node: " (pr-str src)) {})))
    (doseq [{:keys [from to]} (:edges g)]
      (when-not (and (ids from) (ids to))
        (throw (ex-info (str "figure edge names no node: " (pr-str [from to])) {}))))
    g))

(defn sanitize-svg
  "An illustrator's SVG made safe to inline: no script, foreignObject or
  event attribute, no external reference; scaled to the width of its container."
  [svg]
  (let [svg (-> svg
                (str/replace #"(?s)<\?xml.*?\?>|<!DOCTYPE.*?>|<!--.*?-->" "")
                (str/replace #"(?is)<script\b.*?</script\s*>|<script\b[^>]*/>" "")
                (str/replace #"(?is)<foreignObject\b.*?</foreignObject\s*>" "")
                (str/replace #"(?i)\s+on[a-z]+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)" "")
                (str/replace #"(?i)\s+(?:xlink:)?href\s*=\s*(\"(?!#)[^\"]*\"|'(?!#)[^']*')" "")
                (str/replace #"(?i)url\(\s*(['\"]?)(?!#)[^)]*\)" "none")
                (str/replace #"(?i)javascript:" "")
                strip)
        [_ tag] (re-find #"(?s)^(<svg\b[^>]*>)" svg)
        _ (when-not tag (throw (ex-info "illustration is not an svg" {})))
        attr (fn [a] (some-> (re-find (re-pattern (str "(?i)\\s" a "\\s*=\\s*\"([^\"]*)\"")) tag) second))
        vb (or (attr "viewBox")
               (let [w (attr "width") h (attr "height")]
                 (when (and w h (re-matches #"[\d.]+(px)?" w) (re-matches #"[\d.]+(px)?" h))
                   (str "0 0 " (str/replace w "px" "") " " (str/replace h "px" "")))))
        tag' (-> tag
                 (str/replace #"(?i)\s(width|height|style|viewBox)\s*=\s*(\"[^\"]*\"|'[^']*')" "")
                 (str/replace #"^<svg" (str "<svg viewBox=\"" vb "\" width=\"100%\" style=\"display:block;position:absolute;left:0;top:0;width:100%;height:100%\"")))]
    (str tag' (subs svg (count tag)))))

(defn illustration-el
  "The figure container of an illustrator's SVG, held to its aspect ratio by padding, which
  a grid row cannot collapse."
  [raw]
  (let [svg (sanitize-svg raw)
        [w h] (map #(Double/parseDouble %) (take-last 2 (re-seq #"[\d.]+" (second (re-find #"viewBox=\"([^\"]*)\"" svg)))))]
    (str "<div class=\"figure\" style=\"position:relative;height:0;padding-bottom:" (num (* 100.0 (/ h w)))
         "%;overflow:hidden\">" svg "</div>")))

(def ^:dynamic *figures-dir* nil)

(defn diagram?
  "The lines are an ASCII diagram: a sketch that holds at least one edge."
  [lines]
  (boolean (seq (:edges (try (ascii-graph lines) (catch Exception _ nil))))))

;; -------------------------------------------------------------- text fences

;; ------------------------------------------------------------------ tables

(defn table-sep?
  "A table's separator row: dashes between pipes, a colon marking alignment."
  [l]
  (boolean (and (str/includes? l "|")
                (re-matches #"(?U)\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*" l))))

(defn table-at?
  "Line i of ls opens a table: a row with pipes over a separator row."
  [ls i]
  (and (< (inc i) (count ls)) (str/includes? (ls i) "|") (table-sep? (ls (inc i)))))

(defn table-end
  "The index past the last row of the table opening at i."
  [ls i]
  (loop [j (+ i 2)] (if (and (< j (count ls)) (str/includes? (ls j) "|")) (recur (inc j)) j)))

(defn- cells [l]
  (let [t (strip l)
        t (if (str/starts-with? t "|") (subs t 1) t)
        t (if (and (str/ends-with? t "|") (not (str/ends-with? t "\\|"))) (subs t 0 (dec (count t))) t)]
    (mapv #(str/replace (strip %) "\\|" "|") (str/split t #"(?<!\\)\|" -1))))

(defn table-html [ls]
  (let [[head sep & rows] ls
        aligns (mapv #(let [c (strip %)]
                        (cond (and (str/starts-with? c ":") (str/ends-with? c ":")) "center"
                              (str/ends-with? c ":") "right"
                              :else nil))
                     (cells sep))
        row (fn [tag l]
              (str "<tr>" (apply str (map-indexed (fn [k c]
                                                     (str "<" tag (when-let [a (get aligns k)] (str " style=\"text-align:" a "\"")) ">"
                                                          (inline c) "</" tag ">"))
                                                   (cells l)))
                   "</tr>"))]
    (str "<table><thead>" (row "th" head) "</thead><tbody>" (apply str (map #(row "td" %) rows)) "</tbody></table>")))

(def ^:private bullet-re #"^(?:[-*] |\d+\. )")

(defn fence-open
  "The language of a code fence opening line, or nil."
  [l]
  (some-> (re-find #"^```(\w*)\s*$" l) second))

(defn split-chunk
  "A chunk's bodies, each [kind body]: :fm (front matter lines between two ---
  rules, only at the chunk's head), :heading, :list (lines), :code (lang and
  lines), :table, and :p (a paragraph)."
  [content]
  (let [content (vec content)
        n (count content)
        rule? #(= "---" (rstrip (content %)))
        stop? (fn [j] (let [l (content j)]
                        (or (str/starts-with? l "#") (fence-open l)
                            (re-find bullet-re l) (table-at? content j))))]
    (loop [i 0 bodies []]
      (if (>= i n)
        bodies
        (let [l (content i)]
          (cond
            (and (zero? i) (rule? i)
                 (some #(rule? %) (range 1 n)))
            (let [j (first (filter #(rule? %) (range 1 n)))]
              (recur (inc j) (conj bodies [:fm (subvec content (inc i) j)])))

            (re-find #"^#{1,6} " l)
            (recur (inc i) (conj bodies [:heading l]))

            (fence-open l)
            (let [j (loop [j (inc i)] (if (and (< j n) (not= "```" (rstrip (content j)))) (recur (inc j)) j))]
              (recur (inc j) (conj bodies [:code [(fence-open l) (subvec content (inc i) (min n j))]])))

            (re-find bullet-re l)
            (let [j (loop [j (inc i)]
                      (if (and (< j n) (not (str/starts-with? (content j) "#"))
                               (not (fence-open (content j))))
                        (recur (inc j)) j))
                  items (reduce (fn [items x]
                                  (if (re-find bullet-re x)
                                    (conj items [(second (re-find #"^([-*]|\d+\.) " x))
                                                 (str/replace x bullet-re "")])
                                    (update-in items [(dec (count items)) 1] str " " (strip x))))
                                [] (subvec content i j))]
              (recur j (conj bodies [:list items])))

            (table-at? content i)
            (let [j (table-end content i)]
              (recur j (conj bodies [:table (subvec content i j)])))

            :else
            (let [j (loop [j (inc i)]
                      (if (and (< j n) (not (stop? j))) (recur (inc j)) j))]
              (recur j (conj bodies [:p (join-lines (subvec content i j))])))))))))

(defn tokens
  "Words (letters, digits, _ and -), single punctuation marks, whitespace
  runs, and `code` spans; joined back with no separator they give the text."
  [s]
  (vec (re-seq #"`[^`]*`|[\p{L}\p{N}_-]+|\s+|[^\s]" s)))

(defn word-diff
  "Longest-common-subsequence diff of two token vectors, as a vector of
  [:same|:del|:add token]; on a tie the removal comes first."
  [a b]
  (let [a (vec a) b (vec b)
        n (count a) m (count b)
        tbl (reduce
             (fn [t i]
               (reduce (fn [t j]
                         (assoc t [i j]
                                (if (= (a i) (b j))
                                  (inc (t [(inc i) (inc j)]))
                                  (max (t [(inc i) j]) (t [i (inc j)])))))
                       t (range (dec m) -1 -1)))
             (into {} (concat (for [j (range (inc m))] [[n j] 0])
                              (for [i (range (inc n))] [[i m] 0])))
             (range (dec n) -1 -1))]
    (loop [i 0 j 0 out []]
      (cond
        (and (< i n) (< j m) (= (a i) (b j))) (recur (inc i) (inc j) (conj out [:same (a i)]))
        (and (< i n) (or (= j m) (>= (tbl [(inc i) j]) (tbl [i (inc j)]))))
        (recur (inc i) j (conj out [:del (a i)]))
        (< j m) (recur i (inc j) (conj out [:add (b j)]))
        :else out))))

(defn- chunks
  "A word-diff as chunks: [:same tokens] or [:edit removed added]."
  [diff]
  (->> diff
       (partition-by #(if (= :same (first %)) :same :edit))
       (mapv (fn [grp]
               (if (= :same (ffirst grp))
                 [:same (mapv second grp)]
                 [:edit (mapv second (filter #(= :del (first %)) grp))
                  (mapv second (filter #(= :add (first %)) grp))])))))

(defn- joiner?
  "An unchanged run worth folding into its neighbours: only whitespace, or
  one punctuation mark."
  [toks]
  (let [t (str/join toks)]
    (boolean (or (re-matches #"\s+" t)
                 (and (= 1 (count toks)) (re-matches #"[^\p{L}\p{N}\s]" t))))))

(defn- fold-chunks
  "Fold a joiner lying between two edits into both sides, until none is left."
  [cs]
  (loop [cs cs out []]
    (cond
      (empty? cs) out
      (and (seq out) (>= (count cs) 2)
           (= :edit (first (peek out)))
           (= :same (first (first cs))) (joiner? (second (first cs)))
           (= :edit (first (second cs))))
      (let [[_ d1 a1] (peek out) [_ s] (first cs) [_ d2 a2] (second cs)]
        (recur (drop 2 cs)
               (conj (pop out) [:edit (-> d1 (into s) (into d2)) (-> a1 (into s) (into a2))])))
      :else (recur (rest cs) (conj out (first cs))))))

(defn marked
  "One text: unchanged tokens plain, removed in <del>, added in <ins>; spacing
  is kept as written, and a lone space or mark between two edits joins them."
  [old new fmt]
  (->> (word-diff (tokens old) (tokens new))
       chunks
       fold-chunks
       (map (fn [[kind x y]]
              (if (= kind :same)
                (fmt (str/join x))
                (str (when (seq x) (str "<del>" (fmt (str/join x)) "</del>"))
                     (when (seq y) (str "<ins>" (fmt (str/join y)) "</ins>"))))))
       str/join))

(defn- fm-card
  "Front matter lines as a small labelled card: no YAML syntax, one term per key."
  [lines]
  (let [value (fn [v]
                (let [v (strip v)]
                  (cond (= "[]" v) "none"
                        (and (str/starts-with? v "[") (str/ends-with? v "]"))
                        (str/join ", " (map strip (str/split (subs v 1 (dec (count v))) #",")))
                        :else v)))
        rows (for [l lines :when (not (blank? l))]
               (if-let [m (re-find #"^([A-Za-z][\w-]*):\s*(.*)$" l)]
                 (str "<dt>" (esc (str/capitalize (str/replace (m 1) "-" " "))) "</dt><dd>" (inline (value (m 2))) "</dd>")
                 (str "<dd>" (inline l) "</dd>")))]
    (str "<div class=\"fm\"><div class=\"fm-label\">Front matter</div><dl>" (apply str rows) "</dl></div>")))

(defn- heading-html [l fmt]
  (let [[_ hashes t] (re-find #"^(#{1,6}) (.*)$" l)
        lvl (min 6 (+ 2 (count hashes)))]
    (str "<h" lvl ">" (fmt t) "</h" lvl ">")))

(defn body-html
  "One body of a chunk as formatted HTML."
  [[kind body]]
  (case kind
    :fm (fm-card body)
    :heading (heading-html body inline)
    :list (let [tag (if (re-find #"^\d" (ffirst body)) "ol" "ul")]
            (str "<" tag ">" (apply str (map (fn [[_ t]] (str "<li>" (inline t) "</li>")) body)) "</" tag ">"))
    :code (str "<pre><code class=\"language-" (get langs (first body) (if (= "" (first body)) "text" (first body))) "\">"
               (esc (str/join "\n" (second body))) "</code></pre>")
    :table (table-html body)
    (str "<p>" (inline body) "</p>")))

(defn paired-body
  "A removed and an added body, one text; nil unless both are paragraphs or headings."
  [[kind-a a] [kind-b b]]
  (when (= kind-a kind-b)
    (case kind-a
      :p (str "<p>" (marked a b inline) "</p>")
      :heading (let [[_ ha ta] (re-find #"^(#{1,6}) (.*)$" a) [_ hb tb] (re-find #"^(#{1,6}) (.*)$" b)]
                 (when (= ha hb) (heading-html (str ha " " (marked ta tb inline)) identity)))
      nil)))

(defn panel [sign body]
  (let [inner (body-html body)]
    (case sign
      "+" (str "<div class=\"add\"><ins>" inner "</ins></div>")
      "-" (str "<div class=\"del\"><del>" inner "</del></div>")
      (str "<div class=\"ctx\">" inner "</div>"))))

(defn change-panels
  "A removed run and the added run after it: bodies paired in order, each pair
  one marked text; the rest wholly removed or wholly added."
  [removed added]
  (let [ra (vec (split-chunk removed)) aa (vec (split-chunk added))]
    (apply str
           (for [i (range (max (count ra) (count aa)))
                 :let [r (get ra i) a (get aa i)]]
             (cond
               (and r a) (or (paired-body r a) (str (panel "-" r) (panel "+" a)))
               r (panel "-" r)
               :else (panel "+" a))))))

(defn code-lines
  "A non-text fence with removed lines followed by added lines: the same diff
  line by line, lines kept. Nil otherwise; a wholly added or removed fence stays
  tinted by the page script."
  [lines]
  (let [sgn (fn [l] (cond (or (= l "-") (str/starts-with? l "- ")) :del
                          (or (= l "+") (str/starts-with? l "+ ")) :add
                          :else :same))]
    (when (some (fn [[a b]] (and (= :del (sgn a)) (= :add (sgn b)))) (partition 2 1 lines))
      (loop [ls (vec lines) out []]
        (if (empty? ls)
          (str/join "\n" out)
          (if (= :same (sgn (first ls)))
            (recur (subvec ls 1) (conj out (esc (first ls))))
            (let [[rem r1] (split-with #(= :del (sgn %)) ls)
                  [add r2] (split-with #(= :add (sgn %)) r1)
                  rem (vec rem) add (vec add)
                  rows (for [i (range (max (count rem) (count add)))
                             :let [r (some-> (get rem i) (subs (min 2 (count (get rem i)))))
                                   a (some-> (get add i) (subs (min 2 (count (get add i)))))]]
                         (cond
                           (and r a) (str (re-find #"^\s*" a) (marked (strip-left r) (strip-left a) esc))
                           r (str "<del>" (esc r) "</del>")
                           :else (str "<ins>" (esc a) "</ins>")))]
              (recur (vec r2) (into out rows)))))))))

(defn- in-fence?
  "The chunk has an open code fence: a fence line without its closing one."
  [[_ content]]
  (odd? (count (filter #(re-find #"^```" %) content))))

(defn- continues?
  "In a change written line by line, the line goes on the chunk before it:
  that chunk holds an open code fence or front matter, or both are list items
  or table rows."
  [[_ content :as lst] line]
  (let [l (peek content)
        bullet? #(boolean (re-find bullet-re %))
        row? #(str/starts-with? (strip-left %) "|")]
    (or (in-fence? lst)
        (and (= "---" (rstrip (first content)))
             (= 1 (count (filter #(= "---" (rstrip %)) content))))
        (and (bullet? l) (bullet? line))
        (and (row? l) (row? line)))))

(defn- sign-content
  "A change line's sign (\"+\", \"-\" or \" \" for context) and its content."
  [raw]
  (let [signed (and (#{\+ \-} (first raw))
                    (or (= 1 (count raw)) (= \space (nth raw 1))))]
    [(if signed (subs raw 0 1) " ")
     (cond signed (if (> (count raw) 2) (subs raw 2) "")
           (str/starts-with? raw "  ") (subs raw 2)
           :else raw)]))

(defn- code-fence-items
  "Change lines with each inner code fence whose lines carry more than one sign
  taken out as [:code lang lines]: its lines stay code, never markdown, each
  line keeping its sign for the line tint. A fence of one sign stays lines."
  [lines]
  (let [lines (vec lines) n (count lines)
        content #(second (sign-content (lines %)))]
    (loop [i 0 out []]
      (if (>= i n)
        out
        (let [lang (fence-open (content i))
              j (when lang (first (filter #(= "```" (rstrip (content %))) (range (inc i) n))))]
          (if (and j (< 1 (count (set (map #(first (sign-content (lines %))) (range i (inc j)))))))
            (recur (inc j) (conj out [:code lang (subvec lines (inc i) j)]))
            (recur (inc i) (conj out (lines i)))))))))

(defn- code-fence-html
  "An inner code fence of mixed signs: a removed line followed by an added one
  is marked word by word; otherwise every line is tinted by its sign."
  [lang lines]
  (let [cls (get langs lang (if (= "" lang) "text" lang))]
    (if-let [m (code-lines lines)]
      (str "<pre><code class=\"language-" cls "\">" m "</code></pre>")
      (str "<pre data-diff><code class=\"language-" cls "\">" (esc (str/join "\n" lines)) "</code></pre>"))))

(defn text-panels
  "A fenced text block: sign-prefixed lines into stacked panels, and its
  nothing drawn. With per-line, as a change written outside a fence,
  each signed line is its own line: consecutive lines are not one paragraph,
  and a run of removed lines pairs line by line with the added run after it.
  A code fence inside whose lines carry different signs stays code."
  ([lines] (text-panels lines false))
  ([lines per-line]
  (let [chunks (reduce
                (fn [chunks raw]
                  (if (vector? raw)
                    (conj chunks raw)
                  (let [[sign content] (sign-content raw)
                        signed (not= " " sign)
                        sketch (if signed content raw)
                        lst (peek chunks)
                        joins? (and lst (= (first lst) sign)
                                    (or (not per-line) (continues? lst content)))]
                    (cond
                      (and lst (= (first lst) sign) (in-fence? lst)) (conj (pop chunks) (-> lst (update 1 conj content) (update 2 conj sketch)))
                      (blank? content) (conj chunks nil)
                      joins? (conj (pop chunks) (-> lst (update 1 conj content) (update 2 conj sketch)))
                      :else (conj chunks [sign [content] [sketch]])))))
                [] (code-fence-items lines))
        chunks (vec (remove nil? chunks))
        panels (StringBuilder.)
        run (fn [i sign] (count (take-while #(= sign (first %)) (subvec chunks i))))]
    (loop [i 0]
      (when (< i (count chunks))
        (let [[sign content] (chunks i)
              [nsign ncontent] (get chunks (inc i))]
          (cond
            (= :code sign)
            (do (.append panels (apply code-fence-html (rest (chunks i)))) (recur (inc i)))

            (and per-line (= sign "-"))
            (let [nr (run i "-") na (run (+ i nr) "+")]
              (doseq [k (range (max nr na))]
                (.append panels (change-panels (if (< k nr) (second (chunks (+ i k))) [])
                                               (if (< k na) (second (chunks (+ i nr k))) []))))
              (recur (+ i nr na)))
            (and (= sign "-") (= nsign "+"))
            (do (.append panels (change-panels content ncontent)) (recur (+ i 2)))
            :else (do (doseq [body (split-chunk content)]
                        (.append panels (panel sign body)))
                      (recur (inc i)))))))
    (if (pos? (.length panels)) (str "<div class=\"diff\">" panels "</div>") ""))))

;; ------------------------------------------------------------------- blocks

(def list-item-re #"(?U)^\d+\. ")

(defn split-para
  "A numbered list may open mid-paragraph, after its group heading."
  [para]
  (let [para (vec para)
        k (first (keep-indexed (fn [k l] (when (and (pos? k) (re-find list-item-re l)
                                                    (not (re-find list-item-re (para 0))))
                                           k))
                               para))]
    (if k
      [[:para (subvec para 0 k)] [:para (subvec para k)]]
      [[:para para]])))

(defn diff-para?
  "A paragraph written as a change: every line opens with + or - and a space (or
  is that sign alone), and it adds a line or removes a front-matter rule."
  [para]
  (let [signed (fn [l] (or (#{"+" "-"} l) (re-find #"^[-+] " l)))]
    (boolean (and (seq para) (every? signed para)
                  (some #(or (str/starts-with? % "+") (= "- ---" (rstrip %))) para)))))

(defn flush-para
  "A paragraph written as a change is a text fence read line by line."
  [para]
  (if (diff-para? para) [[:fence "text" para :per-line]] (split-para para)))

(def ^:private proposal-heading #"(?U)^#{2,3} Proposal \d+: ")

(defn blocks
  "Split the source into blocks: [:fence lang lines] (a change written outside
  a fence also carries :per-line) or [:para lines]."
  [src]
  (let [lines (vec (str/split src #"\n" -1))
        n (count lines)
        skip #"(?U)^(<!--.*-->|Presentation\.\{.*\})\s*$"
        fence-close #"(?U)^```\s*$"]
    (loop [i 0 out [] para []]
      (if (>= i n)
        (cond-> out (seq para) (into (flush-para para)))
        (let [l (lines i)]
          (if-let [m (re-find #"(?U)^```(\w*)\s*$" l)]
            (let [out (cond-> out (seq para) (into (flush-para para)))
                  lang (if (= "" (m 1)) "text" (m 1))
                  j (loop [j (inc i)] (if (and (< j n) (not (re-find fence-close (lines j)))) (recur (inc j)) j))]
              (recur (inc j) (conj out (with-meta [:fence lang (subvec lines (inc i) (min n j))]
                                         {:bare (= "" (m 1))})) []))
            (cond
              (blank? l) (recur (inc i) (cond-> out (seq para) (into (flush-para para))) [])
              ;; a proposal heading always opens a new proposal, blank line before it or not
              (re-find proposal-heading l)
              (recur (inc i) (-> out (cond-> (seq para) (into (flush-para para))) (conj [:para [l]])) [])
              (re-find skip l) (recur (inc i) out para)
              :else (recur (inc i) out (conj para l)))))))))

(defn parse-list [lines]
  (reduce (fn [items l]
            (if-let [m (re-find #"(?U)^(\d+)\. (.*)$" l)]
              (conj items [(Long/parseLong (m 1)) (m 2)])
              (if (seq items)
                (update-in items [(dec (count items)) 1] str " " (strip l))
                (reduced nil))))
          [] lines))

(defn file-line [lines]
  (let [text (join-lines lines)
        m (re-find #"^File: `([^`]+)`(.*)$" text)
        _ (when-not m (throw (ex-info (str "File line not understood: " (pr-str text)) {})))
        path (m 1)
        rest* (strip (m 2))
        rest* (if (str/starts-with? rest* ", ") (subs rest* 2) rest*)
        rest* (if (and (str/starts-with? rest* "(builds on") (str/ends-with? rest* ")"))
                (subs rest* 1 (dec (count rest*))) rest*)]
    (cond-> (str "<p class=\"target\"><code>" (esc path) "</code></p>")
      (not= "" rest*) (str "<p>" (inline rest*) "</p>"))))

(defn signed-line?
  "A fence line written as a change: opens with + or - and a space, or is that sign alone."
  [l]
  (boolean (and (#{\+ \-} (first l)) (or (= 1 (count l)) (= \space (nth l 1))))))

(def ^:private target-langs
  {"ethos" "ethos" "datom" "datom" "rs" "rust" "clj" "clojure" "cljc" "clojure"
   "edn" "clojure" "sh" "bash" "bash" "bash"})

(defn target-lang
  "The code language a File line's path names by extension; \"text\" otherwise."
  [path]
  (get target-langs (some-> path (str/split #"\.") rest last) "text"))

(defn presentation-title
  "The title of the Presentation datom on the source's first line that is not
  a comment, or nil."
  [src]
  (let [l (first (remove #(or (blank? %) (re-find #"(?U)^<!--.*-->\s*$" %)) (str/split-lines src)))]
    (some->> l (re-find #"(?U)^Presentation\.\{\s*«([^»]*)».*\}\s*$") second strip not-empty)))

(defn proposal-header
  "The opening of a proposal's sheet. With no File line under it, its title
  says where it lands, and is shown as the target chip in the header."
  [n title where?]
  (str "<article class=\"proposal\"><header><span class=\"pnum\">" n "</span>"
       (if where?
         (str "<h2 class=\"target\"><code style=\"font-size:.95rem\">" (esc (str/replace title "`" "")) "</code></h2>")
         (str "<h2>" (inline title) "</h2>"))
       "</header>"))

(defn build [src code]
  (let [nfig (volatile! 0)
        datom-title (presentation-title src)
        bs (vec (blocks src))
        file-next? (fn [i] (let [[kind ls] (get bs (inc i))]
                             (and (= :para kind) (str/starts-with? (first ls) "File: "))))
        show-fig (fn [lines]
                   (let [n (vswap! nfig inc)
                         f (when *figures-dir* (fs/path *figures-dir* (str "fig-" n ".svg")))]
                     (if (and f (fs/exists? f))
                       (illustration-el (slurp (str f) :encoding "UTF-8"))
                       (throw (ex-info (str "diagram " n " (" (pr-str (or (first (remove blank? lines)) ""))
                                            ") has no figure fig-" n ".svg from --figures")
                                       {})))))
        out (atom [])
        target (volatile! nil)
        in-article (volatile! false)
        rulings (volatile! false)
        pending-close (volatile! false)
        record-open (volatile! false)
        glue (volatile! false)
        append! (fn [s] (swap! out conj s))
        extend-last! (fn [s] (swap! out #(conj (pop %) (str (peek %) s))))
        close-rulings (fn [early]
                        (when @rulings
                          (extend-last! "</li></ol></section>")
                          (vreset! rulings false)
                          (vreset! pending-close false)
                          (vreset! glue early)))
        close-record (fn []
                       (when @record-open
                         (extend-last! "</div>")
                         (vreset! record-open false)))
        emit (fn [s] (if (or @rulings @glue) (extend-last! s) (append! s)))]
    (doseq [[i b] (map-indexed vector bs)]
      (if (= :fence (first b))
        (let [[_ lang lines per-line] b]
          (when (and @rulings @pending-close) (close-rulings true))
          (cond
            (and (= lang "figure") (try (read-figure lines) (catch Exception _ nil)))
            (emit (show-fig lines))

            (and (= lang "text") (not-any? signed-line? lines) (diagram? lines))
            (emit (show-fig lines))

            ;; An unlabelled fence outside a proposal is a diagram, boxed or not.
            (and (:bare (meta b)) (not @in-article) (not-any? signed-line? lines))
            (emit (show-fig lines))

            (and (= lang "text") (not-any? signed-line? lines))
            ;; An unsigned fence that is no diagram is a block of code or file text: kept as written.
            (emit (str "<pre><code class=\"language-" (target-lang @target) "\">"
                       (esc (str/join "\n" lines)) "</code></pre>"))

            (= lang "text")
            (let [diff (text-panels lines (= :per-line per-line))]
              (if @record-open
                (let [diff (str/replace-first diff "<div class=\"diff\">" "")
                      diff (if (str/ends-with? diff "</div>") (subs diff 0 (- (count diff) 6)) diff)]
                  (emit diff)
                  (close-record))
                (when (not= "" diff) (emit diff))))

            :else
            (if-let [marked-code (code-lines lines)]
              (emit (str "<pre><code class=\"language-" (get langs lang lang) "\">" marked-code "</code></pre>"))
              (emit (str "<pre data-diff><code class=\"language-" (get langs lang lang) "\">"
                         (esc (str/join "\n" lines)) "</code></pre>")))))
        (let [lines (second b)
              first-line (first lines)
              text (join-lines lines)
              _ (when-let [m (re-find #"^File: `?([^`\s,]+)" text)] (vreset! target (m 1)))]
          (cond
            (str/starts-with? first-line "# ")
            (let [title (strip (subs first-line 2))]
              (append! "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
              (append! (str "<title>" (esc (or datom-title title)) "</title>"))
              (append! (str "<h1 class=\"book-title\">" (esc title) "</h1>")))

            (str/starts-with? first-line "### ")
            (do (close-rulings false)
                (close-record)
                (vreset! glue false)
                (vreset! target nil)
                (when @in-article (append! "</article>"))
                (let [m (re-find #"(?U)^### Proposal (\d+): (.*)$" text)]
                  (when-not m (throw (ex-info (str "proposal heading not understood: " (pr-str text)) {})))
                  (append! (proposal-header (m 1) (m 2) false)))
                (vreset! in-article true))

            (re-find #"(?U)^## Proposal (\d+): (.*)$" text)
            (let [[_ n where] (re-find #"(?U)^## Proposal (\d+): (.*)$" text)]
              (close-rulings false)
              (close-record)
              (vreset! glue false)
              (vreset! target nil)
              (when @in-article (append! "</article>"))
              (append! (proposal-header n (strip where) (not (file-next? i))))
              (vreset! in-article true))

            (str/starts-with? first-line "## ")
            (do (close-rulings false)
                (close-record)
                (vreset! glue false)
                (when @in-article (append! "</article>") (vreset! in-article false))
                (append! (str "<h2>" (inline (strip (subs first-line 3))) "</h2>")))

            (str/starts-with? first-line "File: `")
            (do (when (and @rulings @pending-close) (close-rulings true))
                (emit (file-line lines)))

            ;; a File line naming its target in words
            (and @in-article (str/starts-with? first-line "File: "))
            (do (when (and @rulings @pending-close) (close-rulings true))
                (emit (str "<p class=\"target\"><code>" (esc (strip (subs text 6))) "</code></p>")))

            ;; lines removed outside a fence, inside a proposal
            (and @in-article (every? signed-line? lines))
            (emit (text-panels lines true))

            (some #(table-at? (vec lines) %) (range (count lines)))
            (emit (apply str (map body-html (split-chunk lines))))

            ;; a bullet list outside a proposal; inside one, a leading - is a removal line
            (and (not @in-article) (re-find #"^[-*] " first-line))
            (emit (apply str (map body-html (split-chunk lines))))

            :else
            (if-let [m (do (when (str/starts-with? text "Ruling:") (close-record))
                           (re-find #"^\*\*(Destroy|Archive)\*\*(?U)\s*(.*)$" text))]
              (do (close-record)
                  (emit (cond-> (str "<div class=\"record " (str/lower-case (m 1)) "\">")
                          (not= "" (m 2)) (str "<p>" (inline (m 2)) "</p>")))
                  (vreset! record-open true))
              (if-let [items (seq (parse-list lines))]
                (let [start (ffirst items)
                      attr (cond-> (str " start=\"" start "\"")
                             (> start 1) (str " style=\"counter-reset:choice " (dec start) "\""))]
                  (emit (str "<ol class=\"choices\"" attr ">"
                             (apply str (map (fn [[_ t]] (str "<li>" (inline t) "</li>")) items))
                             "</ol>"))
                  (vreset! pending-close (not (str/ends-with? (rstrip (second (last items))) ":"))))
                (if (str/starts-with? text "Ruling, one number")
                  (do (close-rulings false)
                      (let [n (some #(second (re-find #"<span class=\"pnum\">(\d+)</span>" %)) (rseq @out))]
                        (when-not n (throw (ex-info "ruling before any proposal" {})))
                        (append! (str "<section class=\"rulings\"><ol><li value=\"" n "\"><p>" (inline text) "</p>")))
                      (vreset! rulings true)
                      (vreset! pending-close false))
                  (emit (str "<p>" (inline text) "</p>")))))))))
    (close-rulings false)
    (close-record)
    (when @in-article (append! "</article>"))
    (str (str/join "\n" @out) "\n" code)))

(defn read-text
  "Read a UTF-8 file with newlines normalised to \\n."
  [path]
  (str/replace (slurp (str path) :encoding "UTF-8") #"\r\n?" "\n"))

(defn -main [& args]
  (let [args (vec args)]
    (when (< (count args) 2)
      (binding [*out* *err*]
        (println "usage: bb tools/book-build.clj SOURCE.md OUT.html [--code tools/book-code.html] [--figures DIR]"))
      (System/exit 1))
    (let [[src-path out-path] args
          ci (.indexOf args "--code")
          code-path (if (>= ci 0)
                      (get args (inc ci))
                      (str (fs/path script-dir "book-code.html")))
          fi (.indexOf args "--figures")]
      (binding [*figures-dir* (when (>= fi 0) (get args (inc fi)))]
        (try (spit out-path (build (read-text src-path) (read-text code-path)) :encoding "UTF-8")
             (catch clojure.lang.ExceptionInfo e
               (binding [*out* *err*] (println (str "book-build: " (ex-message e))))
               (System/exit 1)))))))

(when (= *file* (System/getProperty "babashka.file"))
  (apply -main *command-line-args*))
