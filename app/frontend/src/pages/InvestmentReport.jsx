import { useState, useEffect } from "react";
import {
    FiDownload, FiExternalLink, FiTrendingUp, FiTrendingDown,
    FiAlertTriangle, FiChevronUp, FiChevronDown, FiSearch
} from "react-icons/fi";

//  helpers 
const S = {
    card: { background: "#fff", border: "1px solid #e2e8f0", borderRadius: "12px", marginBottom: "1.5rem", overflow: "hidden", boxShadow: "0 1px 4px rgba(0,0,0,0.07)" },
    cardHeader: { width: "100%", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0.9rem 1.4rem", background: "none", border: "none", cursor: "pointer", textAlign: "left" },
    cardBody: { padding: "0.5rem 1.4rem 1.4rem", borderTop: "1px solid #f0f0f0" },
    tag: (bg, color) => ({ background: bg, color, padding: "0.2rem 0.65rem", borderRadius: "999px", fontSize: "0.78rem", fontWeight: "600", display: "inline-block", marginRight: "0.4rem" }),
};

const BADGE_STYLE = {
    BUY: { background: "#d4edda", color: "#155724", border: "1px solid #c3e6cb" },
    SELL: { background: "#f8d7da", color: "#721c24", border: "1px solid #f5c6cb" },
    HOLD: { background: "#fff3cd", color: "#856404", border: "1px solid #ffeeba" },
    HIGH: { background: "#f8d7da", color: "#721c24", border: "1px solid #f5c6cb" },
    MEDIUM: { background: "#fff3cd", color: "#856404", border: "1px solid #ffeeba" },
    LOW: { background: "#d4edda", color: "#155724", border: "1px solid #c3e6cb" },
    POSITIVE: { background: "#d4edda", color: "#155724", border: "1px solid #c3e6cb" },
    NEGATIVE: { background: "#f8d7da", color: "#721c24", border: "1px solid #f5c6cb" },
    NEUTRAL: { background: "#e2e8f0", color: "#4a5568", border: "1px solid #cbd5e0" },
};

function Badge({ label }) {
    const s = BADGE_STYLE[label?.toUpperCase()] || { background: "#e2e8f0", color: "#4a5568", border: "1px solid #cbd5e0" };
    return (
        <span style={{ ...s, padding: "0.25rem 0.75rem", borderRadius: "999px", fontSize: "0.8rem", fontWeight: "700" }}>
            {label}
        </span>
    );
}

function CollapsibleCard({ title, icon, children, defaultOpen = true }) {
    const [open, setOpen] = useState(defaultOpen);
    return (
        <div style={S.card}>
            <button style={S.cardHeader} onClick={() => setOpen(o => !o)}>
                <div style={{ display: "flex", alignItems: "center", gap: "0.7rem" }}>
                    <span style={{ fontSize: "1.15rem" }}>{icon}</span>
                    <span style={{ fontWeight: "600", fontSize: "1rem", color: "#1a202c" }}>{title}</span>
                </div>
                {open ? <FiChevronUp style={{ color: "#a0aec0" }} /> : <FiChevronDown style={{ color: "#a0aec0" }} />}
            </button>
            {open && <div style={S.cardBody}>{children}</div>}
        </div>
    );
}

function SentimentGauge({ score }) {
    const pct = Math.min(Math.max(((score + 1) / 2) * 100, 0), 100);
    const color = pct > 60 ? "#48bb78" : pct < 40 ? "#f56565" : "#ecc94b";
    return (
        <div style={{ marginTop: "0.75rem" }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.72rem", color: "#718096", marginBottom: "4px" }}>
                <span>Bearish (-1)</span><span>Neutral (0)</span><span>Bullish (+1)</span>
            </div>
            <div style={{ width: "100%", background: "#e2e8f0", borderRadius: "999px", height: "16px", position: "relative" }}>
                <div style={{ width: `${pct}%`, background: color, height: "16px", borderRadius: "999px", transition: "width 0.6s" }} />
                <span style={{ position: "absolute", right: "8px", top: 0, fontSize: "0.72rem", color: "#fff", fontWeight: "700", lineHeight: "16px" }}>
                    {score?.toFixed(2)}
                </span>
            </div>
        </div>
    );
}

function fmt(v, prefix = "", suffix = "", scale = 1, dp = 2) {
    if (v == null) return "—";
    return `${prefix}${(v * scale).toLocaleString(undefined, { minimumFractionDigits: dp, maximumFractionDigits: dp })}${suffix}`;
}

function fmtCap(v) {
    if (v == null) return "—";
    if (v >= 1e12) return `$${(v / 1e12).toFixed(2)}T`;
    if (v >= 1e9)  return `$${(v / 1e9).toFixed(2)}B`;
    if (v >= 1e6)  return `$${(v / 1e6).toFixed(2)}M`;
    return `$${v.toLocaleString()}`;
}

//  main component 
export default function InvestmentReport({ symbol: symbolProp }) {
    const [input, setInput]           = useState(symbolProp || "");
    const [active, setActive]         = useState(symbolProp || null);
    const [report, setReport]         = useState(null);
    const [loading, setLoading]       = useState(false);
    const [error, setError]           = useState(null);
    const [exporting, setExporting]   = useState(false);

    useEffect(() => {
        if (!active) return;
        (async () => {
            try {
                setLoading(true); setError(null); setReport(null);
                const res = await fetch(`/api/report/${active}`);
                if (!res.ok) {
                    const body = await res.json().catch(() => ({}));
                    throw new Error(body.description || `Server error ${res.status}`);
                }
                setReport(await res.json());
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        })();
    }, [active]);

    const handleSearch = () => {
        const s = input.trim().toUpperCase();
        if (s) setActive(s);
    };

    const handleExportPDF = async () => {
        try {
            setExporting(true);
            const res = await fetch(`/api/report/${active}/pdf`);
            if (!res.ok) throw new Error("PDF export failed");
            const url = window.URL.createObjectURL(await res.blob());
            const a = document.createElement("a");
            a.href = url; a.download = `${active}_investment_report.pdf`; a.click();
            window.URL.revokeObjectURL(url);
        } catch (err) {
            alert("Failed to export PDF: " + err.message);
        } finally {
            setExporting(false);
        }
    };

    const BTN = (extra = {}) => ({
        display: "flex", alignItems: "center", gap: "0.45rem",
        background: "#4f46e5", color: "#fff", border: "none",
        padding: "0.65rem 1.2rem", borderRadius: "8px",
        fontWeight: "600", cursor: "pointer", fontSize: "0.9rem", ...extra
    });

    return (
        <div style={{ maxWidth: "920px", margin: "0 auto", padding: "2rem 1rem" }}>

            {/*  Search bar  */}
            <div style={{ display: "flex", gap: "0.75rem", marginBottom: "2rem" }}>
                <input
                    type="text"
                    value={input}
                    onChange={e => setInput(e.target.value)}
                    onKeyDown={e => e.key === "Enter" && handleSearch()}
                    placeholder="Enter stock symbol (e.g. AAPL, RELIANCE.NS)"
                    style={{ flex: 1, padding: "0.65rem 1rem", border: "1px solid #cbd5e0", borderRadius: "8px", fontSize: "1rem" }}
                />
                <button
                    onClick={handleSearch}
                    disabled={loading || !input.trim()}
                    style={{ ...BTN(), opacity: (loading || !input.trim()) ? 0.6 : 1 }}
                >
                    <FiSearch /> Generate Report
                </button>
            </div>

            {/*  Loading  */}
            {loading && (
                <div style={{ textAlign: "center", padding: "4rem", color: "#4f46e5" }}>
                    <div style={{ fontSize: "1.05rem", marginBottom: "0.4rem" }}>Generating investment report</div>
                    <div style={{ fontSize: "0.82rem", color: "#a0aec0" }}>Running ML models, fetching financials &amp; sentiment</div>
                </div>
            )}

            {/*  Error  */}
            {error && (
                <div style={{ background: "#fff5f5", border: "1px solid #fed7d7", color: "#c53030", padding: "1rem", borderRadius: "8px" }}>
                    Error: {error}
                </div>
            )}

            {/*  Report  */}
            {report && (
                <>
                    {/* Header */}
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "2rem", flexWrap: "wrap", gap: "1rem" }}>
                        <div>
                            <h1 style={{ margin: 0, fontSize: "1.75rem", fontWeight: "700", color: "#1a202c" }}>
                                {report.company_overview?.name || report.symbol}
                            </h1>
                            <p style={{ margin: "0.2rem 0 0", color: "#718096", fontSize: "0.88rem" }}>
                                {report.symbol} &mdash; {new Date(report.generated_at + "Z").toLocaleString()}
                            </p>
                            <p style={{ margin: "0.4rem 0 0", fontSize: "1.3rem", fontWeight: "700", color: "#4f46e5" }}>
                                {report.currency}{report.current_price?.toFixed(2)}
                            </p>
                        </div>
                        <button onClick={handleExportPDF} disabled={exporting} style={{ ...BTN({ opacity: exporting ? 0.6 : 1 }) }}>
                            <FiDownload /> {exporting ? "Exporting" : "Export PDF"}
                        </button>
                    </div>

                    {/*  Company Overview  */}
                    <CollapsibleCard title="Company Overview" icon="">
                        <div style={{ display: "flex", flexWrap: "wrap", gap: "0.4rem", marginBottom: "0.7rem" }}>
                            {report.company_overview?.sector   && <span style={S.tag("#ebf4ff", "#3182ce")}>{report.company_overview.sector}</span>}
                            {report.company_overview?.industry && <span style={S.tag("#f3e8ff", "#7c3aed")}>{report.company_overview.industry}</span>}
                            {report.company_overview?.country  && <span style={S.tag("#f0fff4", "#276749")}>{report.company_overview.country}</span>}
                        </div>
                        {report.company_overview?.employees && report.company_overview.employees !== "N/A" && (
                            <p style={{ fontSize: "0.84rem", color: "#718096", margin: "0 0 0.4rem" }}>
                                Full-time employees: <strong style={{ color: "#2d3748" }}>{Number(report.company_overview.employees).toLocaleString()}</strong>
                            </p>
                        )}
                        {report.company_overview?.website && report.company_overview.website !== "N/A" && (
                            <a href={report.company_overview.website} target="_blank" rel="noreferrer"
                               style={{ display: "inline-flex", alignItems: "center", gap: "0.3rem", color: "#4f46e5", fontSize: "0.84rem", marginBottom: "0.5rem" }}>
                                <FiExternalLink /> {report.company_overview.website}
                            </a>
                        )}
                        <p style={{ fontSize: "0.88rem", color: "#4a5568", lineHeight: "1.65", margin: 0 }}>
                            {report.company_overview?.description}
                        </p>
                    </CollapsibleCard>

                    {/*  Financial Health  */}
                    <CollapsibleCard title="Financial Health" icon="">
                        <div style={{ overflowX: "auto" }}>
                            <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.88rem" }}>
                                <thead>
                                    <tr style={{ background: "#f7fafc" }}>
                                        <th style={{ textAlign: "left",  padding: "0.55rem 1rem", color: "#718096", fontWeight: "600" }}>Metric</th>
                                        <th style={{ textAlign: "right", padding: "0.55rem 1rem", color: "#718096", fontWeight: "600" }}>Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {[
                                        ["Market Cap",       fmtCap(report.financial_health?.market_cap)],
                                        ["P/E Ratio (TTM)",  fmt(report.financial_health?.pe_ratio, "", "", 1, 1)],
                                        ["Forward P/E",      fmt(report.financial_health?.forward_pe, "", "", 1, 1)],
                                        ["EPS (TTM)",        fmt(report.financial_health?.eps, report.currency, "", 1, 2)],
                                        ["Dividend Yield",   fmt(report.financial_health?.dividend_yield, "", "%", 100, 2)],
                                        ["52-Week High",     fmt(report.financial_health?.["52_week_high"], report.currency)],
                                        ["52-Week Low",      fmt(report.financial_health?.["52_week_low"],  report.currency)],
                                        ["Price-to-Book",    fmt(report.financial_health?.price_to_book)],
                                        ["Debt / Equity",    fmt(report.financial_health?.debt_to_equity, "", "%", 1, 1)],
                                        ["Profit Margin",    fmt(report.financial_health?.profit_margin, "", "%", 100, 1)],
                                        ["Revenue Growth",   fmt(report.financial_health?.revenue_growth, "", "%", 100, 1)],
                                        ["Current Ratio",    fmt(report.financial_health?.current_ratio)],
                                    ].map(([label, value], idx) => (
                                        <tr key={label} style={{ background: idx % 2 === 0 ? "#fff" : "#f7fafc" }}>
                                            <td style={{ padding: "0.5rem 1rem", color: "#4a5568" }}>{label}</td>
                                            <td style={{ padding: "0.5rem 1rem", textAlign: "right", fontWeight: "500", color: "#1a202c" }}>{value}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </CollapsibleCard>

                    {/*  News Sentiment  */}
                    <CollapsibleCard title="News Sentiment" icon="">
                        <div style={{ display: "flex", alignItems: "center", gap: "1rem", flexWrap: "wrap", marginBottom: "0.4rem" }}>
                            <Badge label={report.news_sentiment?.label?.toUpperCase()} />
                            <span style={{ fontSize: "0.85rem", color: "#718096" }}>
                                Based on <strong style={{ color: "#2d3748" }}>{report.news_sentiment?.total_articles}</strong> articles
                            </span>
                        </div>
                        <SentimentGauge score={report.news_sentiment?.score} />
                    </CollapsibleCard>

                    {/*  Model Predictions  */}
                    <CollapsibleCard title="Model Predictions" icon="">
                        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(190px, 1fr))", gap: "1rem" }}>
                            {report.predictions?.map((pred, idx) => (
                                <div key={idx} style={{ background: "#f7fafc", border: "1px solid #e2e8f0", borderRadius: "10px", padding: "1rem" }}>
                                    <div style={{ fontWeight: "600", color: "#2d3748", marginBottom: "0.4rem", fontSize: "0.88rem" }}>
                                        {pred.model}
                                    </div>
                                    <div style={{ fontSize: "1.35rem", fontWeight: "700", color: "#4f46e5" }}>
                                        {report.currency}{pred.prediction?.toFixed(2)}
                                    </div>
                                    <div style={{ fontSize: "0.88rem", fontWeight: "600", marginTop: "0.2rem", color: pred.change > 0 ? "#276749" : "#c53030" }}>
                                        {pred.change > 0 ? "" : ""} {pred.change > 0 ? "+" : ""}{pred.change?.toFixed(2)}%
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CollapsibleCard>

                    {/*  Bull vs Bear  */}
                    <CollapsibleCard title="Bull vs Bear Arguments" icon="">
                        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem" }}>
                            <div>
                                <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.7rem" }}>
                                    <FiTrendingUp style={{ color: "#38a169" }} />
                                    <span style={{ fontWeight: "600", color: "#276749" }}>Bull Case</span>
                                </div>
                                <ul style={{ margin: 0, padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                                    {report.bull_arguments?.map((arg, i) => (
                                        <li key={i} style={{ display: "flex", gap: "0.5rem", fontSize: "0.86rem", color: "#2d3748" }}>
                                            <span style={{ width: "8px", height: "8px", borderRadius: "50%", background: "#48bb78", flexShrink: 0, marginTop: "5px" }} />
                                            {arg}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                            <div>
                                <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", marginBottom: "0.7rem" }}>
                                    <FiTrendingDown style={{ color: "#e53e3e" }} />
                                    <span style={{ fontWeight: "600", color: "#9b2c2c" }}>Bear Case</span>
                                </div>
                                <ul style={{ margin: 0, padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                                    {report.bear_arguments?.map((arg, i) => (
                                        <li key={i} style={{ display: "flex", gap: "0.5rem", fontSize: "0.86rem", color: "#2d3748" }}>
                                            <span style={{ width: "8px", height: "8px", borderRadius: "50%", background: "#fc8181", flexShrink: 0, marginTop: "5px" }} />
                                            {arg}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </CollapsibleCard>

                    {/*  Risk Factors  */}
                    <CollapsibleCard title="Risk Factors" icon="">
                        <div style={{ display: "flex", alignItems: "center", gap: "1.5rem", flexWrap: "wrap" }}>
                            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                                <FiAlertTriangle style={{ color: "#ed8936" }} />
                                <span style={{ fontSize: "0.87rem", color: "#718096" }}>Risk Level:</span>
                                <Badge label={report.risk?.risk_level?.toUpperCase()} />
                            </div>
                            <div>
                                <span style={{ fontSize: "0.87rem", color: "#718096" }}>Annualised Volatility: </span>
                                <strong style={{ color: "#2d3748" }}>{report.risk?.annualised_volatility_pct?.toFixed(2)}%</strong>
                            </div>
                        </div>
                    </CollapsibleCard>

                    {/*  Final Recommendation  */}
                    <CollapsibleCard title="Final Recommendation" icon="" defaultOpen={true}>
                        <div style={{ display: "flex", gap: "2rem", alignItems: "flex-start", flexWrap: "wrap" }}>
                            <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "0.5rem", minWidth: "110px" }}>
                                <Badge label={report.recommendation?.signal} />
                                <div style={{ textAlign: "center" }}>
                                    <div style={{ fontSize: "3rem", fontWeight: "800", color: "#4f46e5", lineHeight: 1 }}>
                                        {report.recommendation?.score}
                                    </div>
                                    <div style={{ fontSize: "0.78rem", color: "#a0aec0" }}>out of 100</div>
                                </div>
                            </div>
                            <div style={{ flex: 1, background: "#f7fafc", border: "1px solid #e2e8f0", borderRadius: "10px", padding: "1rem", fontSize: "0.9rem", color: "#4a5568", lineHeight: "1.65", minWidth: "200px" }}>
                                {report.recommendation?.rationale}
                            </div>
                        </div>
                    </CollapsibleCard>

                    {/* Footer export */}
                    <div style={{ display: "flex", justifyContent: "flex-end", marginTop: "0.5rem" }}>
                        <button onClick={handleExportPDF} disabled={exporting} style={{ ...BTN({ opacity: exporting ? 0.6 : 1, fontSize: "0.95rem", padding: "0.75rem 1.5rem" }) }}>
                            <FiDownload /> {exporting ? "Exporting" : "Download PDF Report"}
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}
