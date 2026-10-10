#!/usr/bin/env bb
;; tangle — extract targeted fenced code blocks from Markdown into files.
;;
;; Usage:
;;   bb tools/tangle.clj [--check | --dry-run] FILE.md...
;;
;; A fenced block is extracted when its info line names a target after the
;; language:
;;
;;   ```ethos target=/git/github.com/LiGoldragon/Curriculum/ethos/signal.ethos
;;   ...
;;   ```
;;
;; - Backtick and tilde fences of any length (>= 3) are recognised; the closing
;;   fence uses the same character and is at least as long.
;; - Blocks naming the same target are concatenated in input order (files in
;;   argument order, blocks in document order).
;; - Each target is written whole: created (with parent directories) or replaced.
;; - Relative targets resolve against the Markdown file's directory.
;; - Blocks without target= are ignored.
;;
;; Modes:
;;   (default)  write every target; print "wrote PATH" or "unchanged PATH"
;;   --check    write nothing; print "differs PATH" per stale target; exit 1 if any
;;   --dry-run  write nothing; print each target path
(ns tangle
  (:require [babashka.fs :as fs]
            [clojure.string :as str]))

(def fence-open #"^ {0,3}(`{3,}|~{3,})\s*(.*)$")

(defn info-target
  "The target named on a fence info line, or nil."
  [info]
  (some (fn [word] (when (str/starts-with? word "target=")
                     (let [t (subs word 7)] (when (seq t) t))))
        (str/split (str/trim info) #"\s+")))

(defn closes? [line fence]
  (let [t (str/trim line)]
    (and (str/starts-with? t (subs fence 0 1))
         (>= (count t) (count fence))
         (every? #(= % (first fence)) t))))

(defn blocks
  "Targeted blocks of one Markdown text as [{:target raw :body text}]."
  [text]
  (loop [lines (str/split-lines text) open nil acc []]
    (if-let [[line & more] (seq lines)]
      (if open
        (if (closes? line (:fence open))
          (recur more nil (if (:target open)
                            (conj acc {:target (:target open)
                                       :body (str/join (map #(str % "\n") (:lines open)))})
                            acc))
          (recur more (update open :lines conj line) acc))
        (if-let [[_ fence info] (re-matches fence-open line)]
          (if (and (= \` (first fence)) (str/includes? info "`"))
            (recur more nil acc)                       ; inline code span, not a fence
            (recur more {:fence fence :target (info-target info) :lines []} acc))
          (recur more nil acc)))
      acc)))

(defn resolve-target [md-file target]
  (str (fs/normalize (fs/absolutize (fs/path (fs/parent (fs/absolutize md-file)) target)))))

(defn tangle
  "Ordered map-like vector of [absolute-target content] over the Markdown files."
  [md-files]
  (let [pairs (for [f md-files
                    {:keys [target body]} (blocks (slurp (str f)))]
                [(resolve-target f target) body])]
    (reduce (fn [acc [t body]]
              (if-let [i (first (keep-indexed (fn [i [k]] (when (= k t) i)) acc))]
                (update-in acc [i 1] str body)
                (conj acc [t body])))
            [] pairs)))

(defn current [path]
  (when (fs/regular-file? path) (slurp path)))

(defn run
  "Returns exit code; prints one line per target."
  [args]
  (let [mode (cond (some #{"--check"} args) :check
                   (some #{"--dry-run"} args) :dry-run
                   :else :write)
        files (remove #(str/starts-with? % "--") args)]
    (if (empty? files)
      (do (binding [*out* *err*]
            (println "usage: tangle.clj [--check | --dry-run] FILE.md..."))
          2)
      (let [targets (tangle files)]
        (case mode
          :dry-run (do (doseq [[t] targets] (println t)) 0)
          :check (let [stale (remove (fn [[t c]] (= c (current t))) targets)]
                   (doseq [[t] stale] (println "differs" t))
                   (if (seq stale) 1 0))
          :write (do (doseq [[t c] targets]
                       (if (= c (current t))
                         (println "unchanged" t)
                         (do (some-> (fs/parent t) fs/create-dirs)
                             (spit t c)
                             (println "wrote" t))))
                     0))))))

(when (= *file* (System/getProperty "babashka.file"))
  (System/exit (run *command-line-args*)))
