<!-- to-the-living:start -->
Presentation.{ «Where the green went» }

# Where the green went

«Tools instead of scripts» has no green block and no code. The page did not lose them; the writer never wrote them. In each of its five proposals the target is a tool described in prose, with no file and no removed or added lines. The last ten books show no code at all, and two of them have no green block.

```
 the book writer starts
          |
          v
 +------------------------------+
 | seat prompt: spirit, design  |
 | no book-format module        |
 +------------------------------+
          |
          v
 +------------------------------+
 | rule: no operational command |
 | reaches a book               |
 +------------------------------+
          |
          v
 +------------------------------+
 | proposal: a tool in prose    |
 | no file, no + or - lines     |
 +------------------------------+
          |
          v
 +------------------------------+
 | checker: any nonblank line   |
 | counts as a proposal         |
 +------------------------------+
          |
          v
 +------------------------------+
 | renderer may not invent      |
 | a change: no green           |
 +------------------------------+
```

## The failures

1. No green block. A proposal describes a change instead of giving it.
2. No code. A book about tools shows none of their code.
3. The target is not a file. "The transcript tool" is not a file anyone can open.
4. No surrounding file. The changed lines are not shown where they sit.
5. Each writer marks a change differently ("Added:", "Replaced by:", "Crystallized:"), so the renderer has to guess.
6. The book was written above the context limit. Fable wrote it at 443k tokens.

The remedies follow, one proposal each. The sixth failure is already being covered by the hook that warns at 200k tokens, so it needs no line here.

## Crystallization

### 1. A book about code shows the code

File: field-context/skills/compensation-book-distillation.md

- How the system runs today is knowledge, landed without the living's review; no runtime version, socket or store path, or operational command reaches a book; the authored file targeted by a proposal stays named.
+ How the system runs today is knowledge, landed without the living's review; no runtime version, socket or store path reaches a book; the authored file targeted by a proposal stays named.
+ A proposal whose subject is code shows the code: the type, the call, the changed lines of the source file.

Ruling: land, amend, or reject.

### 2. One way to write a change

File: field-context/skills/compensation-book-distillation.md

+ A change is written as a line `File: <path>`, then each removed line starting with `- `, each added line with `+ `, and unchanged lines around them starting with two spaces.

Ruling: land, amend, or reject.

### 3. The checker refuses a book with nothing to turn green

File: tools/book-check.mjs

  if (section && line.trim() && !/^Presentation\./.test(line)) section.content = true;
+ if (section && /^File: \S/.test(line)) hasTarget = true;
+ if (section && /^\+ /.test(line)) hasAdded = true;

and, after the existing check for a missing section:

  if (!hasCrystallization) errors.push({ reason: "missing-crystallization" });
+ if (hasCrystallization && !hasTarget) errors.push({ reason: "no-target-file" });
+ if (hasCrystallization && !hasAdded) errors.push({ reason: "no-added-line" });

The two flags are declared beside `hasCrystallization`, both false at the start.

Ruling: land, amend, or reject.

### 4. The book rules reach every Psyche seat

File: tools/main-flow-mode/spirit-system-prompt.mjs

  if (aspect === 'Psyche' || layer === 'Primary') names.push('vision-design');
  if (aspect === 'Psyche' || metaflow) names.push('intent-psyche-interaction');
+ if (aspect === 'Psyche') names.push('vision-book', 'compensation-book-distillation');
  names.push(...startupSkills.filter(name => name.startsWith('intent-')));

Ruling: land, amend, or reject.

### 5. A book about code has a file to target

File: psyche-context/skills/vision-book.md

- A book carries psyche only. Compensation, knowledge and operation skills are the machines' own: they write them and prove them by tests.
+ A book carries psyche, and the code its proposals change. Compensation, knowledge and operation skills are the machines' own: they write them and prove them by tests.

Ruling: land, amend, or reject.

Once these land, a second edition of «Tools instead of scripts» follows, written to these rules.
<!-- to-the-living:end -->
