import json,collections
d=json.load(open('data.json')); S=d['skills']; r=d['vision']['raw']; P=d['vc']['primary']
match={h:sum(1 for s in S if s['generated'][h]=='match') for h in d['tree_counts']}
kinds=collections.Counter(s['kind'] for s in S); repos=collections.Counter(s['repo'] for s in S)
dist=[x for x in r if x['distilled']]
em=collections.Counter(); [em.update(x['entry_months']) for x in r]
places=[]
for lab,pred in [('flows/*/vision',lambda x:x['dir']=='vision'),('flows/*/notion',lambda x:x['dir']=='notion'),('vision-raw',lambda x:x['dir']=='vision-raw')]:
    xs=[x for x in r if pred(x)]; places.append([lab,len(xs),sum(x['distilled'] for x in xs),sum(x['archive'] for x in xs)])
months=[dict(label=k if k!='uncommitted' else 'undated',**v) for k,v in d['vision']['by_month'].items()]
reposclean=all(v['dirty']==0 and v['main']==v['origin_main_remote'] for v in d['vc']['repos'].values())
gt=P['generated_trees']; gtd=sum(g['uncommitted_entries'] for g in gt.values())
ab=P['ahead_behind'].split()
VS=dict(Vision_exists=d['vision']['Vision_exists'],Vision_files=int(d['vision']['Vision_files']),Intent_exists=d['vision']['Intent_exists'],Vision_listing=d['vision']['Vision_listing'],
 vision_skills=kinds['vision'],intent_skills=kinds['intent'],raw_files=len(r),raw_entries=sum(x['entries'] for x in r),archive_files=sum(x['archive'] for x in r),
 distilled_files=len(dist),distilled_entries=sum(x['entries'] for x in dist),distilled_records=len({(x['flow'],x['record'].removeprefix('archive-')) for x in dist}),
 sources_lines=len(d['vision']['sources']),unresolved=len(d['vision']['unresolved_sources']),places=places,dated_entries=sum(x['dated_entries'] for x in r),
 entry_months=', '.join(f'{k}: {v}' for k,v in sorted(em.items())))
allmatch=all(v==len(S) for v in match.values())
status=[
 dict(q='Deployed?',v='yes' if d['deployment']['service']=='active' and allmatch else 'partial',label='YES' if d['deployment']['service']=='active' and allmatch else 'PARTIAL',
  note=f"curriculum-nexus <b>{d['deployment']['service']}</b> since {d['deployment']['active_since'][4:16]}; <b>{len(S)}/{len(S)}</b> skills match source in all {len(match)} trees."),
 dict(q='Version-controlled?',v='yes' if reposclean and P['dirty']==0 else 'partial',label='YES' if reposclean and P['dirty']==0 else 'PARTIAL',
  note=f"Skill repos and Curriculum: clean, main = origin. Primary: <b>{P['dirty']}</b> uncommitted entries, <b>{gtd}</b> in generated trees; repair pause in force."),
 dict(q='Main moved forward?',v='yes' if ab==['0','0'] else 'partial',label='YES' if ab==['0','0'] else 'DIVERGED',
  note=f"origin/main <b>{P['origin_main_remote']}</b> at {P['last5'][0]['date'][11:16]} today; local <b>{ab[0]}</b> ahead / <b>{ab[1]}</b> behind; 5 commits since {P['last5'][-1]['date'][11:16]}."),
 dict(q='Skills in three repos?',v='yes' if d['deployment']['curriculum_skills_dir_entries']==0 and len(repos)==3 else 'no',label='YES',
  note=f"psyche <b>{repos['psyche-skills']}</b> · mind <b>{repos['mind-skills']}</b> · field <b>{repos['field-skills']}</b>; Curriculum <b>0</b> (review/ keeps {d['deployment']['curriculum_review_unapproved']}+{d['deployment']['curriculum_review_retired']} set-aside drafts)."),
 dict(q='Vision migrated?',v='partial',label='PARTIAL',
  note=f"Vision/ still present (<b>{VS['Vision_files']}</b> files), Intent/ gone; <b>{VS['vision_skills']}</b> vision- and <b>{VS['intent_skills']}</b> intent- skills; <b>{VS['distilled_files']}</b> of <b>{VS['raw_files']}</b> raw files distilled."),
]
method=[
 "Skills: every <code>skills/*.md</code> in psyche-skills, mind-skills and field-skills. Kind is the name prefix. Description is the frontmatter <code>description:</code> line. Size is the authored file's bytes; tokens are bytes ÷ 4, an estimate, not a tokenizer count.",
 "Standing set: the last list in <code>Curriculum/roles.datom</code> (the universal modules every role loads).",
 "Generated match: each source is projected the way the Nexus does (<code>{% if claude|codex|pi %}</code> blocks resolved, <code>{% raw %}</code> unwrapped, and <code>user-only: true</code> written as <code>disable-model-invocation: true</code> for Claude; <code>.agents</code> takes the codex branch) and compared byte-for-byte with <code>SKILL.md</code> in each tree. The rule set was inferred from the diffs, not read from Nexus code. <code>.opencode</code> was not compared.",
 "Deployment: <code>systemctl --user</code> for curriculum-nexus.service. Version control: <code>git rev-parse</code>, <code>git ls-remote origin main</code>, <code>git status --porcelain</code>; no fetch was run, so the local tracking ref was checked against ls-remote.",
 "Vision: raw record files under <code>flows/*/vision</code>, <code>flows/*/notion</code> and <code>vision-raw</code>; entries are <code>## </code> headings; month is the file's first-add commit (followed across renames); 12 files have no recoverable add date. Distilled means a skill's <code>## Sources</code> lists <code>&lt;flow&gt; &lt;record&gt;</code> matching the file or its <code>archive-</code> copy.",
 "Data and scripts: <code>flows/d4ae97/reports/skills-status/</code> (data.json, gather.py, build.py)."]
out=dict(measured_at=d['measured_at'],skills=[{k:s[k] for k in ['name','kind','repo','description','bytes','tokens','standing','generated']} for s in S],
 standing_set=d['standing_set'],tree_counts=d['tree_counts'],match=match,deployment=d['deployment'],vc=d['vc'],vision_summary=VS,months=months,status=status,method=method)
t=open('template.html').read().replace('__DATA__',json.dumps(out).replace('</','<\\/'))
open('skills-status.html','w').write(t)
json.dump(dict(status=status,match=match,vision_summary=VS,months=months),open('summary.json','w'),indent=1)
print([ (s['q'],s['label']) for s in status]); print(len(t))
