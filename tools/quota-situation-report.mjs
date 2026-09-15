const required = (input, name) => {
  if (input[name] === undefined) {
    throw new Error(`missing read-only fixture input: ${name}`);
  }
  return input[name];
};

const rounded = (value) => Math.round(value * 10) / 10;

export const renderSituationReport = (input) => {
  const rateLimitsRead = required(input, "account/rateLimits/read");
  const { primary } = rateLimitsRead.rateLimits;
  const { rateLimitsByLimitId, rateLimitResetCredits: credits } = rateLimitsRead;
  const spark = rateLimitsByLimitId.codex_bengalfox;

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
  const sparkUsed = spark.primary.usedPercent === 0 && spark.secondary.usedPercent === 0 ? "0%" : "nonzero";

  const usage = input["account/usage/read"] === null || input["account/usage/read"] === undefined ? "Unknown" : "available (not rendered)";
  const creditText = `+${credits === null ? "Unknown" : credits.availableCount} full-reset credits`;
  return `QUOTA SITREP  ${timestamp}  wk ${elapsedPercent}% gone\nBELOW CODEX PRO ${remainingPercent}% left  ${pace.toFixed(2)}x  ${rounded(remainingPerDay).toFixed(1)} %/day  reset ${weekday} ${resetDay}  ${creditText}  [########..|............]\nSpark footnote: ${sparkUsed} used in both recorded windows; usage ${usage}.\nNO READING CLAUDE MAX --% left  --  -- %/day  reset --  +Unknown full-reset credits  [??????????????????????]`;
};
