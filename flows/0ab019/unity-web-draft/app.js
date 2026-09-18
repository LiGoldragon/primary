const RECEIPT_STATES = new Set(["accepted", "held", "rejected"]);
const VISIBLE_SOURCE_KINDS = new Set(["living-origin-known", "flow-final", "unknown"]);

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function requireString(value, field) {
  if (typeof value !== "string" || value.length === 0) {
    throw new Error(`Adapter response is missing ${field}.`);
  }
  return value;
}

function normalizeRoster(value) {
  if (!value || !Array.isArray(value.flows)) throw new Error("Roster response is malformed.");
  return {
    observed_at: requireString(value.observed_at, "roster observed_at"),
    source_status: requireString(value.source_status, "roster source_status"),
    flows: value.flows.map((flow) => ({
      flow_id: requireString(flow.flow_id, "flow_id"),
      name: requireString(flow.name, "flow name"),
      seat: requireString(flow.seat, "flow seat"),
      state: requireString(flow.state, "flow state"),
      last_activity_at: typeof flow.last_activity_at === "string" ? flow.last_activity_at : null,
      last_activity_source:
        typeof flow.last_activity_source === "string" ? flow.last_activity_source : null,
    })),
  };
}

function normalizeConversation(value, requestedFlowId) {
  if (!value || !Array.isArray(value.entries)) throw new Error("Conversation response is malformed.");
  const flowId = requireString(value.flow_id, "conversation flow_id");
  if (flowId !== requestedFlowId) throw new Error("Conversation response names a different flow.");

  const entries = value.entries
    .map((entry) => ({
      entry_id: requireString(entry.entry_id, "entry_id"),
      sequence: Number(entry.sequence),
      occurred_at: requireString(entry.occurred_at, "entry occurred_at"),
      text: requireString(entry.text, "entry text"),
      source_kind: requireString(entry.source_kind, "entry source_kind"),
      attributed_actor:
        typeof entry.attributed_actor === "string" ? entry.attributed_actor : null,
      provenance_status: requireString(entry.provenance_status, "entry provenance_status"),
    }))
    .filter((entry) => Number.isFinite(entry.sequence) && VISIBLE_SOURCE_KINDS.has(entry.source_kind))
    .sort((left, right) => left.sequence - right.sequence || left.occurred_at.localeCompare(right.occurred_at));

  return {
    flow_id: flowId,
    observed_at: requireString(value.observed_at, "conversation observed_at"),
    source_status: requireString(value.source_status, "conversation source_status"),
    entries,
  };
}

function normalizeReceipt(value, requestId) {
  if (!value || value.request_id !== requestId) throw new Error("Send receipt does not match the request.");
  if (!RECEIPT_STATES.has(value.disposition)) throw new Error("Send receipt has an unknown disposition.");
  return {
    request_id: requestId,
    disposition: value.disposition,
    reason: typeof value.reason === "string" ? value.reason : null,
    relay_id: typeof value.relay_id === "string" ? value.relay_id : null,
    receipt_grade: typeof value.receipt_grade === "string" ? value.receipt_grade : null,
  };
}

function formatTime(value) {
  const instant = new Date(value);
  if (Number.isNaN(instant.valueOf())) return value;
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(instant);
}

function sourceLabel(entry) {
  if (entry.source_kind === "living-origin-known") return "Living";
  if (entry.source_kind === "flow-final") return entry.attributed_actor || "Flow";
  return "Origin unknown";
}

