;; Tests for tools/book-build.clj. Run: bb tools/book-build-test.clj
;; The two c5f24b books are rebuilt with the working-tree tools/book-code.html
;; and compared byte for byte with their published html. The fixture covers
;; Destroy/Archive records, a figure, rulings and lists; its expected page was
;; produced by the former Python builder with the tail TAIL, all but its figure,
;; which is checked by its parts.
(ns book-build-test
  (:require [clojure.test :refer [deftest is run-tests]]
            [clojure.string :as str]
            [babashka.fs :as fs]))

(def tools-dir (str (fs/parent (fs/absolutize *file*))))
(load-file (str (fs/path tools-dir "book-build.clj")))
(def root (str (fs/parent tools-dir)))
(def code (book-build/read-text (fs/path tools-dir "book-code.html")))

(defn rebuilt [book]
  (let [dir (fs/path root "flows/c5f24b/books")]
    (book-build/build (book-build/read-text (fs/path dir (str book ".md"))) code)))

;; The published html of these two books predates the one-text diff, so it is
;; no longer compared byte for byte: no removed panel may stay directly before
;; an added panel, and every ruling card is still built.
(defn no-twice-read? [html]
  (not (re-find #"</del></div><div class=\"add\">" html)))

(deftest context-modules-book
  (let [html (rebuilt "09-context-modules")]
    (is (no-twice-read? html))
    (is (re-find #"<del>" html))
    (is (re-find #"<ins>" html))))

(deftest messaging-book
  (is (no-twice-read? (rebuilt "10-messaging-between-flows"))))

(defn change [md]
  (first (book-build/text-panels (str/split-lines md))))

(deftest one-word-changed
  (is (= "<div class=\"diff\"><p>The <del>old</del> <ins>new</ins> plan holds, for now.</p></div>"
         (change "- The old plan holds, for now.\n+ The new plan holds, for now."))))

(deftest phrase-inserted
  (is (= "<div class=\"diff\"><p>Keep the <ins>whole new</ins> plan.</p></div>"
         (change "- Keep the plan.\n+ Keep the whole new plan."))))

(deftest line-wholly-added
  (is (= "<div class=\"diff\"><div class=\"ctx\"><p>Kept.</p></div><div class=\"add\"><ins><p>Brand new line.</p></ins></div></div>"
         (change "  Kept.\n+ Brand new line."))))

(deftest line-wholly-removed
  (is (= "<div class=\"diff\"><div class=\"del\"><del><p>Gone line.</p></del></div><div class=\"ctx\"><p>Kept.</p></div></div>"
         (change "- Gone line.\n  Kept."))))

(deftest two-lines-paired-with-two
  (is (= "<div class=\"diff\"><p>first <del>old</del> <ins>new</ins> line second <del>old</del> <ins>new</ins> line</p></div>"
         (change "- first old line\n- second old line\n+ first new line\n+ second new line"))))

(deftest code-diff-keeps-lines-and-indent
  (is (= "x\n  (a <del>b)</del> <ins>z)</ins>\n(c)"
         (book-build/code-lines ["x" "-   (a b)" "- (c)" "+   (a z)" "+ (c)"]))))

(def fixture-md
  "# Fixture & <book>\n\n<!-- hidden comment -->\nPresentation.{ Book Fixture }\n\n## Crystallization\n\nAn opening paragraph with `inline <code>` and\na second line & more.\n\n### Proposal 1: Figures & `records`\n\nFile: `skills/vision-x/SKILL.md`, (builds on `vision-y`)\n\n```text\n  ---\n  name: vision-x\n  ---\n  ## A heading kept as text\n  Unchanged context line\n- Removed line one\n- removed line two\n+ Added line with `code`\n+ # added heading\n```\n\n```text\n+-----------------------+\n| Flow                  |\n| with \"two\" lines      |\n+-----------------------+\n           |\n           | sends it's\n           | message\n           v\n+-----------------------+\n| Recipient             |\n+-----------------------+\n     |\n     | reads\n     v\n+-----------------------+\n| Log                   |\n+-----------------------+\n```\n\n**Destroy** the record `flows/aa/vision/x.md` below.\n\nFile: `flows/aa/vision/x.md`\n\n```text\n- A working instruction logged as vision.\n```\n\n**Archive**\n\n```text\n- An archived line.\n```\n\n**Destroy** with nothing following.\n\n```js\nconst x = 1 < 2 && \"y\";\n```\n\nRuling, one number per line:\n\n1. Approve.\n2. Reject:\n\n```text\n+ inside the ruling card\n```\n\nAfter the card.\n\n### Proposal 2: Second\n\nGroup heading\n3. Third choice\ncontinued here.\n4. Fourth choice\n\nRuling, one number per line:\n\n3. Yes\n4. No\n\n```python\nprint(\"tail\")\n```\n\nTrailing paragraph.\n")

(def fixture-expected
  "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>Fixture &amp; &lt;book&gt;</title>\n<h1 class=\"book-title\">Fixture &amp; &lt;book&gt;</h1>\n<h2>Crystallization</h2>\n<p>An opening paragraph with <code>inline &lt;code&gt;</code> and a second line &amp; more.</p>\n<article class=\"proposal\"><header><span class=\"pnum\">1</span><h2>Figures &amp; <code>records</code></h2></header>\n<p class=\"target\"><code>skills/vision-x/SKILL.md</code></p><p>builds on <code>vision-y</code></p>\n<div class=\"diff\"><div class=\"ctx\"><div class=\"textblock\">---\nname: vision-x\n---</div></div><div class=\"ctx\"><div class=\"textblock\">## A heading kept as text</div></div><div class=\"ctx\"><p>Unchanged context line</p></div><p><del>Removed line one removed</del> <ins>Added</ins> line <del>two</del> <ins>with <code>code</code></ins></p><div class=\"add\"><ins><div class=\"textblock\"># added heading</div></ins></div></div>\n<div class=\"figure\">FIGURE</div>\n<div class=\"record destroy\"><p>the record <code>flows/aa/vision/x.md</code> below.</p>\n<p class=\"target\"><code>flows/aa/vision/x.md</code></p>\n<div class=\"del\"><del><p>A working instruction logged as vision.</p></del></div></div>\n<div class=\"record archive\">\n<div class=\"del\"><del><p>An archived line.</p></del></div></div>\n<div class=\"record destroy\"><p>with nothing following.</p>\n<pre data-diff><code class=\"language-javascript\">const x = 1 &lt; 2 &amp;&amp; \"y\";</code></pre>\n<section class=\"rulings\"><ol><li value=\"1\"><p>Ruling, one number per line:</p><ol class=\"choices\" start=\"1\"><li>Approve.</li><li>Reject:</li></ol><div class=\"add\"><ins><p>inside the ruling card</p></ins></div></div><p>After the card.</p></li></ol></section>\n</article>\n<article class=\"proposal\"><header><span class=\"pnum\">2</span><h2>Second</h2></header>\n<p>Group heading</p>\n<ol class=\"choices\" start=\"3\" style=\"counter-reset:choice 2\"><li>Third choice continued here.</li><li>Fourth choice</li></ol>\n<section class=\"rulings\"><ol><li value=\"2\"><p>Ruling, one number per line:</p><ol class=\"choices\" start=\"3\" style=\"counter-reset:choice 2\"><li>Yes</li><li>No</li></ol></li></ol></section><pre data-diff><code class=\"language-python\">print(\"tail\")</code></pre><p>Trailing paragraph.</p>\n</article>\nTAIL\n")

(deftest fixture-records-and-figure
  (let [page (book-build/build fixture-md "TAIL\n")
        svg (re-find #"(?s)<svg .*?</svg>" page)]
    (is (= fixture-expected (str/replace page svg "FIGURE")))
    (is (str/starts-with? svg (str "<svg viewBox=\"0 0 " book-build/fig-w " ")))
    (is (= 3 (count (re-seq #"<rect [^>]*rx=" svg))) "three boxes")
    (is (= 2 (count (re-seq #"<polygon" svg))) "two arrowheads")
    (doseq [t ["Flow" "with &quot;two&quot; lines" "Recipient" "Log" "sends it&#x27;s message" "reads"]]
      (is (str/includes? svg (str ">" t "</text>")) t))))

(deftest table-in-a-proposal-is-a-table
  (let [html (book-build/build (str "### Proposal 1: x\n\n| a | b |\n|:---|---:|\n| 1 | 2 |\n\n"
                                    "```text\n  | c | d |\n  |---|---|\n  | 3 | 4 |\n- Gone line.\n```\n") "")]
    (is (= 2 (count (re-seq #"<table>" html))))
    (is (str/includes? html "<th style=\"text-align:right\">b</th>"))
    (is (str/includes? html "<td>3</td><td>4</td>"))
    (is (not (re-find #"-{3}" html)) "no separator row drawn as text")
    (is (= 1 (count (re-seq #"<del>" html))))
    (is (str/includes? html "<del><p>Gone line.</p></del>") "a line opening with - and a space is still removed")))

(deftest empty-line-in-text-fence
  (is (= "<div class=\"diff\"><div class=\"ctx\"><p>a</p></div><div class=\"ctx\"><p>b</p></div></div>\n"
         (book-build/build "```\na\n\nb\n```\n" ""))))

(deftest bare-markers-equal-marker-space
  (is (= (book-build/code-lines ["x" "- a" "-  " "- b" "+ a" "+ " "+ b"])
         (book-build/code-lines ["x" "- a" "-" "- b" "+ a" "+" "+ b"])))
  (is (= "x\n\n<del></del>"
         (book-build/code-lines ["x" "-" "- " "+"])) "unpaired empties stay empty marks")
  (is (= (change "- a\n- \n+ b\n+ ") (change "- a\n-\n+ b\n+"))))

(deftest fixture-output-has-no-trailing-whitespace
  (is (nil? (re-find #"(?m)[ \t]+$" (book-build/build fixture-md "TAIL\n"))))
  (is (nil? (re-find #"(?m)[ \t]+$"
                     (book-build/build "```clj\nx\n- a\n-\n+ a\n+\n```\n" "")))))

(let [{:keys [fail error]} (run-tests 'book-build-test)]
  (System/exit (if (zero? (+ fail error)) 0 1)))
