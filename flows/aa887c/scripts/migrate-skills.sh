#!/usr/bin/env bash
# Populate psyche-skills, mind-skills and field-skills (and psyche-logs for the
# archived Vision file) per flows/aa887c/reports/placing-table.md.
#
# Usage:
#   migrate-skills.sh --dry-run          list every write and run every check
#   STEM_CASE=kebab|camel CONDUCT_TYPE=vision|intent KEEP_PREFIX_PARAGRAPH=yes|no \
#     migrate-skills.sh                  write the files
#
# The three variables carry the open items 6, 3 and 10 of the table. A real run
# refuses until all three are set explicitly; a dry run uses the defaults
# kebab / vision / yes when they are unset. Sources are never deleted, and
# nothing is committed.
set -euo pipefail

DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1
if [ $# -gt 1 ] || { [ $# -eq 1 ] && [ "$DRY" = 0 ]; }; then echo "usage: $0 [--dry-run]" >&2; exit 2; fi

ROOT=/git/github.com/LiGoldragon
CUR=$ROOT/Curriculum/skills
PRI=/home/li/primary
SPL=$PRI/flows/aa887c/scripts/splits
declare -A REPO=([psyche]=$ROOT/psyche-skills [mind]=$ROOT/mind-skills [field]=$ROOT/field-skills [logs]=$ROOT/psyche-logs)

if [ "$DRY" = 0 ]; then
  for v in STEM_CASE CONDUCT_TYPE KEEP_PREFIX_PARAGRAPH; do
    [ -n "${!v:-}" ] || { echo "refused: $v is not set; it carries an open item for the living" >&2; exit 1; }
  done
fi
STEM_CASE=${STEM_CASE:-kebab}
CONDUCT_TYPE=${CONDUCT_TYPE:-vision}
KEEP_PREFIX_PARAGRAPH=${KEEP_PREFIX_PARAGRAPH:-yes}
case $STEM_CASE in kebab|camel) ;; *) echo "STEM_CASE must be kebab or camel" >&2; exit 1;; esac
case $CONDUCT_TYPE in vision|intent) ;; *) echo "CONDUCT_TYPE must be vision or intent" >&2; exit 1;; esac
case $KEEP_PREFIX_PARAGRAPH in yes|no) ;; *) echo "KEEP_PREFIX_PARAGRAPH must be yes or no" >&2; exit 1;; esac

if [ "$KEEP_PREFIX_PARAGRAPH" = yes ]; then VPSYCHE="whole:$PRI/Vision/psyche.md"
else VPSYCHE="whole:$SPL/85-psyche/psyche-psyche.no-prefix.md"; fi

