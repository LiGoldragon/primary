# The living's words used in the book, each with its raw record.
# verify.py checks every `text` is a verbatim substring of the record's own words.
P = '/home/li/.claude/projects/-home-li-primary/'
QUOTES = {
    'sessions': dict(
        text="Like I said I see these three weird-looking random sessions that cost me money and I don't even know why they are there but I don't see any Mind Astra.",
        file='CODEX:rollout-2026-09-30T23-50-23-01a0f603-8dc3-7fb0-bde5-6ace2a70a4eb.jsonl', line=1169,
        prov='1 October, 17:46 UTC · flow e2a70a, line 1169'),
    'stray': dict(
        text="I didn't say all three workspaces. I said all of the stray workspace.",
        file=P + 'fe945a2e-c785-4af4-9a46-766b6ea512e8.jsonl', line=308,
        prov='1 October, 17:31 UTC · flow fe945a, line 308'),
    'zoom': dict(
        text="This is also very hard to read. I have to zoom to see anything and then I can't even swipe to move the zoom around. I have to unzoom and rezoom. It's basically unusable and I've talked about this.",
        file=P + '183ae001-cb84-40ed-8a1f-f07a76f0d1f4.jsonl', line=715,
        prov='29 September, 00:26 UTC · flow 183ae0, line 715'),
    'comment': dict(
        text="I think the only thing that works really is the comment so we might as well just get rid of the buttons and all that and I'll just comment",
        file=P + '183ae001-cb84-40ed-8a1f-f07a76f0d1f4.jsonl', line=469,
        prov='28 September, 23:35 UTC · flow 183ae0, line 469'),
    'mindlog': dict(
        text="Maybe we'd need another way to log something. It's maybe mind-oriented.",
        file=P + '6997eb8a-30eb-49a1-a787-45279164a43b.jsonl', line=444,
        prov='1 October, 18:02 UTC · flow 6997eb, line 444'),
    'body': dict(
        text="The field is the actual body of the machine.",
        file=P + '6997eb8a-30eb-49a1-a787-45279164a43b.jsonl', line=444,
        prov='1 October, 18:02 UTC · flow 6997eb, line 444'),
    'mark': dict(
        text="We're going to train all of the main flows to, whenever they want to talk to the living, mark that block as intended for the living at the beginning and at the end.",
        file=P + '6997eb8a-30eb-49a1-a787-45279164a43b.jsonl', line=541,
        prov='1 October, 18:08 UTC · flow 6997eb, line 541'),
    'waste': dict(
        text="We have to stop doing that because it's a huge waste of context.",
        file=P + '6997eb8a-30eb-49a1-a787-45279164a43b.jsonl', line=541,
        prov='1 October, 18:08 UTC · flow 6997eb, line 541'),
    'cryptic': dict(
        text="some of the things you say are cryptic, like the box on your bed.",
        file=P + 'c64ee3f5-0732-4315-936e-7ffc63e3000b.jsonl', line=1669,
        prov='30 September, 17:27 UTC · flow c64ee3, line 1669'),
}
