#!/usr/bin/env python3
"""Inject each Claude slash skill as its own idle-gated user turn."""

import json
import subprocess
import sys
import time

SESSION = sys.argv[1]
SKILLS = [
    "/spirit",
    "/psyche",
    "/behavior",
    "/correction",
    "/vocabulary",
    "/testing",
    "/psyche-interraction",
    "/main-flow",
]
INJECT = "/home/li/primary/flows/024bc7/tools/claude_inject.py"


def idle():
    agents = json.loads(subprocess.check_output(["claude", "agents", "--json"], text=True))
    return any(agent.get("id") == SESSION and agent.get("status") == "idle" for agent in agents)


for skill in SKILLS:
    while not idle():
        time.sleep(5)
    subprocess.run(["python3", INJECT, SESSION, skill], check=True)