# Manifest: repo|type|stem|rows|parts
# type CONDUCT resolves to $CONDUCT_TYPE. Parts are joined by one blank line:
#   whole:FILE   the file as it is
#   fm:FILE      the file's frontmatter block only
#   body:FILE    the file without its frontmatter
MANIFEST="
psyche|spirit|spirit|1|whole:$CUR/spirit.md
psyche|vision|psyche|2,85|fm:$CUR/psyche.md $VPSYCHE whole:$SPL/02-psyche/vision-psyche.body.md
psyche|CONDUCT|vocabulary|3|whole:$CUR/vocabulary.md
psyche|CONDUCT|behavior|4|whole:$SPL/04-behavior/vision-behavior.md
psyche|CONDUCT|correction|5|whole:$CUR/correction.md
psyche|CONDUCT|psyche-interraction|6|whole:$SPL/06-psyche-interraction/vision-psyche-interraction.md
psyche|vision|distillation|8,74|whole:$PRI/Vision/distillation.md whole:$SPL/08-psyche-distillation/vision-distillation.add.md
psyche|CONDUCT|skills|10|whole:$SPL/10-skill-designing/psyche-skills.md
psyche|vision|datom|12,72|fm:$CUR/datom.md whole:$PRI/Vision/datom.md body:$CUR/datom.md
psyche|vision|protos|13,84|fm:$CUR/protos.md whole:$PRI/Vision/protos.md body:$CUR/protos.md
psyche|vision|ethos|40,75|fm:$CUR/vision-ethos.md whole:$PRI/Vision/ethos.md body:$CUR/vision-ethos.md
psyche|vision|flow|41,76|fm:$CUR/vision-flow.md whole:$PRI/Vision/flowNexus.md body:$CUR/vision-flow.md
psyche|vision|nexus|42,82|fm:$CUR/vision-nexus.md whole:$PRI/Vision/nexus.md body:$CUR/vision-nexus.md
psyche|vision|modelRoles|47,81|whole:$SPL/81-modelRoles/psyche-modelRoles.md whole:$SPL/47-knowledge-layer-models/psyche-modelRoles.add.md
psyche|vision|messaging|80|whole:$SPL/80-messaging/psyche-messaging.md
psyche|vision|committing|71|whole:$PRI/Vision/committing.md
psyche|vision|deployment|73|whole:$PRI/Vision/deployment.md
psyche|vision|highLevelView|77|whole:$PRI/Vision/highLevelView.md
psyche|vision|horizon|78|whole:$PRI/Vision/horizon.md
psyche|vision|meaning|79|whole:$PRI/Vision/meaning.md
psyche|vision|orchestrate|83|whole:$PRI/Vision/orchestrate.md
psyche|vision|remembering|86|whole:$PRI/Vision/remembering.md
psyche|vision|sema|87|whole:$PRI/Vision/sema.md
psyche|vision|signal|88|whole:$PRI/Vision/signal.md
psyche|vision|x11|89|whole:$PRI/Vision/x11.md
psyche|intent|anatomy|91|whole:$PRI/Intent/anatomy.md
psyche|intent|context|92|whole:$PRI/Intent/context.md
psyche|intent|conversion|93|whole:$PRI/Intent/conversion.md
psyche|intent|data|94|whole:$PRI/Intent/data.md
psyche|intent|mandatoryTraits|95|whole:$PRI/Intent/mandatoryTraits.md
psyche|intent|models|96|whole:$PRI/Intent/models.md
psyche|intent|protosParsing|97|whole:$PRI/Intent/protosParsing.md
psyche|intent|psycheInteraction|98|whole:$PRI/Intent/psycheInteraction.md
psyche|intent|startupPrompt|99|whole:$PRI/Intent/startupPrompt.md
psyche|intent|testing|100|whole:$PRI/Intent/testing.md
mind|operation|psyche-logging|6|whole:$SPL/06-psyche-interraction/mind-operation-psyche-logging.md
mind|operation|psyche-acquisition|7|whole:$CUR/psyche-acquisition.md
mind|operation|psyche-distillation|8|whole:$SPL/08-psyche-distillation/mind-operation-psyche-distillation.md
mind|operation|psyche-grasp|9|whole:$CUR/psyche-grasp.md
mind|operation|skill-designing|10|whole:$SPL/10-skill-designing/mind-operation-skill-designing.md
mind|knowledge|skill-source|10|whole:$SPL/10-skill-designing/mind-knowledge-skill-source.md
mind|operation|main-flow|11|whole:$SPL/11-main-flow/mind-operation-main-flow.md
mind|knowledge|lojix|14|whole:$SPL/14-lojix/mind-knowledge-lojix.md
mind|knowledge|orchestrate|15|whole:$SPL/15-orchestrate/mind-knowledge-orchestrate.md
mind|knowledge|context-strata|16|whole:$CUR/context-strata.md
mind|operation|documentation-placement|17|whole:$CUR/documentation-placement.md
mind|operation|testing|18|whole:$CUR/testing.md
mind|operation|versioning|19|whole:$CUR/versioning.md
mind|operation|prompt-crafting|20|whole:$CUR/prompt-crafting.md
mind|operation|design|21|whole:$CUR/design.md
mind|operation|realization|22|whole:$CUR/realization.md
mind|operation|book|48|whole:$CUR/operation-book.md
mind|operation|flashbook|49|whole:$CUR/operation-flashbook.md
mind|operation|flashbook-illustration|50|whole:$CUR/operation-flashbook-illustration.md
mind|operation|relaying-the-living|51|whole:$CUR/operation-relaying-the-living.md
field|knowledge|psyche-records|2|whole:$SPL/02-psyche/field-knowledge-psyche-records.md
field|knowledge|claude-harness|23|whole:$CUR/claude-harness.md
field|knowledge|codex-harness|24|whole:$SPL/24-codex-harness/field-knowledge-codex-harness.md
field|knowledge|lojix-nexus|14|whole:$SPL/14-lojix/field-knowledge-lojix-nexus.md
field|knowledge|transcript-search|39|whole:$CUR/transcript-search.md
field|knowledge|codex|43|whole:$CUR/knowledge-codex.md
field|knowledge|ethos|44|whole:$CUR/knowledge-ethos.md
field|knowledge|flow|45,11|whole:$CUR/knowledge-flow.md whole:$SPL/11-main-flow/field-knowledge-flow.add.md
field|knowledge|nexus|46,15|whole:$CUR/knowledge-nexus.md whole:$SPL/15-orchestrate/field-knowledge-nexus.add.md
field|knowledge|layer-models|47,81|whole:$SPL/47-knowledge-layer-models/field-knowledge-layer-models.md whole:$SPL/81-modelRoles/field-knowledge-layer-models.add.md
field|knowledge|messaging|80|whole:$SPL/80-messaging/field-knowledge-messaging.md
field|operation|agent-harness-packaging|25|whole:$CUR/agent-harness-packaging.md
field|operation|nix-workflow|26|whole:$CUR/nix-workflow.md
field|operation|nix-input-upgrade|27|whole:$CUR/nix-input-upgrade.md
field|operation|operating-system|28|whole:$CUR/operating-system.md
field|operation|disk-hygiene|29|whole:$CUR/disk-hygiene.md
field|operation|secrets|30|whole:$CUR/secrets.md
field|operation|file-editing|31|whole:$SPL/31-file-editing/field-operation-file-editing.md
field|operation|edit-coordination|32|whole:$CUR/edit-coordination.md
field|operation|beads|33|whole:$CUR/beads.md
field|operation|flow-evidence|34|whole:$CUR/flow-evidence.md
field|operation|repository-lifecycle|35|whole:$CUR/repository-lifecycle.md
field|operation|feature-development|36|whole:$CUR/feature-development.md
field|operation|breaking-upgrades|37|whole:$CUR/breaking-upgrades.md
field|operation|stale-lock|38|whole:$CUR/stale-lock.md
field|operation|compensation-default-effort|52,24|whole:$CUR/compensation-default-effort.md whole:$SPL/24-codex-harness/field-operation-compensation-default-effort.add.md
field|operation|compensation-messenger-clj|53|whole:$CUR/compensation-messenger-clj.md
field|operation|compensation-nix|54|whole:$CUR/compensation-nix.md
field|operation|compensation-nix-rationale|55|whole:$CUR/compensation-nix-rationale.md
field|operation|compensation-primary-commit|56,31|whole:$CUR/compensation-primary-commit.md whole:$SPL/31-file-editing/field-operation-compensation-primary-commit.add.md
field|operation|compensation-subflow|57|whole:$CUR/compensation-subflow.md
field|operation|compensation-update|58|whole:$CUR/compensation-update.md
field|operation|trial-contact-discipline|59|whole:$CUR/trial-contact-discipline.md
field|operation|trial-generated-projection|60|whole:$CUR/trial-generated-projection.md
field|operation|trial-independent-review|61|whole:$CUR/trial-independent-review.md
field|operation|trial-low-power|62|whole:$CUR/trial-low-power.md
field|operation|trial-no-polling|63|whole:$CUR/trial-no-polling.md
field|operation|trial-presentation-book|64|whole:$CUR/trial-presentation-book.md
field|operation|trial-psyche-injection|65|whole:$CUR/trial-psyche-injection.md
field|operation|trial-questions-book|66|whole:$CUR/trial-questions-book.md
field|operation|trial-reaping|67|whole:$CUR/trial-reaping.md
field|operation|trial-recurring-failure|68|whole:$CUR/trial-recurring-failure.md
field|operation|trial-succession|69|whole:$CUR/trial-succession.md
field|operation|trial-unblocking-commands|70|whole:$CUR/trial-unblocking-commands.md
logs|legacy|archive-ethosMonolith|90|whole:$PRI/Vision/archive-ethosMonolith.md
"

