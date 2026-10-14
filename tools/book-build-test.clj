;; Tests for tools/book-build.clj. Run: bb tools/book-build-test.clj
;; The two c5f24b books are rebuilt with the working-tree tools/book-code.html
;; and compared byte for byte with their published html. The fixture covers
;; Destroy/Archive records, a figure, rulings and lists; its expected page was
;; produced by the former Python builder with the tail TAIL.
(ns book-build-test
  (:require [clojure.test :refer [deftest is run-tests]]
            [babashka.fs :as fs]))

(def tools-dir (str (fs/parent (fs/absolutize *file*))))
(load-file (str (fs/path tools-dir "book-build.clj")))
(def root (str (fs/parent tools-dir)))
(def code (book-build/read-text (fs/path tools-dir "book-code.html")))

(defn rebuilt-matches? [book]
  (let [dir (fs/path root "flows/c5f24b/books")]
    (= (slurp (str (fs/path dir (str book ".html"))) :encoding "UTF-8")
       (book-build/build (book-build/read-text (fs/path dir (str book ".md"))) code))))

(deftest context-modules-book
  (is (rebuilt-matches? "09-context-modules")))

(deftest messaging-book
  (is (rebuilt-matches? "10-messaging-between-flows")))

(def fixture-md
  "# Fixture & <book>\n\n<!-- hidden comment -->\nPresentation.{ Book Fixture }\n\n## Crystallization\n\nAn opening paragraph with `inline <code>` and\na second line & more.\n\n### Proposal 1: Figures & `records`\n\nFile: `skills/vision-x/SKILL.md`, (builds on `vision-y`)\n\n```text\n  ---\n  name: vision-x\n  ---\n  ## A heading kept as text\n  Unchanged context line\n- Removed line one\n- removed line two\n+ Added line with `code`\n+ # added heading\n```\n\n```text\n+-----------------------+\n| Flow                  |\n| with \"two\" lines      |\n+-----------------------+\n           |\n           | sends it's\n           | message\n           v\n+-----------------------+\n| Recipient             |\n+-----------------------+\n     |\n     | reads\n     v\n+-----------------------+\n| Log                   |\n+-----------------------+\n```\n\n**Destroy** the record `flows/aa/vision/x.md` below.\n\nFile: `flows/aa/vision/x.md`\n\n```text\n- A working instruction logged as vision.\n```\n\n**Archive**\n\n```text\n- An archived line.\n```\n\n**Destroy** with nothing following.\n\n```js\nconst x = 1 < 2 && \"y\";\n```\n\nRuling, one number per line:\n\n1. Approve.\n2. Reject:\n\n```text\n+ inside the ruling card\n```\n\nAfter the card.\n\n### Proposal 2: Second\n\nGroup heading\n3. Third choice\ncontinued here.\n4. Fourth choice\n\nRuling, one number per line:\n\n3. Yes\n4. No\n\n```python\nprint(\"tail\")\n```\n\nTrailing paragraph.\n")

