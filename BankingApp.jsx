import { useState, useEffect, useRef } from "react";

// ─── MOCK DATA (simulates your Python backend) ───────────────────────────────
// In a real deployment, these functions would call your Python Flask/FastAPI server.
// For this demo, all state lives in React — same logic, browser-based.

const ACCOUNT_TYPES = ["Standard", "Savings", "InterestReward", "Joint", "FixedDeposit"];
const COLORS = {
  Standard: "#4ade80",
  Savings: "#60a5fa",
  InterestReward: "#f59e0b",
  Joint: "#a78bfa",
  FixedDeposit: "#f87171",
};

function generateAccountNumber() {
  return 1000 + Math.floor(Math.random() * 9000);
}

function createAccount(name, type, initialAmount, location, owners = []) {
  const fee = type === "Savings" ? 5 : 0;
  const interestRate = type === "Savings" ? 0.03 : type === "InterestReward" ? 0.05 : type === "FixedDeposit" ? 0.025 : 0;
  return {
    id: generateAccountNumber(),
    name,
    type,
    balance: parseFloat(initialAmount),
    location,
    owners: type === "Joint" ? owners : [],
    fee,
    interestRate,
    dateOpened: new Date().toISOString(),
    transactions: [
      { timestamp: new Date().toISOString(), type: "Account Opened", amount: parseFloat(initialAmount), balanceAfter: parseFloat(initialAmount) }
    ],
  };
}

// ─── COMPONENTS ──────────────────────────────────────────────────────────────

function Badge({ type }) {
  const colors = {
    Standard: "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30",
    Savings: "bg-blue-500/20 text-blue-300 border border-blue-500/30",
    InterestReward: "bg-amber-500/20 text-amber-300 border border-amber-500/30",
    Joint: "bg-violet-500/20 text-violet-300 border border-violet-500/30",
    FixedDeposit: "bg-rose-500/20 text-rose-300 border border-rose-500/30",
  };
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-mono ${colors[type] || colors.Standard}`}>
      {type}
    </span>
  );
}

function AccountCard({ account, onSelect, selected }) {
  const spent = account.transactions
    .filter(t => t.amount < 0)
    .reduce((s, t) => s + Math.abs(t.amount), 0);
  const earned = account.transactions
    .filter(t => t.amount > 0 && t.type !== "Account Opened")
    .reduce((s, t) => s + t.amount, 0);

  return (
    <div
      onClick={() => onSelect(account.id)}
      className={`relative cursor-pointer rounded-2xl p-5 transition-all duration-300 border ${
        selected
          ? "border-white/30 bg-white/10 shadow-lg shadow-black/40 scale-[1.02]"
          : "border-white/10 bg-white/5 hover:bg-white/8 hover:border-white/20"
      }`}
      style={{ fontFamily: "'IBM Plex Mono', monospace" }}
    >
      {/* Accent line */}
      <div
        className="absolute top-0 left-5 right-5 h-px rounded-full"
        style={{ background: `linear-gradient(90deg, transparent, ${COLORS[account.type]}, transparent)` }}
      />

      <div className="flex justify-between items-start mb-4">
        <div>
          <p className="text-white/50 text-xs mb-1">#{account.id}</p>
          <h3 className="text-white font-bold text-lg leading-tight">{account.name}</h3>
          {account.type === "Joint" && account.owners.length > 0 && (
            <p className="text-white/40 text-xs mt-1">{account.owners.join(", ")}</p>
          )}
        </div>
        <Badge type={account.type} />
      </div>

      <div className="mb-4">
        <p className="text-white/40 text-xs">Balance</p>
        <p className="text-3xl font-bold text-white">${account.balance.toLocaleString("en-US", { minimumFractionDigits: 2 })}</p>
      </div>

      <div className="flex gap-4 text-xs text-white/50">
        <span>📍 {account.location}</span>
        <span>↑ ${earned.toFixed(0)}</span>
        <span>↓ ${spent.toFixed(0)}</span>
      </div>
    </div>
  );
}

function TransactionRow({ t, index }) {
  const isCredit = t.amount >= 0;
  return (
    <div
      className="flex items-center justify-between py-3 border-b border-white/5 last:border-0"
      style={{ animation: `fadeIn 0.3s ease ${index * 0.05}s both` }}
    >
      <div className="flex items-center gap-3">
        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm ${isCredit ? "bg-emerald-500/20" : "bg-rose-500/20"}`}>
          {isCredit ? "↑" : "↓"}
        </div>
        <div>
          <p className="text-white text-sm font-medium">{t.type}</p>
          <p className="text-white/40 text-xs">{new Date(t.timestamp).toLocaleString()}</p>
        </div>
      </div>
      <div className="text-right">
        <p className={`font-bold font-mono ${isCredit ? "text-emerald-400" : "text-rose-400"}`}>
          {isCredit ? "+" : ""}${Math.abs(t.amount).toFixed(2)}
        </p>
        <p className="text-white/30 text-xs">${t.balanceAfter.toFixed(2)}</p>
      </div>
    </div>
  );
}

