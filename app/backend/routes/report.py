import io
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, jsonify, send_file, abort
from utils.report_generator import generate_report

# Routes are prefixed /report/… here;
# app.py registers this blueprint with url_prefix='/api',
# so final URLs are /api/report/<symbol> and /api/report/<symbol>/pdf.
report_bp = Blueprint('report', __name__)


# ---------------------------------------------------------------------------
# PDF generator (fpdf2 — pure Python, no system dependencies)
# ---------------------------------------------------------------------------
def _build_pdf(report: dict) -> bytes:
    from fpdf import FPDF

    symbol    = report.get('symbol', '')
    currency  = report.get('currency', '$')
    cur_price = report.get('current_price', 0)

    class PDF(FPDF):
        def header(self):
            self.set_font('Helvetica', 'B', 13)
            self.cell(0, 9, f"Investment Report  \u2014  {symbol}", ln=True)
            self.set_font('Helvetica', '', 8)
            self.cell(0, 5, f"Generated: {report.get('generated_at', '')}  |  "
                            f"Current Price: {currency}{cur_price:.2f}", ln=True)
            self.ln(3)

        def footer(self):
            self.set_y(-13)
            self.set_font('Helvetica', 'I', 8)
            self.cell(0, 8, f'Page {self.page_no()}', align='C')

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=14)
    pdf.add_page()

    # ---- helpers ----
    def section(title: str):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_fill_color(220, 220, 245)
        pdf.cell(0, 7, f'  {title}', ln=True, fill=True)
        pdf.ln(2)

    def kv(label: str, value):
        pdf.set_font('Helvetica', 'B', 9)
        pdf.cell(55, 6, label + ':', ln=False)
        pdf.set_font('Helvetica', '', 9)
        pdf.multi_cell(0, 6, str(value) if value not in (None, 'N/A', '') else '\u2014')

    def bullet(text: str, rgb=(40, 120, 40)):
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(*rgb)
        pdf.multi_cell(0, 5, f'  \u2022  {text}')
        pdf.set_text_color(0, 0, 0)

    def fmt(v, prefix='', suffix='', scale=1, dp=2):
        if v is None:
            return '\u2014'
        return f"{prefix}{v * scale:,.{dp}f}{suffix}"

    def fmt_cap(v):
        if v is None:
            return '\u2014'
        if v >= 1e12: return f'${v/1e12:.2f}T'
        if v >= 1e9:  return f'${v/1e9:.2f}B'
        if v >= 1e6:  return f'${v/1e6:.2f}M'
        return f'${v:,.0f}'

    # ---- Company Overview ----
    ov = report.get('company_overview', {})
    section('Company Overview')
    kv('Name',      ov.get('name'))
    kv('Sector',    ov.get('sector'))
    kv('Industry',  ov.get('industry'))
    kv('Country',   ov.get('country'))
    kv('Employees', f"{int(ov['employees']):,}" if isinstance(ov.get('employees'), int) else ov.get('employees'))
    kv('Website',   ov.get('website'))
    desc = ov.get('description', '')
    if desc and desc not in ('N/A', ''):
        pdf.set_font('Helvetica', '', 8)
        pdf.multi_cell(0, 4, desc[:700] + ('...' if len(desc) > 700 else ''))
    pdf.ln(4)

    # ---- Financial Health ----
    fh = report.get('financial_health', {})
    section('Financial Health')
    rows = [
        ('Market Cap',      fmt_cap(fh.get('market_cap'))),
        ('P/E Ratio (TTM)', fmt(fh.get('pe_ratio'), dp=1)),
        ('Forward P/E',     fmt(fh.get('forward_pe'), dp=1)),
        ('EPS (TTM)',        fmt(fh.get('eps'), currency, dp=2)),
        ('Dividend Yield',  fmt(fh.get('dividend_yield'), suffix='%', scale=100, dp=2)),
        ('52-Week High',    fmt(fh.get('52_week_high'), currency)),
        ('52-Week Low',     fmt(fh.get('52_week_low'),  currency)),
        ('Price-to-Book',   fmt(fh.get('price_to_book'), dp=2)),
        ('Debt / Equity',   fmt(fh.get('debt_to_equity'), suffix='%', dp=1)),
        ('Profit Margin',   fmt(fh.get('profit_margin'), suffix='%', scale=100, dp=1)),
        ('Revenue Growth',  fmt(fh.get('revenue_growth'), suffix='%', scale=100, dp=1)),
        ('Current Ratio',   fmt(fh.get('current_ratio'), dp=2)),
    ]
    for label, val in rows:
        kv(label, val)
    pdf.ln(4)

    # ---- News Sentiment ----
    ns = report.get('news_sentiment', {})
    section('News Sentiment')
    kv('Label',            ns.get('label'))
    kv('Score',            ns.get('score'))
    kv('Articles Assessed', ns.get('total_articles'))
    pdf.ln(4)

    # ---- Model Predictions ----
    section('Model Predictions')
    kv('Current Price', f"{currency}{cur_price:.2f}")
    for p in report.get('predictions', []):
        change = p.get('change', 0)
        arrow  = '\u2191' if change > 0 else '\u2193'
        bullet(
            f"{p['model']}: {currency}{p['prediction']:.2f}  ({arrow} {change:+.2f}%)",
            rgb=(0, 110, 0) if change > 0 else (160, 0, 0)
        )
    pdf.ln(4)

    # ---- Bull vs Bear ----
    section('Bull vs Bear Arguments')
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 6, 'Bull Case', ln=True)
    for arg in report.get('bull_arguments', []):
        bullet(arg, rgb=(0, 120, 0))
    pdf.ln(2)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(0, 6, 'Bear Case', ln=True)
    for arg in report.get('bear_arguments', []):
        bullet(arg, rgb=(160, 0, 0))
    pdf.ln(4)

    # ---- Risk ----
    risk = report.get('risk', {})
    section('Risk Factors')
    kv('Risk Level',           risk.get('risk_level'))
    kv('Annualised Volatility', f"{risk.get('annualised_volatility_pct', 0):.2f}%")
    pdf.ln(4)

    # ---- Recommendation banner ----
    rec    = report.get('recommendation', {})
    signal = rec.get('signal', 'HOLD')
    color_map = {'BUY': (0, 150, 0), 'SELL': (190, 0, 0), 'HOLD': (180, 130, 0)}
    r, g, b = color_map.get(signal, (80, 80, 80))
    pdf.set_fill_color(r, g, b)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 15)
    pdf.cell(0, 13, f"  {signal}  \u2014  Confidence Score: {rec.get('score', 0)} / 100",
             ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)
    pdf.set_font('Helvetica', '', 9)
    pdf.multi_cell(0, 5, rec.get('rationale', ''))

    return bytes(pdf.output())


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@report_bp.route('/report/<symbol>', methods=['GET'])
def get_report(symbol: str):
    """Returns the full JSON investment report for a stock symbol."""
    try:
        data = generate_report(symbol.upper())
        return jsonify(data), 200
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        abort(500, description=f"Failed to generate report: {str(e)}")


@report_bp.route('/report/<symbol>/pdf', methods=['GET'])
def get_report_pdf(symbol: str):
    """Streams a PDF investment report download for a stock symbol."""
    try:
        data = generate_report(symbol.upper())
        pdf_bytes = _build_pdf(data)
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"{symbol.upper()}_investment_report.pdf",
        )
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        abort(500, description=f"Failed to generate PDF: {str(e)}")