(def fixture-expected
  "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>Fixture &amp; &lt;book&gt;</title>\n<h1 class=\"book-title\">Fixture &amp; &lt;book&gt;</h1>\n<h2>Crystallization</h2>\n<p>An opening paragraph with <code>inline &lt;code&gt;</code> and a second line &amp; more.</p>\n<article class=\"proposal\"><header><span class=\"pnum\">1</span><h2>Figures &amp; <code>records</code></h2></header>\n<p class=\"target\"><code>skills/vision-x/SKILL.md</code></p><p>builds on <code>vision-y</code></p>\n<div class=\"diff\"><div class=\"ctx\"><div class=\"textblock\">---\nname: vision-x\n---</div></div><div class=\"ctx\"><div class=\"textblock\">## A heading kept as text</div></div><div class=\"ctx\"><p>Unchanged context line</p></div><div class=\"del\"><del><p>Removed line one removed line two</p></del></div><div class=\"add\"><ins><p>Added line with <code>code</code></p></ins></div><div class=\"add\"><ins><div class=\"textblock\"># added heading</div></ins></div></div>\n<svg viewBox=\"0 0 360 321\" width=\"100%\" role=\"img\" aria-label=\"Flow with &quot;two&quot; lines  sends it&#x27;s message Recipient  reads Log\" xmlns=\"http://www.w3.org/2000/svg\"><rect x=\"30\" y=\"10\" width=\"187.5\" height=\"60\" rx=\"3\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"/><text x=\"42\" y=\"36\" font-size=\"14\" fill=\"currentColor\" font-family=\"IBM Plex Sans Condensed, Arial Narrow, system-ui, sans-serif\">Flow</text><text x=\"42\" y=\"56\" font-size=\"14\" fill=\"currentColor\" font-family=\"IBM Plex Sans Condensed, Arial Narrow, system-ui, sans-serif\">with &quot;two&quot; lines</text><line x1=\"101.25\" y1=\"70\" x2=\"101.25\" y2=\"154\" stroke=\"currentColor\" stroke-width=\"1.5\"/><polygon points=\"97.25,154 105.25,154 101.25,162\" fill=\"currentColor\"/><text x=\"111.25\" y=\"85\" font-size=\"12\" fill=\"currentColor\" font-family=\"JetBrains Mono, ui-monospace, DejaVu Sans Mono, monospace\" text-anchor=\"start\"></text><text x=\"111.25\" y=\"108\" font-size=\"12\" fill=\"currentColor\" font-family=\"JetBrains Mono, ui-monospace, DejaVu Sans Mono, monospace\" text-anchor=\"start\">sends it&#x27;s</text><text x=\"111.25\" y=\"131\" font-size=\"12\" fill=\"currentColor\" font-family=\"JetBrains Mono, ui-monospace, DejaVu Sans Mono, monospace\" text-anchor=\"start\">message</text><rect x=\"30\" y=\"162\" width=\"187.5\" height=\"40\" rx=\"3\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"/><text x=\"42\" y=\"188\" font-size=\"14\" fill=\"currentColor\" font-family=\"IBM Plex Sans Condensed, Arial Narrow, system-ui, sans-serif\">Recipient</text><line x1=\"56.25\" y1=\"202\" x2=\"56.25\" y2=\"263\" stroke=\"currentColor\" stroke-width=\"1.5\"/><polygon points=\"52.25,263 60.25,263 56.25,271\" fill=\"currentColor\"/><text x=\"66.25\" y=\"217\" font-size=\"12\" fill=\"currentColor\" font-family=\"JetBrains Mono, ui-monospace, DejaVu Sans Mono, monospace\" text-anchor=\"start\"></text><text x=\"66.25\" y=\"240\" font-size=\"12\" fill=\"currentColor\" font-family=\"JetBrains Mono, ui-monospace, DejaVu Sans Mono, monospace\" text-anchor=\"start\">reads</text><rect x=\"30\" y=\"271\" width=\"187.5\" height=\"40\" rx=\"3\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.5\"/><text x=\"42\" y=\"297\" font-size=\"14\" fill=\"currentColor\" font-family=\"IBM Plex Sans Condensed, Arial Narrow, system-ui, sans-serif\">Log</text></svg>\n<div class=\"record destroy\"><p>the record <code>flows/aa/vision/x.md</code> below.</p>\n<p class=\"target\"><code>flows/aa/vision/x.md</code></p>\n<div class=\"del\"><del><p>A working instruction logged as vision.</p></del></div></div>\n<div class=\"record archive\">\n<div class=\"del\"><del><p>An archived line.</p></del></div></div>\n<div class=\"record destroy\"><p>with nothing following.</p>\n<pre data-diff><code class=\"language-javascript\">const x = 1 &lt; 2 &amp;&amp; \"y\";</code></pre>\n<section class=\"rulings\"><ol><li value=\"1\"><p>Ruling, one number per line:</p><ol class=\"choices\" start=\"1\"><li>Approve.</li><li>Reject:</li></ol><div class=\"add\"><ins><p>inside the ruling card</p></ins></div></div><p>After the card.</p></li></ol></section>\n</article>\n<article class=\"proposal\"><header><span class=\"pnum\">2</span><h2>Second</h2></header>\n<p>Group heading</p>\n<ol class=\"choices\" start=\"3\" style=\"counter-reset:choice 2\"><li>Third choice continued here.</li><li>Fourth choice</li></ol>\n<section class=\"rulings\"><ol><li value=\"2\"><p>Ruling, one number per line:</p><ol class=\"choices\" start=\"3\" style=\"counter-reset:choice 2\"><li>Yes</li><li>No</li></ol></li></ol></section><pre data-diff><code class=\"language-python\">print(\"tail\")</code></pre><p>Trailing paragraph.</p>\n</article>\nTAIL\n")

(deftest fixture-records-and-figure
  (is (= fixture-expected (book-build/build fixture-md "TAIL\n"))))

(deftest empty-line-in-text-fence
  (is (= "<div class=\"diff\"><div class=\"ctx\"><p>a</p></div><div class=\"ctx\"><p>b</p></div></div>\n"
         (book-build/build "```\na\n\nb\n```\n" ""))))

(let [{:keys [fail error]} (run-tests 'book-build-test)]
  (System/exit (if (zero? (+ fail error)) 0 1)))
