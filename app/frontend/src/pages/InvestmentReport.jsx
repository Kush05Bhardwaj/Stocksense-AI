import React from "react";
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { FiDownload, FiExternalLink, FiTrendingUp, FiTrendingDown, FiAlertTriangle, FiChevronUp, FiChevronDown } from "react-icons/fi";

const CollapsibleCard = ({ title, icon, children, defaultOpen = true }) => {
const [isOpen, setIsOpen] = useState(defaultOpen);

return (
    <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-md mb-6 overflow-hidden border border-gray-100 dark:border-gray-700">
        <button
            className="w-full flex items-center justify-between px-6 py-4 text-left hover:bg-gray-50 dark:hover:bg-gray-750 transition-colors"
            onClick={() => setIsOpen(!isOpen)}
        >
            <div className="flex items-center gap-3">
                <span className="text-indigo-500 text-xl">{icon}</span>
                <h2 className="text-lg font-semibold text-gray-800 dark:text-white">
                    {title}
                </h2>
            </div>
            {isOpen ? (
                <FiChevronUp className="text-gray-400 text-xl" />
            ) : (
                <FiChevronDown className="text-gray-400 text-xl" />
            )}
        </button>
        {isOpen && (
            <div className="px-6 pb-6 pt-2 border-t border-gray-100 dark:border-gray-700">
                {children}
            </div>
        )}
    </div>
);
};

const Badge = ({ label, type }) => {
const colors = {
    BUY: "bg-green-100 text-green-700 border-green-300",
    SELL: "bg-red-100 text-red-700 border-red-300",
    HOLD: "bg-yellow-100 text-yellow-700 border-yellow-300",
    HIGH: "bg-red-100 text-red-700 border-red-300",
    MEDIUM: "bg-yellow-100 text-yellow-700 border-yellow-300",
    LOW: "bg-green-100 text-green-700 border-green-300",
    POSITIVE: "bg-green-100 text-green-700 border-green-300",
    NEGATIVE: "bg-red-100 text-red-700 border-red-300",
    NEUTRAL: "bg-gray-100 text-gray-700 border-gray-300",
};
return (
    <span
        className={`px-3 py-1 rounded-full text-sm font-bold border ${
            colors[label?.toUpperCase()] || "bg-gray-100 text-gray-600"
        }`}
    >
        {label}
    </span>
);
};

const SentimentGauge = ({ score }) => {
const percentage = Math.min(Math.max(((score + 1) / 2) * 100, 0), 100);
const color =
    percentage > 60
        ? "bg-green-500"
        : percentage < 40
        ? "bg-red-500"
        : "bg-yellow-400";

return (
    <div className="mt-3">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
            <span>Bearish (-1)</span>
            <span>Neutral (0)</span>
            <span>Bullish (+1)</span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4 relative">
            <div
                className={`${color} h-4 rounded-full transition-all duration-700`}
                style={{ width: `${percentage}%` }}
            />
            <span className="absolute right-2 top-0 text-xs text-white font-bold leading-4">
                {score?.toFixed(2)}
            </span>
        </div>
    </div>
);
};

const InvestmentReport = () => {
const { symbol } = useParams();
const [report, setReport] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);
const [exporting, setExporting] = useState(false);

