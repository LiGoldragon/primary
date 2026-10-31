#!/usr/bin/env bb
;; Pulse: an hourly scan of what is going on.
;;
;; Usage: pulse.clj PRIMARY_ROOT REPORT_DIRECTORY RECIPIENT
;;   PRIMARY_ROOT      the live workspace: flows/, SKILL_VARIABLES.md, tools/
;;   REPORT_DIRECTORY  where the report is written, e.g. flows/5330c1/pulse
;;   RECIPIENT         the metaflow address the report goes to,
;;                     e.g. "Psyche flow Secondary"
;;
;; Steps: gather (Herdr snapshot, Flow metaflows, flow logs, quotas), hand the
;; gathered text to a headless Sonnet run (low effort, Read and read-only
;; Bash), write its report, deliver a one-line pointer, and append the
;; delivery witness to the report.
;;
;; This process reaches Flow only through the flow CLI. It never opens
;; Flow's store.
(require '[babashka.process :as p]
         '[babashka.fs :as fs]
         '[babashka.http-client :as http]
         '[cheshire.core :as json]
         '[clojure.string :as str])

;; ---- Sanity ceilings and flag thresholds (change here) ----
(def awake-ceiling 12)        ; awake metaflows
(def working-ceiling 4)       ; working Herdr panes
(def sends-per-hour-flag 10)  ; a metaflow sending more than this in the window is listed
(def acknowledgement-start    ; a queued Notice that starts so and is short reads as only acknowledging
  #"(?i)^\s*(ack|acknowledg|received|noted|understood|thanks|thank you|confirmed|ok\b|okay)")
(def acknowledgement-longest 200)

(def arguments (vec *command-line-args*))
(when (not= 3 (count arguments))
  (binding [*out* *err*] (println "usage: pulse.clj PRIMARY_ROOT REPORT_DIRECTORY RECIPIENT"))
  (System/exit 2))
(def primary-root (str (fs/absolutize (arguments 0))))
(def report-directory (fs/absolutize (arguments 1)))
(def recipient (arguments 2))
(def now (java.time.Instant/now))
(def stamp (.format (.withZone (java.time.format.DateTimeFormatter/ofPattern "yyyy-MM-dd'T'HHmm'Z'") java.time.ZoneOffset/UTC) now))
(def report-path (str (fs/path report-directory (str stamp ".md"))))

(defn run [& command]
  (let [r (apply p/shell {:out :string :err :string :continue true :in ""} command)]
    {:exit (:exit r) :out (:out r) :err (:err r)}))

(defn clip [s n] (if (> (count s) n) (str (subs s 0 n) "...") s))

(defn skill-variable [name]
  (some (fn [line] (when (str/starts-with? line (str name ": ")) (subs line (+ 2 (count name)))))
        (str/split-lines (slurp (str (fs/path primary-root "SKILL_VARIABLES.md"))))))

(def open-guillemet (char 171))
(def close-guillemet (char 187))

;; ---- protos reader, enough for flow 'Metaflows' ----

(defn read-protos [^String text]
  (let [n (count text) pos (atom 0)]
    (letfn [(peek-char [] (when (< @pos n) (.charAt text @pos)))
            (skip-space []
              (loop []
                (let [c (peek-char)]
                  (cond (nil? c) nil
                        (Character/isWhitespace c) (do (swap! pos inc) (recur))
                        (= c \;) (do (while (and (peek-char) (not= (peek-char) \newline)) (swap! pos inc)) (recur))))))
            (read-guillemets []
              (swap! pos inc)
              (let [sb (StringBuilder.)]
                (loop []
                  (let [c (peek-char)]
                    (cond (nil? c) (str sb)
                          (and (= c \\) (< (inc @pos) n)) (do (.append sb (.charAt text (inc @pos))) (swap! pos + 2) (recur))
                          (= c close-guillemet) (do (swap! pos inc) (str sb))
                          :else (do (.append sb c) (swap! pos inc) (recur)))))))
            (read-parens []
              (let [start @pos]
                (loop [depth 0]
                  (let [c (peek-char)]
                    (swap! pos inc)
                    (cond (nil? c) (subs text start n)
                          (= c \() (recur (inc depth))
                          (and (= c \)) (= depth 1)) (subs text start @pos)
                          (= c \)) (recur (dec depth))
                          :else (recur depth))))))
            (read-enclosed [close kind]
              (swap! pos inc)
              (loop [children []]
                (skip-space)
                (let [c (peek-char)]
                  (cond (nil? c) {:kind kind :children children}
                        (= c close) (do (swap! pos inc) {:kind kind :children children})
                        :else (recur (conj children (read-one)))))))
            (read-one []
              (skip-space)
              (let [c (peek-char)]
                (case c
                  \{ (read-enclosed \} :struct)
                  \[ (read-enclosed \] :vector)
                  \< (read-enclosed \> :angled)
                  \u00ab {:kind :string :text (read-guillemets)}
                  \( {:kind :meaning :text (read-parens)}
                  (let [start @pos]
                    (while (let [d (peek-char)]
                             (and d (not (Character/isWhitespace d))
                                  (not (#{\{ \} \[ \] \< \> open-guillemet \( \)} d))))
                      (swap! pos inc))
                    (let [run (subs text start @pos)]
                      (if (and (str/ends-with? run ".") (#{\{ \[ \< open-guillemet \(} (peek-char)))
                        {:kind :headed :head (subs run 0 (dec (count run))) :body (read-one)}
                        {:kind :bare :text run}))))))]
      (read-one))))

(defn words [node]
  (case (:kind node)
    :bare (:text node)
    :string (:text node)
    :meaning (:text node)
    :headed (str (:head node) "." (words (:body node)))
    (str/join " " (map words (:children node)))))

(defn delivery-summary [d]
  (let [[id sender mode message] (:children d)
        head (when (= :headed (:kind message)) (:head message))]
    {:id (some-> id :text (str/replace #"logical-delivery-0*" ""))
     :sender (if (= :headed (:kind sender)) (words (:body sender)) (words sender))
     :mode (words mode)
     :kind (or head (words message))
     :text (if (= :headed (:kind message)) (words (:body message)) "")}))

(defn metaflow-summary [m]
  (let [[address state seats deliveries] (:children m)
        ds (map delivery-summary (:children deliveries))
        tally (fn [k] (->> ds (map k) frequencies (sort-by (comp - val)) (map (fn [[x c]] (str x " " c))) (str/join ", ")))]
    (str "- " (words address) " | " (words state) " | ids " (words seats)
         " | queued " (count ds)
         (when (seq ds)
           (str "\n  by sender: " (tally :sender)
                "\n  by kind: " (tally :kind) "; by mode: " (tally :mode)
                (str/join (for [d (concat (take 2 ds) (when (> (count ds) 2) (take-last 2 ds)))]
                            (str "\n  #" (:id d) " " (:kind d) " from " (:sender d) ": " (clip (:text d) 220)))))))))

;; ---- gathering ----

(defn snapshot []
  (let [r (run "herdr" "api" "snapshot")]
    (if (zero? (:exit r))
      {:snapshot (get-in (json/parse-string (:out r) true) [:result :snapshot])}
      {:error (str "UNREADABLE: herdr api snapshot exit " (:exit r) ": " (clip (:err r) 300))})))

(defn gather-panes [{s :snapshot error :error}]
  (if s
    (let [labels (into {} (map (juxt :workspace_id :label) (:workspaces s)))]
      (str/join "\n" (for [pane (:panes s)]
                       (str "- " (:pane_id pane) " | " (:agent pane) " | " (:agent_status pane)
                            " | workspace " (labels (:workspace_id pane))
                            " | terminal title " (:terminal_title_stripped pane)))))
    error))

(defn gather-metaflows []
  (let [r (run "flow" "Metaflows")]
    (if (zero? (:exit r))
      (let [tree (read-protos (:out r))
            listed (if (= :headed (:kind tree)) (:body tree) tree)]
        {:rows (for [m (:children listed)
                     :let [[address state _ deliveries] (:children m)]]
                 {:address (words address) :state (words state)
                  :id (second (re-find #"^Awake\.([0-9a-f]{6})$" (words state)))
                  :deliveries (map delivery-summary (:children deliveries))})
         :text (str (:head tree) ", " (count (:out r)) " bytes\n"
                    (str/join "\n" (map metaflow-summary (:children listed))))
         :flow-ids (keep (fn [m] (second (re-find #"^Awake\.([0-9a-f]{6})$" (words (second (:children m))))))
                         (:children listed))})
      {:text (str "UNREADABLE: flow 'Metaflows' exit " (:exit r) ": " (clip (str (:out r) (:err r)) 300))
       :rows nil :flow-ids []})))

(defn previous-report []
  (->> (fs/glob report-directory "*.md")
       (sort-by #(fs/file-time->millis (fs/last-modified-time %)))
       last))

(defn gather-logs [flow-ids since-millis]
  (let [flows (fs/path primary-root "flows")
        recent (->> (fs/glob flows "*/log.md")
                    (filter #(> (fs/file-time->millis (fs/last-modified-time %)) since-millis))
                    (map #(str (fs/file-name (fs/parent %)))))
        ids (distinct (concat flow-ids recent))]
    (str/join "\n"
              (for [id ids
                    :let [log (fs/path flows id "log.md")]]
                (if (fs/exists? log)
                  (str "### " id " (log modified "
                       (fs/last-modified-time log) ")\n"
                       (str/join "\n" (map #(clip % 500) (take-last 12 (str/split-lines (slurp (str log)))))))
                  (str "### " id ": no log.md"))))))

(defn claude-quota []
  (try
    (let [token (get-in (json/parse-string (slurp (str (fs/path (fs/home) ".claude" ".credentials.json"))) true)
                        [:claudeAiOauth :accessToken])
          r (http/get "https://api.anthropic.com/api/oauth/usage"
                      {:headers {"Authorization" (str "Bearer " token) "anthropic-beta" "oauth-2025-04-20"}
                       :throw false :timeout 15000})]
      (if (= 200 (:status r))
        (let [u (json/parse-string (:body r) true)]
          (str "source: GET api.anthropic.com/api/oauth/usage with the Claude Code login (read "
               (str now) ")\n"
               "five hour: " (get-in u [:five_hour :utilization]) "% used, resets " (get-in u [:five_hour :resets_at]) "\n"
               "seven day: " (get-in u [:seven_day :utilization]) "% used, resets " (get-in u [:seven_day :resets_at]) "\n"
               (str/join "\n" (for [l (:limits u)]
                                (str "limit " (:kind l) (when-let [m (get-in l [:scope :model :display_name])] (str " (" m ")"))
                                     ": " (:percent l) "% " (:severity l) ", resets " (:resets_at l))))))
        (str "UNREADABLE: usage endpoint answered HTTP " (:status r) ": " (clip (str (:body r)) 200))))
    (catch Exception e (str "UNREADABLE: " (.getMessage e)))))

(defn codex-quota []
  (let [home (or (skill-variable "Codex active home") (str (fs/path (fs/home) ".codex")))
        socket (str (fs/path home "app-server-control" "app-server-control.sock"))
        module (str (fs/path primary-root "tools" "field-census" "codex-context.mjs"))
        r (run "node" "--input-type=module" "-e"
               (str "const m = await import(" (json/generate-string module) ");"
                    "console.log(JSON.stringify(await m.readCodexAccountQuota({socketPath: " (json/generate-string socket) "})));"))]
    (if (zero? (:exit r))
      (let [q (json/parse-string (:out r) true)]
        (if (seq (:errors q))
          (str "UNREADABLE: " (clip (str/join "; " (:errors q)) 300) " (socket " socket ")")
          (str "source: app-server account/rateLimits/read on " socket " (read " (:observedAt q) ")\n"
               (str/join "\n" (for [[id b] (:rateLimitsByLimitId q) [window w] [[:primary (:primary b)] [:secondary (:secondary b)]] :when w]
                                (str (name id) " " (name window) ": " (:usedPercent w) "% used, window "
                                     (:windowDurationMins w) " min, resets "
                                     (java.time.Instant/ofEpochSecond (:resetsAt w))
                                     ", plan " (:planType b)
                                     (when-let [x (:rateLimitReachedType b)] (str ", limit reached " x))))))))
      (str "UNREADABLE: node exit " (:exit r) ": " (clip (:err r) 300)))))

;; ---- Sanity ----
;; Flow's send stream carries, per event: sequence, delivery, sender, recipient, state.
;; It carries no time and no body. The window therefore runs from the sequence
;; recorded in the previous report to the stream's head now.

(def state-marker "pulse-state ")

(defn previous-state [previous]
  (when previous
    (when-let [m (re-find (re-pattern (str "<!-- " state-marker "(\\{.*\\}) -->")) (slurp (str previous)))]
      (json/parse-string (second m) true))))

;; A null stored seq sends ObserveSends.None and reads as the first window.
;; Observation, not a cause: the stored seq has been null since the 0747Z run;
;; what emptied it is unknown until that run's file or Flow's reply is read.
(defn sends-since [seq]
  (let [r (run "timeout" "6" "flow" (if seq (str "ObserveSends.Some." seq) "ObserveSends.None"))
        lines (str/split-lines (:out r))
        head (some->> lines (keep #(second (re-find #"^SendsObserved\.\{ (\d+) " %))) first parse-long)
        queued (for [[_ n d sender recipient] (when seq (re-seq #"\{ (\d+) logical-delivery-0*(\d+) Sender\.\{ ([^}]*?) \} \{ ([^}]*?) \} Queued \}" (:out r)))
                     :when (= n d)]
                 {:sender sender :recipient recipient})]
    (if head {:head head :queued queued} {:error (str "UNREADABLE: ObserveSends exit " (:exit r) ": " (clip (:err r) 200))})))

(defn pane-status-by-id [{s :snapshot}]
  (into {} (for [pane (:panes s)
                 :let [id (second (re-find #"([0-9a-f]{6}) \}(?:\s|$)" (str (:title pane) " " (:terminal_title_stripped pane))))]
                 :when id]
             [id (:agent_status pane)])))

(defn sanity [snap rows previous]
  (let [prior (previous-state previous)
        panes (get-in snap [:snapshot :panes])
        awake (filter :id rows)
        working (count (filter #(= "working" (:agent_status %)) panes))
        statuses (pane-status-by-id snap)
        sends (sends-since (:seq prior))
        sent (frequencies (map :sender (:queued sends)))
        queue-now (into {} (map (juxt :address (comp count :deliveries)) rows))
        growth (fn [a] (when-let [before (get-in prior [:queues (keyword a)])] (- (queue-now a) before)))
        busy-senders (sort-by (comp - val) (filter #(> (val %) sends-per-hour-flag) sent))
        grew-idle (for [{:keys [address id]} awake
                        :let [g (growth address) st (statuses id)]
                        :when (and g (pos? g) st (not= "working" st))]
                    (str address " (" st ", +" g ")"))
        acknowledging (for [{:keys [address deliveries]} rows
                            d deliveries
                            :when (and (re-find #"Notice$" (:kind d)) (<= (count (:text d)) acknowledgement-longest)
                                       (re-find acknowledgement-start (:text d)))]
                        (str address " #" (:id d) " from " (:sender d)))
        window (cond (:error sends) (:error sends)
                     (not (:seq prior)) "no earlier state, so the window opens now and send counts start with the next pulse"
                     :else (str "sequence " (:seq prior) " to " (:head sends) " (" (- (:head sends) (:seq prior)) " send events, since " (:time prior) ")"))
        line (fn [& xs] (apply str xs))]
    {:flagged (vec (distinct (concat (map key busy-senders)
                                     (map #(first (str/split % #" \(")) grew-idle)
                                     (map #(first (str/split % #" #")) acknowledging))))
     :text
     (str/join "\n"
       [(line "## Sanity")
        ""
        "Reader: judge your own sanity, and that of the flows around you, before you act on this pulse. Look at what you have sent and received lately. Signs of insanity are an echo chamber, where the same question or claim goes round and round between flows; jargon and nonsense that keep increasing over time; and acknowledgements answering acknowledgements. What is sane is your judgment. The figures below are evidence for it, and none of them is a verdict."
        ""
        "Evidence (W: read from Flow and Herdr by the script):"
        (line "- Awake metaflows: " (count awake) " against a ceiling of " awake-ceiling (when (> (count awake) awake-ceiling) " (over)"))
        (line "- Working panes: " working " against a ceiling of " working-ceiling (when (> working working-ceiling) " (over)"))
        (line "- Window for send counts: " window)
        (line "- Messages sent in the window, per metaflow: "
              (if (seq sent) (str/join ", " (map (fn [[a c]] (str a " " c)) (sort-by (comp - val) sent))) "none")
              ". Metaflows with a queue are listed below with their growth since the earlier report.")
        (str/join "\n" (for [{:keys [address state id]} (sort-by :address rows)
                             :let [q (queue-now address) g (growth address)]
                             :when (or (pos? q) (some-> g pos?) (some-> g neg?))]
                         (line "  - " address " (" (or (statuses id) (if id "awake, no pane" state)) "): queue " q
                               (if g (str ", " (if (neg? g) g (str "+" g)) " since the earlier report") ", growth unknown (no earlier state)"))))
        (line "- Sent more than " sends-per-hour-flag " in the window: "
              (if (seq busy-senders) (str/join ", " (map (fn [[a c]] (str a " " c)) busy-senders)) "none"))
        (line "- Queue grew while its pane was not working: " (if (seq grew-idle) (str/join ", " grew-idle) "none"))
        (line "- Queued Notices (up to " acknowledgement-longest " characters) that begin as an acknowledgement: "
              (if (seq acknowledging) (str/join "; " acknowledging) "none"))
        ""
        "Not measurable from Flow (stated, not guessed):"
        "- A message answering a message with only an acknowledgement: Flow's send events carry no body and no reply link, and a body is visible only while the delivery is still queued. The line above is the only partial view, from queued Notices, by their first words."
        "- A question sent after its own answer had been sent: Flow has no link between a question and an answer, and sent bodies are not observable, so crossed questions cannot be told."
        "- Echo chambers and rising jargon: bodies of delivered messages are not observable; the judgment above rests on what the reader itself sees."
        ""
        (str "<!-- " state-marker (json/generate-string {:seq (:head sends) :time (str now) :queues queue-now}) " -->")])}))

;; ---- the scan ----

(defn scan-prompt [gathered previous]
  (str "You are the Pulse, an hourly Tertiary scan of the flows. Below is what the pulse script gathered just now (" now ", UTC).
Write one short markdown report, plain short words, and print only the report.

Mark every line W (witnessed: read straight from the gathered data below, or from a command you ran) or C (claimed: what a log or a message says). Keep unknowns unknown.

Sections, in this order:
# Pulse " stamp "
1. Busy: which panes are working, which are idle or done; any pane whose title does not match an awake metaflow.
2. Done since the last pulse: from the flow logs, per flow (C), and what the earlier report said that has changed.
3. Queued and not taken up: per metaflow with deliveries held, the count and the oldest and most urgent ones; idle panes with work held first.
4. Quotas: Claude and Codex, percent used, reset time, hours left until each reset. If one is UNREADABLE, say exactly why.
5. Recommendation: one line on whether more Claude or Codex implementation work can be started now. Rule: unused Claude quota that resets soon is spent first, because Claude's output is better; Codex resets often, so leaning on it is cheap.

You may run read-only commands to check a fact (herdr api snapshot, herdr pane read, cat, tail, ls). Never open ~/.local/state/flow. Never type into a pane or send a message.

## Herdr panes
" (:panes gathered) "

## Flow metaflows (summary of flow 'Metaflows')
" (:metaflows gathered) "

## Flow logs (last 12 lines of each awake flow and of each log changed since the last pulse)
" (:logs gathered) "

## Claude quota
" (:claude gathered) "

## Codex quota
" (:codex gathered) "

## The earlier report
" (if previous (str "Path: " previous "\n" (clip (slurp (str previous)) 12000)) "none") "
"))

(defn scan [prompt]
  (let [r (p/shell {:out :string :err :string :continue true :in prompt
                    :dir (str (fs/temp-dir))
                    :extra-env {"CLAUDE_CODE_DISABLE_AUTO_MEMORY" "1"}}
                   "claude" "-p" "--model" "sonnet" "--effort" "low"
                   "--no-session-persistence"
                   "--tools" "Bash,Read"
                   "--allowedTools" "Read,Bash(herdr api snapshot),Bash(herdr pane read *),Bash(cat *),Bash(tail *),Bash(ls *)"
                   "--disallowedTools" "Read(~/.local/state/flow/**)")]
    (if (and (zero? (:exit r)) (not (str/blank? (:out r))))
      (:out r)
      (str "# Pulse " stamp "\n\nW: the scan run failed, exit " (:exit r) ": " (clip (str (:err r) (:out r)) 600) "\n"))))

;; ---- delivery ----

(defn recipient-pane [recipient]
  (let [r (run "herdr" "api" "snapshot")]
    (when (zero? (:exit r))
      (let [s (get-in (json/parse-string (:out r) true) [:result :snapshot])
            labels (into {} (map (juxt :workspace_id :label) (:workspaces s)))
            wanted (re-pattern (str "^\\{ " (java.util.regex.Pattern/quote recipient) " [0-9a-f]{6} \\}$"))
            hits (filter #(or (re-matches wanted (or (:terminal_title_stripped %) ""))
                              (re-matches wanted (or (labels (:workspace_id %)) "")))
                         (:panes s))]
        (when (= 1 (count hits)) (:pane_id (first hits)))))))

(defn deliver [recipient pointer]
  (let [address (str/join " " (str/split recipient #" "))
        flow-send (run "flow" (str "Send.{ Address.{ " address " } Wake MiddleAbrupt.Notice.«"
                                   (str/replace pointer "»" "\\»") "» }"))
        flow-answer (str/trim (str (:out flow-send) (:err flow-send)))]
    (if (and (zero? (:exit flow-send)) (not (re-find #"Refused|Error" flow-answer)))
      (str "- W: path Flow Send. Flow answered: " (clip flow-answer 300))
      (let [pane (recipient-pane recipient)]
        (if-not pane
          (str "- W: Flow Send refused: " (clip flow-answer 300)
               "\n- W: fallback failed: no single pane titled { " recipient " <id> } in the Herdr snapshot.")
          (let [typed (run "herdr" "agent" "prompt" pane pointer)
                flat (fn [s] (str/replace s #"\s+" ""))
                seen (some (fn [_]
                             (Thread/sleep 3000)
                             (str/includes? (flat (:out (run "herdr" "pane" "read" "--source" "recent-unwrapped"
                                                             "--lines" "200" "--format" "text" pane)))
                                            (flat pointer)))
                           (range 4))]
            (str "- W: Flow Send refused: " (clip flow-answer 300)
                 "\n- W: fallback path herdr agent prompt " pane ", exit " (:exit typed)
                 (when-not (str/blank? (:err typed)) (str " (" (clip (str/trim (:err typed)) 200) ")"))
                 "\n- W: pane read within 12 s: the whole pointer " (if seen "seen" "NOT seen") " in the last 200 lines of " pane ".")))))))

(defn poller-line []
  (let [r (run "systemctl" "--user" "show" "pulse.timer" "-p" "ActiveState" "-p" "FragmentPath")]
    (str "pulse.timer, every hour after the last run ends; "
         (str/replace (str/replace (str/trim (:out r)) #"NextElapseUSecRealtime=\n?" "") "\n" "; "))))

(defn quota-critical? [claude-text]
  (boolean (re-find #"\d+% critical" claude-text)))

(defn -main []
  (fs/create-dirs report-directory)
  (let [previous (previous-report)
        since (if previous (fs/file-time->millis (fs/last-modified-time previous)) (- (System/currentTimeMillis) 3600000))
        snap (snapshot)
        metaflows (gather-metaflows)
        gathered {:panes (gather-panes snap)
                  :metaflows (:text metaflows)
                  :logs (gather-logs (:flow-ids metaflows) since)
                  :claude (claude-quota)
                  :codex (codex-quota)}
        sanity-result (sanity snap (:rows metaflows) previous)]
    (when (System/getenv "PULSE_SANITY_ONLY") (println (:text sanity-result)) (System/exit 0))
    (let [prompt (scan-prompt gathered previous)]
      (when (System/getenv "PULSE_GATHER_ONLY") (println prompt) (System/exit 0))
      (let [report (scan prompt)]
        (spit report-path (str (str/trimr report) "\n\n" (:text sanity-result) "\n"))
        ;; The pointer goes to the recipient alone, and only when the Sanity section flags something or a quota is critical.
        (let [flagged (:flagged sanity-result)
              critical (quota-critical? (:claude gathered))
              targets (if (or (seq flagged) critical) [recipient] [])
              reason (str/join "; " (concat (when (seq flagged) ["Sanity flags"]) (when critical ["a quota is critical"])))
              witness (if (empty? targets)
                        "- W: the Sanity section flags nothing and no quota is critical; nothing was sent."
                        (str/join "\n"
                                  (for [t targets
                                        :let [pointer (str "Pulse " stamp ": report at " report-path " (" reason ")")]]
                                    (str "- W: to " t "\n" (deliver t pointer)))))]
          (spit report-path (str "\n## Delivery\n" witness "\n"
                                 "\n## Poller\n- W: " (poller-line) "\n") :append true)
          (println report-path)
          (println witness))))))

(-main)
