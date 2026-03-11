from flask import Blueprint, jsonify, send_file, abort
from app.backend.services.analysis import generate_report
from app.backend.services.pdf_generator import generate_pdf
import io

report_bp = Blueprint("report", __name__, url_prefix="/api/report")


@report_bp.route("/<symbol>", methods=["GET"])
def get_report(symbol: str):
    """Returns full JSON report for a given stock symbol."""
    try:
        report = generate_report(symbol.upper())
        if not report:
            abort(404, description=f"No report found for symbol: {symbol}")
        return jsonify(report), 200
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        abort(500, description=f"Failed to generate report: {str(e)}")


@report_bp.route("/<symbol>/pdf", methods=["GET"])
def get_report_pdf(symbol: str):
    """Streams a PDF file download for a given stock symbol report."""
    try:
        report = generate_report(symbol.upper())
        if not report:
            abort(404, description=f"No report found for symbol: {symbol}")

        pdf_bytes = generate_pdf(report)
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{symbol.upper()}_report.pdf",
        )
    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        abort(500, description=f"Failed to generate PDF: {str(e)}")