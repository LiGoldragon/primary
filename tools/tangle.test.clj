#!/usr/bin/env bb
;; Tests for tools/tangle.clj. Usage: bb tools/tangle.test.clj [WORK-DIR]
;; Fixtures are written under WORK-DIR (default: a fresh temp directory).
(require '[babashka.fs :as fs]
         '[clojure.string :as str]
         '[clojure.test :refer [deftest is run-tests use-fixtures]])

(load-file (str (fs/path (fs/parent (fs/absolutize *file*)) "tangle.clj")))

(def work (str (fs/absolutize (or (first *command-line-args*)
                                  (fs/create-temp-dir {:prefix "tangle-test"})))))
(fs/create-dirs work)

(defn put [rel text] (let [p (str (fs/path work rel))]
                       (some-> (fs/parent p) fs/create-dirs)
                       (spit p text) p))
(defn at [rel] (str (fs/path work rel)))
(defn quietly [args] (let [out (with-out-str (def code (tangle/run args)))]
                       {:code code :out out}))

(def abs-target (at "out/abs.txt"))

(def doc-a
  (str "# A\n\n"
       "```ethos target=gen/signal.ethos\n(Signal a)\n```\n\n"
       "```clojure\n(untargeted)\n```\n\n"
       "~~~~text target=" abs-target "\nabsolute\n```\nnot a close\n~~~~\n\n"
       "```ethos target=gen/signal.ethos\n(Signal b)\n```\n"))

(def doc-b
  (str "```ethos target=../a/gen/signal.ethos\n(Signal c)\n```\n"
       "```sh target=b.sh\necho hi\n```\n"))

(def md-a (put "a/doc.md" doc-a))
(def md-b (put "b/doc.md" doc-b))

(defn clear-outputs []
  (doseq [p [(at "a/gen") (at "out") (at "b/b.sh")]] (fs/delete-tree p)))
(use-fixtures :each (fn [t] (clear-outputs) (t)))

(deftest dry-run-lists-targets-and-writes-nothing
  (let [{:keys [code out]} (quietly ["--dry-run" md-a md-b])]
    (is (= 0 code))
    (is (= [(at "a/gen/signal.ethos") abs-target (at "b/b.sh")]
           (str/split-lines out)))
    (is (not (fs/exists? (at "a/gen/signal.ethos"))))))

(deftest check-before-write-reports-differences
  (let [{:keys [code out]} (quietly ["--check" md-a md-b])]
    (is (= 1 code))
    (is (= 3 (count (str/split-lines out))))
    (is (every? #(str/starts-with? % "differs ") (str/split-lines out)))
    (is (not (fs/exists? abs-target)))))

(deftest write-concatenates-resolves-and-ignores-untargeted
  (let [{:keys [code]} (quietly [md-a md-b])]
    (is (= 0 code))
    (is (= "(Signal a)\n(Signal b)\n(Signal c)\n" (slurp (at "a/gen/signal.ethos"))))
    (is (= "absolute\n```\nnot a close\n" (slurp abs-target)))
    (is (= "echo hi\n" (slurp (at "b/b.sh"))))
    (is (not (str/includes? (slurp (at "a/gen/signal.ethos")) "untargeted")))))

(deftest check-after-write-is-clean-then-detects-drift
  (quietly [md-a md-b])
  (is (= {:code 0 :out ""} (quietly ["--check" md-a md-b])))
  (spit (at "b/b.sh") "echo edited\n")
  (is (= {:code 1 :out (str "differs " (at "b/b.sh") "\n")}
         (quietly ["--check" md-a md-b])))
  (let [{:keys [out]} (quietly [md-a md-b])]
    (is (str/includes? out (str "wrote " (at "b/b.sh"))))
    (is (str/includes? out (str "unchanged " abs-target))))
  (is (= "echo hi\n" (slurp (at "b/b.sh")))))

(deftest write-replaces-whole-file
  (fs/create-dirs (at "out"))
  (spit abs-target "old content that is much longer than the new\n")
  (quietly [md-a])
  (is (= "absolute\n```\nnot a close\n" (slurp abs-target))))

(deftest no-files-is-usage-error
  (is (= 2 (binding [*err* (java.io.StringWriter.)] (tangle/run ["--check"])))))

(let [{:keys [fail error]} (run-tests)]
  (System/exit (if (zero? (+ fail error)) 0 1)))
