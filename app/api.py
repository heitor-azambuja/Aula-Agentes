"""API Flask da calculadora de juros compostos."""

from __future__ import annotations

from typing import Any

from flask import Flask, jsonify, request

from app.calculator import simulate_compound_interest


def _payload_value(payload: dict[str, Any], key: str, default: Any = None) -> Any:
    return payload[key] if key in payload else default


def create_app() -> Flask:
    """Cria a aplicação Flask da calculadora."""
    app = Flask(__name__)

    @app.post("/api/simulate")
    def simulate():
        payload = request.get_json(silent=True) or {}
        try:
            result = simulate_compound_interest(
                initial_amount=float(_payload_value(payload, "initial_amount", 0)),
                annual_interest_rate=float(_payload_value(payload, "annual_interest_rate", 0)),
                duration_months=int(_payload_value(payload, "duration_months", 0)),
                monthly_contribution=float(_payload_value(payload, "monthly_contribution", 0)),
                one_time_withdrawals=_payload_value(payload, "one_time_withdrawals", []),
                recurring_withdrawals=_payload_value(payload, "recurring_withdrawals", []),
            )
        except (TypeError, ValueError) as exc:
            return jsonify({"error": str(exc)}), 400

        return jsonify(result)

    return app
