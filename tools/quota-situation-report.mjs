const required = (input, name) => {
  if (input[name] === undefined) {
    throw new Error(`missing read-only fixture input: ${name}`);
  }
  return input[name];
};

const rounded = (value) => Math.round(value * 10) / 10;

export const renderSituationReport = (input) => {
  const rateLimitsRead = required(input, "account/rateLimits/read");
  required(input, "account/usage/read");

  const primary = rateLimitsRead.rateLimits.primary;
  const spark = rateLimitsRead.rateLimits.codex_bengalfox;
  const credits = rateLimitsRead.rateLimitResetCredits;

  const observedAt = new Date(input.observedAt);
  const resetsAt = new Date(primary.resetsAt);
  const windowMs = primary.windowDurationMins * 60_000;
  const elapsedDays = (observedAt - (resetsAt - windowMs)) / 86_400_000;
  const remainingDays = (resetsAt - observedAt) / 86_400_000;
  const usedPerDay = primary.usedPercent / elapsedDays;
  const remainingPercent = 100 - primary.usedPercent;
  const remainingPerDay = remainingPercent / remainingDays;
  const pace = usedPerDay / (100 / 7);
  const weekday = resetsAt.toLocaleDateString("en-US", { timeZone: "UTC", weekday: "short" });
  const resetDay = resetsAt.toLocaleDateString("en-US", { timeZone: "UTC", day: "2-digit" });
  const timestamp = input.observedAt.replace(/:38Z$/, "Z").replace("T", " ");
  if (remainingDays <= 0) throw new Error("invalid rateLimits.primary.resetsAt: reset must be in the future");
  const elapsedPercent = Math.round((elapsedDays / (primary.windowDurationMins / 1_440)) * 100);
  const sparkUsed = spark.fiveHourUsedPercent === 0 && spark.weeklyUsedPercent === 0 ? "0%" : "nonzero";

  return `QUOTA SITREP  ${timestamp}  wk ${elapsedPercent}% gone\n\nCODEX PRO     ${remainingPercent}% left  BELOW ${pace.toFixed(2)}x\n  may spend ${rounded(remainingPerDay).toFixed(1)} %/day to reset ${weekday} ${resetDay}\n  ran      ${rounded(usedPerDay).toFixed(1)} %/day so far\n  +${credits.availableCount} full-reset credits in hand\n  [########..|............]\n\nSpark footnote: ${sparkUsed} used in both recorded windows.\nClaude: unread (no fixture supplied).\n`;
};