function AIAdvisorPanel({ account }) {
  const [advice, setAdvice] = useState("");
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);

  async function getAdvice() {
    setLoading(true);
    setAdvice("");
    setDone(false);

    const spent = account.transactions.filter(t => t.amount < 0).reduce((s, t) => s + Math.abs(t.amount), 0);
    const deposited = account.transactions.filter(t => t.amount > 0 && t.type !== "Account Opened").reduce((s, t) => s + t.amount, 0);
    const savings = deposited - spent;

    const prompt = `You are a friendly personal finance advisor.

Client profile:
- Name: ${account.name}
- Account Type: ${account.type}
- Current Balance: $${account.balance.toFixed(2)}
- Total Deposited (income): $${deposited.toFixed(2)}
- Total Spent: $${spent.toFixed(2)}
- Net Savings: $${savings.toFixed(2)}
- Location: ${account.location}

Provide:
1. A 1-sentence financial health assessment
2. Three specific investment recommendations for their savings level (use bullet points •)
3. One actionable tip to save more

Be friendly, practical, and encouraging. Keep it under 180 words.`;

    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          stream: true,
          messages: [{ role: "user", content: prompt }],
        }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done: streamDone, value } = await reader.read();
        if (streamDone) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n").filter(l => l.startsWith("data: "));

        for (const line of lines) {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.type === "content_block_delta" && data.delta?.text) {
              setAdvice(prev => prev + data.delta.text);
            }
          } catch {}
        }
      }
    } catch (e) {
      setAdvice(`Could not reach AI Advisor. Error: ${e.message}`);
    }

    setLoading(false);
    setDone(true);
  }

  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-lg">🤖</span>
          <h3 className="text-white font-bold" style={{ fontFamily: "'IBM Plex Mono', monospace" }}>AI Investment Advisor</h3>
        </div>
        <button
          onClick={getAdvice}
          disabled={loading}
          className="px-4 py-1.5 rounded-lg text-sm font-bold transition-all duration-200 disabled:opacity-50"
          style={{
            background: loading ? "rgba(255,255,255,0.1)" : "linear-gradient(135deg, #4ade80, #22d3ee)",
            color: loading ? "#ffffff80" : "#000",
            fontFamily: "'IBM Plex Mono', monospace",
          }}
        >
          {loading ? "Thinking..." : done ? "Refresh" : "Get Advice"}
        </button>
      </div>

      {!advice && !loading && (
        <p className="text-white/30 text-sm italic" style={{ fontFamily: "'IBM Plex Mono', monospace" }}>
          Click "Get Advice" to receive personalized investment recommendations powered by Claude AI.
        </p>
      )}

      {(advice || loading) && (
        <div className="text-white/80 text-sm leading-relaxed whitespace-pre-wrap" style={{ fontFamily: "'Georgia', serif" }}>
          {advice}
          {loading && <span className="inline-block w-2 h-4 bg-white/60 ml-1 animate-pulse" />}
        </div>
      )}
    </div>
  );
}

