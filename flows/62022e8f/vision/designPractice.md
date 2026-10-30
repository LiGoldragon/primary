# Design practice

## Do not spend Fable output on HTML: write markdown, let a subagent convert

> looking at how it looks like you were editing HTML, and I think it's a huge waste of fable to be editing HTML. So I think that if we, going forward, if this is possible, whenever you want to use these web-based user interfaces, I think you're better off writing a markdown, which is more token efficient. And just, you know, and also it gives us like a markdown version of the same thing. And just letting a sub-agent do the conversion. But, you know, I'm not, and consider, like, let's consider all the aspects of this. But yeah, I don't like the idea of using fable output, which is extremely expensive, to write HTML.

-- psyche, STT.

## The converting subflow can also pick the colors

Context: sent while the flow was fixing the clipped mermaid labels on
the recap page, right after the ruling that markdown is authored and
a subagent converts. Recovered from the transcript by flow 995a164e.

> the subflow can also pick colors

-- psyche, typed.