useEffect(() => {
    const fetchReport = async () => {
        try {
            setLoading(true);
            const res = await fetch(`/api/report/${symbol}`);
            if (!res.ok) throw new Error("Failed to fetch report");
            const data = await res.json();
            setReport(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };
    if (symbol) fetchReport();
}, [symbol]);

const handleExportPDF = async () => {
    try {
        setExporting(true);
        const res = await fetch(`/api/report/${symbol}/pdf`);
        if (!res.ok) throw new Error("PDF export failed");
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${symbol}_investment_report.pdf`;
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (err) {
        alert("Failed to export PDF: " + err.message);
    } finally {
        setExporting(false);
    }
};

if (loading)
    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-indigo-500" />
        </div>
    );

if (error)
    return (
        <div className="flex items-center justify-center min-h-screen text-red-500 text-lg">
            Error: {error}
        </div>
    );

if (!report) return null;

const {
    companyOverview,
    financialHealth,
    newsSentiment,
    modelPredictions,
    bullVsBear,
    riskFactors,
    finalRecommendation,
} = report;

return (
    <div className="max-w-4xl mx-auto px-4 py-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
            <div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                    Investment Report
                </h1>
                <p className="text-gray-500 dark:text-gray-400 mt-1">
                    {symbol} &mdash; Full Analysis
                </p>
            </div>
            <button
                onClick={handleExportPDF}
                disabled={exporting}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-xl font-semibold shadow transition disabled:opacity-60"
            >
                <FiDownload />
                {exporting ? "Exporting..." : "Export PDF"}
            </button>
        </div>

        {/* Company Overview */}
        <CollapsibleCard title="Company Overview" icon="🏢">
            <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-2xl font-bold text-gray-800 dark:text-white">
                        {companyOverview?.name}
                    </span>
                    {companyOverview?.website && (
                        <a
                            href={companyOverview.website}
                            target="_blank"
                            rel="noreferrer"
                            className="text-indigo-500 hover:underline flex items-center gap-1 text-sm"
                        >
                            <FiExternalLink /> Website
                        </a>
                    )}
                </div>
                <div className="flex gap-3 flex-wrap mt-1">
                    <span className="bg-indigo-50 dark:bg-indigo-900 text-indigo-600 dark:text-indigo-300 px-3 py-1 rounded-full text-xs font-semibold">
                        {companyOverview?.sector}
                    </span>
                    <span className="bg-purple-50 dark:bg-purple-900 text-purple-600 dark:text-purple-300 px-3 py-1 rounded-full text-xs font-semibold">
                        {companyOverview?.industry}
                    </span>
                </div>
                <p className="text-gray-600 dark:text-gray-300 text-sm mt-3 leading-relaxed">
                    {companyOverview?.description}
                </p>
            </div>
        </CollapsibleCard>

        {/* Financial Health */}
        <CollapsibleCard title="Financial Health" icon="📊">
            <div className="overflow-x-auto">
                <table className="w-full text-sm">
                    <thead>
                        <tr className="bg-gray-50 dark:bg-gray-700">
                            <th className="text-left px-4 py-2 text-gray-600 dark:text-gray-300 font-semibold">
                                Metric
                            </th>
                            <th className="text-right px-4 py-2 text-gray-600 dark:text-gray-300 font-semibold">
                                Value
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {[
                            { label: "Market Cap", value: financialHealth?.marketCap },
                            { label: "P/E Ratio", value: financialHealth?.peRatio },
                            { label: "EPS", value: financialHealth?.eps },
                            {
                                label: "Debt-to-Equity",
                                value: financialHealth?.debtToEquity,
                            },
                            {
                                label: "Gross Margin",
                                value: financialHealth?.grossMargin
                                    ? `${financialHealth.grossMargin}%`
                                    : "—",
                            },
                            {
                                label: "Net Margin",
                                value: financialHealth?.netMargin
                                    ? `${financialHealth.netMargin}%`
                                    : "—",
                            },
                            {
                                label: "Operating Margin",
                                value: financialHealth?.operatingMargin
                                    ? `${financialHealth.operatingMargin}%`
                                    : "—",
                            },
                        ].map((row, idx) => (
                            <tr
                                key={idx}
                                className={
                                    idx % 2 === 0
                                        ? "bg-white dark:bg-gray-800"
                                        : "bg-gray-50 dark:bg-gray-750"
                                }
                            >
                                <td className="px-4 py-2 text-gray-700 dark:text-gray-200">
                                    {row.label}
                                </td>
                                <td className="px-4 py-2 text-right font-medium text-gray-800 dark:text-white">
                                    {row.value ?? "—"}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </CollapsibleCard>

        {/* News Sentiment */}
        <CollapsibleCard title="News Sentiment" icon="📰">
            <div className="flex items-center gap-4 mb-2 flex-wrap">
                <Badge label={newsSentiment?.label?.toUpperCase()} />
                <span className="text-sm text-gray-500 dark:text-gray-400">
                    Based on{" "}
                    <span className="font-semibold text-gray-700 dark:text-gray-200">
                        {newsSentiment?.articleCount}
                    </span>{" "}
                    articles
                </span>
            </div>
            <SentimentGauge score={newsSentiment?.score} />
        </CollapsibleCard>

        {/* Model Predictions */}
        <CollapsibleCard title="Model Predictions" icon="🤖">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {modelPredictions?.map((pred, idx) => (
                    <div
                        key={idx}
                        className="bg-gray-50 dark:bg-gray-700 rounded-xl p-4 border border-gray-200 dark:border-gray-600"
                    >
                        <div className="flex items-center justify-between mb-2">
                            <span className="font-semibold text-gray-700 dark:text-gray-200">
                                {pred.model}
                            </span>
                            <Badge label={pred.signal?.toUpperCase()} />
                        </div>
                        <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400">
                            ${pred.predictedPrice?.toFixed(2)}
                        </div>
                        <div className="text-xs text-gray-400 mt-1">
                            Confidence:{" "}
                            <span className="font-semibold text-gray-600 dark:text-gray-300">
                                {pred.confidence}%
                            </span>
                        </div>
                        {pred.horizon && (
                            <div className="text-xs text-gray-400 mt-0.5">
                                Horizon:{" "}
                                <span className="font-semibold text-gray-600 dark:text-gray-300">
                                    {pred.horizon}
                                </span>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </CollapsibleCard>

        {/* Bull vs Bear */}
        <CollapsibleCard title="Bull vs Bear Arguments" icon="⚖️">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div>
                    <div className="flex items-center gap-2 mb-3">
                        <FiTrendingUp className="text-green-500 text-lg" />
                        <span className="font-semibold text-green-600 dark:text-green-400">
                            Bull Case
                        </span>
                    </div>
                    <ul className="space-y-2">
                        {bullVsBear?.bull?.map((point, idx) => (
                            <li key={idx} className="flex items-start gap-2 text-sm">
                                <span className="mt-1 w-2 h-2 rounded-full bg-green-400 flex-shrink-0" />
                                <span className="text-gray-700 dark:text-gray-200">
                                    {point}
                                </span>
                            </li>
                        ))}
                    </ul>
                </div>
                <div>
                    <div className="flex items-center gap-2 mb-3">
                        <FiTrendingDown className="text-red-500 text-lg" />
                        <span className="font-semibold text-red-600 dark:text-red-400">
                            Bear Case
                        </span>
                    </div>
                    <ul className="space-y-2">
                        {bullVsBear?.bear?.map((point, idx) => (
                            <li key={idx} className="flex items-start gap-2 text-sm">
                                <span className="mt-1 w-2 h-2 rounded-full bg-red-400 flex-shrink-0" />
                                <span className="text-gray-700 dark:text-gray-200">
                                    {point}
                                </span>
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </CollapsibleCard>

        {/* Risk Factors */}
        <CollapsibleCard title="Risk Factors" icon="⚠️">
            <div className="flex items-center gap-4 mb-4 flex-wrap">
                <div className="flex items-center gap-2">
                    <FiAlertTriangle className="text-orange-400" />
                    <span className="text-sm text-gray-600 dark:text-gray-300">
                        Risk Level:
                    </span>
                    <Badge label={riskFactors?.riskLevel?.toUpperCase()} />
                </div>
                <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600 dark:text-gray-300">
                        Volatility:
                    </span>
                    <span className="font-bold text-gray-800 dark:text-white">
                        {riskFactors?.volatility?.toFixed(2)}%
                    </span>
                </div>
            </div>
            {riskFactors?.factors?.length > 0 && (
                <ul className="space-y-2">
                    {riskFactors.factors.map((f, idx) => (
                        <li
                            key={idx}
                            className="flex items-start gap-2 text-sm text-gray-700 dark:text-gray-200"
                        >
                            <span className="mt-1 w-2 h-2 rounded-full bg-orange-400 flex-shrink-0" />
                            {f}
                        </li>
                    ))}
                </ul>
            )}
        </CollapsibleCard>

        {/* Final Recommendation */}
        <CollapsibleCard title="Final Recommendation" icon="🎯" defaultOpen>
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
                <div className="flex flex-col items-center gap-2">
                    <Badge label={finalRecommendation?.signal?.toUpperCase()} />
                    <div className="text-center">
                        <div className="text-4xl font-extrabold text-indigo-600 dark:text-indigo-400">
                            {finalRecommendation?.score}
                            <span className="text-lg font-normal text-gray-400">/100</span>
                        </div>
                        <div className="text-xs text-gray-400 mt-1">Confidence Score</div>
                    </div>
                </div>
                <div className="flex-1 bg-gray-50 dark:bg-gray-700 rounded-xl p-4 border border-gray-200 dark:border-gray-600">
                    <p className="text-sm text-gray-700 dark:text-gray-200 leading-relaxed">
                        {finalRecommendation?.rationale}
                    </p>
                </div>
            </div>
        </CollapsibleCard>

        {/* Footer Export */}
        <div className="flex justify-end mt-4">
            <button
                onClick={handleExportPDF}
                disabled={exporting}
                className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-xl font-semibold shadow-lg transition disabled:opacity-60"
            >
                <FiDownload />
                {exporting ? "Exporting..." : "Download PDF Report"}
            </button>
        </div>
    </div>
);
};

export default InvestmentReport;