function Modal({ title, onClose, children }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" style={{ background: "rgba(0,0,0,0.7)", backdropFilter: "blur(8px)" }}>
      <div className="w-full max-w-md rounded-2xl border border-white/20 bg-[#0f1117] p-6 shadow-2xl" style={{ fontFamily: "'IBM Plex Mono', monospace" }}>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-white font-bold text-lg">{title}</h2>
          <button onClick={onClose} className="text-white/40 hover:text-white text-xl transition-colors">×</button>
        </div>
        {children}
      </div>
    </div>
  );
}

function Input({ label, ...props }) {
  return (
    <div className="mb-4">
      <label className="block text-white/50 text-xs mb-1">{label}</label>
      <input
        {...props}
        className="w-full bg-white/5 border border-white/15 rounded-lg px-3 py-2.5 text-white text-sm outline-none focus:border-white/40 transition-colors"
        style={{ fontFamily: "'IBM Plex Mono', monospace" }}
      />
    </div>
  );
}

function Select({ label, options, ...props }) {
  return (
    <div className="mb-4">
      <label className="block text-white/50 text-xs mb-1">{label}</label>
      <select
        {...props}
        className="w-full bg-[#0f1117] border border-white/15 rounded-lg px-3 py-2.5 text-white text-sm outline-none focus:border-white/40 transition-colors"
        style={{ fontFamily: "'IBM Plex Mono', monospace" }}
      >
        {options.map(o => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  );
}

function Btn({ children, variant = "primary", ...props }) {
  const styles = {
    primary: "bg-white text-black hover:bg-white/90",
    ghost: "bg-white/10 text-white hover:bg-white/15 border border-white/15",
    danger: "bg-rose-500/20 text-rose-300 hover:bg-rose-500/30 border border-rose-500/30",
    success: "bg-emerald-500/20 text-emerald-300 hover:bg-emerald-500/30 border border-emerald-500/30",
  };
  return (
    <button
      {...props}
      className={`w-full px-4 py-2.5 rounded-lg font-bold text-sm transition-all duration-200 ${styles[variant]}`}
      style={{ fontFamily: "'IBM Plex Mono', monospace" }}
    >
      {children}
    </button>
  );
}

// ─── MAIN APP ─────────────────────────────────────────────────────────────────

export default function BankingApp() {
  const [accounts, setAccounts] = useState([
    createAccount("Dhruv", "Standard", 1500, "Punjab"),
    createAccount("Jyotshna", "Savings", 2200, "Delhi"),
    createAccount("Shyam", "InterestReward", 3800, "Mumbai"),
    createAccount("Tirth", "Savings", 5000, "Ahmedabad"),
  ]);

  const [selectedId, setSelectedId] = useState(null);
  const [modal, setModal] = useState(null); // "create" | "deposit" | "withdraw" | "transfer"
  const [form, setForm] = useState({});
  const [toast, setToast] = useState(null);

  const selected = accounts.find(a => a.id === selectedId);

  function showToast(msg, type = "success") {
    setToast({ msg, type });
    setTimeout(() => setToast(null), 3000);
  }

  function updateAccount(id, updater) {
    setAccounts(prev => prev.map(a => a.id === id ? updater(a) : a));
  }

  function addTransaction(account, type, amount) {
    const newBalance = account.balance + amount;
    return {
      ...account,
      balance: newBalance,
      transactions: [
        ...account.transactions,
        { timestamp: new Date().toISOString(), type, amount, balanceAfter: newBalance }
      ]
    };
  }

  function handleDeposit() {
    const amount = parseFloat(form.amount);
    if (!selected || isNaN(amount) || amount <= 0) return showToast("Invalid amount", "error");

    const bonus = selected.type === "InterestReward" || selected.type === "Savings" ? amount * 0.05 : 0;
    const total = amount + bonus;
    const label = bonus > 0 ? `Deposit + ${(bonus / amount * 100).toFixed(0)}% Bonus` : "Deposit";

    updateAccount(selected.id, a => addTransaction(a, label, total));
    showToast(`Deposited $${total.toFixed(2)} into ${selected.name}`);
    setModal(null);
  }

  function handleWithdraw() {
    const amount = parseFloat(form.amount);
    if (!selected || isNaN(amount) || amount <= 0) return showToast("Invalid amount", "error");

    const fee = selected.fee || 0;
    const total = amount + fee;

    if (selected.type === "FixedDeposit") return showToast("FD accounts cannot be withdrawn early", "error");
    if (selected.balance < total) return showToast(`Insufficient funds. Balance: $${selected.balance.toFixed(2)}`, "error");

    const label = fee > 0 ? `Withdrawal (+ $${fee} fee)` : "Withdrawal";
    updateAccount(selected.id, a => addTransaction(a, label, -total));
    showToast(`Withdrew $${amount.toFixed(2)} from ${selected.name}`);
    setModal(null);
  }

  function handleTransfer() {
    const amount = parseFloat(form.amount);
    const target = accounts.find(a => a.id === parseInt(form.targetId));
    if (!selected || !target || isNaN(amount) || amount <= 0) return showToast("Invalid transfer", "error");
    if (selected.balance < amount) return showToast("Insufficient funds", "error");

    setAccounts(prev => prev.map(a => {
      if (a.id === selected.id) return addTransaction(a, `Transfer → ${target.name}`, -amount);
      if (a.id === target.id) return addTransaction(a, `Transfer ← ${selected.name}`, amount);
      return a;
    }));
    showToast(`Transferred $${amount.toFixed(2)} to ${target.name}`);
    setModal(null);
  }

  function handleCreate() {
    if (!form.name || !form.initialAmount || !form.location) return showToast("Fill all fields", "error");
    const owners = form.type === "Joint" ? (form.owners || "").split(",").map(o => o.trim()).filter(Boolean) : [];
    const acc = createAccount(form.name, form.type || "Standard", form.initialAmount, form.location, owners);
    setAccounts(prev => [...prev, acc]);
    setSelectedId(acc.id);
    showToast(`Account created for ${form.name}`);
    setModal(null);
  }

  function applyInterest() {
    if (!selected || !["Savings", "FixedDeposit"].includes(selected.type)) return;
    const rate = selected.interestRate || 0.03;
    const interest = selected.balance * rate;
    updateAccount(selected.id, a => addTransaction(a, "Monthly Interest Applied", interest));
    showToast(`+$${interest.toFixed(2)} interest applied`);
  }

  const totalAssets = accounts.reduce((s, a) => s + a.balance, 0);

  return (
    <div className="min-h-screen bg-[#080a0f] text-white" style={{ fontFamily: "'IBM Plex Mono', monospace" }}>
      {/* Animated background grid */}
      <div className="fixed inset-0 pointer-events-none opacity-20" style={{
        backgroundImage: "linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)",
        backgroundSize: "40px 40px"
      }} />

      {/* Toast */}
      {toast && (
        <div className={`fixed top-4 right-4 z-[100] px-4 py-3 rounded-xl text-sm font-bold shadow-xl transition-all ${
          toast.type === "error" ? "bg-rose-500/90 text-white" : "bg-emerald-500/90 text-black"
        }`}>
          {toast.type === "error" ? "❌" : "✅"} {toast.msg}
        </div>
      )}

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-end justify-between mb-10">
          <div>
            <p className="text-white/30 text-xs tracking-[0.3em] uppercase mb-2">Devankit's</p>
            <h1 className="text-4xl font-black text-white tracking-tight">Banking System</h1>
            <p className="text-white/40 text-sm mt-1">Python OOP · JSON Persistence · Claude AI</p>
          </div>
          <div className="text-right">
            <p className="text-white/30 text-xs mb-1">Total Assets</p>
            <p className="text-3xl font-black text-emerald-400">${totalAssets.toLocaleString("en-US", { minimumFractionDigits: 2 })}</p>
            <p className="text-white/30 text-xs mt-1">{accounts.length} accounts</p>
          </div>
        </div>

        <div className="grid grid-cols-12 gap-6">
          {/* Left: Account List */}
          <div className="col-span-12 lg:col-span-4 space-y-4">
            <div className="flex justify-between items-center mb-2">
              <h2 className="text-white/60 text-xs tracking-widest uppercase">Accounts</h2>
              <button
                onClick={() => { setForm({ type: "Standard" }); setModal("create"); }}
                className="text-xs px-3 py-1.5 rounded-lg bg-white text-black font-bold hover:bg-white/90 transition-colors"
              >
                + New
              </button>
            </div>
            {accounts.map(a => (
              <AccountCard key={a.id} account={a} onSelect={setSelectedId} selected={a.id === selectedId} />
            ))}
          </div>

          {/* Right: Account Detail */}
          <div className="col-span-12 lg:col-span-8">
            {!selected ? (
              <div className="flex items-center justify-center h-64 rounded-2xl border border-white/10 bg-white/5">
                <p className="text-white/30 text-sm">← Select an account to view details</p>
              </div>
            ) : (
              <div className="space-y-5">
                {/* Account header */}
                <div className="rounded-2xl border border-white/10 bg-white/5 p-6 relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-48 h-48 rounded-full opacity-10 blur-3xl"
                    style={{ background: COLORS[selected.type] }} />
                  <div className="relative">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <p className="text-white/40 text-xs mb-1">#{selected.id} · {selected.location}</p>
                        <h2 className="text-2xl font-black text-white">{selected.name}</h2>
                        {selected.type === "Joint" && (
                          <p className="text-white/40 text-sm mt-1">👥 {selected.owners.join(", ")}</p>
                        )}
                      </div>
                      <Badge type={selected.type} />
                    </div>

                    <p className="text-5xl font-black text-white mb-1">
                      ${selected.balance.toLocaleString("en-US", { minimumFractionDigits: 2 })}
                    </p>
                    <p className="text-white/30 text-xs">Opened {new Date(selected.dateOpened).toLocaleDateString()}</p>

                    {/* Action Buttons */}
                    <div className="flex flex-wrap gap-2 mt-5">
                      {[
                        { label: "Deposit", action: () => { setForm({}); setModal("deposit"); }, style: "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/30" },
                        { label: "Withdraw", action: () => { setForm({}); setModal("withdraw"); }, style: "bg-rose-500/20 text-rose-300 border border-rose-500/30 hover:bg-rose-500/30" },
                        { label: "Transfer", action: () => { setForm({}); setModal("transfer"); }, style: "bg-blue-500/20 text-blue-300 border border-blue-500/30 hover:bg-blue-500/30" },
                        ...(["Savings", "FixedDeposit"].includes(selected.type)
                          ? [{ label: "Apply Interest", action: applyInterest, style: "bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30" }]
                          : []),
                      ].map(({ label, action, style }) => (
                        <button key={label} onClick={action}
                          className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${style}`}>
                          {label}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                {/* AI Advisor */}
                <AIAdvisorPanel account={selected} />

                {/* Transaction History */}
                <div className="rounded-2xl border border-white/10 bg-white/5 p-5">
                  <h3 className="text-white/60 text-xs tracking-widest uppercase mb-4">Transaction History</h3>
                  {selected.transactions.length === 0 ? (
                    <p className="text-white/30 text-sm">No transactions yet.</p>
                  ) : (
                    <div>
                      {[...selected.transactions].reverse().map((t, i) => (
                        <TransactionRow key={i} t={t} index={i} />
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ── MODALS ── */}
      {modal === "create" && (
        <Modal title="Create New Account" onClose={() => setModal(null)}>
          <Input label="Account Holder Name" placeholder="e.g. Dhruv" value={form.name || ""} onChange={e => setForm(p => ({ ...p, name: e.target.value }))} />
          <Input label="Initial Deposit ($)" type="number" placeholder="1000" value={form.initialAmount || ""} onChange={e => setForm(p => ({ ...p, initialAmount: e.target.value }))} />
          <Input label="Location" placeholder="e.g. Mumbai" value={form.location || ""} onChange={e => setForm(p => ({ ...p, location: e.target.value }))} />
          <Select label="Account Type" options={ACCOUNT_TYPES} value={form.type || "Standard"} onChange={e => setForm(p => ({ ...p, type: e.target.value }))} />
          {form.type === "Joint" && (
            <Input label="Owners (comma-separated)" placeholder="Shruti, Devankit" value={form.owners || ""} onChange={e => setForm(p => ({ ...p, owners: e.target.value }))} />
          )}
          <Btn onClick={handleCreate}>Create Account</Btn>
        </Modal>
      )}

      {modal === "deposit" && selected && (
        <Modal title={`Deposit → ${selected.name}`} onClose={() => setModal(null)}>
          <p className="text-white/40 text-sm mb-4">Current balance: <span className="text-white">${selected.balance.toFixed(2)}</span></p>
          {(selected.type === "InterestReward" || selected.type === "Savings") && (
            <p className="text-amber-300/70 text-xs mb-4 p-3 rounded-lg bg-amber-500/10 border border-amber-500/20">⭐ This account earns 5% deposit bonus</p>
          )}
          <Input label="Amount ($)" type="number" placeholder="500" value={form.amount || ""} onChange={e => setForm(p => ({ ...p, amount: e.target.value }))} />
          <Btn onClick={handleDeposit}>Deposit</Btn>
        </Modal>
      )}

      {modal === "withdraw" && selected && (
        <Modal title={`Withdraw ← ${selected.name}`} onClose={() => setModal(null)}>
          <p className="text-white/40 text-sm mb-4">Current balance: <span className="text-white">${selected.balance.toFixed(2)}</span></p>
          {selected.fee > 0 && (
            <p className="text-rose-300/70 text-xs mb-4 p-3 rounded-lg bg-rose-500/10 border border-rose-500/20">⚠️ ${selected.fee} fee applies per withdrawal</p>
          )}
          <Input label="Amount ($)" type="number" placeholder="200" value={form.amount || ""} onChange={e => setForm(p => ({ ...p, amount: e.target.value }))} />
          <Btn variant="danger" onClick={handleWithdraw}>Withdraw</Btn>
        </Modal>
      )}

      {modal === "transfer" && selected && (
        <Modal title={`Transfer from ${selected.name}`} onClose={() => setModal(null)}>
          <p className="text-white/40 text-sm mb-4">Available: <span className="text-white">${selected.balance.toFixed(2)}</span></p>
          <Input label="Amount ($)" type="number" placeholder="100" value={form.amount || ""} onChange={e => setForm(p => ({ ...p, amount: e.target.value }))} />
          <div className="mb-4">
            <label className="block text-white/50 text-xs mb-1">Transfer To</label>
            <select
              className="w-full bg-[#0f1117] border border-white/15 rounded-lg px-3 py-2.5 text-white text-sm outline-none focus:border-white/40"
              style={{ fontFamily: "'IBM Plex Mono', monospace" }}
              value={form.targetId || ""}
              onChange={e => setForm(p => ({ ...p, targetId: e.target.value }))}
            >
              <option value="">Select account...</option>
              {accounts.filter(a => a.id !== selected.id).map(a => (
                <option key={a.id} value={a.id}>{a.name} (#{a.id}) — ${a.balance.toFixed(2)}</option>
              ))}
            </select>
          </div>
          <Btn onClick={handleTransfer}>Transfer</Btn>
        </Modal>
      )}

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;700&display=swap');
        @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } }
      `}</style>
    </div>
  );
}
