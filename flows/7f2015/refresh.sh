#!/usr/bin/env bash
# Refresh of { Psyche core Secondary } on the new Flow Nexus, by path a.
# Run by another flow of the new Nexus, so that the Launch is identified.
set -u
W=/home/li/primary/flows/0f074c/migration
NB=/nix/store/r1k4wad7zdic9mg24fkqpqjx8xf58f0q-flow-configured-0.44.0/bin
LOG=/home/li/primary/flows/7f2015/refresh.log
NAME="Psyche core Secondary"
OLD=7f2015
meta(){ FLOW_META_SOCKET=/run/user/1001/flow-harnessflags/flow-meta.sock $NB/flow-meta "$@"; }
flw(){ FLOW_SOCKET=/run/user/1001/flow-harnessflags/flow.sock $NB/flow "$@"; }
flip(){ # CONT TAG
  meta Configuration > $W/$2-pre.txt || return 1
  python3 -I $W/flip.py build $W/$2-pre.txt "$NAME" "$1" $W/$2-sent.datom || return 1
  meta "$(cat $W/$2-sent.datom)" || return 1
  meta Configuration > $W/$2-readback.txt || return 1
  python3 -I $W/flip.py diff $W/$2-pre.txt $W/$2-readback.txt || { echo DIFF-BAD; return 1; }
}
exec >>"$LOG" 2>&1
echo "== $(date -Is) refresh begins"
sleep 60
flw Metaflows | grep -o "{ { $NAME } [A-Za-z]*\.[0-9a-f]*" || true
flip OnDemand refresh-cs-a || { echo "STOP at flip OnDemand"; exit 1; }
echo "-- Retire"; meta "Retire.$OLD" || { echo "STOP at Retire"; exit 1; }
sleep 5
echo "-- Launch"
flw "Launch.{ { $NAME } Custom.[ $OLD ] «read your handover whole first» }" || echo "LAUNCH FAILED"
flip Maintained refresh-cs-b || echo "FLIP BACK FAILED"
flw Metaflows | grep -o "{ { $NAME } [A-Za-z]*\.[0-9a-f]*" || true
echo "== $(date -Is) refresh ends"
