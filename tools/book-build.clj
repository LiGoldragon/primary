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
                        lst (peek chunks)]
                    (cond
                      (blank? content) (conj chunks nil)
                      (and lst (= (first lst) sign)) (conj (pop chunks) (update lst 1 conj content))
                      :else (conj chunks [sign [content]]))))
                [] lines)
        chunks (vec (remove nil? chunks))
        panels (StringBuilder.)
        figures (transient [])]
    (loop [i 0]
      (when (< i (count chunks))
        (let [[sign content] (chunks i)
              [nsign ncontent] (get chunks (inc i))]
          (cond
            (figure? content) (do (conj! figures (svg-figure content)) (recur (inc i)))
            (and (= sign "-") (= nsign "+") (not (figure? ncontent)))
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
          (if (= lang "text")
            (let [[diff figs] (text-panels lines)]
              (if @record-open
                (let [diff (str/replace-first diff "<div class=\"diff\">" "")
                      diff (if (str/ends-with? diff "</div>") (subs diff 0 (- (count diff) 6)) diff)]
                  (emit diff)
                  (close-record))
                (when (not= "" diff) (emit diff)))
              (run! emit figs))
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
