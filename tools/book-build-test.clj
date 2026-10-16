;; Tests for tools/book-build.clj. Run: bb tools/book-build-test.clj
;; The two c5f24b books are rebuilt with the working-tree tools/book-code.html
;; and compared byte for byte with their published html. The fixture covers
;; Destroy/Archive records, a figure, rulings and lists; its expected page was
;; produced by the former Python builder with the tail TAIL, all but its figure,
;; which is checked by its parts.
(ns book-build-test
  (:require [clojure.test :refer [deftest is run-tests]]
            [clojure.string :as str]
            [clojure.java.shell]
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
  (book-build/text-panels (str/split-lines md)))

(deftest one-word-changed
  (is (= "<div class=\"diff\"><p>The <del>old</del><ins>new</ins> plan holds, for now.</p></div>"
         (change "- The old plan holds, for now.\n+ The new plan holds, for now."))))

(deftest phrase-inserted
  (is (= "<div class=\"diff\"><p>Keep the <ins>whole new </ins>plan.</p></div>"
         (change "- Keep the plan.\n+ Keep the whole new plan."))))

(deftest line-wholly-added
  (is (= "<div class=\"diff\"><div class=\"ctx\"><p>Kept.</p></div><div class=\"add\"><ins><p>Brand new line.</p></ins></div></div>"
         (change "  Kept.\n+ Brand new line."))))

(deftest line-wholly-removed
  (is (= "<div class=\"diff\"><div class=\"del\"><del><p>Gone line.</p></del></div><div class=\"ctx\"><p>Kept.</p></div></div>"
         (change "- Gone line.\n  Kept."))))

(deftest two-lines-paired-with-two
  (is (= "<div class=\"diff\"><p>first <del>old</del><ins>new</ins> line second <del>old</del><ins>new</ins> line</p></div>"
         (change "- first old line\n- second old line\n+ first new line\n+ second new line"))))

(deftest code-diff-keeps-lines-and-indent
  (is (= "x\n  (a <del>b</del><ins>z</ins>)\n(c)"
         (book-build/code-lines ["x" "-   (a b)" "- (c)" "+   (a z)" "+ (c)"]))))

(def fixture-md
  "# Fixture & <book>\n\n<!-- hidden comment -->\nPresentation.{ Book Fixture }\n\n## Crystallization\n\nAn opening paragraph with `inline <code>` and\na second line & more.\n\n### Proposal 1: Figures & `records`\n\nFile: `skills/vision-x/SKILL.md`, (builds on `vision-y`)\n\n```text\n  ---\n  name: vision-x\n  ---\n  ## A heading kept as text\n  Unchanged context line\n- Removed line one\n- removed line two\n+ Added line with `code`\n+ # added heading\n```\n\n```text\n+-----------------------+\n| Flow                  |\n| with \"two\" lines      |\n+-----------------------+\n           |\n           | sends it's\n           | message\n           v\n+-----------------------+\n| Recipient             |\n+-----------------------+\n     |\n     | reads\n     v\n+-----------------------+\n| Log                   |\n+-----------------------+\n```\n\n**Destroy** the record `flows/aa/vision/x.md` below.\n\nFile: `flows/aa/vision/x.md`\n\n```text\n- A working instruction logged as vision.\n```\n\n**Archive**\n\n```text\n- An archived line.\n```\n\n**Destroy** with nothing following.\n\n```js\nconst x = 1 < 2 && \"y\";\n```\n\nRuling, one number per line:\n\n1. Approve.\n2. Reject:\n\n```text\n+ inside the ruling card\n```\n\nAfter the card.\n\n### Proposal 2: Second\n\nGroup heading\n3. Third choice\ncontinued here.\n4. Fourth choice\n\nRuling, one number per line:\n\n3. Yes\n4. No\n\n```python\nprint(\"tail\")\n```\n\nTrailing paragraph.\n")

(def fixture-expected
  "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>Fixture &amp; &lt;book&gt;</title>\n<h1 class=\"book-title\">Fixture &amp; &lt;book&gt;</h1>\n<h2>Crystallization</h2>\n<p>An opening paragraph with <code>inline &lt;code&gt;</code> and a second line &amp; more.</p>\n<article class=\"proposal\"><header><span class=\"pnum\">1</span><h2>Figures &amp; <code>records</code></h2></header>\n<p class=\"target\"><code>skills/vision-x/SKILL.md</code></p><p>builds on <code>vision-y</code></p>\n<div class=\"diff\"><div class=\"ctx\"><div class=\"fm\"><div class=\"fm-label\">Front matter</div><dl><dt>Name</dt><dd>vision-x</dd></dl></div></div><div class=\"ctx\"><h4>A heading kept as text</h4></div><div class=\"ctx\"><p>Unchanged context line</p></div><p><del>Removed</del><ins>Added</ins> line <del>one removed line two</del><ins>with <code>code</code></ins></p><div class=\"add\"><ins><h3>added heading</h3></ins></div></div>\n<div class=\"figure\">FIGURE</div>\n<div class=\"record destroy\"><p>the record <code>flows/aa/vision/x.md</code> below.</p>\n<p class=\"target\"><code>flows/aa/vision/x.md</code></p>\n<div class=\"del\"><del><p>A working instruction logged as vision.</p></del></div></div>\n<div class=\"record archive\">\n<div class=\"del\"><del><p>An archived line.</p></del></div></div>\n<div class=\"record destroy\"><p>with nothing following.</p>\n<pre data-diff><code class=\"language-javascript\">const x = 1 &lt; 2 &amp;&amp; \"y\";</code></pre>\n<section class=\"rulings\"><ol><li value=\"1\"><p>Ruling, one number per line:</p><ol class=\"choices\" start=\"1\"><li>Approve.</li><li>Reject:</li></ol><div class=\"add\"><ins><p>inside the ruling card</p></ins></div></div><p>After the card.</p></li></ol></section>\n</article>\n<article class=\"proposal\"><header><span class=\"pnum\">2</span><h2>Second</h2></header>\n<p>Group heading</p>\n<ol class=\"choices\" start=\"3\" style=\"counter-reset:choice 2\"><li>Third choice continued here.</li><li>Fourth choice</li></ol>\n<section class=\"rulings\"><ol><li value=\"2\"><p>Ruling, one number per line:</p><ol class=\"choices\" start=\"3\" style=\"counter-reset:choice 2\"><li>Yes</li><li>No</li></ol></li></ol></section><pre data-diff><code class=\"language-python\">print(\"tail\")</code></pre><p>Trailing paragraph.</p>\n</article>\nTAIL\n")

(def illustration
  (str "<?xml version=\"1.0\"?><svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" "
       "viewBox=\"0 0 360 520\" width=\"360\" height=\"520\" onload=\"evil()\">"
       "<script>alert(1)</script><a href=\"https://evil.example/x\"><rect id=\"keep\" width=\"10\" height=\"10\" onclick=\"evil()\"/></a>"
       "<use xlink:href=\"http://evil.example/y.svg#a\"/><use href=\"#keep\"/>"
       "<image href=\"data-not-allowed\"/><foreignObject><p>x</p></foreignObject><text>ILLUSTRATED</text></svg>"))

(defn with-figures [files f]
  (let [dir (fs/create-temp-dir)]
    (try (doseq [[n body] files] (spit (str (fs/path dir n)) body))
         (binding [book-build/*figures-dir* (str dir)] (f))
         (finally (fs/delete-tree dir)))))

(def drawn
  "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 239 100\"><text>DRAWN</text></svg>")

(deftest fixture-records-and-figure
  (let [page (with-figures {"fig-1.svg" drawn} #(book-build/build fixture-md "TAIL\n"))
        fig (re-find #"(?s)<div class=\"figure\"[^>]*>.*?</svg></div>" page)]
    (is (= fixture-expected (str/replace page fig "<div class=\"figure\">FIGURE</div>")))
    (is (str/includes? fig ">DRAWN</text>") "the figure is the supplied fig-1.svg")
    (is (not (str/includes? page "Recipient")) "the sketch is not drawn")))

(deftest fixture-output-has-no-trailing-whitespace
  (is (nil? (re-find #"(?m)[ \t]+$" (with-figures {"fig-1.svg" drawn} #(book-build/build fixture-md "TAIL\n")))))
  (is (nil? (re-find #"(?m)[ \t]+$"
                     (book-build/build "```clj\nx\n- a\n-\n+ a\n+\n```\n" "")))))

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
  (is (= "<div class=\"diff\"><div class=\"add\"><ins><p>a</p></ins></div><div class=\"add\"><ins><p>b</p></ins></div></div>\n"
         (book-build/build "```\n+ a\n\n+ b\n```\n" ""))))

(deftest bare-markers-equal-marker-space
  (is (= (book-build/code-lines ["x" "- a" "-  " "- b" "+ a" "+ " "+ b"])
         (book-build/code-lines ["x" "- a" "-" "- b" "+ a" "+" "+ b"])))
  (is (= "x\n\n<del></del>"
         (book-build/code-lines ["x" "-" "- " "+"])) "unpaired empties stay empty marks")
  (is (= (change "- a\n- \n+ b\n+ ") (change "- a\n-\n+ b\n+"))))

(deftest new-module-renders-as-web
  (let [md (str "### Proposal 1: m\n\nFile: `a/b.md`, new\n\n+ ---\n+ description: Does a thing.\n+ dependencies: [x, y]\n+ ---\n+\n"
                "+ ## Head\n+\n+ Para with `code` & more.\n+\n+ - one\n+ - two\n+\n+ ```rust\n+ let a = 1;\n+\n+ - kept < code\n+ ```\n\n"
                "- ---\n- description: Old.\n- ---\n- Old body.\n")
        html (book-build/build md "")]
    (is (str/includes? html "<div class=\"add\"><ins><div class=\"fm\"><div class=\"fm-label\">Front matter</div><dl><dt>Description</dt><dd>Does a thing.</dd><dt>Dependencies</dt><dd>x, y</dd></dl></div></ins></div>"))
    (is (str/includes? html "<div class=\"add\"><ins><h4>Head</h4></ins></div>"))
    (is (str/includes? html "<p>Para with <code>code</code> &amp; more.</p>"))
    (is (str/includes? html "<ul><li>one</li><li>two</li></ul>"))
    (is (str/includes? html "<pre><code class=\"language-rust\">let a = 1;\n\n- kept &lt; code</code></pre>") "fence stays code, blank line kept")
    (is (str/includes? html "<div class=\"del\"><del><div class=\"fm\">") "removed module is rendered and marked")
    (is (not (str/includes? html "---")) "no YAML syntax shown")
    (is (not (str/includes? html "<div class=\"textblock\">")))))

(deftest unsigned-fence-is-code
  (let [ethos (str "; The kind of a subflow: aspect, role and level.\nLibrary\n[]                    ; imports: intrinsics only\n"
                   "[ Aspect.[ Psyche     ; thinking, psyche records\n           Mind       ; documentation, tools,\n"
                   "                      ; code changes, audit review\n           Field ]    ; debugging, system audit,\n"
                   "                      ; system search, deploy\n  Role.[ Explorer     ; locate and read\n"
                   "         Researcher ] ; the web\n  Level.[ Secondary\n          Tertiary\n          Quaternary ]\n"
                   "  Kind.{ Aspect\n         Role\n         Level } ]\n[]                    ; kinds\n[]                    ; associations")
        md (fn [file] (str "### Proposal 1: The Kind in Ethos\n\nFile: " file "\n\n```\n" ethos "\n```\n\nAfter.\n"))
        esc* (book-build/esc ethos)]
    (doseq [[file lang] [["Curriculum/kinds.ethos, new" "ethos"] ["`Curriculum/kinds.ethos`, new" "ethos"] ["a/b.md, new" "text"]]
            :let [html (book-build/build (md file) "")]]
      (is (str/includes? html (str "<pre><code class=\"language-" lang "\">" esc* "</code></pre>")) file)
      (is (not (str/includes? html "<div class=\"diff\">")))
      (is (not (str/includes? html "<div class=\"ctx\">"))))))

(deftest bullet-list-after-heading
  (let [html (book-build/build "## Why\n\n- **one** is first.\n- **two** is second,\n  continued.\n\nAfter.\n" "")]
    (is (str/includes? html "<ul><li><strong>one</strong> is first.</li><li><strong>two</strong> is second, continued.</li></ul>"))
    (is (not (str/includes? html "**"))))
  (let [html (book-build/build "### Proposal 1: T\n\nFile: a.md\n\n- old\n+ new\n" "")]
    (is (not (str/includes? html "<ul>")))))

(def sketch-md
  (str "```text\n+-------+\n| One   |\n+-------+\n    |\n    | sends\n    v\n+-------+\n| Two   |\n+-------+\n```\n\n"
       "```text\n+-------+\n| Red   |\n+-------+\n    |\n    v\n+-------+\n| Blue  |\n+-------+\n```\n"))

(deftest illustration-replaces-the-nth-figure
  (let [html (with-figures {"fig-1.svg" illustration "fig-2.svg" drawn} #(book-build/build sketch-md ""))
        figs (re-seq #"(?s)<div class=\"figure\"[^>]*>.*?</div>" html)]
    (is (= 2 (count figs)))
    (is (str/includes? (first figs) "ILLUSTRATED") "figure 1 is the illustration")
    (is (not (str/includes? html ">One<")))
    (is (str/includes? (first figs) "width=\"100%\"") "scaled to the container")
    (is (str/includes? (first figs) "viewBox=\"0 0 360 520\""))
    (is (str/includes? (first figs) "padding-bottom:144.44%") "the container holds the aspect height")
    (is (str/includes? (second figs) "DRAWN") "figure 2 is fig-2.svg")))

(deftest illustration-is-sanitized
  (let [html (with-figures {"fig-1.svg" illustration} #(book-build/build (first (str/split sketch-md #"\n\n")) ""))
        fig (re-find #"(?s)<div class=\"figure\"[^>]*>.*?</div>" html)]
    (is (not (re-find #"(?i)<script|alert|onload|onclick|evil|foreignObject|<\?xml" fig)))
    (is (not (re-find #"https?://[^\"]*evil" fig)))
    (is (str/includes? fig "xmlns=\"http://www.w3.org/2000/svg\"") "the namespace stays")
    (is (str/includes? fig "<use href=\"#keep\"/>") "an internal reference stays")
    (is (str/includes? fig "id=\"keep\""))))

(defn refusal
  "The message of the refusal, or nil when the build succeeds."
  [md]
  (try (book-build/build md "") nil (catch clojure.lang.ExceptionInfo e (ex-message e))))

(deftest diagram-without-figure-is-refused
  (let [msg (refusal sketch-md)]
    (is (some? msg))
    (is (str/includes? msg "diagram 1"))
    (is (str/includes? msg "fig-1.svg"))
    (is (not (str/includes? msg "\n")) "one line"))
  (is (str/includes? (with-figures {} #(refusal sketch-md)) "diagram 1") "empty directory")
  (is (str/includes? (with-figures {"fig-2.svg" drawn} #(refusal sketch-md)) "diagram 1") "no fig-1")
  (is (str/includes? (with-figures {"fig-1.svg" drawn} #(refusal sketch-md)) "diagram 2") "no fig-2")
  (is (nil? (with-figures {"fig-1.svg" drawn "fig-2.svg" drawn} #(refusal sketch-md))))
  (is (str/includes? (refusal "### Proposal 1: x\n\n```\n+-------+\n| One   |\n+-------+\n    |\n    v\n+-------+\n| Two   |\n+-------+\n```\n") "diagram 1")
      "an unlabelled fence is a text fence")
  (is (str/includes? (refusal "```figure\n{:nodes [{:id 1 :label \"a\"} {:id 2 :label \"b\"}] :edges [{:from 1 :to 2}]}\n```\n") "diagram 1")
      "a figure fence needs its figure too"))

(deftest refusal-names-the-diagram
  (is (str/includes? (refusal sketch-md) "+-------+")))

(deftest cli-exits-nonzero-with-one-line
  (let [dir (fs/create-temp-dir)
        src (str (fs/path dir "b.md")) out (str (fs/path dir "b.html"))]
    (try (spit src sketch-md)
         (let [r (clojure.java.shell/sh "bb" (str (fs/path tools-dir "book-build.clj")) src out)]
           (is (= 1 (:exit r)))
           (is (str/starts-with? (:err r) "book-build: diagram 1"))
           (is (= 1 (count (str/split-lines (:err r)))))
           (is (not (fs/exists? out))))
         (let [fd (fs/create-dirs (fs/path dir "figs"))]
           (spit (str (fs/path fd "fig-1.svg")) drawn) (spit (str (fs/path fd "fig-2.svg")) drawn)
           (let [r (clojure.java.shell/sh "bb" (str (fs/path tools-dir "book-build.clj")) src out "--figures" (str fd))]
             (is (= 0 (:exit r)) (:err r))
             (is (str/includes? (slurp out) "DRAWN"))))
         (finally (fs/delete-tree dir)))))

(deftest code-and-signed-fences-need-no-figure
  (is (nil? (refusal "### Proposal 1: x\n\n```\nlet a = 1;\nlet b = 2;\n```\n")))
  (is (nil? (refusal "### Proposal 1: x\n\n```rust\nlet a = 1;\n```\n")))
  (is (nil? (refusal "### Proposal 1: x\n\n```text\n- +-------+\n- | One   |\n- +-------+\n- |\n- v\n- +-------+\n- | Two   |\n- +-------+\n+ plain\n```\n"))
      "a proposal's signed lines are code, not a diagram"))

(deftest section-proposal-says-where-it-lands
  (let [html (book-build/build (str "## Proposal 2: add to the vision of `books`\n\n+ One line.\n\nRuling: land, amend, or reject.\n\n"
                                    "## Technical part\n\n- a note\n") "")]
    (is (str/includes? html (str "<article class=\"proposal\"><header><span class=\"pnum\">2</span>"
                                 "<h2 class=\"target\"><code style=\"font-size:.95rem\">add to the vision of books</code></h2></header>")))
    (is (str/includes? html "<p>Ruling: land, amend, or reject.</p>\n</article>\n<h2>Technical part</h2>\n<ul><li>a note</li></ul>")
        "the next section closes the proposal")))

(deftest section-proposal-with-a-file-line
  (let [html (book-build/build "## Proposal 1: no noise\n\nFile: the vision of books\n\n+ Plain.\n" "")]
    (is (str/includes? html "<span class=\"pnum\">1</span><h2>no noise</h2></header>"))
    (is (str/includes? html "<p class=\"target\"><code>the vision of books</code></p>")))
  (let [html (book-build/build "## Proposal 1: T\n\nFile: `a/b.md`\n\n+ Plain.\n" "")]
    (is (str/includes? html "<h2>T</h2>"))
    (is (str/includes? html "<p class=\"target\"><code>a/b.md</code></p>"))))

(deftest each-signed-line-outside-a-fence-is-its-own-line
  (let [html (book-build/build "## Proposal 1: x\n\n+ First added.\n+ Second added.\n+ - item one\n+ - item two\n" "")]
    (is (str/includes? html (str "<div class=\"diff\"><div class=\"add\"><ins><p>First added.</p></ins></div>"
                                 "<div class=\"add\"><ins><p>Second added.</p></ins></div>"
                                 "<div class=\"add\"><ins><ul><li>item one</li><li>item two</li></ul></ins></div></div>"))))
  (let [html (book-build/build "## Proposal 1: x\n\n- Gone one.\n- Gone two.\n" "")]
    (is (str/includes? html "<div class=\"del\"><del><p>Gone one.</p></del></div><div class=\"del\"><del><p>Gone two.</p></del></div>")))
  (let [html (book-build/build "## Proposal 1: x\n\n- old one\n- old two\n+ new one\n+ new two\n+ three\n" "")]
    (is (str/includes? html (str "<p><del>old</del><ins>new</ins> one</p><p><del>old</del><ins>new</ins> two</p>"
                                 "<div class=\"add\"><ins><p>three</p></ins></div>"))
        "removed lines pair line by line with the added lines after them"))
  (is (= "<div class=\"diff\"><p>first <del>old</del><ins>new</ins> line second <del>old</del><ins>new</ins> line</p></div>"
         (change "- first old line\n- second old line\n+ first new line\n+ second new line"))
      "inside a fence, lines still flow as one paragraph"))

(deftest title-from-presentation-datom
  (let [html (book-build/build "<!-- c -->\nPresentation.{ «Drawing ideas, 2nd edition» }\n\n# Drawing ideas\n" "")]
    (is (str/includes? html "<title>Drawing ideas, 2nd edition</title>"))
    (is (str/includes? html "<h1 class=\"book-title\">Drawing ideas</h1>"))
    (is (not (str/includes? html "Presentation.{"))))
  (is (str/includes? (book-build/build "# Plain\n" "") "<title>Plain</title>")))

(let [{:keys [fail error]} (run-tests 'book-build-test)]
  (System/exit (if (zero? (+ fail error)) 0 1)))
