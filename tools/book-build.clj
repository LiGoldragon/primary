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

;; ------------------------------------------------------------ graph layout

;; A figure is drawn at the width it is shown at and never scaled down, so
;; its 12px text is 12px on screen. On a 320px page (tools/book-code.html)
;; whose browser keeps a 15px scrollbar, the page is 305 wide: the body's
;; content is 305 - 2*16 = 273; a proposal's, 273 - 2*16 padding - 2*1
;; border = 239; a ruling's inside it, 239 - 3.4rem - 16 padding - 2*1
;; border = 166.
(def fig-w 239)
(def ruling-fig-w 166)
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
  "Greedy word wrap at maxc code points, only at spaces; a word longer than
  maxc stands whole on its line. The source's lines are kept when each fits;
  when one does not, the whole text flows as one."
  [text maxc]
  (let [maxc (max 1 maxc)
        src (remove #(= "" %) (map strip (str/split-lines (or text ""))))
        fill (fn [words]
               (reduce (fn [acc w]
                         (let [l (peek acc)]
                           (if (and l (<= (+ (cp-count l) 1 (cp-count w)) maxc))
                             (conj (pop acc) (str l " " w))
                             (conj acc w))))
                       [] words))
        words-of #(remove (fn [w] (= "" w)) (str/split % #"(?U)\s+"))]
    (if (every? #(<= (cp-count %) maxc) src)
      (vec src)
      (fill (mapcat words-of src)))))

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
  drawn at width w, the width it is shown at, so its text keeps its size."
  ([g] (graph-svg g fig-w))
  ([{:keys [nodes edges]} fig-w]
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
        ;; an edge closing a cycle runs up a lane at the right, its verb on
        ;; the lane; edges whose ranks do not meet share a lane. When the
        ;; lanes would take a third of the width, their verbs wrap at their
        ;; longest word
        lanes (reduce (fn [lanes e]
                        (let [lo (rank (:to e)) hi (rank (:from e))
                              free? (fn [l] (every? #(or (< (rank (:from %)) lo) (< hi (rank (:to %)))) l))
                              k (first (keep-indexed #(when (free? %2) %1) lanes))]
                          (if k (update lanes k conj e) (conj lanes [e]))))
                      [] (sort-by #(rank (:to %)) backs))
        lane-width (fn [verbs] (mapv (fn [l] (reduce max 10 (for [e l :let [ls (verbs (:i e))] :when ls]
                                                               (+ 12 (* verb-cw (reduce max 0 (map cp-count ls)))))))
                                     lanes))
        verbs-at (fn [maxc] (into {} (for [e backs :when (:verb e)] [(:i e) (wrap (:verb e) (maxc (:verb e)))])))
        back-verb (let [v (verbs-at (constantly 10))]
                    (if (< (* 3 (reduce + (lane-width v))) fig-w)
                      v
                      (verbs-at #(reduce max 1 (map cp-count (str/split (strip %) #"(?U)\s+"))))))
        lane-ws (lane-width back-verb)
        lane (reduce + lane-ws)
        inner (- fig-w (* 2 margin) lane)
        ;; verbs: shared at a fork's or join's trunk when all its edges
        ;; carry one; otherwise each edge's own, on its first segment
        outs (group-by :from fwd)
        ins (group-by :to fwd)
        shared-verb (fn [es] (let [vs (map :verb es)]
                               (when (and (< 1 (count es)) (first vs) (apply = vs)) (first vs))))
        fork-verb (into {} (for [[n es] outs :let [v (shared-verb es)] :when v] [n v]))
        join-verb (into {} (for [[n es] ins
                                 :when (not-any? #(fork-verb (:from %)) es)
                                 :let [v (shared-verb es)] :when v]
                             [n v]))
        own-text (fn [{:keys [e first?]}]
                   (let [{:keys [from to verb]} (edges e)]
                     (when (and first? verb (not (fork-verb from)) (not (join-verb to))) verb)))
        fork? (fn [{:keys [a first?]}] (boolean (and first? (< 1 (count (outs a))))))
        ;; Every edge runs down its source's column, turns at a level of
        ;; its own in the gap below, and runs down its target's column, so
        ;; a verb drawn in a column has under it only its own edge. Edges
        ;; joining at a target with verbs of their own come down side by
        ;; side in its column, each at a port, and meet just above it.
        ported (into {} (for [[b ss] seg-in
                              :when (and (< 1 (count ss)) (some own-text ss))]
                          [b (vec (sort-by #(.indexOf ^java.util.List (layers (item-rank (:a %))) (:a %)) ss))]))
        lines-of (fn [t] (str/split-lines (strip (or t ""))))
        words-of (fn [ls] (mapcat #(str/split % #"(?U)\s+") ls))
        text-w (fn [ls cw extra] (if (seq ls) (+ extra (* cw (reduce max 0 (map cp-count ls)))) 0))
        verb-w (fn [ls] (text-w ls verb-cw 6))
        port-w (fn [s unit] (if-let [t (own-text s)] (verb-w (unit (lines-of t))) 0))
        ;; what a column draws: its box, the verbs at its x, its ports
        column (fn [it unit bcw gap hpad]
                 (let [{:keys [label note]} (node it)
                       real? (not (vector? it))
                       ps (ported it)
                       in-own (when-not ps (keep own-text (seg-in it)))]
                   (max (if real? (max (text-w (unit (lines-of label)) bcw (* 2 hpad))
                                       (text-w (unit (lines-of note)) verb-cw (* 2 hpad)))
                            0)
                        (reduce max 0 (map #(verb-w (unit (lines-of %)))
                                           (concat (keep fork-verb [it]) (keep join-verb [it]) in-own)))
                        (if ps (+ (reduce + (map #(port-w % unit) ps)) (* gap (dec (count ps)))) 0))))
        ;; widths: a rank shares its width among its columns. A column takes
        ;; what it draws on one line; when they do not all fit, the widest
        ;; are capped alike, never below their longest word. A rank whose
        ;; words do not fit narrows its gaps, then sets its boxes at 12px,
        ;; then narrows its boxes' side padding to 4; then the figure's
        ;; margins narrow to 2; when even then they do
        ;; not fit, the figure widens
        narrow? (fn [it] (and (vector? it) (not (ported it)) (empty? (keep own-text (seg-in it)))))
        fits (fn [l gap size hpad]
               (let [fixed (set (filter narrow? l))
                     free (remove fixed l)
                     bcw (* box-cw (/ size 14.0))]
                 {:fixed fixed :free free :gap gap :size size :pad hpad
                  :avail (- inner (* gap (dec (count l))) (* dummy-w (count fixed)))
                  :need (into {} (for [it free] [it (column it identity bcw gap hpad)]))
                  :floor (into {} (for [it free] [it (min (column it identity bcw gap hpad) (column it words-of bcw gap hpad))]))}))
        words-fit? (fn [{:keys [floor avail]}] (<= (reduce + (vals floor)) avail))
        row-fit (vec (for [l layers]
                       (or (first (filter words-fit? (for [[gap size hpad] [[col-gap 14 pad] [4 14 pad] [4 12 pad]]]
                                                       (fits l gap size hpad))))
                           (fits l 4 12 4))))
        over (reduce max 0 (map #(- (reduce + (vals (:floor %))) (:avail %)) row-fit))
        trim (min over (* 2 (- margin 2)))
        margin (- margin (/ trim 2.0))
        over (- over trim)
        inner (+ inner trim over)
        fig-w (+ fig-w over)
        lane-x (into {} (for [[k l] (map-indexed vector lanes)
                              :let [x (- fig-w margin (reduce + (take k lane-ws)) (/ (lane-ws k) 2.0))]
                              {:keys [i]} l]
                          [i x]))
        row-fit (mapv #(update % :avail + trim over) row-fit)
        col-w (into {}
                    (for [[r l] (map-indexed vector layers)
                          :let [{:keys [fixed free need floor avail]} (row-fit r)
                                fit (fn [cap] (reduce + (map #(max (floor %) (min (need %) cap)) free)))
                                cap (if (<= (reduce + (vals need)) avail)
                                      ##Inf
                                      (loop [lo 0.0 hi (reduce max 0.0 (vals need)) n 0]
                                        (if (< n 40)
                                          (let [mid (/ (+ lo hi) 2)]
                                            (if (<= (fit mid) avail) (recur mid hi (inc n)) (recur lo mid (inc n))))
                                          lo)))]
                          it l]
                      [it (if (fixed it) dummy-w (max (floor it) (min (need it) cap)))]))
        gap-at (fn [it] (:gap (row-fit (item-rank it))))
        size-at (fn [it] (:size (row-fit (item-rank it))))
        chars (fn [w cw extra] (int (+ 1e-9 (/ (- w extra) cw))))
        ;; each port takes its share of its column
        port (into {} (for [[b ps] ported
                            :let [needs (map #(port-w % identity) ps)
                                  room (- (col-w b) (* (gap-at b) (dec (count ps))))
                                  ws (map #(* room (/ % (reduce + needs))) needs)]
                            [s w] (map vector ps ws)]
                        [s {:w w :lines (wrap (own-text s) (chars w verb-cw 6))}]))
        fork-shared (into {} (for [[n v] fork-verb] [n (wrap v (chars (col-w n) verb-cw 6))]))
        join-shared (into {} (for [[n v] join-verb] [n (wrap v (chars (col-w n) verb-cw 6))]))
        own (fn [s] (when (own-text s)
                      (if (port s) (:lines (port s)) (wrap (own-text s) (chars (col-w (:b s)) verb-cw 6)))))
        geom (into {}
                   (for [l layers
                         it l :when (not (vector? it))
                         :let [{:keys [label note bare]} (node it)
                               s (col-w it)
                               size (size-at it)
                               bcw (* box-cw (/ size 14.0))
                               blh (* box-lh (/ size 14.0))
                               hpad (:pad (row-fit (item-rank it)))
                               lines (wrap label (chars s bcw (* 2 hpad)))
                               nlines (if note (wrap note (chars s verb-cw (* 2 hpad))) [])
                               w (min s (max 40 (+ (* 2 hpad)
                                                   (max (* bcw (reduce max 0 (map cp-count lines)))
                                                        (* verb-cw (reduce max 0 (map cp-count nlines)))))))
                               h (+ (* 2 pad) (* blh (count lines)) (if (seq nlines) (+ 4 (* verb-lh (count nlines))) 0))]]
                     [it {:w w :h h :lines lines :notes nlines :bare bare :size size :lh blh}]))
        band-h (vec (for [l layers] (reduce max 0 (map #(:h (geom %) 0) l))))
        ;; x: each item drawn toward its neighbours, order kept, each
        ;; footprint (box, verbs and ports drawn at its x) apart
        foot (into {} (for [l layers it l]
                        [it (reduce max (if (vector? it) dummy-w (:w (geom it)))
                                    (concat (map verb-w (keep #(% it) [fork-shared join-shared]))
                                            (keep #(some-> (own %) verb-w) (when-not (ported it) (seg-in it)))
                                            (when-let [ps (ported it)]
                                              [(+ (reduce + (map #(:w (port %)) ps)) (* (gap-at it) (dec (count ps))))])))]))
        place (fn [l desired]
                (let [col-gap (gap-at (first l))
                      lo (+ margin) hi (+ margin inner)
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
                           :let [col-gap (gap-at (first l))
                                 total (+ (reduce + (map foot l)) (* col-gap (dec (count l))))
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
        ;; where a segment comes down in its target's column
        port-x (into {} (for [[b ps] ported
                              :let [ws (map #(:w (port %)) ps)
                                    g (gap-at b)
                                    total (+ (reduce + ws) (* g (dec (count ps))))
                                    lefts (reductions + (- (xs b) (/ total 2.0)) (map #(+ % g) ws))]
                              [s left w] (map vector ps lefts ws)]
                          [s (Math/rint (+ left (/ w 2.0)))]))
        x-in (fn [s] (or (port-x s) (xs (:b s))))
        turns? (fn [s] (or (fork? s) (not (== (xs (:a s)) (x-in s)))))
        ;; y: a gap holds, top to bottom, the verbs shared at fork trunks,
        ;; one level per source whose edges turn, the verb band, and the
        ;; meeting of ports above the arrowheads
        verb-h (fn [ls] (* verb-lh (count ls)))
        turners (vec (for [r (range (dec nranks))]
                       (vec (sort-by xs (distinct (for [s segs :when (and (= r (item-rank (:a s))) (turns? s))] (:a s)))))))
        gap (vec (for [r (range (dec nranks))
                       :let [shared (reduce max 0 (map verb-h (keep fork-shared (layers r))))
                             fs (if (pos? shared) (+ shared 12) 0)
                             nlev (count (turners r))
                             levels (if (pos? nlev) (+ 8 (* 7 (dec nlev))) 0)
                             band (reduce max 13 (map #(+ 10 (verb-h %))
                                                      (concat (keep own (filter #(= r (item-rank (:a %))) segs))
                                                              (keep join-shared (layers (inc r))))))]]
                   {:fs fs :levels levels :band band}))
        tops-of (fn [extra] (vec (reductions + 10 (map + band-h (concat (map-indexed #(+ (:fs %2) (:levels %2) (:band %2) 16 (extra %1 0)) gap) [0])))))
        mid (fn [tops it] (+ (tops (item-rank it)) (/ (:h (geom it)) 2.0)))
        ;; a gap a cycle's lane spans grows until the lane's verb fits
        ;; the longest stretch of a lane no other edge crosses, as
        ;; [top bottom rank-at-top]
        free-span (fn [tops {:keys [i from to]}]
                    (let [ends (fn [{:keys [from to]}] [[(+ (mid tops from) 5) (item-rank from)]
                                                       [(- (mid tops to) 5) (item-rank to)]])
                          [[y1 r1] [y2 r2]] (ends {:from from :to to})
                          [lo hi] (sort-by first [[y1 r1] [y2 r2]])
                          cuts (sort-by first (for [e backs :when (> (lane-x (:i e)) (lane-x i))
                                                    [y r] (ends e) :when (< (first lo) y (first hi))]
                                                [y r]))
                          spans (map vector (cons lo cuts) (concat cuts [hi]))
                          [[s0 r0] [s1 _]] (apply max-key (fn [[[p] [q]]] (- q p)) spans)]
                      [s0 s1 r0]))
        extra (reduce (fn [extra _]
                        (let [tops (tops-of extra)]
                          (reduce (fn [m {:keys [i] :as e}]
                                    (let [ls (back-verb i)
                                          [s0 s1 r] (free-span tops e)
                                          short (- (+ 10 (* verb-lh (count ls))) (- s1 s0))]
                                      (if (and ls (pos? short) (< r (dec nranks)))
                                        (update m r (fnil + 0) short)
                                        m)))
                                  extra backs)))
                      {} (range 3))
        tops (tops-of extra)
        height (peek tops)
        top-of (fn [it] (tops (item-rank it)))
        out-y (fn [it] (if (vector? it) (+ (top-of it) (band-h (item-rank it))) (+ (top-of it) (:h (geom it)))))
        bottom (fn [r] (+ (tops r) (band-h r)))
        level (fn [a] (let [r (item-rank a)]
                        (+ (bottom r) (:fs (gap r)) 8 (* 7 (.indexOf ^java.util.List (turners r) a)))))
        band-top (fn [r] (+ (bottom r) (:fs (gap r)) (:levels (gap r))))
        band-bottom (fn [r] (- (tops (inc r)) 16))
        parts (StringBuilder.)
        add! #(.append parts %)
        ;; a verb on a lane sits clear of the edges crossing the lane
        back-ys (into {} (for [{:keys [i from to]} backs
                               :let [ga (geom from) gb (geom to)]]
                           [i [(+ (top-of from) (/ (:h ga) 2.0) 5) (- (+ (top-of to) (/ (:h gb) 2.0)) 5)]]))]
    ;; edges first, so boxes and verbs sit over them
    (doseq [{:keys [a b] :as s} segs]
      (let [xa (xs a) xb (xs b) ya (out-y a) yb (top-of b)
            xt (x-in s)
            real-b? (not (vector? b))
            meet (- yb 14)]
        (add! (path-el (concat [[xa ya]]
                               (when (turns? s) [[xa (level a)] [xt (level a)]])
                               (when (port-x s) [[xt meet] [xb meet]])
                               [[xb (if real-b? (- yb arrow) yb)]])))
        (when (vector? a)
          (add! (path-el [[xa (top-of a)] [xa ya]])))
        (when real-b? (add! (arrow-el xb yb [0 1])))))
    (doseq [{:keys [i from to]} backs
            :let [lx (lane-x i)
                  [y1 y2] (back-ys i)
                  x1 (+ (xs from) (/ (:w (geom from)) 2.0))
                  x2 (+ (xs to) (/ (:w (geom to)) 2.0))]]
      (add! (path-el [[x1 y1] [lx y1] [lx y2] [(+ x2 arrow) y2]]))
      (add! (arrow-el x2 y2 [-1 0]))
      (when-let [ls (back-verb i)]
        (let [lo (min y1 y2) hi (max y1 y2)
              ;; edges whose lanes lie further right cross this one
              [s0 s1] (free-span tops {:i i :from from :to to})]
          (add! (verb-el lx s0 s1 ls)))))
    ;; verbs
    (doseq [{:keys [a] :as s} segs :let [ls (own s)] :when ls
            :let [r (item-rank a)]]
      (add! (verb-el (x-in s) (band-top r) (band-bottom r) ls)))
    (doseq [[n ls] fork-shared]
      (add! (verb-el (xs n) (out-y n) (level n) ls)))
    (doseq [[n ls] join-shared]
      (let [r (dec (item-rank n))]
        (add! (verb-el (xs n) (band-top r) (band-bottom r) ls))))
    ;; nodes
    (doseq [[it {:keys [w h lines notes bare size lh]}] geom]
      (let [x (- (xs it) (/ w 2.0)) y (top-of it)]
        (when-not bare
          (add! (str "<rect x=\"" (num x) "\" y=\"" (num y) "\" width=\"" (num w) "\" height=\"" (num h)
                     "\" rx=\"3\" stroke-width=\"1.5\" style=\"" sheet ";stroke:var(--fg,currentColor)\"/>")))
        (doseq [[j l] (map-indexed vector lines)]
          (add! (text-el (xs it) (+ y pad (* 13 (/ size 14.0)) (* lh j)) "middle" size box-font fg l)))
        (doseq [[j l] (map-indexed vector notes)]
          (add! (text-el (xs it) (+ y pad 4 11 (* lh (count lines)) (* verb-lh j)) "middle" 12 label-font muted l)))))
    (str "<svg viewBox=\"0 0 " (num fig-w) " " (num height) "\" width=\"" (num fig-w) "\" height=\"" (num height)
         "\" style=\"display:block\" role=\"img\" aria-label=\""
         (esc-attr (str/join " " (mapcat lines-of (concat (mapcat (fn [n] (keep n [:label :note])) nodes) (keep :verb edges)))))
         "\" xmlns=\"http://www.w3.org/2000/svg\">" parts "</svg>"))))

;; A figure stands in a block of its own; the page's CSS (book-code.html,
;; .figure) holds the box to the whole height it is drawn at.
(defn figure-el [svg] (str "<div class=\"figure\">" svg "</div>"))

(defn figure-svg
  "The SVG of a sketch at width w, or nil when it draws no edge."
  ([content raws] (figure-svg content raws fig-w))
  ([_content raws w]
   (let [graph (try (ascii-graph raws) (catch Exception _ nil))]
     (when (seq (:edges graph)) (graph-svg graph w)))))

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

(defn text-panels
  "A fenced text block: sign-prefixed lines into stacked panels, and its
  figures drawn w wide."
  ([lines] (text-panels lines fig-w))
  ([lines w]
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
                      (and lst (= (first lst) sign) (in-fence? lst)) (conj (pop chunks) (-> lst (update 1 conj content) (update 2 conj sketch)))
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
              fig (figure-svg content sketch w)]
          (cond
            fig (do (conj! figures fig) (recur (inc i)))
            (and (= sign "-") (= nsign "+") (not (figure-svg ncontent nsketch w)))
            (do (.append panels (change-panels content ncontent)) (recur (+ i 2)))
            :else (do (doseq [body (split-chunk content)]
                        (.append panels (panel sign body)))
                      (recur (inc i)))))))
    [(if (pos? (.length panels)) (str "<div class=\"diff\">" panels "</div>") "")
     (persistent! figures)])))

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

(defn flush-para [para]
  (if (diff-para? para) [[:fence "text" para]] (split-para para)))

(defn blocks
  "Split the source into blocks: [:fence lang lines] or [:para lines]."
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
              (recur (inc j) (conj out [:fence lang (subvec lines (inc i) (min n j))]) []))
            (cond
              (blank? l) (recur (inc i) (cond-> out (seq para) (into (flush-para para))) [])
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

(defn build [src code]
  (let [out (atom [])
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
    (doseq [b (blocks src)]
      (if (= :fence (first b))
        (let [[_ lang lines] b]
          (when (and @rulings @pending-close) (close-rulings true))
          (cond
            (and (= lang "figure") (try (read-figure lines) (catch Exception _ nil)))
            (emit (figure-el (graph-svg (read-figure lines) (if @rulings ruling-fig-w fig-w))))

            (and (= lang "text") (not-any? signed-line? lines)
                 (empty? (second (text-panels lines (if @rulings ruling-fig-w fig-w)))))
            ;; An unsigned fence that draws no figure is a block of code or file text: kept as written.
            (emit (str "<pre><code class=\"language-" (target-lang @target) "\">"
                       (esc (str/join "\n" lines)) "</code></pre>"))

            (= lang "text")
            (let [[diff figs] (text-panels lines (if @rulings ruling-fig-w fig-w))]
              (if @record-open
                (let [diff (str/replace-first diff "<div class=\"diff\">" "")
                      diff (if (str/ends-with? diff "</div>") (subs diff 0 (- (count diff) 6)) diff)]
                  (emit diff)
                  (close-record))
                (when (not= "" diff) (emit diff)))
              (run! (comp emit figure-el) figs))

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
              (append! (str "<title>" (esc title) "</title>"))
              (append! (str "<h1 class=\"book-title\">" (esc title) "</h1>")))

            (str/starts-with? first-line "### ")
            (do (close-rulings false)
                (close-record)
                (vreset! glue false)
                (vreset! target nil)
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

            (some #(table-at? (vec lines) %) (range (count lines)))
            (emit (apply str (map body-html (split-chunk lines))))

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
