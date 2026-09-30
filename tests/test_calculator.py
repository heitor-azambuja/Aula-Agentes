import math

from app.calculator import simulate_compound_interest


def test_simulates_effective_annual_rate_without_monthly_contributions():
    result = simulate_compound_interest(
        initial_amount=1000,
        annual_interest_rate=12,
        duration_months=12,
        monthly_contribution=0,
    )

    assert math.isclose(result["summary"]["final_balance"], 1120.0, abs_tol=0.01)
    assert result["summary"]["total_contributed"] == 1000.0
    assert result["summary"]["total_withdrawn"] == 0.0
    assert math.isclose(result["summary"]["total_interest"], 120.0, abs_tol=0.01)
    assert len(result["monthly_records"]) == 12


def test_simulates_monthly_contributions():
    result = simulate_compound_interest(
        initial_amount=1000,
        annual_interest_rate=0,
        duration_months=3,
        monthly_contribution=100,
    )

    assert result["summary"] == {
        "final_balance": 1300.0,
        "total_contributed": 1300.0,
        "total_withdrawn": 0.0,
        "total_interest": 0.0,
    }
    assert [record["contribution"] for record in result["monthly_records"]] == [
        100.0,
        100.0,
        100.0,
    ]
    assert [record["ending_balance"] for record in result["monthly_records"]] == [
        1100.0,
        1200.0,
        1300.0,
    ]