# Sources sidecars beside their modules (item 9). The flowNexus sources follow
# their module's stem, flow.
SIDECARS=""
for f in "$PRI"/Vision/sources/*.md; do
  s=$(basename "$f" .md); [ "$s" = flowNexus ] && s=flow
  SIDECARS+="psyche|vision/sources|$s|-|whole:$f"$'\n'
done
for f in "$PRI"/Intent/sources/*.md; do
  SIDECARS+="psyche|intent/sources|$(basename "$f" .md)|-|whole:$f"$'\n'
done

restem() { # apply STEM_CASE; compensation-/trial- prefixes stay as prefixes
  local s=$1 pre=""
  case $s in compensation-*) pre=compensation-; s=${s#compensation-};; trial-*) pre=trial-; s=${s#trial-};; esac
  if [ "$STEM_CASE" = kebab ]; then s=$(sed -E 's/([a-z0-9])([A-Z])/\1-\L\2/g' <<<"$s")
  else s=$(sed -E 's/-([a-z0-9])/\U\1/g' <<<"$s"); fi
  printf '%s%s' "$pre" "$s"
}
fm()   { awk 'NR==1&&$0!="---"{exit} {print} NR>1&&$0=="---"{exit}' "$1"; }
body() { if [ "$(head -n1 "$1")" = "---" ]; then awk 'f==2{print;next} $0=="---"{f++}' "$1" | sed '/./,$!d'; else cat "$1"; fi; }
compose() {
  local first=1 p kind file
  for p in "$@"; do
    kind=${p%%:*}; file=${p#*:}
    [ $first = 1 ] || echo
    first=0
    case $kind in
      whole) sed -e :a -e '/^\n*$/{$d;N;ba' -e '}' "$file";;
      fm) fm "$file";;
      body) body "$file" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}';;
    esac
  done
}

fail=0
err() { echo "REFUSED: $*" >&2; fail=1; }

# Repositories clean.
for r in psyche mind field logs; do
  d=${REPO[$r]}
  [ -d "$d" ] || { err "$d missing"; continue; }
  [ -z "$(git -C "$d" status --porcelain --untracked-files=all)" ] || err "$d has changes"
done

# Split parts present, and their sources unchanged since the cut.
while IFS=$'\t' read -r part src sha _; do
  [ "$part" = part ] && continue
  [ -f "$SPL/$part" ] || err "split part missing: $SPL/$part"
  [ "$(sha256sum "$src" | cut -d' ' -f1)" = "$sha" ] || err "source changed since the cut: $src (part $part)"
done < "$SPL/index.tsv"

# Resolve the plan.
declare -A seen_path seen_deployed stem_types counts
declare -a PLAN
rows=""
while IFS='|' read -r repo type stem rws parts; do
  [ -n "$repo" ] || continue
  [ "$type" = CONDUCT ] && type=$CONDUCT_TYPE
  if [ "$repo" = logs ]; then nstem=$stem; else nstem=$(restem "$stem"); fi
  path=${REPO[$repo]}/$type/$nstem.md
  for p in $parts; do [ -f "${p#*:}" ] || err "source missing for $path: ${p#*:}"; done
  [ -e "$path" ] && err "target exists: $path"
  [ -n "${seen_path[$path]:-}" ] && err "two modules at $path"
  seen_path[$path]=1
  if [ "$repo" != logs ] && [[ $type != */sources ]]; then
    dep="$type-$nstem"; [ "$type" = spirit ] && dep=spirit
    [ -n "${seen_deployed[$dep]:-}" ] && err "stem $nstem occurs twice as $type: ${seen_deployed[$dep]} and $repo"
    seen_deployed[$dep]=$repo
    stem_types[$nstem]="${stem_types[$nstem]:-} $repo/$type"
  fi
  [ "$rws" != - ] && rows+=",$rws"
  counts["$repo/$type"]=$(( ${counts["$repo/$type"]:-0} + 1 ))
  PLAN+=("$path|$parts")
