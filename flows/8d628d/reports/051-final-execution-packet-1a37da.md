# Current operator identity supplement

Core explicitly appoints Psyche core Secondary1a37da/native1a37dae5-9b69-5be0-8e8e-c41ce2dae7f6. This packet changes ONLY the operator identity; reviewed payload/comparator/guards are unchanged. Previous interval cancelled, no reuse. Stop on any further identity drift. Read-only cancelled-window reconciliation is separately authorized, not permission to write. A new explicit interval and actual READY remain required.

# 051 final execution packet — awaiting explicit START

Sole executor: existing Psyche core Secondary1a37da. No other operator. No effect is authorized by this packet alone. Coordinator supplies an explicit interval of at most two minutes after renewed holds/READY. Stop on refusal, uncertainty, mismatch, changed identity or expiry; never replay a write.

## Reviewed immutable inputs
Independent final payload reviewer /root/final_051_payload_review structurally compared all65 declarations, four frozen hashes, and finaldiff. PASS: only55 presentation substitutions plus exactaudit/book trims; all other fields/models preserved. CorePrimary explicitly reaffirmed afterSHA702ded after reading accessible finaldiff/partition; historical audit is not authority.
- Frozen BEFORE /home/li/primary/flows/1d381c/reports/three-change-classes.before.datom SHA256 b9a777394f77145c62e8442104c92f44d7cf575f795e4726581706d948f96197.
- Frozen AFTER /home/li/primary/flows/1d381c/reports/three-change-classes.after.PROPOSED.datom SHA256 702deda8c5b6600423b25b19dfa3b36a49193cd00092ca9b4aa95356ffba9bef.
- FINALdiff /home/li/primary/flows/1d381c/reports/three-change-classes.FINAL-PROPOSED.diff SHA25697ba1a78a65d095f65f691791e76b26a03fdb74b5163e653c54488d28161abf9.
- FINALpartition /home/li/primary/flows/1d381c/reports/three-change-classes.FINAL-partition.json SHA256720e5e27889c6eb3e1725f2826e0f27aeb2c8094ceca0aa0bc0e46dd312c01de.
- ACTUAL ONE write payload /home/li/primary/flows/8d628d/reports/051-reviewed-configure.datom SHA25696efe7a273426d9443856065ba6ff4c81c6408e3dd9fd9af71f3cfa323010e63. Exact bytes Configure.Metaflows. prefixed to frozenAFTER vector. No added newline or other edits.
- Read-only comparator /home/li/primary/flows/8d628d/reports/configuration-metaflows-compare.py SHA256bf4e70730e681ddb1f0ed4d73ae83de616c2b8756d8df66c2ed0aa7630ac9904.

Comparator follows pinnedmeta281f5aa: Configuration.{snapshot}, exactly11positions, completeMetaflows vector atindex5. Includes EVERY declaration field, omits none; no runtimefieldprojection. Purelocal tests against actual frozenbefore/after pass matching, mismatchedvectors, nestedmutation, whitespace/comments, refusal/wronghead/arity/trailing/malformed/escapedguillemet cases. No livequery was used to claim a hash. Compare structuralvector to exact expectedbytes, not whole unrelatedconfiguration snapshot.

## Ordered operator procedure during explicit interval
1. Verify all five relevant input hashes and actual UTC interval. Read-only caller preflight from ACTUAL own toolprocess; capture PID,UID,start via /proc,self/executable/native linkage, resolve that real identity using ResolvePeer, and read Configuration plus Inspect.{ Psyche core Secondary }. Require positively current1a37da/Psyche and guard admission; Unknown/refusal/mismatch stops. No identity spoof, MetaAspects change or historical inference.
2. Obtain fresh Configuration. Run comparator against frozenBEFORE and its hash; require PASS immediately before write. Wholefamily API has no CAS: any changed declaration stops, no rebase. Also read Inspect.{ Psyche flowAudit Secondary }; capture currentnode999b21 and exact currentnative. If not current999b21 or identity absent, stop and report rather than retarget.
3. Invoke /home/li/.local/bin/flow-meta with the complete immutable actualpayload as its ONE datom argument ONCE. Require typed successful outcome; any refusal, uncertain submission/receipt or error stops, no retry. Preserve wholeanswer.
4. Obtain fresh Configuration, compare against frozenAFTER with exact hash; require PASS. Report Configure outcome separately from Retire. This confirms auditOnDemand, bookmakerMaintained, all other declarations preserved.
5. Immediately before separate ONE Retire, fresh Inspect.{ Psyche flowAudit Secondary } must still show current999b21 and EXACT native capturedstep2 plus committedOnDemand. Any mismatch stops. Then invoke flow-meta 'Retire.999b21' ONCE. Require FlowRetired nodeID999b21, guardednative, lifecycleRetired; obtain Inspect audit/current-past and actualpaneclosure witness. RetireRejected or uncertain/StoreRefused stops; Close can occur beforeStoreRefused so never blindlyretry. Do not launch audit; Psyche controls relaunch.
6. Return exact UTC start/end, actualcaller evidence, all complete replies, pre/post comparator receipts, immediateRetireguard and closure evidence. Confirm intervalclosed and noeffects leftinflight. No other Configure, restart, refresh, deploy, furnishing, publication or probe.

## Comparator invocation
python3 -B /home/li/primary/flows/8d628d/reports/configuration-metaflows-compare.py EXPECTED_PATH EXPECTED_SHA256 < saved-configuration-reply.datom

Owned evidence files only; this invocation is read-only. Typedrefusal/Unconfigured cannot pass.

## Safe actual caller capture (read-only, NOT a START)
Keep this Python process alive during its real CLI child queries; values are actual, not set identities:
python3 - <<'PY'
import os, pathlib, subprocess
p=pathlib.Path('/proc/self')
pid,uid=os.getpid(),p.stat().st_uid
start=(p/'stat').read_text().rsplit(') ',1)[1].split()[19]
print({'pid':pid,'uid':uid,'start':start,'exe':os.readlink(p/'exe'),'ppid':os.getppid()},flush=True)
for q in [f'ResolvePeer.{{ {pid} {uid} {start} }}','Configuration','Inspect.{ Psyche core Secondary }']:
    subprocess.run(['/home/li/.local/bin/flow-meta',q],check=True)
PY
A CLI exit0 is not typed admission. Decode the actual reply; only current1a37da/Psyche plus currentnative binding is acceptable. This preflight does not start or authorize any effect.
