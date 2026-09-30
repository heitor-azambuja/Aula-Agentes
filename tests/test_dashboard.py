from dash import Dash

from app.dashboard import build_balance_figure, build_summary_cards, create_dashboard


def _collect_ids(component):
    found = set()
    component_id = getattr(component, "id", None)
    if component_id is not None:
        found.add(component_id)

    children = getattr(component, "children", None)
    if children is None:
        return found
    if not isinstance(children, list):
        children = [children]
    for child in children:
        found.update(_collect_ids(child))
    return found


def test_dashboard_exposes_form_result_graph_and_table_components():
    dashboard = create_dashboard()

    assert isinstance(dashboard, Dash)
    ids = _collect_ids(dashboard.layout)
    assert {
        "initial-amount",
        "duration-years",
        "annual-interest-rate",
        "monthly-contribution",
        "one-time-withdrawals",
        "recurring-withdrawals",
        "simulate-button",
        "summary-cards",
        "balance-graph",
        "monthly-table",
        "error-message",
    }.issubset(ids)


def test_summary_cards_render_financial_totals():
    cards = build_summary_cards(
        {
            "final_balance": 1200,
            "total_contributed": 1000,
            "total_withdrawn": 50,
            "total_interest": 250,
        }
    )

    rendered_text = " ".join(str(card.children) for card in cards)
    assert "Saldo final" in rendered_text
    assert "R$ 1,200.00" in rendered_text
    assert "Juros acumulados" in rendered_text


def test_balance_figure_uses_monthly_records_as_line_series():
    figure = build_balance_figure(
        [
            {"month": 1, "ending_balance": 1000},
            {"month": 2, "ending_balance": 1100},
        ]
    )

    assert list(figure.data[0].x) == [1, 2]
    assert list(figure.data[0].y) == [1000, 1100]
