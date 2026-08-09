**`app/page.js`**
```jsx
"use client";

import React, {
  useState,
  useEffect,
  useRef,
  useCallback,
  useMemo,
  memo,
  Component,
} from "react";
import {
  Terminal,
  Cpu,
  Pause,
  Play,
  Send,
  Activity,
  DollarSign,
  Database,
  TrendingUp,
  AlertTriangle,
  ArrowLeft,
  RefreshCw,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

const MASTER_TABS_REGISTRY = Object.freeze({
  1: { id: 1, name: "AI & Autonomous Research Engine", status: "Active", uptime: "24/7", rate: "12 req/m", lastAction: "Scanning global SaaS trends..." },
  2: { id: 2, name: "Global Control State Engine", status: "Optimal", focusScore: 88, operationalState: "Deep Focus Mode" },
  3: { id: 3, name: "Unified Vault Synchronization", status: "Synced", integrity: "100%", encryption: "AES-GCM-256" },
  4: { id: 4, name: "Secure Financial Ledger", balance: 145800, currency: "INR", forecast: "Stable", data: [{ name: "Week 1", amount: 4200 }, { name: "Week 2", amount: 7800 }, { name: "Week 3", amount: 3100 }, { name: "Week 4", amount: 9800 }] },
  5: { id: 5, name: "Document Ingestion & Vector RAG Store", status: "Active", embeddedTokens: "4.2M", totalNodes: 1240 },
  6: { id: 6, name: "Task & Project Management Hub", status: "Active", openTasks: 2, doneTasks: 1 },
  7: { id: 7, name: "Focus & Performance Analytics", avgEfficiency: "94.2%", metrics: [{ day: "Mon", score: 85 }, { day: "Tue", score: 92 }, { day: "Wed", score: 89 }, { day: "Thu", score: 95 }] },
  8: { id: 8, name: "Market Intelligence Hub", status: "Tracking", signalStrength: "Strong" },
  9: { id: 9, name: "Knowledge Base & Vault Viewer", documents: 412, linkedClusters: 58 },
  10: { id: 10, name: "API Integration & Webhook Center", webhooksActive: 14, failoverNodes: 3, status: "Connected" },
  11: { id: 11, name: "System Health & Diagnostics Monitor", cpuLoad: 34, ramUsage: "4.8GB / 16GB", ping: "11ms" },
  12: { id: 12, name: "Automation Scheduler", activeJobs: 2, status: "Running" },
  13: { id: 13, name: "User Profile & Security Settings", identity: "Aadi Admin", authLevel: "Root Level 0" },
  14: { id: 14, name: "Analytics & Executive Reports", generated: 47, autoDelivery: "Enabled" },
  15: { id: 15, name: "Communication & Notification Center", warnings: 0, vitalAlerts: "All loops operational" },
  16: { id: 16, name: "Backup & Recovery Hub", snapshotsCount: 28, lastVerifiedBackup: "Today 04:00 AM" },
  17: { id: 17, name: "Developer Terminal & Live Logs View", environment: "Production", activeStream: true },
  18: { id: 18, name: "Content & Media Ingestion Tab", queueStatus: "Empty", processedToday: 34 },
  19: { id: 19, name: "Strategy & Goal Execution Matrix", priorityTarget: "Scale Omni Infrastructure", completionProgress: 82 },
  20: { id: 20, name: "Autonomous Decision & Policy Engine", authorizationMode: "Fully Unattended", modelConfidence: "98.9%" },
  21: { id: 21, name: "Master Dashboard & Omnipresent Command Center", coreUptime: "99.99%", systemMode: "Master Autonomous Control" },
});

const BACKGROUND_ACTIONS = Object.freeze([
  "[AI Engine] Evaluated Tab 4 Ledger data. No structural budget anomalies detected.",
  "[AI Engine] Running predictive health routines inside Tab 11. Core nodes healthy.",
  "[AI Engine] Parsed unstructured telemetry into Tab 5 RAG Knowledge Store.",
  "[AI Engine] Tab 3 confirmed local system arrays match remote cloud states.",
]);

const MAX_TERMINAL_LINES = 20;
const TICK_MS = 3500;

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

const pushCapped = (list, entries, cap) => {
  const merged = [...entries, ...list];
  return merged.length > cap ? merged.slice(0, cap) : merged;
};

class TabErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.error("[TabErrorBoundary] Render failure captured:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="bg-red-950/20 border border-red-500/30 rounded-xl p-6 flex flex-col items-start gap-3">
          <div className="flex items-center gap-2 text-red-400 font-mono text-sm font-bold">
            <AlertTriangle size={16} />
            <span>MODULE FAULT ISOLATED</span>
          </div>
          <p className="text-xs text-slate-400 font-mono leading-relaxed">
            इस टैब का रेंडर पाथ एक अप्रत्याशित डेटा शेप की वजह से फेल हुआ। बाकी सिस्टम सुरक्षित और चालू है।
            स्वयं-सुधार (self-heal) के लिए नीचे बटन दबाएँ।
          </p>
          <button
            type="button"
            onClick={() => this.setState({ hasError: false })}
            className="flex items-center gap-2 bg-red-500/10 hover:bg-red-500/20 border border-red-500/40 text-red-300 font-mono text-xs px-3 py-1.5 rounded-md transition-colors"
          >
            <RefreshCw size={12} />
            Retry Module
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

function safeMetaEntries(tabObject) {
  try {
    if (!tabObject || typeof tabObject !== "object") {
      throw new Error("Invalid tab payload");
    }
    return Object.entries(tabObject).filter(
      ([key, value]) => key !== "id" && key !== "name" && typeof value !== "object"
    );
  } catch (err) {
    console.error("[safeMetaEntries] fallback triggered:", err);
    return [];
  }
}

const SidebarNavButton = memo(function SidebarNavButton({ tab, isActive, onSelect }) {
  return (
    <button
      type="button"
      onClick={() => onSelect(tab.id)}
      className={`w-full text-left font-mono text-xs px-3 py-2.5 rounded-md flex items-center justify-between border transition-colors ${
        isActive
          ? "bg-cyan-950/30 border-cyan-500/40 text-cyan-400 shadow-[inset_0_0_8px_rgba(6,182,212,0.08)]"
          : "border-transparent text-slate-400 hover:bg-slate-900 hover:text-white"
      }`}
    >
      <span className="truncate flex items-center gap-2">
        <span className="text-[10px] text-slate-600">{String(tab.id).padStart(2, "0")}</span>
        <span className="truncate">{tab.name}</span>
      </span>
      {tab.id === 21 && <Cpu size={12} className="text-cyan-400 shrink-0 ml-2" />}
    </button>
  );
});

const FocusStateCard = memo(function FocusStateCard({ tab2 }) {
  return (
    <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider">Tab 2: Global Control State</span>
        <span className="text-[10px] font-mono text-green-400">LIVE</span>
      </div>
      <div className="text-3xl font-black text-cyan-400 font-mono mb-1">{tab2.focusScore}%</div>
      <p className="text-xs text-slate-500 mb-3">Focus State: {tab2.operationalState}</p>
      <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden">
        <div
          className="bg-cyan-400 h-full transition-all duration-700"
          style={{ width: `${tab2.focusScore}%` }}
        />
      </div>
    </div>
  );
});

const LedgerCard = memo(function LedgerCard({ tab4 }) {
  return (
    <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider">Tab 4: Secure Ledger</span>
        <DollarSign size={14} className="text-emerald-400" />
      </div>
      <div className="text-2xl font-black text-emerald-400 font-mono mb-1">
        ₹{tab4.balance.toLocaleString("en-IN")}
      </div>
      <p className="text-xs text-slate-500 mb-2">Predictive Analytics: {tab4.forecast}</p>
      <p className="text-[10px] text-slate-600 font-mono">Auto-Tag Deduplication: Encrypted</p>
    </div>
  );
});

const VectorStoreCard = memo(function VectorStoreCard({ tab5 }) {
  return (
    <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider">Tab 5: Vector RAG Store</span>
        <Database size={14} className="text-purple-400" />
      </div>
      <div className="text-2xl font-black text-purple-400 font-mono mb-1">{tab5.embeddedTokens}</div>
      <p className="text-xs text-slate-500 mb-2">Parsed via Multi-Modal Engine</p>
      <p className="text-[10px] text-slate-600 font-mono">Semantic Nodes Active: {tab5.totalNodes}</p>
    </div>
  );
});

const TelemetryCard = memo(function TelemetryCard({ tab11 }) {
  return (
    <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider">Tab 11: Telemetry</span>
        <Activity size={14} className="text-amber-400" />
      </div>
      <div className="text-2xl font-black text-amber-400 font-mono mb-1">{tab11.cpuLoad}%</div>
      <p className="text-xs text-slate-500 mb-2">Server Ping: {tab11.ping}</p>
      <p className="text-[10px] text-slate-600 font-mono">Self-Healing Loop: Stable</p>
    </div>
  );
});

const LedgerChart = memo(function LedgerChart({ data }) {
  return (
    <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4">
      <h3 className="text-xs font-mono text-slate-400 uppercase tracking-wider mb-3">
        Tab 4 & Tab 14 Analytics Balance Curve
      </h3>
      <div style={{ width: "100%", height: 220 }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="name" stroke="#475569" fontSize={10} />
            <YAxis stroke="#475569" fontSize={10} />
            <Tooltip contentStyle={{ backgroundColor: "#020205", borderColor: "#1e293b" }} />
            <Line type="monotone" dataKey="amount" stroke="#10b981" strokeWidth={2} dot={{ r: 4 }} isAnimationActive={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
});

const EfficiencyChart = memo(function EfficiencyChart({ data }) {
  return (
    <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4">
      <h3 className="text-xs font-mono text-slate-400 uppercase tracking-wider mb-3">
        Tab 7 Behavioral Efficiency Score
      </h3>
      <div style={{ width: "100%", height: 220 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis dataKey="day" stroke="#475569" fontSize={10} />
            <YAxis stroke="#475569" fontSize={10} />
            <Tooltip contentStyle={{ backgroundColor: "#020205", borderColor: "#1e293b" }} />
            <Bar dataKey="score" fill="#06b6d4" radius={[4, 4, 0, 0]} isAnimationActive={false} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
});

const TerminalFeed = memo(function TerminalFeed({ feed }) {
  return (
    <div className="bg-black/70 border border-slate-800 rounded-xl p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2 text-slate-400 font-mono text-xs uppercase tracking-wider">
          <Terminal size={14} />
          Tab 17 Engine Live Output Feed
        </div>
        <span className="text-[10px] font-mono text-cyan-500">STREAMING_LOOP</span>
      </div>
      <div className="space-y-1.5 max-h-64 overflow-y-auto font-mono text-[11px] leading-relaxed">
        {feed.map((line, index) => (
          <div
            key={`${index}-${line.slice(0, 24)}`}
            className={
              line.startsWith("[Master AI")
                ? "text-cyan-400 font-bold"
                : line.startsWith(">")
                ? "text-slate-100"
                : "text-slate-500"
            }
          >
            {line}
          </div>
        ))}
      </div>
    </div>
  );
});

const CommandBar = memo(function CommandBar({ value, onChange, onSubmit }) {
  return (
    <form onSubmit={onSubmit} className="bg-slate-950/70 border border-cyan-900/40 rounded-xl p-4">
      <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs uppercase tracking-wider mb-3">
        <Cpu size={14} />
        Master Conversational Intent Engine
      </div>
      <div className="flex gap-2">
        <input
          type="text"
          value={value}
          onChange={onChange}
          placeholder="Command your Life OS via natural language (e.g. 'route to ledger', 'optimize system arrays')..."
          className="flex-1 bg-black border border-slate-800 rounded-lg px-4 py-2.5 text-xs font-mono text-cyan-300 focus:outline-none focus:border-cyan-500 transition-colors placeholder-slate-700"
        />
        <button
          type="submit"
          className="flex items-center gap-2 bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/40 text-cyan-300 font-mono text-xs px-4 py-2.5 rounded-lg transition-colors shrink-0"
        >
          <Send size={12} />
          Execute
        </button>
      </div>
    </form>
  );
});

const GenericTabPanel = memo(function GenericTabPanel({ tab, onReturn }) {
  const entries = safeMetaEntries(tab);
  return (
    <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-6 max-w-3xl">
      <p className="text-[10px] font-mono text-slate-600 uppercase tracking-wider mb-1">
        System Boundary / Node {tab && tab.id != null ? tab.id : "?"} of 21
      </p>
      <h2 className="text-lg font-bold text-cyan-300 mb-4">{(tab && tab.name) || "Unknown Module"}</h2>
      <div className="flex items-center gap-2 text-emerald-400 text-xs font-mono mb-3">
        <Activity size={12} />
        Autonomous Engine Engaged
      </div>
      <p className="text-xs text-slate-500 leading-relaxed mb-5">
        [Active State Protocol]: यह विशिष्ट मॉड्यूल पूरी तरह से स्वचालित (Automated Runtime Architecture) पर चल रहा
        है। इसकी सिंक्रनाइज़्ड डेटा स्ट्रीम्स सीधे आपके कोर रिपोजिटरी में मैप हो रही हैं।
      </p>
      {entries.length > 0 ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-5">
          {entries.map(([metaKey, metaVal]) => (
            <div key={metaKey} className="bg-black/40 border border-slate-900 rounded-lg px-3 py-2">
              <p className="text-[10px] text-slate-600 font-mono uppercase">
                {metaKey.replace(/([A-Z])/g, " $1")}
              </p>
              <p className="text-sm text-slate-200 font-mono">
                {metaKey === "balance" ? `₹${Number(metaVal).toLocaleString("en-IN")}` : String(metaVal)}
              </p>
            </div>
          ))}
        </div>
      ) : (
        <p className="text-xs text-amber-500 font-mono mb-5">
          इस मॉड्यूल के लिए कोई डिस्प्ले-योग्य मेटाडेटा नहीं मिला — फॉलबैक स्टेट सुरक्षित रूप से लागू है।
        </p>
      )}
      <button
        type="button"
        onClick={onReturn}
        className="bg-slate-900 border border-slate-800 hover:border-cyan-500/40 text-slate-300 font-mono text-xs px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
      >
        <ArrowLeft size={12} />
        Return to Command Center
      </button>
    </div>
  );
});

export default function AadiOmniAgentLifeOS() {
  const [tabsData, setTabsData] = useState(MASTER_TABS_REGISTRY);
  const [activeTab, setActiveTab] = useState(21);
  const [autonomousAI, setAutonomousAI] = useState(true);
  const [userInput, setUserInput] = useState("");
  const [terminalFeed, setTerminalFeed] = useState([
    "[System Initialization] Aadi Omni-Agent Life OS Online.",
    "[Orchestrator Engine] Initializing cross-tab semantic sync...",
    "[AI Agent] Standard loop listening on Port 3000...",
  ]);

  const isMountedRef = useRef(true);
  const timeoutIdRef = useRef(null);

  useEffect(() => {
    isMountedRef.current = true;

    if (!autonomousAI) {
      return () => {
        isMountedRef.current = false;
        if (timeoutIdRef.current) clearTimeout(timeoutIdRef.current);
      };
    }

    const tick = () => {
      if (!isMountedRef.current) return;

      if (typeof document !== "undefined" && document.visibilityState === "hidden") {
        timeoutIdRef.current = setTimeout(tick, TICK_MS);
        return;
      }

      const currentCpu = Math.floor(Math.random() * (55 - 22 + 1)) + 22;
      const currentLatency = Math.floor(Math.random() * (18 - 6 + 1)) + 6;
      const drift = Math.floor(Math.random() * 3) - 1;
      const fireLog = BACKGROUND_ACTIONS[Math.floor(Math.random() * BACKGROUND_ACTIONS.length)];

      setTabsData((prev) => ({
        ...prev,
        2: { ...prev[2], focusScore: clamp(prev[2].focusScore + drift, 60, 100) },
        11: { ...prev[11], cpuLoad: currentCpu, ping: `${currentLatency}ms` },
        1: { ...prev[1], lastAction: `Scrape complete. Target index refreshed at ${new Date().toLocaleTimeString()}` },
      }));

      setTerminalFeed((prev) => pushCapped(prev, [fireLog], MAX_TERMINAL_LINES));

      timeoutIdRef.current = setTimeout(tick, TICK_MS);
    };

    timeoutIdRef.current = setTimeout(tick, TICK_MS);

    return () => {
      isMountedRef.current = false;
      if (timeoutIdRef.current) {
        clearTimeout(timeoutIdRef.current);
        timeoutIdRef.current = null;
      }
    };
  }, [autonomousAI]);

  const handleSelectTab = useCallback((id) => {
    setActiveTab(id);
  }, []);

  const handleInputChange = useCallback((e) => {
    setUserInput(e.target.value);
  }, []);

  const handleToggleAutonomous = useCallback(() => {
    setAutonomousAI((prev) => !prev);
  }, []);

  const executeMasterIntent = useCallback(
    (e) => {
      e.preventDefault();
      const trimmed = userInput.trim();
      if (!trimmed) return;

      const cmd = trimmed.toLowerCase();
      let response = "[Master AI Co-Pilot] Command cached. No explicit cross-tab route matched this pattern.";
      let nextActiveTab = null;

      if (cmd.includes("optimize") || cmd.includes("clear")) {
        setTabsData((prev) => ({
          ...prev,
          2: { ...prev[2], focusScore: 98 },
          10: { ...prev[10], status: "Connected" },
        }));
        response = "[Master AI Co-Pilot] Structural optimization triggered: focus raised to 98%, API queues cleared.";
      } else if (cmd.includes("finance") || cmd.includes("ledger") || cmd.includes("money")) {
        nextActiveTab = 4;
        response = "[Master AI Co-Pilot] Routing interface focus to Tab 4 (Secure Financial Ledger Engine).";
      } else if (cmd.includes("research") || cmd.includes("scrape")) {
        nextActiveTab = 1;
        response = "[Master AI Co-Pilot] Routing interface focus to Tab 1 (Autonomous Research Matrix).";
      } else if (cmd.includes("dashboard") || cmd.includes("master")) {
        nextActiveTab = 21;
        response = "[Master AI Co-Pilot] Restoring full viewport matrix to Tab 21 Omnipresent Command Center.";
      } else if (cmd.includes("diagnostic") || cmd.includes("health")) {
        nextActiveTab = 11;
        response = "[Master AI Co-Pilot] Navigated to Tab 11 Telemetry Monitor. Performance indexing online.";
      }

      if (nextActiveTab !== null) setActiveTab(nextActiveTab);
      setTerminalFeed((prev) => pushCapped(prev, [response, `> ${trimmed}`], MAX_TERMINAL_LINES));
      setUserInput("");
    },
    [userInput]
  );

  const handleReturnToCommandCenter = useCallback(() => {
    setActiveTab(21);
  }, []);

  const tabList = useMemo(() => Object.values(tabsData), [tabsData]);
  const ledgerChartData = useMemo(() => tabsData[4].data, [tabsData[4].data]);
  const efficiencyChartData = useMemo(() => tabsData[7].metrics, [tabsData[7].metrics]);
  const activeTabData = tabsData[activeTab];

  return (
    <div className="min-h-screen bg-[#020205] text-slate-200 font-sans selection:bg-cyan-500 selection:text-black antialiased">
      <header className="border-b border-cyan-950/80 bg-slate-950/70 backdrop-blur-md px-6 py-4 flex items-center justify-between sticky top-0 z-50 shadow-[0_1px_10px_rgba(6,182,212,0.05)]">
        <div className="flex items-center gap-3">
          <div className="w-2.5 h-2.5 bg-cyan-400 rounded-full animate-pulse shadow-[0_0_12px_#22d3ee]" />
          <h1 className="text-md font-mono uppercase tracking-widest font-black text-cyan-400">
            Aadi Omni-Agent Life OS
          </h1>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-slate-900/90 border border-slate-800 px-3 py-1 rounded-md text-xs font-mono">
            <span className="text-slate-500">AI CORE RUNTIME:</span>
            <span className={`font-bold ${autonomousAI ? "text-green-400" : "text-amber-400"}`}>
              {autonomousAI ? "AUTONOMOUS MODE" : "STANDBY"}
            </span>
            <button
              type="button"
              onClick={handleToggleAutonomous}
              className="text-slate-400 hover:text-white ml-2"
              aria-label={autonomousAI ? "Pause autonomous engine" : "Resume autonomous engine"}
            >
              {autonomousAI ? <Pause size={12} /> : <Play size={12} />}
            </button>
          </div>
        </div>
      </header>

      <div className="flex">
        <aside className="w-72 border-r border-slate-900 bg-slate-950/60 p-4 h-[calc(100vh-61px)] overflow-y-auto hidden lg:block shrink-0">
          <span className="text-[10px] font-mono text-slate-500 tracking-wider block mb-4 uppercase px-2">
            System Execution Matrix (21 Tabs)
          </span>
          <div className="space-y-1">
            {tabList.map((tab) => (
              <SidebarNavButton
                key={tab.id}
                tab={tab}
                isActive={activeTab === tab.id}
                onSelect={handleSelectTab}
              />
            ))}
          </div>
        </aside>

        <main className="flex-1 p-6 overflow-y-auto h-[calc(100vh-61px)]">
          <TabErrorBoundary key={activeTab}>
            {activeTab === 21 ? (
              <div className="space-y-6">
                <CommandBar value={userInput} onChange={handleInputChange} onSubmit={executeMasterIntent} />

                <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
                  <FocusStateCard tab2={tabsData[2]} />
                  <LedgerCard tab4={tabsData[4]} />
                  <VectorStoreCard tab5={tabsData[5]} />
                  <TelemetryCard tab11={tabsData[11]} />
                </div>

                <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                  <LedgerChart data={ledgerChartData} />
                  <EfficiencyChart data={efficiencyChartData} />
                </div>

                <TerminalFeed feed={terminalFeed} />
              </div>
            ) : (
              <GenericTabPanel tab={activeTabData} onReturn={handleReturnToCommandCenter} />
            )}
          </TabErrorBoundary>
        </main>
      </div>
    </div>
  );
}
```

**`app/layout.js`**
```jsx
import "./globals.css";

export const metadata = {
  title: "Aadi Omni-Agent Life OS",
  description: "Autonomous multi-agent life operating system dashboard.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

**`app/globals.css`**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**`tailwind.config.js`**
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{js,jsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

**`postcss.config.js`**
```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

**`package.json`**
```json
{
  "name": "aadi-omni-agent-life-os",
  "version": "1.2.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "lucide-react": "^0.300.0",
    "next": "14.0.4",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.10.3"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0"
  }
}
```
