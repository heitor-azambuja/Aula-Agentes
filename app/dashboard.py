"""Interface Dash da calculadora de juros compostos."""

from __future__ import annotations

import json
from typing import Any

import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dash_table, dcc, html

from app.calculator import simulate_compound_interest

_EMPTY_FIGURE = go.Figure(layout={"template": "plotly_white"})


def _format_currency(value: float) -> str:
    return f"R$ {value:,.2f}"


def _parse_json_list(raw_value: str | None) -> list[dict[str, Any]]:
    if not raw_value or not raw_value.strip():
        return []
    parsed = json.loads(raw_value)
    if not isinstance(parsed, list):
        raise ValueError("retiradas devem ser informadas como uma lista JSON")
    return parsed


def build_summary_cards(summary: dict[str, float]) -> list[html.Div]:
    """Cria cards de resumo financeiro para o dashboard."""
    labels = {
        "final_balance": "Saldo final",
        "total_contributed": "Total aportado",
        "total_withdrawn": "Total retirado",
        "total_interest": "Juros acumulados",
    }
    return [
        html.Div(
            [html.Strong(label), html.Span(_format_currency(float(summary.get(key, 0))))],
            className="summary-card",
        )
        for key, label in labels.items()
    ]


def build_balance_figure(monthly_records: list[dict[str, Any]]) -> go.Figure:
    """Cria gráfico de linha com a evolução do saldo mensal."""
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=[record["month"] for record in monthly_records],
            y=[record["ending_balance"] for record in monthly_records],
            mode="lines+markers",
            name="Saldo",
        )
    )
    figure.update_layout(
        title="Evolução do patrimônio",
        xaxis_title="Mês",
        yaxis_title="Saldo",
        template="plotly_white",
    )
    return figure


def _build_layout() -> html.Div:
    return html.Div(
        [
            html.H1("Calculadora de Juros Compostos"),
            html.P("Simule aportes, juros compostos e retiradas ao longo do tempo."),
            html.Div(
                [
                    html.Label("Aporte inicial"),
                    dcc.Input(id="initial-amount", type="number", min=0, value=1000, step=100),
                    html.Label("Tempo de investimento (anos)"),
                    dcc.Input(id="duration-years", type="number", min=1, value=10, step=1),
                    html.Label("Juros anuais (%)"),
                    dcc.Input(id="annual-interest-rate", type="number", min=0, value=8, step=0.1),
                    html.Label("Aportes mensais"),
                    dcc.Input(id="monthly-contribution", type="number", min=0, value=100, step=50),
                    html.Label("Retiradas pontuais (JSON)"),
                    dcc.Textarea(
                        id="one-time-withdrawals",
                        value='[{"month": 12, "amount": 500}]',
                        style={"width": "100%", "height": 80},
                    ),
                    html.Label("Retiradas recorrentes (JSON)"),
                    dcc.Textarea(
                        id="recurring-withdrawals",
                        value='[{"start_month": 24, "amount": 100, "frequency_months": 12}]',
                        style={"width": "100%", "height": 80},
                    ),
                    html.Button("Simular", id="simulate-button", n_clicks=0),
                ],
                className="form-panel",
            ),
            html.Div(id="error-message", role="alert"),
            html.Div(id="summary-cards", className="summary-grid"),
            dcc.Graph(id="balance-graph", figure=_EMPTY_FIGURE),
            dash_table.DataTable(
                id="monthly-table",
                columns=[
                    {"name": "Mês", "id": "month"},
                    {"name": "Saldo inicial", "id": "beginning_balance"},
                    {"name": "Aporte", "id": "contribution"},
                    {"name": "Retirada", "id": "withdrawal"},
                    {"name": "Juros", "id": "interest"},
                    {"name": "Saldo final", "id": "ending_balance"},
                ],
                data=[],
                page_size=12,
            ),
        ],
        className="app-container",
    )


def create_dashboard(server: Any | None = None, route_prefix: str = "/") -> Dash:
    """Cria a aplicação Dash da calculadora."""
    dashboard = Dash(
        __name__,
        server=server,
        routes_pathname_prefix=route_prefix,
        requests_pathname_prefix=route_prefix,
    )
    dashboard.title = "Calculadora de Juros Compostos"
    dashboard.layout = _build_layout()

    @dashboard.callback(
        Output("summary-cards", "children"),
        Output("balance-graph", "figure"),
        Output("monthly-table", "data"),
        Output("error-message", "children"),
        Input("simulate-button", "n_clicks"),
        State("initial-amount", "value"),
        State("duration-years", "value"),
        State("annual-interest-rate", "value"),
        State("monthly-contribution", "value"),
        State("one-time-withdrawals", "value"),
        State("recurring-withdrawals", "value"),
    )
    def run_simulation(
        _clicks: int,
        initial_amount: float,
        duration_years: float,
        annual_interest_rate: float,
        monthly_contribution: float,
        one_time_withdrawals: str,
        recurring_withdrawals: str,
    ):
        try:
            result = simulate_compound_interest(
                initial_amount=float(initial_amount or 0),
                annual_interest_rate=float(annual_interest_rate or 0),
                duration_months=int(float(duration_years or 0) * 12),
                monthly_contribution=float(monthly_contribution or 0),
                one_time_withdrawals=_parse_json_list(one_time_withdrawals),
                recurring_withdrawals=_parse_json_list(recurring_withdrawals),
            )
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            return [], _EMPTY_FIGURE, [], f"Erro: {exc}"

        return (
            build_summary_cards(result["summary"]),
            build_balance_figure(result["monthly_records"]),
            result["monthly_records"],
            "",
        )

    return dashboard
