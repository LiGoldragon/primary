#!/usr/bin/env python3
"""Proposal 2 finite admission boundary. No runtime action occurs without a complete manifest."""
import json
import pathlib
import sys
import os, re, hashlib, subprocess, shlex

REQUIRED = {
    "candidate_commit", "flow_package", "curriculum_package", "place_compiler",
    "herdr", "raw_codex", "host_path", "bash", "python", "systemd_run",
    "systemctl", "provider_hashes", "admission_review_hash", "driver_hash",
    "unit_name", "root", "event_observer_api", "native_prompts_hash",
}
EXPECTED_COMMIT = "fe5a6930871707a7086c9a647867a519734220ef"

class AdmissionError(Exception):
    pass

def validate(doc):
    if not isinstance(doc, dict):
        raise AdmissionError("manifest must be a JSON object")
    missing = sorted(REQUIRED - doc.keys())
    if missing:
        raise AdmissionError("unobserved required inputs: " + ", ".join(missing))
    if doc["candidate_commit"] != EXPECTED_COMMIT:
        raise AdmissionError("candidate commit differs from reviewed source pin")
    for key in REQUIRED - {"provider_hashes"}:
        value = doc[key]
        if not isinstance(value, str) or not value.strip() or "PENDING" in value.upper():
            raise AdmissionError(f"unobserved or invalid {key}")
    hashes = doc["provider_hashes"]
    if not isinstance(hashes, dict) or not hashes:
        raise AdmissionError("provider_hashes must bind every executable/provider")
    for name, digest in hashes.items():
        if not isinstance(name, str) or not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise AdmissionError("provider hash malformed")
    for key in ("flow_package", "curriculum_package", "place_compiler", "herdr", "raw_codex", "host_path", "bash", "python", "systemd_run", "systemctl"):
        if not os.path.isabs(doc[key]): raise AdmissionError(f"{key} must be an absolute path")
    return doc

def receipt(actual, expected):
    tok = re.compile(r'«(?:\\.|[^»])*»|[{}\[\]]|[^\s{}\[\]«»]+')
    def lex(s): return [x[1:-1].replace('\\»','»') if x.startswith('«') else x for x in tok.findall(s.strip())]
    if not actual.strip() or lex(actual) != lex(expected): raise AdmissionError("typed receipt mismatch")

def render_prompts(root, flow):
    cli = shlex.quote(os.path.join(flow,"bin/flow")); xdg=shlex.quote(os.path.join(root,"config"))
    env=f"XDG_CONFIG_HOME={xdg} {cli}"
    return [
      f"Task: {env} 'Send.{{ {{ Mind proposalTwoReceiver Luna }} Soft.Task.{{ 15 «P2-task-before: hold until phase A authorization.» }} }}'",
      f"Living: {env} 'Send.{{ {{ Mind proposalTwoReceiver Luna }} Soft.Living.{{ «Proposal 2 isolated matrix» «P2-living-before: record this statement.» }} }}'",
      f"Done: {env} 'Send.{{ {{ Mind proposalTwoSender Luna }} Soft.Done.{{ <captured-T> «P2-done-before» }} }}'",
      f"PhaseB Task: {env} 'Send.{{ {{ Mind proposalTwoReceiver Luna }} Soft.Task.{{ 15 «P2-task-carry-required-7a97» }} }}'",
    ]

def unit_guard(saved, observed):
    keys=("Id","InvocationID","ControlGroup","MainPID","ExecStart")
    if any(not saved.get(k) or saved.get(k)!=observed.get(k) for k in keys): raise AdmissionError("unit identity mismatch: refuse stop")

def cgroup_guard(expected, observed):
    if not expected or observed != expected: raise AdmissionError("cgroup mismatch or populated cgroup: retain custody")

def production_compare(before, after):
    required=("configuration.datom","fable-current.datom","services","clients")
    if any(before.get(k) is None or before.get(k)!=after.get(k) for k in required): raise AdmissionError("production witness changed/incomplete")