function requestId() {
  if (globalThis.crypto?.randomUUID) return globalThis.crypto.randomUUID();
  return `unity-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export function createHttpAdapter({ baseUrl = "", fetchImpl = globalThis.fetch } = {}) {
  if (typeof fetchImpl !== "function") throw new Error("Fetch is unavailable in this browser.");
  const request = async (path, options = {}) => {
    const response = await fetchImpl(`${baseUrl}${path}`, {
      headers: { Accept: "application/json", ...(options.headers || {}) },
      ...options,
    });
    if (!response.ok) throw new Error(`Mentci adapter returned HTTP ${response.status}.`);
    return response.json();
  };
  return {
    mode: "live",
    getRoster: () => request("/mentci/v1/roster"),
    getConversation: (flowId) =>
      request(`/mentci/v1/conversation?flow_id=${encodeURIComponent(flowId)}`),
    send: (payload) =>
      request("/mentci/v1/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }),
  };
}

const SYNTHETIC_ROSTER = {
  observed_at: "2026-09-18T22:14:00Z",
  source_status: "synthetic-fixture",
  flows: [
    {
      flow_id: "fable01",
      name: "Fable",
      seat: "design",
      state: "idle",
      last_activity_at: "2026-09-18T22:12:00Z",
      last_activity_source: "synthetic-fixture",
    },
    {
      flow_id: "field02",
      name: "Field",
      seat: "build",
      state: "working",
      last_activity_at: "2026-09-18T22:13:00Z",
      last_activity_source: "synthetic-fixture",
    },
  ],
};

const SYNTHETIC_CONVERSATIONS = {
  fable01: {
    flow_id: "fable01",
    observed_at: "2026-09-18T22:14:00Z",
    source_status: "synthetic-fixture",
    entries: [
      {
        entry_id: "synthetic:fable01:1",
        sequence: 10,
        occurred_at: "2026-09-18T22:08:00Z",
        text: "Review the synthetic conversation surface on a narrow screen.",
        source_kind: "living-origin-known",
        attributed_actor: "Living",
        provenance_status: "synthetic-verified-origin",
      },
      {
        entry_id: "synthetic:fable01:2",
        sequence: 20,
        occurred_at: "2026-09-18T22:09:00Z",
        text: "The draft keeps adapter uncertainty visible and orders entries oldest first.",
        source_kind: "flow-final",
        attributed_actor: "Fable",
        provenance_status: "synthetic-final-response",
      },
      {
        entry_id: "synthetic:fable01:3",
        sequence: 30,
        occurred_at: "2026-09-18T22:10:00Z",
        text: "This input has no independently known living origin.",
        source_kind: "unknown",
        provenance_status: "unverified",
      },
    ],
  },
  field02: {
    flow_id: "field02",
    observed_at: "2026-09-18T22:14:00Z",
    source_status: "synthetic-fixture",
    entries: [
      {
        entry_id: "synthetic:field02:1",
        sequence: 10,
        occurred_at: "2026-09-18T22:11:00Z",
        text: "The static review fixture has no live transport.",
        source_kind: "flow-final",
        attributed_actor: "Field",
        provenance_status: "synthetic-final-response",
      },
    ],
  },
};

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

export function createSyntheticAdapter({ disposition = "accepted", delay = 0 } = {}) {
  const requests = [];
  return {
    mode: "synthetic",
    requests,
    getRoster: async () => clone(SYNTHETIC_ROSTER),
    getConversation: async (flowId) => {
      const conversation = SYNTHETIC_CONVERSATIONS[flowId];
      if (!conversation) throw new Error("Synthetic fixture does not contain that flow.");
      return clone(conversation);
    },
    send: async (payload) => {
      requests.push(clone(payload));
      if (delay > 0) await new Promise((resolve) => globalThis.setTimeout(resolve, delay));
      return {
        request_id: payload.request_id,
        disposition,
        reason: disposition === "held" ? "Synthetic review hold." : undefined,
        relay_id: disposition === "accepted" ? "synthetic-relay" : undefined,
        receipt_grade: "synthetic-only",
      };
    },
  };
}

export function createUnityClient({ root, adapter }) {
  if (!root) throw new Error("Unity Web requires a root element.");
  const state = {
    roster: null,
    conversation: null,
    selectedFlowId: null,
    drafts: new Map(),
    receipt: null,
    observing: false,
    sending: false,
    lastObservedAt: null,
    error: null,
  };

  const shell = element("div", "app-shell");
  const header = element("header", "topbar");
  const brand = element("div", "brand");
  brand.append(element("span", "brand-mark", "U"), element("div", "brand-copy"));
  brand.lastChild.append(element("strong", "brand-title", "Unity"), element("span", "brand-subtitle", "Mentci client draft"));
  const mode = element("span", `mode-badge ${adapter.mode === "synthetic" ? "is-demo" : "is-live"}`, adapter.mode === "synthetic" ? "Synthetic demo" : "Live adapter");
  header.append(brand, mode);

  const demoNotice = element("aside", "demo-notice");
  demoNotice.setAttribute("role", "note");
  demoNotice.textContent = "Synthetic demo — local fixtures only. Nothing on this page is live or sent to Mentci.";

  const observationBar = element("section", "observation-bar");
  observationBar.setAttribute("aria-label", "Observation status");
  const observationCopy = element("div", "observation-copy");
  const observationLabel = element("span", "eyebrow", "Last observed");
  const observationStatus = element("strong", "observation-status", "Not observed yet");
  observationStatus.setAttribute("aria-live", "polite");
  observationCopy.append(observationLabel, observationStatus);
  const refreshButton = element("button", "button button-secondary", "Refresh");
  refreshButton.type = "button";
  refreshButton.setAttribute("aria-label", "Refresh roster and selected conversation");
  observationBar.append(observationCopy, refreshButton);

  const workspace = element("main", "workspace");
  const rosterPanel = element("section", "panel roster-panel");
  rosterPanel.setAttribute("aria-labelledby", "roster-title");
  const rosterHeader = element("div", "panel-heading");
  const rosterHeadingCopy = element("div");
  const rosterTitle = element("h1", "panel-title", "Flows");
  rosterTitle.id = "roster-title";
  const rosterSummary = element("p", "panel-summary", "Waiting for a roster observation.");
  rosterHeadingCopy.append(rosterTitle, rosterSummary);
  rosterHeader.append(rosterHeadingCopy);
  const rosterList = element("div", "roster-list");
  rosterList.setAttribute("role", "list");
  rosterPanel.append(rosterHeader, rosterList);

  const conversationPanel = element("section", "panel conversation-panel");
  conversationPanel.setAttribute("aria-labelledby", "conversation-title");
  const conversationHeader = element("div", "conversation-heading");
  const conversationIdentity = element("div");
  const conversationEyebrow = element("span", "eyebrow", "Conversation");
  const conversationTitle = element("h2", "conversation-title", "Select a flow");
  conversationTitle.id = "conversation-title";
  const conversationMeta = element("p", "conversation-meta", "No conversation selected.");
  conversationIdentity.append(conversationEyebrow, conversationTitle, conversationMeta);
  conversationHeader.append(conversationIdentity);
  const entries = element("ol", "conversation-list");
  entries.setAttribute("aria-live", "polite");

  const composer = element("form", "composer");
  const composerLabel = element("label", "composer-label", "Message selected flow");
  composerLabel.htmlFor = "unity-compose";
  const textarea = element("textarea", "composer-input");
  textarea.id = "unity-compose";
  textarea.name = "message";
  textarea.rows = 3;
  textarea.placeholder = "Write a message…";
  const composerFooter = element("div", "composer-footer");
  const composerHint = element("span", "composer-hint", "Ctrl/⌘ + Enter to send");
  const sendButton = element("button", "button button-primary", "Send");
  sendButton.type = "submit";
  composerFooter.append(composerHint, sendButton);
  const receipt = element("div", "receipt");
  receipt.setAttribute("aria-live", "polite");
  composer.append(composerLabel, textarea, composerFooter, receipt);
  conversationPanel.append(conversationHeader, entries, composer);
  workspace.append(rosterPanel, conversationPanel);
  shell.append(header);
  if (adapter.mode === "synthetic") shell.append(demoNotice);
  shell.append(observationBar, workspace);
  root.replaceChildren(shell);

  function selectedFlow() {
    return state.roster?.flows.find((flow) => flow.flow_id === state.selectedFlowId) || null;
  }

  function renderRoster() {
    rosterList.replaceChildren();
    const flows = state.roster?.flows || [];
    rosterSummary.textContent = flows.length === 1 ? "1 observed flow" : `${flows.length} observed flows`;
    if (flows.length === 0) {
      rosterList.append(element("p", "empty-state", "No flows were present in the latest observation."));
      return;
    }
    for (const flow of flows) {
      const item = element("button", "flow-card");
      item.type = "button";
      item.dataset.flowId = flow.flow_id;
      item.setAttribute("role", "listitem");
      item.setAttribute("aria-label", `Select ${flow.name}, ${flow.seat}, ${flow.state}`);
      item.setAttribute("aria-pressed", String(flow.flow_id === state.selectedFlowId));
      if (flow.flow_id === state.selectedFlowId) item.classList.add("is-selected");
      const top = element("span", "flow-card-top");
      top.append(element("strong", "flow-name", flow.name), element("span", `state-dot state-${flow.state}`, flow.state));
      const identity = element("span", "flow-identity", `${flow.seat} · ${flow.flow_id}`);
      const activity = element("span", "flow-activity", flow.last_activity_at ? `Active ${formatTime(flow.last_activity_at)}` : "Activity unavailable");
      item.append(top, identity, activity);
      item.addEventListener("click", () => selectFlow(flow.flow_id));
      rosterList.append(item);
    }
  }

  function renderConversation() {
    const flow = selectedFlow();
    conversationTitle.textContent = flow?.name || "Select a flow";
    conversationMeta.textContent = flow
      ? `${flow.seat} · ${flow.flow_id} · ${state.conversation?.source_status || "not observed"}`
      : "No conversation selected.";
    entries.replaceChildren();
    const conversationEntries = state.conversation?.entries || [];
    if (!flow) entries.append(element("li", "empty-state", "Choose a flow to read its conversation."));
    else if (conversationEntries.length === 0) entries.append(element("li", "empty-state", "No eligible entries were present in the latest observation."));
    for (const entry of conversationEntries) {
      const item = element("li", `message message-${entry.source_kind}`);
      item.dataset.entryId = entry.entry_id;
      item.dataset.sequence = String(entry.sequence);
      const messageHeader = element("div", "message-header");
      messageHeader.append(element("strong", "message-source", sourceLabel(entry)), element("time", "message-time", formatTime(entry.occurred_at)));
      const body = element("p", "message-body", entry.text);
      const provenance = element("span", "provenance", entry.provenance_status);
      item.append(messageHeader, body, provenance);
      entries.append(item);
    }
    textarea.disabled = !flow || state.sending;
    sendButton.disabled = !flow || state.sending;
    textarea.value = flow ? state.drafts.get(flow.flow_id) || "" : "";
  }

  function renderReceipt() {
    receipt.replaceChildren();
    if (!state.receipt) return;
    const status = state.receipt.disposition;
    receipt.className = `receipt receipt-${status}`;
    const title = status === "pending" ? "Sending" : status[0].toUpperCase() + status.slice(1);
    receipt.append(element("strong", "receipt-title", title));
    if (state.receipt.reason) receipt.append(element("span", "receipt-detail", state.receipt.reason));
    if (state.receipt.receipt_grade) receipt.append(element("span", "receipt-grade", state.receipt.receipt_grade));
  }

  function renderObservation() {
    refreshButton.disabled = state.observing;
    if (state.observing) observationStatus.textContent = "Observing…";
    else if (state.error) observationStatus.textContent = `Unavailable — ${state.error}`;
    else if (state.lastObservedAt) observationStatus.textContent = `${formatTime(state.lastObservedAt)} · ${state.roster?.source_status || "unknown source"}`;
    else observationStatus.textContent = "Not observed yet";
  }

  async function loadConversation(flowId) {
    state.conversation = null;
    renderConversation();
    const result = await adapter.getConversation(flowId);
    if (state.selectedFlowId === flowId) {
      state.conversation = normalizeConversation(result, flowId);
      renderConversation();
    }
  }

  async function selectFlow(flowId) {
    if (state.selectedFlowId === flowId && state.conversation) return;
    state.selectedFlowId = flowId;
    state.receipt = null;
    renderRoster();
    renderReceipt();
    try {
      await loadConversation(flowId);
    } catch (error) {
      state.error = error instanceof Error ? error.message : "Conversation observation failed.";
      renderObservation();
      renderConversation();
    }
  }

  async function refresh() {
    if (state.observing) return;
    state.observing = true;
    state.error = null;
    renderObservation();
    try {
      state.roster = normalizeRoster(await adapter.getRoster());
      const stillPresent = state.roster.flows.some((flow) => flow.flow_id === state.selectedFlowId);
      if (!stillPresent) state.selectedFlowId = state.roster.flows[0]?.flow_id || null;
      renderRoster();
      if (state.selectedFlowId) await loadConversation(state.selectedFlowId);
      else {
        state.conversation = null;
        renderConversation();
      }
      state.lastObservedAt = state.roster.observed_at;
    } catch (error) {
      state.error = error instanceof Error ? error.message : "Observation failed.";
    } finally {
      state.observing = false;
      renderObservation();
    }
  }

  textarea.addEventListener("input", () => {
    if (state.selectedFlowId) state.drafts.set(state.selectedFlowId, textarea.value);
  });
  textarea.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
      event.preventDefault();
      composer.requestSubmit();
    }
  });
  refreshButton.addEventListener("click", refresh);
  composer.addEventListener("submit", async (event) => {
    event.preventDefault();
    const flowId = state.selectedFlowId;
    const text = textarea.value.trim();
    if (!flowId || !text || state.sending) return;
    const id = requestId();
    const payload = { request_id: id, flow_id: flowId, text };
    state.sending = true;
    state.receipt = { request_id: id, disposition: "pending" };
    renderReceipt();
    renderConversation();
    try {
      state.receipt = normalizeReceipt(await adapter.send(payload), id);
      if (state.receipt.disposition === "accepted") {
        state.drafts.set(flowId, "");
        if (state.selectedFlowId === flowId) textarea.value = "";
      }
    } catch (error) {
      state.receipt = {
        request_id: id,
        disposition: "rejected",
        reason: error instanceof Error ? error.message : "Send failed.",
        receipt_grade: "client-error",
      };
    } finally {
      state.sending = false;
      renderReceipt();
      renderConversation();
    }
  });

  renderRoster();
  renderConversation();
  renderReceipt();
  renderObservation();
  const ready = refresh();
  return { ready, refresh, state, elements: { rosterList, entries, textarea, sendButton, receipt, observationStatus } };
}

const autoRoot = document.querySelector("#app");
if (autoRoot) {
  const parameters = new URLSearchParams(globalThis.location?.search || "");
  const adapter = parameters.get("demo") === "synthetic"
    ? createSyntheticAdapter()
    : createHttpAdapter({ baseUrl: parameters.get("endpoint") || "" });
  createUnityClient({ root: autoRoot, adapter });
}