done <<<"$MANIFEST$SIDECARS"

# Every table row maps.
missing=""
for i in $(seq 1 100); do grep -qE "(^|,)$i(,|$)" <<<"${rows#,}" || missing+=" $i"; done
[ -z "$missing" ] || err "rows not mapped:$missing"

echo "parameters: STEM_CASE=$STEM_CASE CONDUCT_TYPE=$CONDUCT_TYPE KEEP_PREFIX_PARAGRAPH=$KEEP_PREFIX_PARAGRAPH"
for e in "${PLAN[@]}"; do
  path=${e%%|*}; parts=${e#*|}
  echo "WRITE $path <- ${parts//$PRI\//}" | sed "s#$CUR/#Curriculum:#g; s#$ROOT/##"
done
echo "counts:"
for k in $(printf '%s\n' "${!counts[@]}" | sort); do printf '  %-24s %s\n' "$k" "${counts[$k]}"; done
echo "rows mapped: $(tr ',' '\n' <<<"${rows#,}" | sort -un | wc -l) of 100"
shared=""
for s in "${!stem_types[@]}"; do w=(${stem_types[$s]}); [ ${#w[@]} -gt 1 ] && shared+=" $s(${stem_types[$s]# })"; done
echo "stems shared across types (distinct deployed names):${shared:- none}"

[ "$fail" = 0 ] || { echo "checks failed; nothing written" >&2; exit 1; }
echo "checks passed"
[ "$DRY" = 1 ] && { echo "dry run: nothing written"; exit 0; }

for e in "${PLAN[@]}"; do
  path=${e%%|*}; read -r -a parts <<<"${e#*|}"
  mkdir -p "$(dirname "$path")"
  compose "${parts[@]}" > "$path"
done
echo "written ${#PLAN[@]} files; sources untouched; nothing committed"
