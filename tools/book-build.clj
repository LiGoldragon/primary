#!/usr/bin/env bb
;; Build a book page from its Markdown source.
;;
;; usage: bb tools/book-build.clj SOURCE.md OUT.html [--code tools/book-code.html]
;;
;; The source is a book in the to-the-living form: a title, a
;; Crystallization heading, proposals (### Proposal N: title), File:
;; lines, fenced text as red/green/context panels, fenced code as code
;; blocks, and numbered rulings. An ASCII box-and-arrow figure inside a
;; fenced text block is drawn as an SVG. A paragraph opening with
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
(defn strip [s] (-> s (str/replace ws-left "") rstrip))
(defn blank? [s] (= "" (strip s)))

(defn cp-count [^String s] (.codePointCount s 0 (.length s)))

(defn cp-slice
  "Code-point slice of s from a to (cp-count s) - b."
  [^String s a b]
  (let [n (cp-count s)
        end (- n b)]
    (if (<= end a)
      ""
      (subs s (.offsetByCodePoints s 0 a) (.offsetByCodePoints s 0 end)))))

(defn esc [s]
  (-> s (str/replace "&" "&amp;") (str/replace "<" "&lt;") (str/replace ">" "&gt;")))

(defn esc-attr [s]
  (-> (esc s) (str/replace "\"" "&quot;") (str/replace "'" "&#x27;")))

(defn num [x]
  (let [x (double x)]
    (if (== x (Math/floor x)) (str (long x)) (str x))))

(defn inline
  "Escape text and turn `code` into <code>."
  [text]
  (let [m (re-matcher #"`([^`]+)`" text)
        sb (StringBuilder.)]
    (loop [pos 0]
      (if (.find m)
        (do (.append sb (esc (subs text pos (.start m))))
            (.append sb (str "<code>" (esc (.group m 1)) "</code>"))
            (recur (.end m)))
        (do (.append sb (esc (subs text pos)))
            (str sb))))))

(defn join-lines [lines]
  (str/join " " (keep #(let [t (strip %)] (when (not= "" t) t)) lines)))

;; ------------------------------------------------------------------ figures

(def edge-re #"\+-+\+")

(defn figure? [lines]
  (boolean (and (seq lines) (re-matches edge-re (rstrip (first lines))))))

(defn parse-figure [lines]
  (let [lines (vec lines)
        n (count lines)
        width (cp-count (rstrip (first lines)))]
    (loop [i 0 boxes [] arrows []]
      (if (>= i n)
        [width boxes arrows]
        (let [l (rstrip (lines i))]
          (cond
            (re-matches edge-re l)
            (let [[i texts] (loop [i (inc i) texts []]
                              (if (and (< i n) (str/starts-with? (rstrip (lines i)) "|"))
                                (recur (inc i) (conj texts (strip (cp-slice (rstrip (lines i)) 1 1))))
                                [i texts]))]
              (recur (inc i) (conj boxes texts) arrows))

            (re-find #"(?U)^\s*v\s*$" l)
            (recur (inc i) boxes arrows)

            :else
            (let [m (re-find #"(?U)^(\s*)\|\s?(.*)$" l)]
              (when-not m
                (throw (ex-info (str "figure line not understood: " (pr-str l)) {})))
              (let [col (cp-count (m 1))
                    arrows (if (< (count arrows) (count boxes)) (conj arrows [col []]) arrows)
                    k (dec (count arrows))
                    arrows (update-in arrows [k 1] conj (rstrip (m 2)))]
                (recur (inc i) boxes arrows)))))))))

(defn svg-figure [lines]
  (let [[width boxes arrows] (parse-figure lines)
        boxw (* width 7.5)
        x 30
        parts (StringBuilder.)
        label-parts (transient [])]
    (loop [k 0 y 10 maxw 360]
      (if (>= k (count boxes))
        (str "<svg viewBox=\"0 0 " (num maxw) " " (num (+ y 10))
             "\" width=\"100%\" role=\"img\" aria-label=\""
             (esc-attr (str/join " " (persistent! label-parts)))
             "\" xmlns=\"http://www.w3.org/2000/svg\">" parts "</svg>")
        (let [texts (boxes k)
              h (+ 40 (* 20 (dec (count texts))))]
          (.append parts (str "<rect x=\"" (num x) "\" y=\"" (num y) "\" width=\"" (num boxw)
                              "\" height=\"" (num h)
                              "\" rx=\"3\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"/>"))
          (doseq [[j t] (map-indexed vector texts)]
            (.append parts (str "<text x=\"" (num (+ x 12)) "\" y=\"" (num (+ y 26 (* 20 j)))
                                "\" font-size=\"14\" fill=\"currentColor\" font-family=\"" box-font "\">"
                                (esc-attr t) "</text>"))
            (conj! label-parts t))
          (let [maxw (max maxw (+ x boxw 30))
                y1 (+ y h)]
            (if (< k (count arrows))
              (let [[col labels] (arrows k)
                    lx (+ 30 (* (+ col 0.5) 7.5))
                    length (+ 38 (* 23 (dec (count labels))))
                    y2 (+ y1 length)]
                (.append parts (str "<line x1=\"" (num lx) "\" y1=\"" (num y1) "\" x2=\"" (num lx)
                                    "\" y2=\"" (num y2) "\" stroke=\"currentColor\" stroke-width=\"1.5\"/>"))
                (.append parts (str "<polygon points=\"" (num (- lx 4)) "," (num y2) " "
                                    (num (+ lx 4)) "," (num y2) " " (num lx) "," (num (+ y2 8))
                                    "\" fill=\"currentColor\"/>"))
                (let [maxw (reduce
                            (fn [maxw [j lab]]
                              (.append parts (str "<text x=\"" (num (+ lx 10)) "\" y=\"" (num (+ y1 15 (* 23 j)))
                                                  "\" font-size=\"12\" fill=\"currentColor\" font-family=\""
                                                  label-font "\" text-anchor=\"start\">" (esc-attr lab) "</text>"))
                              (conj! label-parts lab)
                              (max maxw (Math/rint (+ (+ (+ lx 10) (* (cp-count lab) 7.2)) 14))))
                            maxw (map-indexed vector labels))]
                  (recur (inc k) (+ y2 8) maxw)))
              (recur (inc k) y1 maxw))))))))

;; ------------------------------------------------------------ graph figures
;;
;; Any box-and-arrow sketch is read cell by cell into an EDN graph,
;;   {:nodes [{:id "n1" :label "his comment"} ...]
;;    :edges [{:from "n1" :to "n2" :verb "rules a line"} ...]}
;; a node may also carry :note (free text beside its box) or :bare true (an
;; unboxed text that a line starts or ends at). A ```figure fence may give the
;; graph directly as EDN. The graph is drawn top to bottom: ranks by longest
;; path, long edges through placeholder slots, order by barycentre sweeps,
;; orthogonal edges with a shared trunk at every fork and join.

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
                            note-blocks)]
        ;; a sketch read only in part is not drawn: a box inside a box, or
        ;; a line that joins no two nodes
        (when-not (or (some #(re-find #"[+|]-{3,}|-{3,}[+|]" (box-text g %)) boxes)
                      (some (fn [[k ks]] (and (not (edges-of k)) (< 1 (count (mapcat cells-of ks)))))
                            comps))
        {:nodes (vec (for [[kind i :as nk] node-keys]
                       (cond-> {:id (ids nk)
                                :label (if (= kind :box) (box-text g (boxes i)) (:text (blocks i)))}
                         (= kind :text) (assoc :bare true)
                         (and (= kind :box) (notes i))
                         (assoc :note (str/join "\n" (map #(:text (blocks %)) (sort-by #(pos [:text %]) (notes i))))))))
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

(defn chain?
  "A single line of nodes, each edge to the next."
  [{:keys [nodes edges]}]
  (and (= (count edges) (dec (count nodes)))
       (every? #(<= % 1) (vals (frequencies (map :from edges))))
       (every? #(<= % 1) (vals (frequencies (map :to edges))))
       (= 1 (- (count (set (map :id nodes))) (count (set (map :to edges)))))))

;; ------------------------------------------------------------ graph layout

(def fig-w 375)
(def ^:private margin 8)
(def ^:private col-gap 12)
(def ^:private pad 9)
(def ^:private box-cw 8.0)
(def ^:private box-lh 18)
(def ^:private verb-cw 7.2)
(def ^:private verb-lh 15)
(def ^:private dummy-w 10)
(def ^:private arrow 8)

(defn wrap
  "Greedy word wrap at maxc code points; each source line wraps alone."
  [text maxc]
  (let [maxc (max 4 maxc)]
    (vec (mapcat (fn [line]
                   (let [words (mapcat (fn [w] (map #(apply str %) (partition-all maxc (re-seq #"(?s)." w))))
                                       (remove #(= "" %) (str/split (strip line) #"(?U)\s+")))]
                     (if (empty? words)
                       []
                       (reduce (fn [acc w]
                                 (let [l (peek acc)]
                                   (if (and l (<= (+ (cp-count l) 1 (cp-count w)) maxc))
                                     (conj (pop acc) (str l " " w))
                                     (conj acc w))))
                               [] words))))
                 (str/split-lines (or text ""))))))

(defn- back-edge-set
  "Indices of edges that close a cycle, found by depth-first search."
  [ids edges]
  (let [out (group-by :from edges)
        state (volatile! {})
        back (volatile! #{})]
    (letfn [(visit [n]
              (vswap! state assoc n :open)
              (doseq [e (out n)]
                (let [s (@state (:to e))]
                  (cond (= s :open) (vswap! back conj (:i e))
                        (nil? s) (visit (:to e)))))
              (vswap! state assoc n :done))]
      (doseq [n ids] (when-not (@state n) (visit n))))
    @back))

(defn- text-el [x y anchor size font style t]
  (str "<text x=\"" (num x) "\" y=\"" (num y) "\" text-anchor=\"" anchor "\" font-size=\"" size
       "\" font-family=\"" font "\" style=\"" style "\">" (esc-attr t) "</text>"))

(def ^:private fg "fill:var(--fg,currentColor)")
(def ^:private muted "fill:var(--muted,currentColor)")
(def ^:private sheet "fill:var(--sheet,Canvas)")
(def ^:private stroke "fill:none;stroke:var(--fg,currentColor)")

(defn- verb-el
  "Verb lines centred at x, in the band y0..y1, over a sheet backdrop."
  [x y0 y1 lines]
  (let [h (* verb-lh (count lines))
        w (+ 6 (* verb-cw (reduce max 0 (map cp-count lines))))
        top (+ y0 (/ (- (- y1 y0) h) 2.0))]
    (str "<rect x=\"" (num (- x (/ w 2.0))) "\" y=\"" (num top) "\" width=\"" (num w) "\" height=\""
         (num h) "\" style=\"" sheet "\"/>"
         (apply str (map-indexed (fn [j l] (text-el x (+ top 11 (* verb-lh j)) "middle" 12 label-font muted l))
                                 lines)))))

(defn- arrow-el [x y [dx dy]]
  (let [pts (if (zero? dx)
              [[(- x 4) (- y (* dy arrow))] [(+ x 4) (- y (* dy arrow))] [x y]]
              [[(- x (* dx arrow)) (- y 4)] [(- x (* dx arrow)) (+ y 4)] [x y]])]
    (str "<polygon points=\"" (str/join " " (map (fn [[a b]] (str (num a) "," (num b))) pts))
         "\" style=\"" fg "\"/>")))

(defn- path-el [pts]
  (str "<path d=\"M" (str/join " L" (map (fn [[a b]] (str (num a) " " (num b))) (dedupe pts)))
       "\" stroke-width=\"1.5\" style=\"" stroke "\"/>"))

(defn graph-svg
  "Inline SVG of a graph {:nodes [{:id :label}] :edges [{:from :to :verb}]},
  at most fig-w wide."
  [{:keys [nodes edges]}]
  (let [nodes (vec nodes)
        ids (mapv :id nodes)
        node (zipmap ids nodes)
        index (zipmap ids (range))
        edges (vec (map-indexed #(assoc %2 :i %1) edges))
        back (back-edge-set ids edges)
        fwd (remove #(back (:i %)) edges)
        backs (filter #(back (:i %)) edges)
        preds (group-by :to fwd)
        rank (memoize (fn rank [n] (reduce max 0 (map #(inc (rank (:from %))) (preds n)))))
        rank (into {} (map (fn [n] [n (rank n)]) ids))
        ;; segments between adjacent ranks; a long edge passes placeholders
        segs (vec (mapcat (fn [{:keys [from to i]}]
                            (let [k (- (rank to) (rank from))
                                  chain (concat [from] (map #(vector :d i %) (range 1 k)) [to])]
                              (map-indexed (fn [j [a b]] {:a a :b b :e i :first? (zero? j)})
                                           (partition 2 1 chain))))
                          fwd))
        item-rank (merge rank (into {} (for [{:keys [from i] :as e} fwd
                                             k (range 1 (- (rank (:to e)) (rank from)))]
                                         [[:d i k] (+ (rank from) k)])))
        nranks (inc (reduce max 0 (vals rank)))
        start-key (fn [it] (if (vector? it)
                             (+ (index (:from (edges (second it)))) 0.5)
                             (index it)))
        layers (vec (for [r (range nranks)]
                      (vec (sort-by start-key (filter #(= r (item-rank %)) (keys item-rank))))))
        seg-in (group-by :b segs)
        seg-out (group-by :a segs)
        sweep (fn [layers down?]
                (reduce (fn [layers r]
                          (let [nb (if down? (dec r) (inc r))
                                p (zipmap (layers nb) (range))
                                cur (zipmap (layers r) (range))
                                key (fn [it]
                                      (let [ns (keep p (map (if down? :a :b) ((if down? seg-in seg-out) it)))]
                                        (if (seq ns) (/ (reduce + ns) (double (count ns))) (double (cur it)))))]
                            (assoc layers r (vec (sort-by key (layers r))))))
                        layers (if down? (range 1 nranks) (range (- nranks 2) -1 -1))))
        layers (reduce (fn [l d] (sweep l d)) layers [true false true false true])
        ;; an edge closing a cycle runs up a lane of its own at the right,
        ;; its verb on the lane
        back-verb (into {} (for [e backs :when (:verb e)] [(:i e) (wrap (:verb e) 10)]))
        lane-w (into {} (for [e backs]
                          [(:i e) (max 10 (+ 6 (if-let [ls (back-verb (:i e))]
                                                 (+ 6 (* verb-cw (reduce max 0 (map cp-count ls))))
                                                 0)))]))
        lane (reduce + (vals lane-w))
        inner (- fig-w (* 2 margin) lane)
        ;; widths
        slot (vec (for [l layers]
                    (let [k (count (remove vector? l)) m (count (filter vector? l))]
                      (/ (- inner (* col-gap (dec (count l))) (* dummy-w m)) (double (max 1 k))))))
        geom (into {}
                   (for [[r l] (map-indexed vector layers)
                         it l :when (not (vector? it))
                         :let [{:keys [label note bare]} (node it)
                               s (slot r)
                               lines (wrap label (int (/ (- s (* 2 pad)) box-cw)))
                               nlines (if note (wrap note (int (/ (- s (* 2 pad)) verb-cw))) [])
                               w (min s (max 40 (+ (* 2 pad)
                                                   (max (* box-cw (reduce max 0 (map cp-count lines)))
                                                        (* verb-cw (reduce max 0 (map cp-count nlines)))))))
                               h (+ (* 2 pad) (* box-lh (count lines)) (if (seq nlines) (+ 4 (* verb-lh (count nlines))) 0))]]
                     [it {:w w :h h :lines lines :notes nlines :bare bare}]))
        band-h (vec (for [l layers] (reduce max 0 (map #(:h (geom %) 0) l))))
        ;; verbs: shared at a fork's or join's trunk when all its edges carry one
        outs (group-by :from fwd)
        ins (group-by :to fwd)
        verb-max (fn [r] (int (/ (- (reduce min (map slot (filter #(< -1 % nranks) [r (inc r)]))) 8) verb-cw)))
        shared-verb (fn [es] (let [vs (map :verb es)]
                               (when (and (< 1 (count es)) (first vs) (apply = vs)) (first vs))))
        fork-shared (into {} (for [[n es] outs :let [v (shared-verb es)] :when v]
                               [n (wrap v (verb-max (rank n)))]))
        join-shared (into {} (for [[n es] ins
                                   :when (not-any? #(fork-shared (:from %)) es)
                                   :let [v (shared-verb es)] :when v]
                               [n (wrap v (verb-max (dec (rank n))))]))
        own-verb (into {} (for [e fwd
                                :when (and (:verb e) (not (fork-shared (:from e))) (not (join-shared (:to e))))]
                            [(:i e) (wrap (:verb e) (verb-max (rank (:from e))))]))
        ;; x: each item drawn toward its neighbours, order kept, each
        ;; footprint (box or the verbs drawn at its x) apart
        verb-w (fn [ls] (+ 6 (* verb-cw (reduce max 0 (map cp-count ls)))))
        foot (reduce (fn [m [it ls]] (update m it (fnil max 0) (verb-w ls)))
                     (into {} (for [l layers it l] [it (if (vector? it) dummy-w (:w (geom it)))]))
                     (concat fork-shared join-shared
                             (for [{:keys [a b e first?]} segs :when (and first? (own-verb e))]
                               [(if (< 1 (count (outs a))) b a) (own-verb e)])))
        place (fn [l desired]
                (let [lo (+ margin) hi (+ margin inner)
                      fw (reduce (fn [acc it]
                                   (let [w (/ (foot it) 2.0)
                                         x (max (desired it) (+ lo w))
                                         x (if-let [[p px] (peek acc)] (max x (+ px (/ (foot p) 2.0) col-gap w)) x)]
                                     (conj acc [it x])))
                                 [] l)
                      bw (reduce (fn [acc [it x]]
                                   (let [w (/ (foot it) 2.0)
                                         x (min x (- hi w))
                                         x (if-let [[n nx] (first acc)] (min x (- nx (/ (foot n) 2.0) col-gap w)) x)]
                                     (cons [it x] acc)))
                                 () (rseq fw))]
                  (into {} bw)))
        xs0 (into {} (for [l layers
                           :let [total (+ (reduce + (map foot l)) (* col-gap (dec (count l))))
                                 x0 (+ margin (/ (- inner total) 2.0))]
                           [it x] (map vector l (reductions + (+ x0 (/ (foot (first l)) 2.0))
                                                            (map (fn [a b] (+ (/ (foot a) 2.0) col-gap (/ (foot b) 2.0)))
                                                                 l (rest l))))]
                       [it x]))
        xs (reduce (fn [xs down?]
                     (reduce (fn [xs r]
                               (let [nbrs (fn [it] (map (if down? :a :b) ((if down? seg-in seg-out) it)))
                                     desired (fn [it] (let [ns (map xs (nbrs it))]
                                                        (if (seq ns) (/ (reduce + ns) (double (count ns))) (xs it))))]
                                 (merge xs (place (layers r) desired))))
                             xs (if down? (range 1 nranks) (range (- nranks 2) -1 -1))))
                   xs0 [true false true])
        shift (let [l (reduce min (map (fn [[it x]] (- x (/ (foot it) 2.0))) xs))
                    r (reduce max (map (fn [[it x]] (+ x (/ (foot it) 2.0))) xs))]
                (- (+ margin (/ inner 2.0)) (/ (+ l r) 2.0)))
        xs (update-vals xs #(Math/rint (+ % shift)))
        trunk (fn [n shared es] (when (< 1 (count es)) (+ 12 (if-let [ls (shared n)] (+ 6 (* verb-lh (count ls))) 0))))
        split-len (into {} (for [[n es] outs :let [t (trunk n fork-shared es)] :when t] [n t]))
        merge-len (into {} (for [[n es] ins :let [t (trunk n join-shared es)] :when t] [n t]))
        gap (vec (for [r (range (dec nranks))]
                   (+ 26
                      (reduce max 0 (keep split-len (layers r)))
                      (reduce max 0 (keep merge-len (layers (inc r))))
                      (reduce max 0 (for [{:keys [a e first?]} segs
                                          :when (and first? (= r (item-rank a)) (own-verb e))]
                                      (+ 8 (* verb-lh (count (own-verb e)))))))))
        tops (vec (reductions + 10 (map + band-h (concat gap [0]))))
        height (+ (peek tops) 0)
        top-of (fn [it] (tops (item-rank it)))
        out-y (fn [it] (if (vector? it) (+ (top-of it) (band-h (item-rank it))) (+ (top-of it) (:h (geom it)))))
        parts (StringBuilder.)
        add! #(.append parts %)]
    ;; edges first, so boxes and verbs sit over them
    (doseq [{:keys [a b e first?]} segs]
      (let [xa (xs a) xb (xs b) ya (out-y a) yb (top-of b)
            real-b? (not (vector? b))
            fork? (and first? (split-len a))
            join? (and real-b? (merge-len b))
            jog (cond fork? (+ ya (split-len a))
                      join? (- yb (merge-len b))
                      :else (- yb 13))
            end (if real-b? (- yb arrow) yb)
            pts (if (and (== xa xb) (not fork?) (not join?))
                  [[xa ya] [xa end]]
                  [[xa ya] [xa jog] [xb jog] [xb end]])]
        (add! (path-el pts))
        (when (vector? a)
          (add! (path-el [[xa (top-of a)] [xa ya]])))
        (when real-b? (add! (arrow-el xb yb [0 1])))))
    (doseq [[i {:keys [from to verb]}] (map-indexed vector edges) :when (back i)
            :let [before (take-while #(not= i %) (map :i backs))
                  lx (- fig-w margin (reduce + (map lane-w before)) (/ (lane-w i) 2.0))
                  ga (geom from) gb (geom to)
                  x1 (+ (xs from) (/ (:w ga) 2.0)) y1 (+ (top-of from) (/ (:h ga) 2.0) 5)
                  x2 (+ (xs to) (/ (:w gb) 2.0)) y2 (- (+ (top-of to) (/ (:h gb) 2.0)) 5)]]
      (add! (path-el [[x1 y1] [lx y1] [lx y2] [(+ x2 arrow) y2]]))
      (add! (arrow-el x2 y2 [-1 0]))
      (when-let [ls (back-verb i)]
        (add! (verb-el lx (min y1 y2) (max y1 y2) ls))))
    ;; verbs
    (doseq [{:keys [a b e first?]} segs :when (and first? (own-verb e))]
      (let [ya (out-y a) yb (top-of b)
            real-b? (not (vector? b))
            lo (if (split-len a) (+ ya (split-len a)) ya)
            hi (- (if (and real-b? (merge-len b)) (- yb (merge-len b)) yb) arrow)
            x (if (split-len a) (xs b) (xs a))]
        (add! (verb-el x lo (if (split-len a) hi (min hi (- yb 13))) (own-verb e)))))
    (doseq [[n ls] fork-shared]
      (add! (verb-el (xs n) (out-y n) (+ (out-y n) (split-len n)) ls)))
    (doseq [[n ls] join-shared]
      (add! (verb-el (xs n) (- (top-of n) (merge-len n)) (- (top-of n) arrow) ls)))
    ;; nodes
    (doseq [[it {:keys [w h lines notes bare]}] geom]
      (let [x (- (xs it) (/ w 2.0)) y (top-of it)]
        (when-not bare
          (add! (str "<rect x=\"" (num x) "\" y=\"" (num y) "\" width=\"" (num w) "\" height=\"" (num h)
                     "\" rx=\"3\" stroke-width=\"1.5\" style=\"" sheet ";stroke:var(--fg,currentColor)\"/>")))
        (doseq [[j l] (map-indexed vector lines)]
          (add! (text-el (xs it) (+ y pad 13 (* box-lh j)) "middle" 14 box-font fg l)))
        (doseq [[j l] (map-indexed vector notes)]
          (add! (text-el (xs it) (+ y pad 4 11 (* box-lh (count lines)) (* verb-lh j)) "middle" 12 label-font muted l)))))
    (str "<svg viewBox=\"0 0 " fig-w " " (num height) "\" width=\"" fig-w
         "\" style=\"display:block;max-width:100%;height:auto\" role=\"img\" aria-label=\""
         (esc-attr (str/join " " (concat (mapcat (fn [n] (keep n [:label :note])) nodes) (keep :verb edges))))
         "\" xmlns=\"http://www.w3.org/2000/svg\">" parts "</svg>")))

(defn figure-svg
  "The SVG of a sketch, or nil when it draws no edge. A chain the former
  reader takes keeps its former drawing."
  [content raws]
  (let [graph (try (ascii-graph raws) (catch Exception _ nil))
        old (when (figure? content) (try (parse-figure content) (catch Exception _ nil)))]
    (cond
      (and old (or (nil? graph) (chain? graph))) (svg-figure content)
      (seq (:edges graph)) (graph-svg graph)
      :else nil)))

;; -------------------------------------------------------------- text fences

(defn split-chunk
  "A chunk may open with front matter or a heading, kept as text."
  [content]
  (let [content (vec content)
        n (count content)
        rule? #(= "---" (rstrip (content %)))]
    (loop [i 0 bodies []]
      (if (>= i n)
        bodies
        (let [l (content i)]
          (cond
            (rule? i)
            (let [j (loop [j (inc i)] (if (and (< j n) (not (rule? j))) (recur (inc j)) j))]
              (recur (inc j) (conj bodies [:text (str/join "\n" (subvec content i (min n (inc j))))])))

            (str/starts-with? l "#")
            (recur (inc i) (conj bodies [:text l]))

            :else
            (let [j (loop [j i]
                      (if (and (< j n) (not (str/starts-with? (content j) "#")) (not (rule? j)))
                        (recur (inc j)) j))]
              (recur j (conj bodies [:p (join-lines (subvec content i j))])))))))))

(defn tokens
  "Whitespace-separated words, punctuation attached; a `code` span is one word."
  [s]
  (vec (re-seq #"(?:`[^`]*`|\S)+" s)))

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

(defn marked
  "One text: unchanged words plain, removed words in <del>, added in <ins>;
  adjacent words of one kind share one span."
  [old new fmt]
  (->> (word-diff (tokens old) (tokens new))
       (partition-by first)
       (map (fn [grp]
              (let [words (str/join " " (map (comp fmt second) grp))]
                (case (ffirst grp)
                  :del (str "<del>" words "</del>")
                  :add (str "<ins>" words "</ins>")
                  words))))
       (str/join " ")))

(defn paired-body
  "A removed and an added body, one text; nil when their kinds differ."
  [[kind-a a] [kind-b b]]
  (when (= kind-a kind-b)
    (if (= kind-a :text)
      (let [la (vec (str/split a #"\n" -1)) lb (vec (str/split b #"\n" -1))
            rows (for [i (range (max (count la) (count lb)))
                       :let [x (get la i) y (get lb i)]]
                   (cond
                     (and x y) (marked x y esc)
                     x (str "<del>" (esc x) "</del>")
                     :else (str "<ins>" (esc y) "</ins>")))]
        (str "<div class=\"textblock\">" (str/join "\n" rows) "</div>"))
      (str "<p>" (marked a b inline) "</p>"))))

(defn panel [sign [kind text]]
  (let [inner (if (= kind :text)
                (str "<div class=\"textblock\">" (esc text) "</div>")
                (str "<p>" (inline text) "</p>"))]
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
                           (and r a) (str (re-find #"^\s*" a) (marked r a esc))
                           r (str "<del>" (esc r) "</del>")
                           :else (str "<ins>" (esc a) "</ins>")))]
              (recur (vec r2) (into out rows)))))))))

(defn text-panels
  "A fenced text block: sign-prefixed lines into stacked panels."
  [lines]
  (let [chunks (reduce
                (fn [chunks raw]
                  (let [signed (and (#{\+ \-} (first raw))
                                    (or (= 1 (count raw)) (= \space (nth raw 1))))
                        sign (if signed (subs raw 0 1) " ")
                        content (cond signed (if (> (count raw) 2) (subs raw 2) "")
                                      (str/starts-with? raw "  ") (subs raw 2)
                                      :else raw)
                        sketch (if signed content raw)
                        lst (peek chunks)]
                    (cond
                      (blank? content) (conj chunks nil)
                      (and lst (= (first lst) sign)) (conj (pop chunks) (-> lst (update 1 conj content) (update 2 conj sketch)))
                      :else (conj chunks [sign [content] [sketch]]))))
                [] lines)
        chunks (vec (remove nil? chunks))
        panels (StringBuilder.)
        figures (transient [])]
    (loop [i 0]
      (when (< i (count chunks))
        (let [[sign content sketch] (chunks i)
              [nsign ncontent nsketch] (get chunks (inc i))
              fig (figure-svg content sketch)]
          (cond
            fig (do (conj! figures fig) (recur (inc i)))
            (and (= sign "-") (= nsign "+") (not (figure-svg ncontent nsketch)))
            (do (.append panels (change-panels content ncontent)) (recur (+ i 2)))
            :else (do (doseq [body (split-chunk content)]
                        (.append panels (panel sign body)))
                      (recur (inc i)))))))
    [(if (pos? (.length panels)) (str "<div class=\"diff\">" panels "</div>") "")
     (persistent! figures)]))

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

(defn blocks
  "Split the source into blocks: [:fence lang lines] or [:para lines]."
  [src]
  (let [lines (vec (str/split src #"\n" -1))
        n (count lines)
        skip #"(?U)^(<!--.*-->|Presentation\.\{.*\})\s*$"
        fence-close #"(?U)^```\s*$"]
    (loop [i 0 out [] para []]
      (if (>= i n)
        (cond-> out (seq para) (into (split-para para)))
        (let [l (lines i)]
          (if-let [m (re-find #"(?U)^```(\w*)\s*$" l)]
            (let [out (cond-> out (seq para) (conj [:para para]))
                  lang (if (= "" (m 1)) "text" (m 1))
                  j (loop [j (inc i)] (if (and (< j n) (not (re-find fence-close (lines j)))) (recur (inc j)) j))]
              (recur (inc j) (conj out [:fence lang (subvec lines (inc i) (min n j))]) []))
            (cond
              (blank? l) (recur (inc i) (cond-> out (seq para) (into (split-para para))) [])
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

(defn build [src code]
  (let [out (atom [])
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
    (doseq [b (blocks src)]
      (if (= :fence (first b))
        (let [[_ lang lines] b]
          (when (and @rulings @pending-close) (close-rulings true))
          (cond
            (and (= lang "figure") (try (read-figure lines) (catch Exception _ nil)))
            (emit (graph-svg (read-figure lines)))

            (= lang "text")
            (let [[diff figs] (text-panels lines)]
              (if @record-open
                (let [diff (str/replace-first diff "<div class=\"diff\">" "")
                      diff (if (str/ends-with? diff "</div>") (subs diff 0 (- (count diff) 6)) diff)]
                  (emit diff)
                  (close-record))
                (when (not= "" diff) (emit diff)))
              (run! emit figs))

            :else
            (if-let [marked-code (code-lines lines)]
              (emit (str "<pre><code class=\"language-" (get langs lang lang) "\">" marked-code "</code></pre>"))
              (emit (str "<pre data-diff><code class=\"language-" (get langs lang lang) "\">"
                         (esc (str/join "\n" lines)) "</code></pre>")))))
        (let [lines (second b)
              first-line (first lines)
              text (join-lines lines)]
          (cond
            (str/starts-with? first-line "# ")
            (let [title (strip (subs first-line 2))]
              (append! "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
              (append! (str "<title>" (esc title) "</title>"))
              (append! (str "<h1 class=\"book-title\">" (esc title) "</h1>")))

            (str/starts-with? first-line "### ")
            (do (close-rulings false)
                (close-record)
                (vreset! glue false)
                (when @in-article (append! "</article>"))
                (let [m (re-find #"(?U)^### Proposal (\d+): (.*)$" text)]
                  (when-not m (throw (ex-info (str "proposal heading not understood: " (pr-str text)) {})))
                  (append! (str "<article class=\"proposal\"><header><span class=\"pnum\">" (m 1)
                                "</span><h2>" (inline (m 2)) "</h2></header>")))
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

            :else
            (if-let [m (re-find #"^\*\*(Destroy|Archive)\*\*(?U)\s*(.*)$" text)]
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
        (println "usage: bb tools/book-build.clj SOURCE.md OUT.html [--code tools/book-code.html]"))
      (System/exit 1))
    (let [[src-path out-path] args
          ci (.indexOf args "--code")
          code-path (if (>= ci 0)
                      (get args (inc ci))
                      (str (fs/path script-dir "book-code.html")))]
      (spit out-path (build (read-text src-path) (read-text code-path)) :encoding "UTF-8"))))

(when (= *file* (System/getProperty "babashka.file"))
  (apply -main *command-line-args*))
