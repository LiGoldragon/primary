import csv, json, pathlib, subprocess, importlib.util, statistics, datetime, hashlib
root=pathlib.Path('/home/li/primary'); out=pathlib.Path('/tmp/field-world-20260921/skills')
auth=pathlib.Path('/home/li/wt/github.com/LiGoldragon/Curriculum/curriculum-data-only')
scopes={
 'authored_available_checkout':sorted((auth/'skills').glob('*.md')),
 'generated_agents':sorted((root/'.agents/skills').glob('*/SKILL.md')),
 'generated_claude':sorted((root/'.claude/skills').glob('*/SKILL.md')),
}
def item(p):
 b=p.read_bytes(); name=p.parent.name if p.name=='SKILL.md' else p.stem
 return {'name':name,'bytes':len(b),'path':str(p),'sha256':hashlib.sha256(b).hexdigest()}
data={k:[item(p) for p in v] for k,v in scopes.items()}
def distribution(v):
 s=sorted(x['bytes'] for x in v)
 return {'count':len(s),'totalBytes':sum(s),'medianBytes':statistics.median(s) if s else 0,
         'p90Bytes':s[min(len(s)-1,int(.9*(len(s)-1)))] if s else 0,
         'maxBytes':max(s) if s else 0,
         'testingPrefixCount':sum(x['name'].startswith('testing-') for x in v),
         'operationalPrefixCount':sum(x['name'].startswith('operational-') for x in v)}
projections={k:{x['name']:x for x in data[k]} for k in ('generated_agents','generated_claude')}
shared=set(projections['generated_agents'])&set(projections['generated_claude'])
pairedIdentical=sum(projections['generated_agents'][x]['sha256']==projections['generated_claude'][x]['sha256'] for x in shared)
profiles=[]
for seat,path,pred,fresh in [
 ('field-astra-of-6db4fe','flows/6db4fe/field-astra-native/profile.json','6db4fe',False),
 ('field-sol-of-7091ea','flows/6db4fe/field-sol-native/profile.json','7091ea',False),
 ('mind-sol','flows/6db4fe/mind-sol-native/profile.json',None,True)]:
 p=root/path; x=json.loads(p.read_text()); args=['node',str(root/'tools/native-seat-launch.mjs'),'--seat',seat,'--profile-file',str(p),'--cwd',str(root),'--prompt']+(['--fresh'] if fresh else ['--predecessor',pred]);
 try:
  result=subprocess.run(args,capture_output=True,check=True); prompt=result.stdout.rstrip(b'\n'); err=None
 except subprocess.CalledProcessError as e: prompt=b'';err=e.stderr.decode(errors='replace')[:180]
 profiles.append({'profile':path,'harness':'Codex','role':x.get('role'),'model':x.get('model'),'skillsCount':len(x.get('skills',[])),
  'sourceCount':len(x.get('sourceManifest',[])),'sourceBodyBytes':sum((root/s).stat().st_size for s in x.get('sourceManifest',[]) if (root/s).is_file()),
  'renderedPromptBytes':len(prompt) if prompt else None,'renderMethod':'native-seat-launch.mjs --prompt','error':err})
p=root/'tools/claude-native-seat-refresh.py'; spec=importlib.util.spec_from_file_location('claude_seat',p); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
for path in ['flows/753e69/psyche-low-native/profile.json','flows/753e69/psyche-haiku-native/profile.json']:
 p=root/path;x=json.loads(p.read_text())
 try:
  sources=mod.validate_sources(x,root); prompt=mod.role_prompt(x,sources); err=None
 except Exception as e:
  sources=[{'body':(root/y['path']).read_text()} for y in x.get('sources',[]) if (root/y['path']).is_file()]; prompt=None; err=str(e)[:180]
 profiles.append({'profile':path,'harness':'Claude','role':x.get('role'),'model':x.get('model'),'skillsCount':len(x.get('skills',[])),
  'sourceCount':len(sources),'sourceBodyBytes':sum(len(y['body'].encode()) for y in sources),
  'renderedPromptBytes':len(prompt.encode()) if prompt is not None else None,'renderMethod':'claude-native-seat-refresh.role_prompt after source validation','error':err})
result={'snapshotAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':str(root),'authoredAvailableCheckout':str(auth),
 'caveat':'Available Curriculum checkout is not proven to be the latest source of the installed projections; generated inventory is current disk snapshot, not loaded model context.',
 'distribution':{k:distribution(v) for k,v in data.items()},
 'largestGeneratedAgents':sorted(data['generated_agents'],key=lambda x:x['bytes'],reverse=True)[:10],
 'projectionDuplicate':{'sharedNames':len(shared),'identicalBodies':pairedIdentical,'totalProjectionBytes':sum(x['bytes'] for k in ('generated_agents','generated_claude') for x in data[k]),'uniqueBodiesAcrossTwoTrees':len({x['sha256'] for k in ('generated_agents','generated_claude') for x in data[k]})},
 'profiles':profiles,'estimate':'No token counts; bytes are UTF-8 source/prompt lengths. chars/4 would be a rough estimate, not API usage.'}
(out/'inventory.json').write_text(json.dumps(result,indent=2)+'\n')
with (out/'skill-sizes.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['scope','name','bytes','path']);w.writeheader()
 for k,v in data.items():
  for x in v:w.writerow({a:(k if a=='scope' else x[a]) for a in ('scope','name','bytes','path')})
with (out/'profile-prompts.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['profile','harness','role','model','skillsCount','sourceCount','sourceBodyBytes','renderedPromptBytes','renderMethod','error']);w.writeheader();w.writerows(profiles)
print(json.dumps({'distribution':result['distribution'],'projectionDuplicate':result['projectionDuplicate'],'profiles':profiles},indent=2))