def prepare(root, doc):
    # Side effects begin only after complete manifest validation and explicit roots.
    root=pathlib.Path(root); root.mkdir(mode=0o700, parents=False, exist_ok=False)
    for p in ("home","config/nexus/proposalTwo","config/herdr/sessions/proposal2-e7552e","runtime/nexus/proposalTwo","runtime/curriculum","runtime/codex","state","codex/sessions","source/flows","contexts","bin","evidence"):
        (root/p).mkdir(mode=0o700,parents=True,exist_ok=True)
    (root/"config/nexus/flow-nexus.datom").write_text("{ proposalTwo }\n")
    (root/"place.datom").write_text(f'{{ proposalTwo «{root}/runtime/nexus/proposalTwo» «{root}/state» }}\n')
    (root/"evidence/auth-target-metadata.json").write_text("METADATA_ONLY: operator lstat required before link\n")
    # Immutable candidate scripts only; the missing native event subscriber is
    # an explicit gate before any service start or authentication link.
    (root/"evidence/native-entrypoint.status").write_text("DISABLED: event-only observer/admission not supplied\n")

def unit_stop_command(saved, observed, unit):
    unit_guard(saved, observed)
    if not re.fullmatch(r"proposal2-[A-Za-z0-9_.-]+\.service",unit): raise AdmissionError("unit name outside reserved namespace")
    return ["systemctl","--user","stop","--job-mode=fail",unit]

def metadata_record(target, link):
    st=os.stat(target,follow_symlinks=False)
    if not os.path.isfile(target) or st.st_uid != os.getuid(): raise AdmissionError("auth target must be owned regular file")
    if os.path.lexists(link): raise AdmissionError("private auth link already exists")
    return {"uid":st.st_uid,"mode":oct(st.st_mode & 0o777),"device":st.st_dev,"inode":st.st_ino,"size":st.st_size,"mtime_ns":st.st_mtime_ns}

def write_private_config(root, manifest):
    root=pathlib.Path(root)
    content='approval_policy = "never"\nsandbox_mode = "danger-full-access"\ncli_auth_credentials_store = "file"\nmodel = "gpt-6-luna"\nmodel_reasoning_effort = "medium"\n'
    (root/"codex/config.toml").write_text(content)
    (root/"config/herdr/config.toml").write_text(f'[agents]\ncodex_executables = ["{root}/bin/codex-private"]\n')
    (root/"bin/codex-private").write_text(f'#!/bin/sh\nexport CODEX_HOME="{root}/codex"\nexec "{manifest["raw_codex"]}" "$@"\n')
    os.chmod(root/"bin/codex-private",0o700)

def private_environment(root, manifest):
    root=str(pathlib.Path(root).resolve())
    return {"HOME":root+"/home","USER":"li","LOGNAME":"li","LANG":"C.UTF-8",
      "PATH":root+"/bin:"+manifest["flow_package"]+"/bin:"+manifest["host_path"],
      "XDG_CONFIG_HOME":root+"/config","XDG_DATA_HOME":root+"/home/.local/share",
      "XDG_STATE_HOME":root+"/home/.local/state","XDG_CACHE_HOME":root+"/home/.cache",
      "XDG_RUNTIME_DIR":root+"/runtime","CODEX_HOME":root+"/codex",
      "CURRICULUM_CONTEXT_LAYOUT":"2","CURRICULUM_CONTEXT_REFRESH_PROGRAM":root+"/bin/context-refresh",
      "CURRICULUM_RECORDS_DIR":root+"/source/flows"}

def main(argv):
    if len(argv) < 3:
        print("usage: controller.py MANIFEST {preflight|prepare|prompts}", file=sys.stderr); return 64
    try:
        doc=validate(json.loads(pathlib.Path(argv[1]).read_text()))
        op=argv[2]
        if op=="preflight": print("manifest structurally valid; native execution still requires reviewed admission"); return 0
        if op=="prepare": prepare(argv[3],doc); return 0
        if op=="prompts": print("\n".join(render_prompts(argv[3],doc["flow_package"]))); return 0
        if op=="unit-guard": unit_guard(json.loads(pathlib.Path(argv[3]).read_text()),json.loads(pathlib.Path(argv[4]).read_text())); return 0
        if op=="cgroup-guard": cgroup_guard(pathlib.Path(argv[3]).read_text().strip(),pathlib.Path(argv[4]).read_text().strip()); return 0
        raise AdmissionError("unknown operation")
    except (OSError, json.JSONDecodeError, AdmissionError, IndexError) as exc:
        print(f"STOP: {exc}", file=sys.stderr); return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
