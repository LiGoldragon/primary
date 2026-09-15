const asObject = (value, label) => {
  if (value === null || typeof value !== "object" || Array.isArray(value)) throw new Error(`invalid ${label}: expected an object`);
  return value;
};

const validPercent = (value, label) => {
  if (typeof value !== "number" || !Number.isFinite(value) || value < 0 || value > 100) throw new Error(`invalid ${label}: expected a percentage from 0 through 100`);
  return value;
};

const normalizedWindow = (value, label, observedAt) => {
  const window = asObject(value, label);
  validPercent(window.usedPercent, `${label}.usedPercent`);
  if (typeof window.windowDurationMins !== "number" || !Number.isFinite(window.windowDurationMins) || window.windowDurationMins <= 0) throw new Error(`invalid ${label}.windowDurationMins: expected a positive number`);
  if (typeof window.resetsAt !== "number" || !Number.isFinite(window.resetsAt) || window.resetsAt <= 0) throw new Error(`invalid ${label}.resetsAt: expected epoch seconds`);
  const resetsAt = new Date(window.resetsAt * 1_000);
  if (resetsAt <= observedAt) throw new Error(`invalid ${label}.resetsAt: reset must be in the future`);
  return { usedPercent: window.usedPercent, windowDurationMins: window.windowDurationMins, resetsAt: resetsAt.toISOString() };
};

export const normalizeRateLimitReadings = ({ rateLimits, observedAt }) => {
  const observed = new Date(observedAt);
  if (Number.isNaN(observed.valueOf())) throw new Error("invalid observedAt: expected an ISO date");
  const result = asObject(rateLimits, "account/rateLimits/read result");
  const primary = normalizedWindow(asObject(result.rateLimits, "rateLimits").primary, "rateLimits.primary", observed);
  const spark = asObject(asObject(result.rateLimitsByLimitId, "rateLimitsByLimitId").codex_bengalfox, "rateLimitsByLimitId.codex_bengalfox");
  const rawCredits = result.rateLimitResetCredits;
  let credits = null;
  if (rawCredits !== undefined && rawCredits !== null) {
    credits = asObject(rawCredits, "rateLimitResetCredits");
    if (!Number.isInteger(credits.availableCount) || credits.availableCount < 0) throw new Error("invalid rateLimitResetCredits.availableCount: expected a non-negative integer");
    credits = { availableCount: credits.availableCount };
  }
  return { rateLimits: { primary }, rateLimitsByLimitId: { codex_bengalfox: { primary: normalizedWindow(spark.primary, "rateLimitsByLimitId.codex_bengalfox.primary", observed), secondary: normalizedWindow(spark.secondary, "rateLimitsByLimitId.codex_bengalfox.secondary", observed) } }, rateLimitResetCredits: credits };
};
